"""Check real OpenSCAD mitre solids and edge treatment, including both opening rims."""
from pathlib import Path
import math
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
MODEL = HERE/'bedside_table.scad'
PARTS = ('board_bottom_solid', 'board_top_solid', 'board_left_solid', 'board_right_solid')

def mesh(path):
    vertices = [tuple(map(float, line.split()[1:])) for line in path.read_text().splitlines()
                if line.strip().startswith('vertex ')] if path.exists() else []
    volume = abs(math.fsum((a[0]*(b[1]*c[2]-b[2]*c[1]) +
                           a[1]*(b[2]*c[0]-b[0]*c[2]) +
                           a[2]*(b[0]*c[1]-b[1]*c[0]))/6
                          for a,b,c in zip(vertices[::3],vertices[1::3],vertices[2::3])))
    return vertices, volume

def export(folder, name, body, definitions):
    source = folder/f'{name}.scad'
    source.write_text(f'include <{MODEL}>\n'+(SAMPLES if name=='probes' else '')+
                      f'\nscale(UNIT) {{\n{body}\n}}\n')
    target = folder/f'{name}.stl'
    target.unlink(missing_ok=True)
    command = ['openscad', '-o', str(target), '-D', 'mode="none"', '-D', 'show_legs=false']
    for definition in definitions:
        command += ['-D', definition]
    result = subprocess.run(command+[str(source)], capture_output=True, text=True)
    assert 'ERROR:' not in result.stderr, result.stderr
    assert result.returncode == 0 or 'Current top level object is empty' in result.stderr, result.stderr
    return mesh(target)

SAMPLES = '''
module probes(f) {
    a = f*CHAMFER;
    for (y = [a,D-a]) {
        for (z = [a,H-a,T-a,H-T+a])
            translate([W/2,y,z]) cube(0.002,center=true);
        for (x = [a,W-a,T-a,W-T+a])
            translate([x,y,H/2]) cube(0.002,center=true);
    }
    for (x = [a,W-a], z = [a,H-a])
        translate([x,D/2,z]) cube(0.002,center=true);
}
'''
with tempfile.TemporaryDirectory(prefix='cubby-geometry-') as tmp:
    folder = Path(tmp)
    for width, depth, height, thickness, chamfer in [(16,12,7,.75,.0625),(18,13,8,.625,.03125)]:
        definitions = [f'W={width}',f'D={depth}',f'H={height}',f'T={thickness}',f'CHAMFER={chamfer}']
        for i, part in enumerate(PARTS):
            vertices, volume = export(folder,'part',f'{part}();',definitions+['chamfer_on=false'])
            assert vertices, part
            expected = ((width-thickness) if i<2 else (height-thickness))*depth*thickness*25.4**3
            assert math.isclose(volume,expected,rel_tol=1e-5),(part,volume,expected)
            spans = [max(v[a] for v in vertices)-min(v[a] for v in vertices) for a in range(3)]
            sizes = [width,depth,thickness] if i<2 else [thickness,depth,height]
            assert all(abs(a-b*25.4)<.001 for a,b in zip(spans,sizes)),(part,spans)
        for enabled in (False,True):
            params = definitions+[f'chamfer_on={str(enabled).lower()}']
            for factor in (.25,.75):
                removed = enabled and factor==.25
                # Removed probes must not intersect any board. Kept probes must
                # lie entirely inside the assembly, on all 20 treated edges.
                operation = 'intersection' if removed else 'difference'
                body = f'{operation}() {{probes({factor}); union() {{carcass();}}}}'
                _, volume = export(folder,'probes',body,params)
                assert volume<.0001,(params,factor,volume)
        pairs = '\n'.join(f'intersection() {{{a}(); {b}();}}'
                          for i,a in enumerate(PARTS) for b in PARTS[i+1:])
        _, volume = export(folder,'collisions','union() {'+pairs+'}',definitions)
        assert volume<.001,volume
        print(f'{width} × {depth} × {height}: mitre sizes/volumes, 20 chamfer edges and board clearances pass',flush=True)
print('All real-mesh geometry checks passed.')
