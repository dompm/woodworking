"""OpenSCAD publication PNGs: shared palette and supersampling, with original cameras."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile

from PIL import Image

HERE=Path(__file__).resolve().parent

def install_theme():
    # OpenSCAD 2021 selects palettes by installed name, not a JSON file path.
    # Register our own palette without changing the user's selected default.
    result=subprocess.run(['openscad','--info'],capture_output=True,text=True,check=True)
    match=re.search(r'^User Config Path: (.+)$',result.stdout+result.stderr,re.MULTILINE)
    if not match:raise RuntimeError('OpenSCAD did not report its user configuration directory')
    target=Path(match[1].strip())/'color-schemes'/'render'/'cad-publication.json'
    data=(HERE/'drawing_theme.json').read_text()
    target.parent.mkdir(parents=True,exist_ok=True)
    if not target.exists() or target.read_text()!=data:
        if target.exists() and json.loads(target.read_text()).get('name')!='Woodworking':
            raise RuntimeError(f'Refusing to replace unrelated palette: {target}')
        target.write_text(data)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--size',required=True)
    ap.add_argument('arguments',nargs=argparse.REMAINDER)
    args=ap.parse_args()
    extra=args.arguments[1:] if args.arguments[:1]==['--'] else args.arguments
    width,height=map(int,args.size.split(','))
    if not any(arg.startswith('--colorscheme') for arg in extra):extra=['--colorscheme=Woodworking',*extra]
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='drawing-',dir=args.out.parent) as tmp:
        raw=Path(tmp)/'supersampled.png'
        result=subprocess.run(['openscad','-o',str(raw),f'--imgsize={width*2},{height*2}',*extra],capture_output=True,text=True)
        if result.returncode or 'ERROR:' in result.stderr or 'Unknown color scheme' in result.stderr:
            raise RuntimeError(result.stderr)
        image=Image.open(raw).convert('RGB').resize((width,height),Image.Resampling.LANCZOS)
        image.save(args.out)

if __name__=='__main__':main()
