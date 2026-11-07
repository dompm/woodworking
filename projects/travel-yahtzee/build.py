"""Export OpenSCAD parts and cut lists. Optional --render invokes Blender."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('--render', action='store_true')
ap.add_argument('--samples', type=int, default=64)
ap.add_argument('--resolution', type=int, default=1400)
ap.add_argument('--only', choices=['finger','butt','finger_strips'])
args = ap.parse_args()
scad = shutil.which('openscad')
assert scad, 'OpenSCAD is required'

def run_scad(extra, out):
    command = [scad, '-o', str(out), *extra, str(HERE / 'yahtzee_box.scad')]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode or 'ERROR:' in result.stderr or 'WARNING:' in result.stderr:
        raise RuntimeError(result.stderr)
    return result.stderr

def export(joinery, track):
    label = joinery if track == 'groove' else f'{joinery}_{track}'
    folder = HERE / 'exports' / f'parts_{label}'
    folder.mkdir(parents=True, exist_ok=True)
    defs = ['-D', f'joinery="{joinery}"', '-D', f'track="{track}"']
    echo = run_scad([*defs, '-D', 'mode="manifest"'], folder / 'manifest.echo')
    # OpenSCAD writes ECHO to the .echo file rather than stderr for this format.
    lines = (folder / 'manifest.echo').read_text().splitlines()
    records = [json.loads(line[6:]) for line in lines if line.startswith('ECHO: ')]
    assert records and records[0][0] == 'dimensions'
    dim = records[0][1:]
    parts = [dict(index=r[0], name=r[1], position=r[2], size=r[3], material=r[4], axis=r[5]) for r in records[1:]]
    manifest = dict(joinery=joinery, track=track, dimensions=dim, parts=parts)
    (folder / 'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    def one(p):
        run_scad([*defs, '-D', 'mode="export"', '-D', f'PART={p["index"]}'], folder / f'{p["name"]}.stl')
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(one, parts))
    # Keep physical boards separate. Fusing an assembly with edge/face contacts
    # can create non-manifold meshes; it is not a printable monolithic object.
    cut = ['# Generated blank sizes', '', f'Joinery: {joinery}. Lid tracks: {track}. Sizes precede machining.', '',
           '| Part | Inches (X × Y × Z) | Millimetres (X × Y × Z) |', '|---|---|---|']
    for p in parts:
        if p['material'] in ('wall','ply','rail'):
            inch=' × '.join(f'{v:.4f}' for v in p['size'])
            mm=' × '.join(f'{v*25.4:.2f}' for v in p['size'])
            cut.append(f'| {p["name"]} | {inch} | {mm} |')
    (HERE / 'exports' / f'{label}_cutlist.md').write_text('\n'.join(cut)+'\n')
    print(f'Exported {label}: '+ ' × '.join(f'{v*25.4:.2f}' for v in dim[:3])+' mm', flush=True)

for pair in [('finger','groove'),('butt','groove'),('finger','strips')]:
    label=pair[0] if pair[1]=='groove' else f'{pair[0]}_{pair[1]}'
    if args.only is None or args.only==label:
        export(*pair)
if args.render:
    blender=shutil.which('blender') or '/Applications/Blender.app/Contents/MacOS/Blender'
    subprocess.run([blender,'-b','-P',str(HERE/'render_scene.py'),'--',
                    '--samples',str(args.samples),'--resolution',str(args.resolution),
                    *(['--only',args.only] if args.only else [])],check=True)
