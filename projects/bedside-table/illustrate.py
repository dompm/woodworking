"""Dimensioned edge-treatment figure, using the OpenSCAD model's manifest."""
from pathlib import Path
from fractions import Fraction
import subprocess
import tempfile
import re

HERE = Path(__file__).resolve().parent
with tempfile.TemporaryDirectory() as tmp:
    result = subprocess.run(['openscad', '-o', str(Path(tmp)/'manifest.csg'),
                             '-D', 'mode="manifest"', str(HERE/'bedside_table.scad')],
                            capture_output=True, text=True, check=True)
    match = re.search(r'CUBBY\|([0-9.|]+)', result.stderr)
    if not match:
        raise RuntimeError(result.stderr)
    width, depth, height, thickness, chamfer = map(float, match[1].split('|'))
chamfer_label = str(Fraction(chamfer).limit_denominator(1024))

scale = 29
x, y = 40, 100
w, h, t = width*scale, height*scale, thickness*scale
c = chamfer*scale
# Same X-Z cross-sections as the mitred assembly, viewed from its front.
outer = [(x+c,y),(x+w-c,y),(x+w,y+c),(x+w,y+h-c),
         (x+w-c,y+h),(x+c,y+h),(x,y+h-c),(x,y+c)]
inner = [(x+t,y+t),(x+w-t,y+t),(x+w-t,y+h-t),(x+t,y+h-t)]
def points(values):
    return ' '.join(f'{a:.3f},{b:.3f}' for a,b in values)
q = 110
qx,qy = 700,105
ct = chamfer/thickness*q
s = q
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 450" role="img" aria-labelledby="title desc">
<title id="title">Mitred cubby and chamfer locations</title>
<desc id="desc">Front opening, four mitre seams, and an enlarged top-left corner section. Chamfers are {chamfer*25.4:.2f} mm along each adjacent face.</desc>
<style>
text {{font-family:system-ui,sans-serif;fill:#263a3b;font-size:17px}}
.label {{font-size:14px;fill:#53696a}} .line {{fill:none;stroke:#476368;stroke-width:1.5}}
.accent {{fill:none;stroke:#315d6a;stroke-width:3}} .dim {{fill:none;stroke:#53696a;stroke-width:1}}
</style>
<rect width="1100" height="450" fill="#faf8f3"/>
<text x="40" y="42">Chamfer locations</text><text x="700" y="42">Top-left corner section</text>
<polygon points="{points(outer)}" fill="#dfc7a1" stroke="#476368" stroke-width="1.5"/>
<polygon points="{points(inner)}" fill="#faf8f3" stroke="#315d6a" stroke-width="3"/>
<polygon points="{points(outer)}" class="accent"/>
'''
for ox,oy,ix,iy in [(x,y,x+t,y+t),(x+w,y,x+w-t,y+t),
                    (x,y+h,x+t,y+h-t),(x+w,y+h,x+w-t,y+h-t)]:
    svg += f'<path d="M{ox},{oy} L{ix},{iy}" class="line"/>\n'
svg += f'''
<path d="M{x},{y-16} H{x+w}" class="dim"/><text x="{x+w/2}" y="{y-25}" text-anchor="middle">{width:g} in</text>
<text x="{x+w+16}" y="{y+h/2}">{height:g} in</text>
<text x="40" y="350" class="label">Chamfer both front and back opening rims.</text>
<text x="40" y="377" class="label">Also chamfer the four outside corners along the {depth:g}-inch depth.</text>
<polygon points="{points([(qx+ct,qy),(qx+2.8*s,qy),(qx+2.8*s,qy+s),(qx+s,qy+s),(qx+ct/2,qy+ct/2)])}" fill="#dfc7a1" stroke="#476368" stroke-width="1.5"/>
<polygon points="{points([(qx,qy+ct),(qx+ct/2,qy+ct/2),(qx+s,qy+s),(qx+s,qy+2.1*s),(qx,qy+2.1*s)])}" fill="#bfd7dc" stroke="#476368" stroke-width="1.5"/>
<path d="M{qx+ct},{qy} L{qx},{qy+ct}" class="accent"/>
<path d="M{qx+ct/2},{qy+ct/2} L{qx-28},{qy-20} H{qx-65}" class="dim"/>
<text x="{qx-70}" y="{qy-27}" text-anchor="end" class="label">{chamfer_label} in on each face</text>
<text x="{qx+1.4*s}" y="{qy+0.55*s}" text-anchor="middle">Top</text>
<text x="{qx+0.45*s}" y="{qy+1.65*s}" text-anchor="middle">Side</text>
<path d="M{qx+0.7*s},{qy+0.7*s} L{qx+1.3*s},{qy+1.4*s} H{qx+2.7*s}" class="dim"/>
<text x="{qx+1.35*s}" y="{qy+1.65*s}" class="label">45° mitre face</text>
<text x="700" y="390" class="label">Route after the joint is glued and flushed.</text>
</svg>'''
target = HERE/'renders/chamfer_detail.svg'
target.write_text(svg)
print(target)
