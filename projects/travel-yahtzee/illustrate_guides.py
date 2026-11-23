"""Generate explanatory SVGs; box dimensions are read from OpenSCAD exports."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
OUT=HERE/'renders'
manifest=json.loads((HERE/'exports'/'parts_butt'/'manifest.json').read_text())
parts={p['name']:p for p in manifest['parts']}
t=parts['left']['size'][0]*25.4
depth=manifest['dimensions'][6]*25.4
slot=manifest['dimensions'][7]*25.4
lid=parts['lid']['size'][2]*25.4
style='''<style>text{font-family:Arial,sans-serif;font-size:19px;fill:#263a3b}.title{font-size:27px;font-weight:bold}.small{font-size:16px}.wood{fill:#dfc7a1;stroke:#69543c;stroke-width:2}.metal{fill:#bfd7dc;stroke:#315d6a;stroke-width:2}.line{fill:none;stroke:#476368;stroke-width:1.6}.dim{fill:none;stroke:#476368;stroke-width:1.6;marker-start:url(#tick);marker-end:url(#tick)}</style><defs><marker id="tick" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto"><path d="M5 0V10" stroke="#476368" stroke-width="1.5"/></marker></defs>'''
def save(name,title,content,height=520):
    (OUT/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {height}" role="img" aria-label="{title}"><rect width="1000" height="{height}" fill="#faf8f3"/>{style}<text x="36" y="46" class="title">{title}</text>{content}</svg>')

s=20;x=125;top=95;right=x+t*s;back=x+(t-depth)*s;gy=top+t*s;gb=gy+slot*s
save('guide_groove_section.svg','Sliding lid: enlarged cross-section',f'''
<path class="wood" d="M{x} {top}H{right}V{gy}H{back}V{gb}H{right}V420H{x}Z"/>
<rect class="metal" x="{back+4}" y="{gy+4}" width="360" height="{lid*s}"/>
<path class="line" d="M{right} 120H610"/><text x="625" y="126">{t:.2f} mm upper lip</text>
<path class="line" d="M{back+364} {gy+lid*s/2+4}H610"/><text x="625" y="{gy+lid*s/2+10}">{lid:.2f} mm plywood lid</text>
<path class="line" d="M{back} {gb+12}L490 365H610"/><text x="625" y="371">{depth:.2f} mm groove depth</text>
<path class="dim" d="M{x} 452H{right}"/><text x="{x}" y="484">{t:.2f} mm wall</text>
<text x="625" y="420">{t-depth:.2f} mm wood behind groove</text>
<text x="625" y="451" class="small">Slot: {slot:.2f} mm nominal; fit to finished lid.</text>
<text x="625" y="478" class="small">Shown with 0.20 mm clearance per face.</text>
''')

save('guide_finger_spacing.svg','Finger-joint jig: what gets adjusted','''
<text x="65" y="91" class="small">Top view of spacing only — complete sled, clamps and guard are omitted here.</text>
<rect x="200" y="140" width="500" height="22" class="wood"/>
<rect x="300" y="162" width="100" height="100" class="wood"/>
<circle cx="550" cy="212" r="50" class="metal"/>
<text x="274" y="123">Indexing key</text><text x="515" y="123">Cutter</text>
<path class="dim" d="M300 302H400"/><path class="dim" d="M400 302H500"/><path class="dim" d="M500 302H600"/>
<text x="300" y="342">¼-in key</text><text x="413" y="374">¼-in gap</text><text x="516" y="342">¼-in cutter</text>
<path class="line" d="M350 264V295M550 264V295"/>
<text x="65" y="435">Match the key and gap to the actual test cut, then tune on scrap.</text>
<text x="65" y="472" class="small">Cut depth follows wall thickness; finger width and stock thickness are separate settings.</text>
''')

save('guide_table_plan.svg','Router table: plan the hardware before cutting','''
<rect x="80" y="85" width="520" height="440" class="wood"/>
<rect x="222.5" y="182.5" width="235" height="165" rx="4" fill="#d1d8d6" stroke="#476368" stroke-width="2"/>
<circle cx="340" cy="265" r="10" fill="#315d6a"/>
<rect x="100" y="246" width="227" height="15" class="wood"/><rect x="353" y="246" width="227" height="15" class="wood"/>
<rect x="80" y="375" width="520" height="15" fill="#688185"/>
<text x="260" y="317">Insert plate</text><text x="145" y="235">Fence</text>
<text x="197" y="427">Front / operator side</text>
<path class="dim" d="M80 564H600"/><text x="290" y="595">26 in</text>
<path class="dim" d="M49 85V525"/><text x="28" y="320" transform="rotate(-90 28 320)">22 in</text>
<path class="line" d="M340 265H675V130H705"/><text x="719" y="135">Bit center</text>
<path class="dim" d="M640 265V375"/><text x="665" y="326">5½ in in this concept</text>
<text x="665" y="403">¾ × ⅜-in miter slot</text>
<text x="665" y="442" class="small">Distance is to the slot edge</text><text x="665" y="467" class="small">nearest the cutter.</text>
<text x="80" y="645" class="small">Concept plate envelope: 11¾ × 8¼ in. Final recess and slot follow the actual plate and jig.</text>
''',680)
print('Generated groove, finger-spacing and table-layout diagrams')
