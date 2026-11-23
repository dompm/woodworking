"""Real OpenSCAD mesh checks: collisions, lid travel, and invalid contents."""
from concurrent.futures import ThreadPoolExecutor
import math
from pathlib import Path
import subprocess
import tempfile

HERE=Path(__file__).resolve().parent
MODEL=HERE/'yahtzee_box.scad'

def volume(path):
    # OpenSCAD's ASCII STL can include zero-volume contact sheets when two
    # physical boards meet. Only positive-volume intersections are collisions.
    vertices=[tuple(map(float,line.split()[1:])) for line in path.read_text().splitlines()
              if line.strip().startswith('vertex ')]
    return abs(math.fsum((a[0]*(b[1]*c[2]-b[2]*c[1])+
                         a[1]*(b[2]*c[0]-b[0]*c[2])+
                         a[2]*(b[0]*c[1]-b[1]*c[0]))/6
                        for a,b,c in zip(vertices[::3],vertices[1::3],vertices[2::3])))

def check(pair):
    joint,track=pair
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp)
        # Real CSG intersection of the independently modeled physical boards.
        # A moving lid must remain clear of the body along its whole exit path.
        harness=tmp/'check.scad'
        harness.write_text(f'include <{MODEL}>\n'
            'scale(UNIT) union() {\n'
            'for(s=[0,L/4,L/2,3*L/4,L])\n'
            'intersection() { translate([0,-s,0]) lid();\n'
            'union() { for(i=[0:len(wood_parts)+len(rail_parts)-1])\n'
            'if(parts[i][0]!="lid") part(i); }} }\n')
        for name,source,mode in [('boards',MODEL,'collisions'),('lid_travel',harness,'none')]:
            out=tmp/f'{name}.stl'
            result=subprocess.run(['openscad','-o',str(out),'-D',f'joinery="{joint}"',
                '-D',f'track="{track}"','-D',f'mode="{mode}"',str(source)],capture_output=True,text=True)
            assert 'ERROR:' not in result.stderr,result.stderr
            if out.exists():
                overlap=volume(out)
                assert overlap < .001,f'{joint}/{track} {name}: {overlap} mm3 interference'
            else:
                assert 'Current top level object is empty' in result.stderr,result.stderr
        # Every separately exported board must have real positive volume.
        folder=HERE/'exports'/('parts_'+joint+('_strips' if track=='strips' else ''))
        if folder.exists():
            for p in folder.glob('*.stl'):
                assert volume(p)>0,f'Empty part: {p}'
    return f'{joint}/{track}: boards and five lid-travel positions clear'

with ThreadPoolExecutor(max_workers=4) as pool:
    for result in pool.map(check,[(joint,track) for joint in ('finger','butt') for track in ('groove','strips')]):
        print(result,flush=True)
with tempfile.TemporaryDirectory() as tmp:
    for definition in ['DIE=1','PENCIL_L=8','T=0.15']:
        r=subprocess.run(['openscad','-o',str(Path(tmp)/'invalid.csg'),'-D',definition,str(MODEL)],capture_output=True,text=True)
        assert 'ERROR: Assertion' in r.stderr,f'Invalid parameter accepted: {definition}'
print('Oversize contents and insufficient groove backing rejected',flush=True)
