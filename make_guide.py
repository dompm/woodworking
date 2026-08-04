#!/usr/bin/env python3
"""
Build the illustrated shop guide.

Every dimension and every drawing below is derived from the same constants the
OpenSCAD model uses, so the guide can't drift from the design. Renders are
downscaled and inlined as data URIs -- the published page has to be
self-contained.

    python3 make_guide.py   ->  guide.html
"""
import base64
import io
import os
from fractions import Fraction

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- model facts
T          = 0.75
DEPTH      = 9.00
OPENING    = 4.00
COLS, ROWS = 2, 6
DADO       = 0.25
DADO_DIV   = 0.1875
LAP_DEPTH  = DEPTH / 2
LEG_LENGTH = 10.0
LEG_TILT   = 8.0

W = COLS * OPENING + (COLS + 1) * T          # 10.25
H = ROWS * OPENING + (ROWS + 1) * T          # 29.25
hz = lambda j: j * (OPENING + T)

STILE_LEN  = H                                # 29.25
HORIZ_LEN  = W - 2 * T + 2 * DADO             # 9.25
DIV_Z0     = hz(0) + T - DADO_DIV
DIV_LEN    = hz(ROWS) + DADO_DIV - DIV_Z0     # 28.125
DIV_SLOTS  = [hz(j) - DIV_Z0 for j in range(1, ROWS)]
STILE_DADO = [hz(j) for j in range(ROWS + 1)]
SHELF_SLOT_X = (T - DADO)                     # shelf starts here in case coords
SLOT_FROM_END = (COLS * OPENING + (COLS + 1) * T) / 2 - T / 2 - SHELF_SLOT_X

import math
LEG_RISE  = LEG_LENGTH * math.cos(math.radians(LEG_TILT)) + 0.325
OVERALL_H = H + LEG_RISE


def frac(x, denom=16):
    """2.1875 -> '2-3/16'.  Shop notation, not decimals."""
    f = Fraction(x).limit_denominator(denom)
    whole, rem = divmod(f, 1)
    if rem == 0:
        return str(int(whole))
    if whole == 0:
        return f"{rem.numerator}/{rem.denominator}"
    return f"{int(whole)}-{rem.numerator}/{rem.denominator}"


# ---------------------------------------------------------------- images
def img(rel, width=900, quality=78):
    path = os.path.join(ROOT, rel)
    im = Image.open(path).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/jpeg;base64,{b64}"


# ---------------------------------------------------------------- drawings
def svg_stile():
    """The stile lying flat, as you actually rout it, with the seven housings
    dimensioned from the bottom end."""
    s = 25.0
    pad_l, pad_t, pad_b, pad_r = 16, 26, 78, 22
    bw, bh = STILE_LEN * s, DEPTH * s
    ww, hh = bw + pad_l + pad_r, bh + pad_t + pad_b
    o = [f'<svg viewBox="0 0 {ww:.0f} {hh:.0f}" class="dwg" role="img" '
         f'aria-label="Stile laid flat showing seven housing positions">']
    o.append(f'<rect class="wp" x="{pad_l}" y="{pad_t}" width="{bw:.1f}" height="{bh:.1f}"/>')
    for i, p in enumerate(STILE_DADO):
        x = pad_l + p * s
        cls = "cut end" if i in (0, len(STILE_DADO) - 1) else "cut"
        o.append(f'<rect class="{cls}" x="{x:.1f}" y="{pad_t}" '
                 f'width="{T*s:.1f}" height="{bh:.1f}"/>')
    # dimension line
    dy = pad_t + bh + 22
    o.append(f'<line class="dim" x1="{pad_l}" y1="{dy}" x2="{pad_l+bw:.1f}" y2="{dy}"/>')
    for i, p in enumerate(STILE_DADO):
        x = pad_l + p * s
        o.append(f'<line class="tick" x1="{x:.1f}" y1="{dy-5}" x2="{x:.1f}" y2="{dy+5}"/>')
        o.append(f'<text class="num" x="{x:.1f}" y="{dy+21}" text-anchor="middle">'
                 f'{frac(p)}</text>')
    o.append(f'<text class="lbl" x="{pad_l}" y="{pad_t-10}">BOTTOM END</text>')
    o.append(f'<text class="lbl end-lbl" x="{pad_l+bw:.1f}" y="{pad_t-10}" '
             f'text-anchor="end">TOP END</text>')
    o.append(f'<text class="note" x="{pad_l}" y="{dy+38}">'
             f'the two brass housings run off the ends &mdash; those are rabbets</text>')
    o.append("</svg>")
    return "\n".join(o)


def svg_slots():
    """Which edge each lap slot enters from -- the one thing that will not
    assemble if you get it backwards."""
    s = 17.0
    pad, gap, lblw = 16, 46, 96
    sh_w, sh_h = HORIZ_LEN * s, DEPTH * s
    dv_w, dv_h = DIV_LEN * s, DEPTH * s
    ww = lblw + max(sh_w, dv_w) + pad * 2
    hh = pad + sh_h + gap + dv_h + pad + 26
    o = [f'<svg viewBox="0 0 {ww:.0f} {hh:.0f}" class="dwg" role="img" '
         f'aria-label="Shelf and divider showing which edge each slot enters from">']

    def board(x0, y0, w, h, name, size):
        o.append(f'<rect class="wp" x="{x0}" y="{y0}" width="{w:.1f}" height="{h:.1f}"/>')
        o.append(f'<text class="lbl" x="{x0-10}" y="{y0+h/2-4}" text-anchor="end">{name}</text>')
        o.append(f'<text class="note" x="{x0-10}" y="{y0+h/2+11}" text-anchor="end">{size}</text>')
        o.append(f'<text class="edge" x="{x0+w/2:.1f}" y="{y0-7}" text-anchor="middle">BACK EDGE</text>')
        o.append(f'<text class="edge front" x="{x0+w/2:.1f}" y="{y0+h+15}" '
                 f'text-anchor="middle">FRONT EDGE</text>')

    # shelf: slot enters from the BACK edge
    x0, y0 = lblw, pad + 12
    board(x0, y0, sh_w, sh_h, "SHELF &times;5", f'{frac(HORIZ_LEN)}" long')
    sx = x0 + (SLOT_FROM_END) * s
    o.append(f'<rect class="cut" x="{sx:.1f}" y="{y0}" width="{T*s:.1f}" '
             f'height="{LAP_DEPTH*s:.1f}"/>')
    o.append(f'<path class="arrow" d="M {sx+T*s/2:.1f} {y0-4} v {LAP_DEPTH*s:.0f}"/>')

    # divider: slots enter from the FRONT edge
    x1, y1 = lblw, pad + sh_h + gap + 12
    board(x1, y1, dv_w, dv_h, "DIVIDER &times;1", f'{frac(DIV_LEN)}" long')
    for p in DIV_SLOTS:
        dx = x1 + p * s
        o.append(f'<rect class="cut" x="{dx:.1f}" y="{y1+dv_h-LAP_DEPTH*s:.1f}" '
                 f'width="{T*s:.1f}" height="{LAP_DEPTH*s:.1f}"/>')
        o.append(f'<path class="arrow" d="M {dx+T*s/2:.1f} {y1+dv_h+4:.1f} '
                 f'v -{LAP_DEPTH*s:.0f}"/>')
    o.append("</svg>")
    return "\n".join(o)


def svg_pattern_bit():
    """Cross-section through a pattern-bit template jig.  The mechanism lives
    inside the slot where no photograph or 3D view can show it."""
    S = 88.0                      # px per inch
    pad = 26
    wp_w = 6.0
    gap = T                       # the whole point: gap == housing width
    bit = 0.5
    tpl = 0.75
    base_t = 0.28
    bear_h = 0.30

    ww = wp_w*S + pad*2
    gx0 = pad + (wp_w*S - gap*S)/2
    y_wp = pad + 150              # top of workpiece
    y_tpl = y_wp - tpl*S          # top of template
    y_base = y_tpl - base_t*S
    hh = y_wp + T*S + pad + 34

    o = [f'<svg viewBox="0 0 {ww:.0f} {hh:.0f}" class="dwg" role="img" '
         f'aria-label="Cross-section of a pattern-bit template jig">']
    # workpiece with the housing cut into it
    o.append(f'<path class="wp" d="M {pad} {y_wp} H {gx0:.1f} V {y_wp + DADO*S:.1f} '
             f'H {gx0 + gap*S:.1f} V {y_wp} H {pad + wp_w*S:.1f} '
             f'V {y_wp + T*S:.1f} H {pad} Z"/>')
    # template either side of the gap
    for x0, x1 in ((pad, gx0), (gx0 + gap*S, pad + wp_w*S)):
        o.append(f'<rect class="tpl" x="{x0:.1f}" y="{y_tpl:.1f}" '
                 f'width="{x1-x0:.1f}" height="{tpl*S:.1f}"/>')
    # router base, sitting on top of the template
    bx = gx0 + bit*S/2
    o.append(f'<rect class="rtr" x="{bx - 2.6*S:.1f}" y="{y_base:.1f}" '
             f'width="{5.2*S:.1f}" height="{base_t*S:.1f}"/>')
    # shank -- a different diameter, and it guides nothing
    o.append(f'<rect class="shank" x="{bx - 0.22*S:.1f}" y="{pad}" '
             f'width="{0.44*S:.1f}" height="{y_base - pad:.1f}"/>')
    # cutter, reaching into the work
    o.append(f'<rect class="cutter" x="{gx0:.1f}" y="{y_tpl + bear_h*S:.1f}" '
             f'width="{bit*S:.1f}" height="{y_wp + DADO*S - y_tpl - bear_h*S:.1f}"/>')
    # the bearing -- SAME width as the cutter
    o.append(f'<rect class="bearing" x="{gx0:.1f}" y="{y_tpl:.1f}" '
             f'width="{bit*S:.1f}" height="{bear_h*S:.1f}"/>')
    # dimension across the gap
    dy = y_wp + T*S + 22
    o.append(f'<line class="dim" x1="{gx0:.1f}" y1="{dy}" x2="{gx0+gap*S:.1f}" y2="{dy}"/>')
    for x in (gx0, gx0+gap*S):
        o.append(f'<line class="tick" x1="{x:.1f}" y1="{dy-5}" x2="{x:.1f}" y2="{dy+5}"/>')
    o.append(f'<text class="num" x="{gx0 + gap*S/2:.1f}" y="{dy+20}" text-anchor="middle">'
             f'gap = housing width = {frac(T)}"</text>')
    # labels
    o.append(f'<text class="lbl" x="{pad+6}" y="{y_base - 9:.1f}">ROUTER BASE</text>')
    o.append(f'<text class="edge" x="{pad+6}" y="{y_tpl + tpl*S/2 + 4:.1f}">TEMPLATE</text>')
    o.append(f'<text class="edge" x="{pad+6}" y="{y_wp + T*S/2 + 4:.1f}">WORKPIECE</text>')
    o.append(f'<text class="note" x="{bx + 0.32*S:.1f}" y="{pad + 26:.1f}">shank &mdash; '
             f'guides nothing</text>')
    o.append(f'<text class="warn" x="{ww - 10:.0f}" y="{y_tpl + 16:.1f}" '
             f'text-anchor="end">bearing &Oslash; = cutter &Oslash;, so zero offset</text>')
    o.append("</svg>")
    return "\n".join(o)


def svg_elevation():
    s = 13.0
    pad_l, pad_t, pad_r, pad_b = 104, 38, 120, 26
    cw, ch = W * s, H * s
    total = OVERALL_H * s
    ww, hh = cw + pad_l + pad_r, total + pad_t + pad_b
    o = [f'<svg viewBox="0 0 {ww:.0f} {hh:.0f}" class="dwg portrait" role="img" '
         f'aria-label="Front elevation with overall dimensions">']
    top = pad_t
    # carcass grid
    o.append(f'<rect class="wp" x="{pad_l}" y="{top}" width="{cw:.1f}" height="{ch:.1f}"/>')
    for j in range(ROWS):
        for i in range(COLS):
            ox = pad_l + (T + i * (OPENING + T)) * s
            oy = top + ch - (hz(j) + T + OPENING) * s
            o.append(f'<rect class="void" x="{ox:.1f}" y="{oy:.1f}" '
                     f'width="{OPENING*s:.1f}" height="{OPENING*s:.1f}"/>')
    # legs
    foot = top + total
    spread = LEG_LENGTH * math.sin(math.radians(LEG_TILT)) / math.sqrt(2)
    for sx in (-1, 1):
        tx = pad_l + (cw / 2) + sx * (cw / 2 - 1.5625 * s)
        fx = tx + sx * spread * s
        o.append(f'<path class="leg" d="M {tx:.1f} {top+ch:.1f} L {fx:.1f} {foot:.1f}"/>')
    # dimensions
    o.append(f'<line class="dim" x1="{pad_l}" y1="{top-9}" x2="{pad_l+cw:.1f}" y2="{top-9}"/>')
    o.append(f'<text class="num" x="{pad_l+cw/2:.1f}" y="{top-14}" text-anchor="middle">'
             f'{frac(W)}"</text>')
    xr = pad_l + cw + 14
    o.append(f'<line class="dim" x1="{xr}" y1="{top}" x2="{xr}" y2="{foot:.1f}"/>')
    o.append(f'<text class="num" x="{xr+7}" y="{top+total/2:.1f}">{frac(OVERALL_H,8)}" overall</text>')
    xl = pad_l - 14
    o.append(f'<line class="dim" x1="{xl}" y1="{top}" x2="{xl}" y2="{top+ch:.1f}"/>')
    o.append(f'<text class="num" x="{xl-7}" y="{top+ch/2:.1f}" text-anchor="end">'
             f'{frac(H)}" case</text>')
    oy = top + ch - (hz(0) + T + OPENING) * s
    o.append(f'<text class="num" x="{pad_l + (T+OPENING/2)*s:.1f}" y="{oy+OPENING*s/2+4:.1f}" '
             f'text-anchor="middle">{frac(OPENING)}"</text>')
    o.append("</svg>")
    return "\n".join(o)


# ---------------------------------------------------------------- page
CSS = """
:root{
  --paper:#F1EFEA; --surface:#FBFAF7; --ink:#1D1B18; --muted:#6B655C;
  --rule:#DAD5CB; --brass:#8A6D26; --brass-soft:#EDE4CE; --wine:#7C2B36;
  --wood:#C8A882; --cut:#A87F4C; --void:#E7E2D9; --shadow:rgba(29,27,24,.08);
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;
  --serif:ui-serif,Charter,"Bitstream Charter","Iowan Old Style",Georgia,serif;
  --mono:ui-monospace,"SF Mono",SFMono-Regular,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark){
  :root{
    --paper:#16171A; --surface:#1E2024; --ink:#E9E5DE; --muted:#9A968D;
    --rule:#33363B; --brass:#C9A44E; --brass-soft:#2A2519; --wine:#D2707B;
    --wood:#6A4E33; --cut:#93714A; --void:#24262A; --shadow:rgba(0,0,0,.4);
  }
}
:root[data-theme="dark"]{
  --paper:#16171A; --surface:#1E2024; --ink:#E9E5DE; --muted:#9A968D;
  --rule:#33363B; --brass:#C9A44E; --brass-soft:#2A2519; --wine:#D2707B;
  --wood:#6A4E33; --cut:#93714A; --void:#24262A; --shadow:rgba(0,0,0,.4);
}
:root[data-theme="light"]{
  --paper:#F1EFEA; --surface:#FBFAF7; --ink:#1D1B18; --muted:#6B655C;
  --rule:#DAD5CB; --brass:#8A6D26; --brass-soft:#EDE4CE; --wine:#7C2B36;
  --wood:#C8A882; --cut:#A87F4C; --void:#E7E2D9; --shadow:rgba(29,27,24,.08);
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font:400 17px/1.65 var(--serif);-webkit-font-smoothing:antialiased}
.wrap{max-width:47rem;margin:0 auto;padding:0 1.35rem 6rem}
h1,h2,h3,.eyebrow,.num-badge,th,.chip,.lede{font-family:var(--sans)}
h1{font:700 clamp(2rem,6vw,2.9rem)/1.08 var(--sans);letter-spacing:-.025em;
  margin:0 0 .5rem;text-wrap:balance}
h2{font:650 1.32rem/1.3 var(--sans);letter-spacing:-.012em;margin:0;text-wrap:balance}
h3{font:650 .95rem/1.4 var(--sans);letter-spacing:.01em;margin:2rem 0 .4rem}
p{margin:0 0 1rem}
a{color:var(--brass)}
.eyebrow{font:600 .68rem/1 var(--sans);letter-spacing:.17em;text-transform:uppercase;
  color:var(--brass);margin:0 0 1rem}
header.top{padding:3.6rem 0 1.4rem}
.lede{font:400 1.06rem/1.6 var(--sans);color:var(--muted);max-width:34rem;margin:0}
.specs{display:flex;flex-wrap:wrap;gap:.4rem;margin:1.6rem 0 0;padding:0;list-style:none}
.chip{font:600 .72rem/1 var(--sans);letter-spacing:.04em;text-transform:uppercase;
  color:var(--muted);background:var(--surface);border:1px solid var(--rule);
  border-radius:2px;padding:.48rem .6rem}
.chip b{color:var(--ink);font-variant-numeric:tabular-nums}
figure{margin:1.8rem 0;padding:0}
figure img,figure svg{display:block;width:100%;height:auto;border-radius:2px}
figure svg.portrait{width:auto;max-width:100%;height:min(560px,72vh);margin-inline:auto}
figure img{background:var(--surface);box-shadow:0 1px 3px var(--shadow)}
figcaption{font:400 .85rem/1.5 var(--sans);color:var(--muted);margin-top:.6rem;
  padding-left:.85rem;border-left:2px solid var(--brass)}
.wide{margin-left:calc(-1*min(4.5rem,4vw));margin-right:calc(-1*min(4.5rem,4vw))}
.dwg{background:var(--surface);border:1px solid var(--rule);padding:.4rem}
.dwg .wp{fill:var(--wood);stroke:var(--ink);stroke-width:1.1;stroke-opacity:.55}
.dwg .void{fill:var(--void);stroke:var(--ink);stroke-width:.8;stroke-opacity:.4}
.dwg .cut{fill:var(--cut);stroke:var(--ink);stroke-width:.8;stroke-opacity:.5}
.dwg .cut.end{fill:var(--brass);fill-opacity:.75}
.dwg .leg{stroke:var(--ink);stroke-width:2.6;stroke-opacity:.6;stroke-linecap:round;fill:none}
.dwg .dim,.dwg .tick{stroke:var(--brass);stroke-width:1;fill:none}
.dwg .arrow{stroke:var(--wine);stroke-width:1.6;fill:none}
.dwg text{font-family:var(--mono);font-variant-numeric:tabular-nums}
.dwg .num{font-size:11px;fill:var(--ink)}
.dwg .lbl{font-size:10px;letter-spacing:.11em;fill:var(--brass)}
.dwg .edge{font-size:9.5px;letter-spacing:.13em;fill:var(--muted)}
.dwg .edge.front{fill:var(--wine)}
.dwg .tpl{fill:var(--brass-soft);stroke:var(--ink);stroke-width:.9;stroke-opacity:.5}
.dwg .rtr{fill:#41454b;stroke:none}
.dwg .shank{fill:#9aa0a6;stroke:var(--ink);stroke-width:.6;stroke-opacity:.4}
.dwg .cutter{fill:#8d949c;stroke:var(--ink);stroke-width:.7;stroke-opacity:.5}
.dwg .bearing{fill:var(--wine);stroke:var(--ink);stroke-width:.7;stroke-opacity:.5}
.dwg .warn{font-size:10.5px;fill:var(--wine)}
.dwg .note{font-size:9.5px;fill:var(--muted)}
.step{border-top:1px solid var(--rule);padding:2.6rem 0 .6rem;
  display:grid;grid-template-columns:3.1rem 1fr;gap:0 1rem;align-items:start}
.num-badge{font:600 .78rem/1 var(--mono);letter-spacing:.04em;color:var(--brass);
  background:var(--brass-soft);border-radius:2px;padding:.42rem .1rem;text-align:center;
  font-variant-numeric:tabular-nums;margin-top:.2rem}
.step-body>*:first-child{margin-top:0}
.step-head{display:flex;align-items:baseline;justify-content:space-between;gap:1rem}
.done{font:600 .68rem/1 var(--sans);letter-spacing:.1em;text-transform:uppercase;
  color:var(--muted);display:inline-flex;align-items:center;gap:.42rem;cursor:pointer;
  user-select:none;white-space:nowrap;flex:none}
.done input{accent-color:var(--brass);width:1rem;height:1rem;cursor:pointer;margin:0}
.step.is-done .step-body>:not(.step-head){opacity:.42}
.step.is-done h2{text-decoration:line-through;text-decoration-color:var(--rule)}
.callout{background:var(--surface);border:1px solid var(--rule);
  border-left:3px solid var(--wine);border-radius:2px;padding:.9rem 1.05rem;margin:1.4rem 0}
.callout p{margin:0}
.callout .k{font:600 .68rem/1 var(--sans);letter-spacing:.13em;text-transform:uppercase;
  color:var(--wine);display:block;margin-bottom:.4rem}
.tablewrap{overflow-x:auto;margin:1.4rem 0}
table{border-collapse:collapse;width:100%;font-size:.92rem}
th,td{text-align:left;padding:.52rem .7rem;border-bottom:1px solid var(--rule)}
th{font:600 .68rem/1 var(--sans);letter-spacing:.1em;text-transform:uppercase;
  color:var(--muted)}
td.n{font-family:var(--mono);font-variant-numeric:tabular-nums;white-space:nowrap}
tbody tr:last-child td{border-bottom:none}
ul.tight{margin:0 0 1rem;padding-left:1.15rem}
ul.tight li{margin-bottom:.4rem}
.mono{font-family:var(--mono);font-variant-numeric:tabular-nums;font-size:.94em}
.risks{counter-reset:r;list-style:none;padding:0;margin:1.4rem 0 0}
.risks li{counter-increment:r;position:relative;padding-left:2.1rem;margin-bottom:1rem}
.risks li::before{content:counter(r);position:absolute;left:0;top:.15rem;
  font:600 .72rem/1 var(--mono);color:var(--wine);border:1px solid var(--wine);
  border-radius:50%;width:1.4rem;height:1.4rem;display:grid;place-items:center}
footer{border-top:1px solid var(--rule);margin-top:3.4rem;padding-top:1.4rem;
  font:400 .85rem/1.6 var(--sans);color:var(--muted)}
@media (max-width:640px){
  body{font-size:16px}
  .step{grid-template-columns:1fr;gap:.55rem}
  .num-badge{justify-self:start;padding:.36rem .6rem}
  .wide{margin-left:0;margin-right:0}
}
@media print{
  body{background:#fff;color:#000;font-size:10.5pt}
  .wrap{max-width:none}
  .step{break-inside:avoid;page-break-inside:avoid}
  figure{break-inside:avoid}
  .done{display:none}
}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

JS = """
(function(){
  var KEY='winerack-guide-v1';
  var done={};
  try{done=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
  document.querySelectorAll('.step').forEach(function(step){
    var id=step.id, box=step.querySelector('input[type=checkbox]');
    if(!box) return;
    if(done[id]){box.checked=true;step.classList.add('is-done')}
    box.addEventListener('change',function(){
      step.classList.toggle('is-done',box.checked);
      done[id]=box.checked;
      try{localStorage.setItem(KEY,JSON.stringify(done))}catch(e){}
    });
  });
})();
"""


def step(n, title, body):
    sid = f"s{n}"
    return f"""<section class="step" id="{sid}">
<div class="num-badge">{n:02d}</div>
<div class="step-body">
<div class="step-head"><h2>{title}</h2>
<label class="done"><input type="checkbox" aria-label="Mark step {n} done"> done</label></div>
{body}
</div></section>"""


def figure(src, cap, wide=True, raster=True):
    cls = ' class="wide"' if wide else ""
    inner = f'<img src="{src}" alt="{cap}" loading="lazy">' if raster else src
    return f'<figure{cls}>{inner}<figcaption>{cap}</figcaption></figure>'


def build():
    hero = img("renders/beauty_walnut.png", 1000, 80)
    jd = img("renders/jigs/dado.png", 860, 76)
    jd2 = img("renders/jigs/dado_pass2.png", 860, 76)
    uj = img("renders/jigs/ujig.png", 860, 76)
    ujb = img("renders/jigs/ujig_bearing.png", 860, 76)
    jp = img("renders/jigs/dado_pair.png", 860, 76)
    js_ = img("renders/jigs/slot.png", 860, 76)
    lap = img("renders/lap.png", 780, 76)
    joint = img("renders/joint.png", 780, 76)
    expl = img("renders/exploded.png", 700, 76)
    egg = img("renders/eggcrate.png", 720, 78)
    base = img("renders/base.png", 780, 76)

    cut_rows = [
        ("A", "Stile (side)", 2, f'3/4 &times; {frac(DEPTH)} &times; {frac(STILE_LEN)}'),
        ("B", "Horizontal &mdash; 2 rails + 5 shelves, all one blank", 7,
         f'3/4 &times; {frac(DEPTH)} &times; {frac(HORIZ_LEN)}'),
        ("C", "Divider, one continuous piece", 1,
         f'3/4 &times; {frac(DEPTH)} &times; {frac(DIV_LEN)}'),
        ("D", "Angled leg plate, 8&deg;, + hangar bolt", 4, "steel, 2-3/8 sq"),
        ("E", "Tapered leg", 4, f'{frac(LEG_LENGTH)}" long, bought'),
        ("F", "Brass ferrule", 4, "7/8 ID"),
    ]
    rows = "".join(
        f'<tr><td class="n">{a}</td><td>{b}</td><td class="n">{c}</td><td class="n">{d}</td></tr>'
        for a, b, c, d in cut_rows)

    steps = []

    steps.append(step(1, "Lock the two things you don't control", f"""
<p>Both of these decide dimensions downstream, so settle them before any wood is cut.</p>
<p><b>Buy the legs first.</b> You want {frac(LEG_LENGTH)}&Prime; tapered legs with brass
ferrules and <b>8&deg; angled mounting plates</b>. Check the plates are angled &mdash; plenty
of sellers ship flat 0&deg; ones by default. A {frac(LEG_LENGTH)}&Prime; leg gives
{frac(OVERALL_H,8)}&Prime; overall.</p>
<p><b>Ask what board width your yard actually stocks, surfaced.</b> Whatever you get
becomes the case depth. Don't design around {frac(DEPTH)}&Prime; and then find out.</p>
<div class="callout"><span class="k">The one thing to get right</span>
<p>Every part uses the <b>full width of the board</b>, and those edges become the visible
front and back edges of the case. So all your stock has to finish at exactly the same
width.</p></div>"""))

    steps.append(step(2, "Bring every board to one width", """
<p>With no jointer: screw or tape each board to a straight strip of plywood, run the
plywood against the table saw fence, and the blade gives you a dead-straight edge.
Then flip that edge to the fence and rip every board to final width
<b>at one fence setting</b>. Don't move the fence between boards.</p>
<p>Check three of them with calipers. They must match. A board 1/64&Prime; narrow means a
shelf sits proud at the front of the case permanently.</p>"""))

    steps.append(step(3, "Cut the parts to length", f"""
<p>Mitre saw with a <b>stop block</b>, or a crosscut sled. Never measure each piece
individually.</p>
<div class="tablewrap"><table>
<thead><tr><th>Part</th><th>What</th><th>Qty</th><th>Size (in)</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p>The seven B parts set the case width. If they differ from each other the case racks
and no amount of clamping fixes it. One stop setting, seven cuts.</p>
<p><b>Label every part in pencil, and mark which edge is the FRONT.</b> That matters in
step 8 and it is not recoverable later.</p>
<p>Cut two extra offcuts for test joints. Don't skip them.</p>"""))

    steps.append(step(4, "Measure your actual stock thickness", """
<p>Put calipers on your &ldquo;3/4 inch&rdquo; boards. They will read something like
<span class="mono">0.72</span>&Prime; or <span class="mono">0.74</span>&Prime;.
<b>Write that number on the wall.</b> Every housing you cut has to match it, not the
nominal 3/4&Prime;.</p>
<div class="callout"><span class="k">Most common way first projects go wrong</span>
<p>Cutting housings to nominal 3/4&Prime; when the wood is 0.72&Prime;. Every joint in the
piece ends up sloppy and there is no fixing it afterwards.</p></div>"""))

    steps.append(step(5, "Build the T-square jig", f"""
<p>A strip of 1/2&Prime; plywood about 30&Prime; long, with a shorter piece fixed across one
end at 90&deg;. The long arm is the fence the router rides; the short arm hooks over the
edge of the board, which is what makes the cut square without measuring an angle.</p>
{figure(jd, "Pass 1. The fence lies on the board, the crossbar hooks the near edge, and the router base runs against the fence. This cuts the reference wall. The router is drawn see-through &mdash; a real one covers the cut it is making.")}
<p>The housing has to match <b>your</b> stock, not a number. Two ways to guarantee that;
the first is much easier to set up.</p>

<h3>Option A &mdash; pattern bit and template</h3>
<p>A <b>pattern bit</b> (top-bearing straight bit) has a ball bearing above the cutter,
made to <b>exactly the cutter's diameter</b>. So the cut reproduces the template
one-to-one, with no offset at all &mdash; which means the gap in your jig simply
<em>is</em> the housing.</p>
<div class="callout" style="border-left-color:var(--brass)">
<span class="k" style="color:var(--brass)">Set it with the board itself</span>
<p>Clamp the two rails against a piece of your actual shelf stock, tighten, pull the
stock out. The jig now cuts a housing that fits that stock. No arithmetic, no router
base diameter, nothing measured.</p></div>
{figure(svg_pattern_bit(), "Section through the jig. The bearing rides the template edge and the cutter is the same diameter as it, so the housing lands exactly where the template says. The shank is a different size and guides nothing.", raster=False)}
{figure(ujb, "The same jig from above. The router body sits on top of the template rather than down beside it &mdash; only the bit passes through the gap.")}
<p><b>The one dimension to get right:</b> template thickness &asymp; cutter length &minus;
cut depth, so the bearing lands within the template's thickness. With a typical
1&Prime; cutter and a {frac(DADO)}&Prime; deep housing that's <b>3/4&Prime; ply or MDF</b>,
not 1/2&Prime;. Too thin and the bearing rides above the template and guides nothing.</p>
<p>Run the bearing against one rail, then back along the other. Add a crossbar at
90&deg; so the jig registers square to the edge.</p>

<h3>Option B &mdash; two fences, no special bit</h3>
<p>If you'd rather not buy a pattern bit, capture the router <em>base</em> between two
fences instead. Same idea, but now the base diameter enters the arithmetic:</p>
<p class="mono" style="background:var(--surface);border:1px solid var(--rule);padding:.7rem .9rem;border-radius:2px">
gap between fences&nbsp;= width + base&Oslash; &minus; bit&Oslash;<br>
router free travel&nbsp;&nbsp;= width &minus; bit&Oslash;</p>
<p>With a 6&Prime; base and a 1/2&Prime; bit on 3/4&Prime; stock: a 6-1/4&Prime; gap and
1/4&Prime; of travel. Make one fence adjustable, then dial it in with test cuts in scrap.</p>
{figure(uj, "The base-riding version. It works and costs nothing extra, but the gap depends on your router's base diameter and has to be found by trial rather than set with the board.")}
<div class="callout"><span class="k">Mark the base and keep it facing one way</span>
<p>This version references <em>opposite</em> sides of the router base, so if the base
isn't perfectly concentric with the bit, that error goes straight into the width.
Keeping the same part of the base against each fence makes the error constant, and your
test cuts then absorb it. The pattern bit has no such problem &mdash; its bearing is
concentric by construction.</p></div>
<div class="callout"><span class="k">You are not trying to hit 0.750 inches</span>
<p>You are matching your own stock. If your boards measure 0.727&Prime;, a
&ldquo;perfect&rdquo; 0.750&Prime; housing is a <em>bad</em> housing. The target is a feel:
slides in with firm hand pressure, no mallet.</p></div>"""))

    steps.append(step(6, "Cut test joints in real offcuts", f"""
<p>Half an hour here saves the project. Pine will lie to you about fit &mdash; it crushes.
Use walnut or cherry offcuts.</p>
<ul class="tight">
<li><b>A housing plus a shelf end.</b> Creep the second pass until an offcut slides in
with hand pressure and no mallet.</li>
<li><b>A rabbet at a board end.</b> Same setup, run off the end.</li>
<li><b>One lap crossing.</b> The only joint here you haven't done before.</li>
</ul>
{figure(lap, "The half lap that makes the interior grid. Each part gives up half its 9&Prime; width where they cross &mdash; the shelf keeps the front half, the divider the back half.")}
<p>Write the final jig offset on the jig in pencil, then stop.</p>"""))

    steps.append(step(7, "Rout the seven housings in each stile", f"""
<p>Each is 3/4&Prime; wide (your real thickness) &times; <b>1/4&Prime; deep</b>, straight through
front to back. Measured from the <b>bottom end</b> to the <b>lower edge</b> of each:</p>
{figure(svg_stile(), "The stile lying flat, as you actually rout it. The two brass housings at the ends run off the board, so they are rabbets rather than trenches &mdash; you can saw those out instead.", raster=False)}
{figure(jp, "Rout both stiles at once: side by side, inner faces up, bottom ends against a common stop. Now the housings are at identical heights by construction rather than by measurement &mdash; which is exactly the error that makes a twelve-cell grid read as crooked.")}"""))

    steps.append(step(8, "Cut the ten lap slots", f"""
<p>All 3/4&Prime; wide &times; <b>{frac(LAP_DEPTH)}&Prime; deep</b>, cut in from an edge, all the
way through the thickness. Five in the shelves, five in the divider.</p>
{figure(svg_slots(), "The shelves are slotted from the BACK edge, the divider from the FRONT. Get this backwards and the grid will not assemble.", raster=False)}
{figure(js_, "The slot setup: straightedge for the router to follow, a stop block (red) that ends the cut at the right depth, and a sacrificial board underneath because these cuts go all the way through.")}
<p>Three or four depth passes &mdash; don't try to hog {frac(T)}&Prime; of walnut in one go.
Cut the slot a hair fat so the parts go together without forcing.</p>
<div class="callout"><span class="k">Why not the table saw</span>
<p>{frac(LAP_DEPTH)}&Prime; is past a 10&Prime; blade's reach, and stopping a crosscut mid-board
leaves the blade's arc cutting far past your line on the underside.</p></div>"""))

    steps.append(step(9, "Housings for the divider ends", f"""
<p>Only the top and bottom rails get these &mdash; the five shelves don't, because the lap
does that job there.</p>
<p>3/4&Prime; wide &times; <b>3/16&Prime; deep</b>, through, centred
<span class="mono">{frac(SLOT_FROM_END)}&Prime;</span> to
<span class="mono">{frac(SLOT_FROM_END + T)}&Prime;</span> from either end. Bottom rail on
its top face only; top rail on its bottom face only.</p>
{figure(joint, "The corner: the stiles run the full height and the end rails land in a 1/4&Prime; rabbet, which is the same cut as a housing, just run off the end of the board.")}"""))

    steps.append(step(10, "Dry fit &mdash; twice", f"""
<p><b>First just the egg crate.</b> Stand the five shelves up in order, line the divider
up behind them with its notches on the shelves, and <b>push it forward
{frac(LAP_DEPTH)}&Prime; until everything is flush.</b> It goes together by hand and
stands square on its own.</p>
{figure(egg, "The only motion that works. The shelf slots open toward the back and the divider's notches open toward the front, so the two engage by sliding along the depth axis &mdash; divider in from the back, travelling forward.")}
<div class="callout"><span class="k">The divider cannot drop in from above</span>
<p>It is full depth everywhere except at its five notches, and a full-depth section
can't pass a shelf &mdash; the shelf's slot only removes the back half. Assemble the grid
with a horizontal slide, never a vertical drop.</p></div>
<p>Measure the openings while it's dry; they should all be {frac(OPENING)}&Prime;.</p>
<p><b>Then the whole carcass</b>, dry, no glue. Measure the diagonals of the front face
&mdash; they must match. Fix problems now.</p>"""))

    steps.append(step(11, "Glue up, in two stages", f"""
<p>Do it in two stages. Landing fourteen housings and ten lap joints in one go is the
most stressful glue-up in the project, and it is avoidable. Use <b>Titebond Extend or
liquid hide glue</b> &mdash; you want the open time.</p>
<p><b>Stage one &mdash; the egg crate on its own.</b> Glue the ten lap faces lightly, slide
the divider forward into the shelves as you did dry, square it up, clamp lightly and let
it cure. You now have one rigid grid instead of six loose parts.</p>
<p><b>Stage two &mdash; the carcass.</b></p>
{figure(expl, "One stile flat on the bench; the two end rails and the cured egg crate into their housings; the second stile lowered onto all seven shelf ends at once.")}
<ul class="tight">
<li>Thin glue in the housing, not on the shelf end &mdash; less squeeze-out to clean.</li>
<li>One clamp per pair of shelves, with cauls. Snug, not crushing.</li>
<li>Check the diagonals and rack it square before the glue grabs.</li>
<li>Wipe squeeze-out inside the cells now. Dried glue blocks finish and shows as pale
patches.</li>
</ul>
<p>Leave it overnight.</p>"""))

    steps.append(step(12, "Base, then finish", f"""
{figure(base, "The legs spring straight off the underside on angled steel plates. No blocks &mdash; the bottom rail is 3/4&Prime; stock, so a bored tenon would break through it.")}
<ul class="tight">
<li>Glue a <b>3/4 &times; 1-1/2 cleat</b> along the front and back edges of the bottom cell
floor, inside. It doubles the screw purchase and is invisible from outside.</li>
<li>Screw the plates to the underside, set in 3/8&Prime; from the edges, each rotated
<b>45&deg; in plan</b> so its angle leans out toward the nearest corner.</li>
<li>Screw in the legs. If it rocks, trim the long foot <b>flat and parallel to the
floor</b> &mdash; not square to the leg.</li>
<li>Sand 120 &rarr; 180 &rarr; 220, breaking every sharp edge. Hardwax oil or wiping
varnish, two or three thin coats.</li>
</ul>
<p>Cherry keeps darkening for about a year. That's normal, and it's the good part.</p>"""))

    html = f"""<title>Wine Rack &mdash; Shop Build Guide</title>
<style>{CSS}</style>
<div class="wrap">
<header class="top">
  <p class="eyebrow">Shop build guide</p>
  <h1>Mid-century wine rack</h1>
  <p class="lede">Twelve bottles in walnut or cherry, on splayed tapered legs.
  Written for a table saw, router, mitre saw and hand tools &mdash; and for someone whose
  last project was a picture frame.</p>
  <ul class="specs">
    <li class="chip">Finished <b>{frac(W)} &times; {frac(DEPTH)} &times; {frac(OVERALL_H,8)} in</b></li>
    <li class="chip">Openings <b>{frac(OPENING)} in square</b></li>
    <li class="chip">Stock <b>3/4 in, {frac(DEPTH)} in wide</b></li>
    <li class="chip">Material <b>~18 linear ft</b></li>
  </ul>
</header>

{figure(hero, "The piece as designed: stiles running full height, an egg-crate interior, and bought legs on angled plates.")}

<h3>What it is</h3>
<p>The five shelves are housed into the stiles. The interior grid is a half-lapped egg
crate &mdash; one continuous divider notched into the shelves where they cross. At the top
and bottom the rails land in a rabbet, so the outside of the case shows nothing but two
continuous vertical lines.</p>

{figure(svg_elevation(), "Front elevation. The case is 29-1/4&Prime;; the legs set the rest of the height, so buy them first.", raster=False)}

{"".join(steps)}

<section class="step" style="border-top-width:2px">
<div class="num-badge" style="color:var(--wine);background:transparent;border:1px solid var(--wine)">!</div>
<div class="step-body">
<h2>The five things most likely to go wrong</h2>
<p>None of these are skill problems. They are all preventable with setup.</p>
<ol class="risks">
<li><b>Boards not all the same width.</b> Shelves sit proud or shy at the front. Fixed in
step 2, nowhere else.</li>
<li><b>Housings cut to nominal 3/4&Prime; instead of your real thickness.</b> Sloppy joints
throughout. Step 4.</li>
<li><b>Stiles routed separately.</b> Shelves land at slightly different heights left to
right and the whole grid looks off. Step 7 &mdash; clamp them together.</li>
<li><b>Lap slots cut from the wrong edge.</b> The grid won't assemble. Step 8.</li>
<li><b>Rushing the glue-up.</b> Long-open-time glue, and dry fit twice.</li>
</ol>
</div></section>

<footer>
<p>Not a weekend. Milling and cutting to size is an evening; jigs and test joints another;
the joinery is the bulk of it; then glue-up plus overnight, and finishing spread over a
few days. Take the joinery slowly &mdash; everything else is forgiving and that part isn't.</p>
<p>Every dimension on this page is generated from the CAD model, so the guide and the
drawings can't drift apart.</p>
</footer>
</div>
<script>{JS}</script>
"""
    out = os.path.join(ROOT, "guide.html")
    with open(out, "w") as f:
        f.write(html)
    print(f"wrote {out}  ({len(html)/1024:.0f} KB)")


if __name__ == "__main__":
    build()
