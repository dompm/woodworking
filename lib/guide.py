#!/usr/bin/env python3
"""
Build the illustrated shop guide.

Every dimension and every drawing below is derived from the same constants the
OpenSCAD model uses, so the guide can't drift from the design. Renders are
downscaled and inlined as data URIs -- the published page has to be
self-contained.

    python3 lib/guide.py             ->  projects/wine-rack/guide.html
    python3 lib/guide.py documents   ->  projects/document-unit/guide.html

Both pieces come out of one OpenSCAD model, so they come out of one generator
too -- the joinery is identical and only the cell proportions differ.  For the
same reason both guides share illustrations: the jig drawings live under lib/,
and the joinery renders live with the wine rack because that is where they were
made, not because they only apply there.  img() searches for a name across all
of those directories rather than encoding which piece owns which picture.
"""
import base64
import io
import math
import os
import sys
from fractions import Fraction

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- which piece
PIECE = sys.argv[1] if len(sys.argv) > 1 else "winerack"
PIECES = {
    "winerack":  dict(open_w=4.0,  open_h=4.0,  rows=6, depth=9.00, legs=True,
                      title="Mid-century wine rack",
                      lede="Twelve bottles in walnut or cherry, on splayed tapered "
                           "legs. Written for a table saw, router, mitre saw and "
                           "hand tools &mdash; and for someone whose last project "
                           "was a picture frame.",
                      stock="4/4 walnut, 9 in wide", hero="renders/beauty_walnut.png"),
    "documents": dict(open_w=12.0, open_h=3.5,  rows=5, depth=9.25, legs=False,
                      title="Document unit",
                      lede="Ten cells for letter and A4 laid flat, in pine. The same "
                           "joinery as the wine rack at a different scale &mdash; "
                           "which is what makes it the right piece to build first.",
                      stock="1x10 pine, 9-1/4 in actual",
                      hero="renders/beauty_documents.png"),
}
if PIECE not in PIECES:
    raise SystemExit("piece must be one of: " + ", ".join(PIECES))
P = PIECES[PIECE]
DOCS = (PIECE == "documents")
PROJECT = "document-unit" if DOCS else "wine-rack"

# Where img() looks, in order.  Both guides share illustrations, and now that
# each project owns its renders/ the short names collide on purpose --
# exploded.png exists for both pieces.  So: this piece first, then the wine rack
# as the fallback (the joinery drawings were all made there), then lib for the
# jigs.  The coffee table is deliberately absent; nothing here cites it, and
# leaving it out keeps its beauty_walnut.png from shadowing the rack's.
IMG_ROOTS = [
    "projects/%s/renders" % PROJECT,
    "projects/wine-rack/renders",
    "lib/renders",
]

# ---------------------------------------------------------------- model facts
T          = 0.75
DEPTH      = P["depth"]
OPENING_W  = P["open_w"]
OPENING_H  = P["open_h"]
COLS, ROWS = 2, P["rows"]
DADO       = 0.25
DADO_DIV   = 0.1875
LAP_DEPTH  = DEPTH / 2
LEG_LENGTH = 10.0
LEG_TILT   = 8.0
# scandinavian square leg
SQ_TOP = 1.50
SQ_BOT = 0.875
SQ_POST = 1.50

W = COLS * OPENING_W + (COLS + 1) * T
H = ROWS * OPENING_H + (ROWS + 1) * T
hz = lambda j: j * (OPENING_H + T)

STILE_LEN  = H
HORIZ_LEN  = W - 2 * T + 2 * DADO
DIV_Z0     = hz(0) + T - DADO_DIV
DIV_LEN    = hz(ROWS) + DADO_DIV - DIV_Z0
DIV_SLOTS  = [hz(j) - DIV_Z0 for j in range(1, ROWS)]
STILE_DADO = [hz(j) for j in range(ROWS + 1)]
SHELF_SLOT_X = (T - DADO)
SLOT_FROM_END = W / 2 - T / 2 - SHELF_SLOT_X

PARTS_LEN = 2 * STILE_LEN + (ROWS + 1) * HORIZ_LEN + DIV_LEN
MATERIAL_FT = PARTS_LEN / 12 * 1.35 + 2      # parts, waste, test offcuts

LEG_RISE  = LEG_LENGTH * math.cos(math.radians(LEG_TILT)) + 0.325
OVERALL_H = H + (LEG_RISE if P["legs"] else 0.0)


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
def find_img(rel):
    """Resolve "renders/jigs/dado.png" against every project's renders/ dir.

    Fails loudly.  A missing illustration used to sail through as a broken
    <img> in the published page, which is exactly the sort of thing nobody
    notices until they are standing at the bench.
    """
    tail = rel[len("renders/"):] if rel.startswith("renders/") else rel
    for root in IMG_ROOTS:
        path = os.path.join(ROOT, root, tail)
        if os.path.exists(path):
            return path
    raise SystemExit(
        "guide: no such render %r -- looked in %s"
        % (tail, ", ".join(IMG_ROOTS))
    )


def img(rel, width=900, quality=78):
    im = Image.open(find_img(rel)).convert("RGB")
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


def svg_scandi_leg():
    """Square tapered leg: elevation plus a plan showing which two faces get
    the taper.  Getting that wrong is the only way to ruin one."""
    S = 34.0
    pad_l, pad_t = 84, 44
    LH = LEG_LENGTH * S
    top_w, bot_w, post = SQ_TOP * S, SQ_BOT * S, SQ_POST * S
    x0, y0 = pad_l, pad_t
    plan_x, plan_y = pad_l + top_w + 190, pad_t + 30
    ww, hh = plan_x + top_w + 130, y0 + LH + 62

    o = [f'<svg viewBox="0 0 {ww:.0f} {hh:.0f}" class="dwg" role="img" '
         f'aria-label="Square tapered leg, elevation and plan">']
    # elevation: outer face plumb on the left, inner face tapering on the right
    o.append(f'<path class="wp" d="M {x0} {y0} H {x0+top_w:.1f} '
             f'V {y0+post:.1f} L {x0+bot_w:.1f} {y0+LH:.1f} '
             f'H {x0} V {y0} Z"/>')
    o.append(f'<line class="tick" x1="{x0}" y1="{y0+post:.1f}" '
             f'x2="{x0+top_w:.1f}" y2="{y0+post:.1f}" stroke-dasharray="4 3"/>')
    o.append(f'<text class="edge" x="{x0-8}" y="{y0+post/2+4:.1f}" text-anchor="end">'
             f'SQUARE POST</text>')
    o.append(f'<text class="note" x="{x0-8}" y="{y0+post/2+17:.1f}" text-anchor="end">'
             f'blocks glue here</text>')
    o.append(f'<text class="edge front" x="{x0+top_w+10:.1f}" y="{y0+LH*0.62:.1f}">'
             f'TAPER</text>')
    o.append(f'<text class="lbl" x="{x0-8}" y="{y0-14}" text-anchor="end">OUTER FACE</text>')
    o.append(f'<text class="note" x="{x0-8}" y="{y0-2}" text-anchor="end">stays plumb</text>')

    # dimensions
    dy = y0 - 22
    o.append(f'<line class="dim" x1="{x0}" y1="{dy}" x2="{x0+top_w:.1f}" y2="{dy}"/>')
    o.append(f'<text class="num" x="{x0+top_w/2:.1f}" y="{dy-6}" text-anchor="middle">'
             f'{frac(SQ_TOP)}"</text>')
    fy = y0 + LH + 20
    o.append(f'<line class="dim" x1="{x0}" y1="{fy}" x2="{x0+bot_w:.1f}" y2="{fy}"/>')
    o.append(f'<text class="num" x="{x0+bot_w/2:.1f}" y="{fy+17}" text-anchor="middle">'
             f'{frac(SQ_BOT)}"</text>')
    lx = x0 - 62
    o.append(f'<line class="dim" x1="{lx}" y1="{y0}" x2="{lx}" y2="{y0+LH:.1f}"/>')
    o.append(f'<text class="num" x="{lx-6}" y="{y0+LH/2:.1f}" text-anchor="end">'
             f'{frac(LEG_LENGTH)}"</text>')
    o.append(f'<line class="dim" x1="{lx+22}" y1="{y0}" x2="{lx+22}" y2="{y0+post:.1f}"/>')
    o.append(f'<text class="num" x="{lx+16}" y="{y0+post/2+4:.1f}" text-anchor="end">'
             f'{frac(SQ_POST)}"</text>')

    # plan at the top of the leg, showing which faces taper
    o.append(f'<rect class="wp" x="{plan_x}" y="{plan_y}" '
             f'width="{top_w:.1f}" height="{top_w:.1f}"/>')
    o.append(f'<text class="lbl" x="{plan_x}" y="{plan_y-32}">PLAN AT THE TOP</text>')
    o.append(f'<text class="edge" x="{plan_x - 8}" y="{plan_y - 8}" text-anchor="end">'
             f'case corner</text>')
    o.append(f'<circle cx="{plan_x}" cy="{plan_y}" r="4" fill="var(--brass)"/>')
    # arrows on the two inner faces
    o.append(f'<path class="arrow" d="M {plan_x+top_w+26:.1f} {plan_y+top_w/2:.1f} '
             f'H {plan_x+top_w+5:.1f}"/>')
    o.append(f'<path class="arrow" d="M {plan_x+top_w/2:.1f} {plan_y+top_w+26:.1f} '
             f'V {plan_y+top_w+5:.1f}"/>')
    o.append(f'<text class="warn" x="{plan_x+top_w+32:.1f}" y="{plan_y+top_w/2+4:.1f}">'
             f'taper</text>')
    o.append(f'<text class="warn" x="{plan_x+top_w/2:.1f}" y="{plan_y+top_w+42:.1f}" '
             f'text-anchor="middle">taper</text>')
    o.append(f'<text class="note" x="{plan_x}" y="{plan_y+top_w+62:.1f}">'
             f'all four legs are the same part, rotated</text>')
    o.append("</svg>")
    return "\n".join(o)


BOARD_LEN = 96.0      # 8 ft
KERF      = 0.125
END_TRIM  = 1.0       # squared off each end before anything else


def pack_boards():
    """First-fit-decreasing onto 8-foot boards.  Not optimal, but it is what a
    person actually does at the bench: cut the longest parts first."""
    parts = ([("stile", STILE_LEN)] * 2
             + [("shelf/rail", HORIZ_LEN)] * (ROWS + 1)
             + [("divider", DIV_LEN)])
    parts.sort(key=lambda t: -t[1])
    boards = []
    for name, ln in parts:
        for b in boards:
            if b["free"] >= ln + KERF:
                b["parts"].append((name, ln)); b["free"] -= ln + KERF; break
        else:
            boards.append({"parts": [(name, ln)],
                           "free": BOARD_LEN - 2 * END_TRIM - ln - KERF})
    return boards


def svg_cutlayout():
    """Where every part comes from.  Cutting to a plan rather than to the next
    free bit of board is most of the difference between three boards and four."""
    S = 9.2
    pad_l, pad_t, row_h, gap = 78, 34, 40, 20
    boards = pack_boards()
    ww = pad_l + BOARD_LEN * S + 96
    hh = pad_t + len(boards) * (row_h + gap) + 38
    o = [f'<svg viewBox="0 0 {ww:.0f} {hh:.0f}" class="dwg" role="img" '
         f'aria-label="Cutting layout across {len(boards)} boards">']
    for i, b in enumerate(boards):
        y = pad_t + i * (row_h + gap)
        o.append(f'<rect class="wp" x="{pad_l}" y="{y}" '
                 f'width="{BOARD_LEN*S:.1f}" height="{row_h}"/>')
        o.append(f'<text class="lbl" x="{pad_l-10}" y="{y+row_h/2+4}" '
                 f'text-anchor="end">BOARD {i+1}</text>')
        x = pad_l + END_TRIM * S
        for name, ln in b["parts"]:
            o.append(f'<rect class="cut" x="{x:.1f}" y="{y}" '
                     f'width="{ln*S:.1f}" height="{row_h}"/>')
            o.append(f'<text class="num" x="{x + ln*S/2:.1f}" y="{y+row_h/2-2}" '
                     f'text-anchor="middle">{frac(ln)}"</text>')
            o.append(f'<text class="note" x="{x + ln*S/2:.1f}" y="{y+row_h/2+11}" '
                     f'text-anchor="middle">{name}</text>')
            x += (ln + KERF) * S
        spare = pad_l + (BOARD_LEN - END_TRIM) * S - x
        if spare > 26:
            o.append(f'<text class="note" x="{x + spare/2:.1f}" y="{y+row_h/2+4}" '
                     f'text-anchor="middle">{frac(spare/S)}" spare</text>')
    o.append(f'<text class="note" x="{pad_l}" y="{hh-12}">'
             f'{len(boards)} boards. Allows {frac(END_TRIM)}" trimmed off each end and a '
             f'{frac(KERF)}" kerf per cut. Spare on the last board is your test stock.'
             f'</text>')
    o.append("</svg>")
    return "\n".join(o)


def svg_fit():
    """Why step 4 matters, in one picture: the same housing against three
    different shelf thicknesses."""
    S, pw, gap, pad = 62.0, 210, 26, 22
    stile_t, hs = T * S, T * S
    cases = [("too tight", +0.045, "var(--wine)", "splits the stile as you clamp"),
             ("correct",    0.0,   "var(--brass)", "slides with hand pressure"),
             ("too loose", -0.045, "var(--wine)", "a gap you will see forever")]
    hh = pad + 200 + 52
    o = [f'<svg viewBox="0 0 {pad*2 + 3*pw + 2*gap:.0f} {hh:.0f}" class="dwg" '
         f'role="img" aria-label="Housing fit: too tight, correct, too loose">']
    for i, (name, delta, col, note) in enumerate(cases):
        x0 = pad + i * (pw + gap)
        ytop, hgt = pad + 16, 150
        # stile in section, housing notched into its right face
        o.append(f'<path class="wp" d="M {x0} {ytop} H {x0+stile_t:.1f} '
                 f'V {ytop+hgt/2-hs/2:.1f} H {x0+stile_t-DADO*S:.1f} '
                 f'V {ytop+hgt/2+hs/2:.1f} H {x0+stile_t:.1f} V {ytop+hgt:.1f} '
                 f'H {x0} Z"/>')
        # the shelf end, thickness varying by delta
        th = (T + delta) * S
        o.append(f'<rect class="cut" x="{x0+stile_t-DADO*S:.1f}" '
                 f'y="{ytop+hgt/2-th/2:.1f}" width="{pw*0.62:.1f}" height="{th:.1f}" '
                 f'style="fill:{col};fill-opacity:.55"/>')
        o.append(f'<text class="lbl" x="{x0}" y="{ytop-8}" style="fill:{col}">'
                 f'{name.upper()}</text>')
        o.append(f'<text class="note" x="{x0}" y="{ytop+hgt+20}">{note}</text>')
    o.append(f'<text class="note" x="{pad}" y="{hh-10}">The housing is a fixed '
             f'{frac(DADO)}&#8221; deep. What changes is your stock.</text>')
    o.append("</svg>")
    return "\n".join(o)


def svg_clamping():
    """Where the clamps and cauls go.  Six across the width, one at nearly every
    housing, and a caul each side so the pressure reaches between them."""
    S = 12.0
    pad_l, pad_t = 96, 30
    cw, ch = W * S, H * S
    ww, hh = pad_l + cw + 210, pad_t * 2 + ch + 40
    o = [f'<svg viewBox="0 0 {ww:.0f} {hh:.0f}" class="dwg" role="img" '
         f'aria-label="Clamp and caul placement">']
    o.append(f'<rect class="wp" x="{pad_l}" y="{pad_t}" width="{cw:.1f}" height="{ch:.1f}"/>')
    for j in range(ROWS):
        for i in range(COLS):
            ox = pad_l + (T + i * (OPENING_W + T)) * S
            oy = pad_t + ch - (hz(j) + T + OPENING_H) * S
            o.append(f'<rect class="void" x="{ox:.1f}" y="{oy:.1f}" '
                     f'width="{OPENING_W*S:.1f}" height="{OPENING_H*S:.1f}"/>')
    # cauls, outside each stile
    for cx in (pad_l - 11, pad_l + cw + 3):
        o.append(f'<rect x="{cx:.1f}" y="{pad_t}" width="8" height="{ch:.1f}" '
                 f'style="fill:var(--brass);fill-opacity:.5;stroke:var(--ink);'
                 f'stroke-opacity:.4;stroke-width:.8"/>')
    o.append(f'<text class="lbl" x="{pad_l-18}" y="{pad_t-10}" text-anchor="end">CAUL</text>')
    # a clamp at every housing
    for j in range(ROWS + 1):
        y = pad_t + ch - (hz(j) + T / 2) * S
        o.append(f'<line x1="{pad_l-34:.1f}" y1="{y:.1f}" x2="{pad_l+cw+34:.1f}" '
                 f'y2="{y:.1f}" style="stroke:var(--wine);stroke-width:2.4"/>')
        for jx in (pad_l - 34, pad_l + cw + 26):
            o.append(f'<rect x="{jx:.1f}" y="{y-9:.1f}" width="8" height="18" '
                     f'style="fill:var(--wine)"/>')
    o.append(f'<text class="warn" x="{pad_l+cw+46:.1f}" y="{pad_t+ch/2:.1f}">'
             f'{ROWS+1} clamps, one per housing</text>')
    o.append(f'<text class="note" x="{pad_l}" y="{hh-24}">Snug, not crushing.</text>')
    o.append(f'<text class="note" x="{pad_l}" y="{hh-10}">The housings locate '
             f'everything; the clamps only hold it while the glue cures.</text>')
    o.append("</svg>")
    return "\n".join(o)


def svg_rail():
    """The end rail in plan.  It is the only part carrying three different cuts,
    so it is worth drawing on its own."""
    S = 26.0
    pad_l, pad_t = 60, 46
    bw, bh = HORIZ_LEN * S, DEPTH * S
    ww, hh = pad_l + bw + 60, pad_t + bh + 74
    o = [f'<svg viewBox="0 0 {ww:.0f} {hh:.0f}" class="dwg" role="img" '
         f'aria-label="End rail in plan with its divider housing">']
    o.append(f'<rect class="wp" x="{pad_l}" y="{pad_t}" width="{bw:.1f}" height="{bh:.1f}"/>')
    # end rabbets, one at each end
    for x in (pad_l, pad_l + bw - DADO * S):
        o.append(f'<rect class="cut end" x="{x:.1f}" y="{pad_t}" '
                 f'width="{DADO*S:.1f}" height="{bh:.1f}"/>')
    # divider housing, through, on one face only
    hx = pad_l + SLOT_FROM_END * S
    o.append(f'<rect class="cut" x="{hx:.1f}" y="{pad_t}" width="{T*S:.1f}" '
             f'height="{bh:.1f}"/>')
    dy = pad_t + bh + 20
    o.append(f'<line class="dim" x1="{pad_l}" y1="{dy}" x2="{hx:.1f}" y2="{dy}"/>')
    o.append(f'<text class="num" x="{(pad_l+hx)/2:.1f}" y="{dy+17}" text-anchor="middle">'
             f'{frac(SLOT_FROM_END)}"</text>')
    o.append(f'<line class="dim" x1="{hx+T*S:.1f}" y1="{dy}" x2="{pad_l+bw:.1f}" y2="{dy}"/>')
    o.append(f'<text class="num" x="{(hx+T*S+pad_l+bw)/2:.1f}" y="{dy+17}" '
             f'text-anchor="middle">{frac(SLOT_FROM_END)}"</text>')
    o.append(f'<text class="lbl" x="{pad_l}" y="{pad_t-24}">END RAIL &#215;2</text>')
    o.append(f'<text class="note" x="{pad_l}" y="{pad_t-10}">'
             f'{frac(HORIZ_LEN)}&#8221; long &#183; the same blank as a shelf</text>')
    o.append(f'<text class="edge front" x="{pad_l+bw+8:.1f}" y="{pad_t+14:.1f}">'
             f'rabbet {frac(DADO)}&#8221;</text>')
    o.append(f'<text class="warn" x="{hx+T*S+8:.1f}" y="{pad_t+bh-8:.1f}">'
             f'housing {frac(DADO_DIV)}&#8221; deep, ONE face only</text>')
    o.append(f'<text class="note" x="{pad_l}" y="{hh-10}">Bottom rail: housing on its '
             f'top face. Top rail: on its bottom face.</text>')
    o.append("</svg>")
    return "\n".join(o)


def svg_square():
    """Measuring diagonals is the only check that catches a racked case, and it
    has to happen before the glue grabs."""
    S = 11.0
    pad = 46
    cw, ch = W * S, H * S
    ww, hh = pad * 2 + cw + 120, pad * 2 + ch + 22
    o = [f'<svg viewBox="0 0 {ww:.0f} {hh:.0f}" class="dwg" role="img" '
         f'aria-label="Check the diagonals">']
    o.append(f'<rect class="wp" x="{pad}" y="{pad}" width="{cw:.1f}" height="{ch:.1f}"/>')
    for j in range(ROWS):
        for i in range(COLS):
            ox = pad + (T + i * (OPENING_W + T)) * S
            oy = pad + ch - (hz(j) + T + OPENING_H) * S
            o.append(f'<rect class="void" x="{ox:.1f}" y="{oy:.1f}" '
                     f'width="{OPENING_W*S:.1f}" height="{OPENING_H*S:.1f}"/>')
    for x1, y1, x2, y2 in ((pad, pad, pad + cw, pad + ch),
                           (pad + cw, pad, pad, pad + ch)):
        o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'style="stroke:var(--wine);stroke-width:2;stroke-dasharray:7 5"/>')
    import math as _m
    diag = _m.hypot(W, H)
    o.append(f'<text class="warn" x="{pad+cw+14:.1f}" y="{pad+ch/2-6:.1f}">'
             f'both diagonals</text>')
    o.append(f'<text class="warn" x="{pad+cw+14:.1f}" y="{pad+ch/2+10:.1f}">'
             f'{frac(diag,8)}&#8221; if square</text>')
    o.append(f'<text class="note" x="{pad}" y="{hh-10}">If they differ, push the long '
             f'diagonal until they match. Do it before the glue grabs, not after.</text>')
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
            ox = pad_l + (T + i * (OPENING_W + T)) * s
            oy = top + ch - (hz(j) + T + OPENING_H) * s
            o.append(f'<rect class="void" x="{ox:.1f}" y="{oy:.1f}" '
                     f'width="{OPENING_W*s:.1f}" height="{OPENING_H*s:.1f}"/>')
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
    oy = top + ch - (hz(0) + T + OPENING_H) * s
    o.append(f'<text class="num" x="{pad_l + (T+OPENING_W/2)*s:.1f}" y="{oy+OPENING_H*s/2+4:.1f}" '
             f'text-anchor="middle">{frac(OPENING_W)}&#215;{frac(OPENING_H)}"</text>')
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


def figure(src, cap="", wide=True, raster=True):
    cls = ' class="wide"' if wide else ""
    inner = f'<img src="{src}" alt="{cap}" loading="lazy">' if raster else src
    return f'<figure{cls}>{inner}<figcaption>{cap}</figcaption></figure>'


def build():
    hero = img(P["hero"], 1000, 80)
    jd = img("renders/jigs/dado.png", 860, 76)
    rip = img("renders/jigs/ripsled.png", 860, 76)
    stopb = img("renders/jigs/stopblock.png", 860, 76)
    jd2 = img("renders/jigs/dado_pass2.png", 860, 76)
    uj = img("renders/jigs/ujig.png", 860, 76)
    ujb = img("renders/jigs/ujig_bearing.png", 860, 76)
    sbase = img("renders/scandi_base.png", 820, 78)
    spine = img("renders/beauty_pine.png", 900, 80)
    jp = img("renders/jigs/dado_pair.png", 860, 76)
    js_ = img("renders/jigs/slot.png", 860, 76)
    lap = img("renders/lap.png", 780, 76)
    joint = img("renders/joint.png", 780, 76)
    expl = img("renders/exploded.png", 700, 76)
    egg = img("renders/eggcrate.png", 720, 78)
    base = img("renders/base.png", 780, 76)

    cut_rows = [
        ("A", "Stile (side)", 2,
         f'3/4 &times; {frac(DEPTH)} &times; {frac(STILE_LEN)}'),
        ("B", f"Horizontal &mdash; 2 rails + {ROWS-1} shelves, all one blank", ROWS + 1,
         f'3/4 &times; {frac(DEPTH)} &times; {frac(HORIZ_LEN)}'),
        ("C", "Divider, one continuous piece", 1,
         f'3/4 &times; {frac(DEPTH)} &times; {frac(DIV_LEN)}'),
    ] + ([
        ("D", "Angled leg plate, 8&deg;, + hangar bolt", 4, "steel, 2-3/8 sq"),
        ("E", "Tapered leg", 4, f'{frac(LEG_LENGTH)}" long, bought'),
        ("F", "Brass ferrule", 4, "7/8 ID"),
    ] if P["legs"] else [])
    rows = "".join(
        f'<tr><td class="n">{a}</td><td>{b}</td><td class="n">{c}</td><td class="n">{d}</td></tr>'
        for a, b, c, d in cut_rows)

    steps = []

    steps.append(step(1, "Lock the thing you don't control", f"""
<p>{"Two things drive every other dimension and both are outside your control, so settle them first." if P["legs"] else "One thing drives every other dimension, so settle it first."}</p>
""" + ("""
<p><b>Buy the legs first.</b> You want 10&Prime; tapered legs with brass ferrules and
<b>8&deg; angled mounting plates</b>. Check the plates are angled &mdash; plenty of
sellers ship flat 0&deg; ones by default.</p>
<p><b>Ask what board width your yard actually stocks, surfaced.</b> Whatever you get
becomes the case depth.</p>""" if P["legs"] else f"""
<p><b>The board width becomes the case depth.</b> A nominal 1&times;10 is actually
<b>{frac(DEPTH)}&Prime;</b>, not 10 &mdash; softwood is sold nominal. Everything below
assumes that number; if yours differs, set <span class="mono">DEPTH</span> in the model
and re-read the cut list.</p>
<p><b>Check {frac(W)}&Prime; against wherever this is going.</b> That width is not a
style choice &mdash; it is two columns of letter-width cells and there is nothing to
negotiate. Measure the closet before you buy wood.</p>
<div class="callout"><span class="k">Legal paper will not fit</span>
<p>Cells are {frac(OPENING_W)}&Prime; wide, which takes letter (11&Prime;) and A4
(11.69&Prime;) laid flat with room to spare. Legal is 14&Prime; long and will never
go in. If you need legal, the cell width has to change and so does everything else.</p>
</div>""") + """
<div class="callout"><span class="k">The one thing to get right</span>
<p>Every part uses the <b>full width of the board</b>, and those edges become the
visible front and back edges of the case. So all your stock has to finish at exactly
the same width.</p></div>"""))

    steps.append(step(2, "Bring every board to one width", f"""
<p>With no jointer: screw or tape each board to a straight strip of plywood, run the
plywood against the table saw fence, and the blade gives you a dead-straight edge.
Then flip that edge to the fence and rip every board to final width
<b>at one fence setting</b>. Don't move the fence between boards.</p>
{figure(rip, "Straight-line ripping. The board is fixed to a straight plywood sled and the SLED rides the fence &mdash; nothing references the rough edge. The blade then makes the second edge parallel to the first.")}
<p>Check three of them with calipers. They must match. A board 1/64&Prime; narrow means a
shelf sits proud at the front of the case permanently.</p>"""))

    steps.append(step(3, "Cut the parts to length", f"""
<p>Mitre saw with a <b>stop block</b>, or a crosscut sled. Never measure each piece
individually.</p>
{figure(stopb, "The stop block is what makes identical parts. Slide the board until it touches the stop, cut, repeat &mdash; the length is set by the setup, not by your pencil line.")}
<div class="callout"><span class="k">Check your saw crosses {frac(DEPTH)}&Prime; first</span>
<p>Every cut here is <em>across</em> the board's width. A <b>non-sliding</b> mitre saw
tops out around 5-3/4&Prime; (10&Prime;) or 7-3/4&Prime; (12&Prime;) and will not reach.
You need a <b>sliding</b> mitre saw, or a table saw crosscut sled.</p>
<p>Don't cut halfway and flip the board to meet in the middle. It works in general, but
these are the parts that have to match each other, and any misalignment between the two
passes leaves a step exactly at the joint line.</p></div>
<p><b>Check the fence is square before you cut anything real.</b> Across
{frac(DEPTH)}&Prime; a fence off by half a degree puts the ends 0.08&Prime; out of
square, the shelf then seats skewed in its housing, and the case leans. Cut a test
piece, flip one half over and butt the two cut edges together &mdash; any error doubles
and becomes obvious.</p>
<p>Support the offcut. A {frac(HORIZ_LEN)}&Prime; piece hanging in mid-air droops as you
finish the cut, pinches the blade and burns.</p>
<div class="tablewrap"><table>
<thead><tr><th>Part</th><th>What</th><th>Qty</th><th>Size (in)</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p>The {ROWS+1} B parts set the case width. If they differ from each other the case
racks and no amount of clamping fixes it. One stop setting, {ROWS+1} cuts.</p>
{figure(svg_cutlayout(), raster=False, cap="Where every part comes from. Cutting to a plan rather than to the next free bit of board is most of the difference between three boards and four &mdash; and the spare on the last one is the test stock you need in step 6.")}
<p><b>Cut the longest parts first.</b> If you start with the short ones you will find
yourself two feet short of a stile with only offcuts left. Lay out every part in pencil
on the boards before the saw runs, and put the knots where they will be cut away.</p>
<p><b>Label every part in pencil, and mark which edge is the FRONT.</b> That matters in
step 8 and it is not recoverable later.</p>
<p>Cut two extra offcuts for test joints. Don't skip them.</p>"""))

    steps.append(step(4, "Measure your actual stock thickness", f"""
<p>Put calipers on your &ldquo;3/4 inch&rdquo; boards. They will read something like
<span class="mono">0.72</span>&Prime; or <span class="mono">0.74</span>&Prime;.
<b>Write that number on the wall.</b> Every housing you cut has to match it, not the
nominal 3/4&Prime;.</p>
<div class="callout"><span class="k">Most common way first projects go wrong</span>
<p>Cutting housings to nominal 3/4&Prime; when the wood is 0.72&Prime;. Every joint in the
piece ends up sloppy and there is no fixing it afterwards.</p></div>
{figure(svg_fit(), raster=False, cap="The same " + frac(DADO) + "&Prime;-deep housing against three shelf thicknesses. You are not aiming at a number, you are aiming at the middle one.")}"""))

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
<div class="tablewrap"><table>
<thead><tr><th>Cut in</th><th>From which edge</th><th>Position</th></tr></thead>
<tbody>
<tr><td>The {ROWS-1} shelves</td><td class="n">BACK</td>
<td class="n">{frac(SLOT_FROM_END)} to {frac(SLOT_FROM_END + T)} from either end</td></tr>
<tr><td>The divider</td><td class="n">FRONT</td>
<td class="n">{", ".join(frac(v) for v in DIV_SLOTS)} from the bottom end</td></tr>
</tbody></table></div>
<p class="mono" style="color:var(--muted);font-size:.85rem">Positions are to the lower /
nearer edge of each slot. All {2*(ROWS-1)} are {frac(T)}&Prime; wide &times;
{frac(LAP_DEPTH)}&Prime; deep.</p>
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
{figure(svg_rail(), raster=False, cap="The end rail carries three cuts: a rabbet at each end where the stile lands, and one shallow housing for the divider. It is otherwise the same blank as a shelf.")}
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
<p>Measure the openings while it's dry; they should all be {frac(OPENING_W)} &times; {frac(OPENING_H)}&Prime;.</p>
<p><b>Then the whole carcass</b>, dry, no glue.</p>
{figure(svg_square(), raster=False, cap="The only check that catches a racked case. Measure corner to corner both ways; if the numbers differ, push on the long diagonal until they agree.")}
<p>Fix problems now. Once glue is on twelve housings you have minutes, not hours.</p>"""))

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
</ul>
{figure(svg_clamping(), raster=False, cap="Clamp at every housing, with a caul down each stile. A clamp bearing straight on the stile closes the joint beside it and much less four inches away; the caul is what carries the pressure between them.")}
<ul class="tight">
<li>Check the diagonals and rack it square before the glue grabs.</li>
<li>Wipe squeeze-out inside the cells now. Dried glue blocks finish and shows as pale
patches.</li>
</ul>
<p>Leave it overnight.</p>"""))

    if DOCS:
        steps.append(step(12, "Finish", f"""
<p>No base and no legs &mdash; it sits flat. That is one whole operation you do not have
to do on your first piece.</p>
<ul class="tight">
<li>Sand 120 &rarr; 180 &rarr; 220. Break every sharp edge, especially the front edges
of the cells, which get touched constantly.</li>
<li>Vacuum, then wipe with a barely damp cloth and let it dry.</li>
</ul>
<div class="callout"><span class="k">Oil will turn pine orange</span>
<p>This single choice decides whether it reads as considered or as a hardware-store
shelf. Oil and oil-based varnish amber pine badly and blotch it. Use a <b>water-based
clear</b>, a white or liming wax, or the traditional soap or lye finish that keeps
nordic pine pale.</p></div>
<p>If it sits on a closet floor, put a couple of thin strips underneath to keep it off
the deck &mdash; dust and damp both find end grain first.</p>"""))
    else:
        steps.append(step(12, "Base, then finish", f"""
{figure(base, "The legs spring straight off the underside on angled steel plates. No blocks &mdash; the bottom rail is 3/4&Prime; stock, so a bored tenon would break through it.")}
<ul class="tight">
<li>Glue a <b>3/4 &times; 1-1/2 cleat</b> along the front and back edges of the bottom
cell floor, inside. It doubles the screw purchase and is invisible from outside.</li>
<li>Screw the plates to the underside, set in 3/8&Prime; from the edges, each rotated
<b>45&deg; in plan</b> so its angle leans out toward the nearest corner.</li>
<li>Screw in the legs. If it rocks, trim the long foot <b>flat and parallel to the
floor</b> &mdash; not square to the leg.</li>
<li>Sand 120 &rarr; 180 &rarr; 220, breaking every sharp edge. Hardwax oil or wiping
varnish, two or three thin coats.</li>
</ul>
<p>Cherry keeps darkening for about a year. That's normal, and it's the good part.</p>"""))

    BLURB = (f"""<p>Ten cells sized so letter and A4 sit flat with the long edge
left to right &mdash; which is the trick that lets {frac(DEPTH)}&Prime; boards hold
11&Prime; paper. The five shelves are housed into the stiles, the interior grid is a
half-lapped egg crate, and the end rails land in a rabbet.</p>
<p>It is the same joinery as the walnut wine rack at a different scale, which is exactly
why it is the right thing to build first.</p>""" if DOCS else """<p>The five shelves are
housed into the stiles. The interior grid is a half-lapped egg crate &mdash; one
continuous divider notched into the shelves where they cross. At the top and bottom the
rails land in a rabbet, so the outside of the case shows nothing but two continuous
vertical lines.</p>""")

    LEGS_SECTION = "" if DOCS else f"""<section class="step" style="border-top-width:2px">
<div class="num-badge" style="color:var(--brass);background:transparent;border:1px solid var(--brass)">ALT</div>
<div class="step-body">
<h2>Variant &mdash; the Scandinavian legs</h2>
<p>The mid-century version uses bought splayed legs on angled plates. The
Scandinavian version uses square tapered legs you make yourself, standing plumb,
held by glue blocks &mdash; <b>no bought hardware at all</b>. It is also the cheaper
first build, which is why it makes a good rehearsal.</p>
{figure(spine, "The same rack in pine with square tapered legs. Plumb stance, no ferrules, no plates.")}

<h3>Stock</h3>
<p>A nominal <b>2&times;2 is actually 1-1/2&Prime; square</b> &mdash; exactly the leg
section, so no glue-up. One short length covers all four legs plus spares. Pick
it carefully: construction 2&times;2 is often twisted and knotty, and a leg that
isn't straight is obvious in a way a shelf isn't.</p>

<h3>Cut the taper on the two INNER faces only</h3>
{figure(svg_scandi_leg(), "The outer faces stay plumb and carry the line of the case sides down to the floor. Only the two faces looking into the case are tapered. All four legs are the same part, just rotated into their corners.", raster=False)}
<div class="callout" style="border-left-color:var(--brass)">
<span class="k" style="color:var(--brass)">Leave the top {frac(SQ_POST)}&Prime; square</span>
<p>The taper starts below a square post. That is not decoration &mdash; the glue
blocks need a flat parallel face to sit against. Taper from the very top and the
blocks meet a sloping face and leave a wedge-shaped gap.</p></div>

<p><b>How to cut it.</b> Two options, and for four short pine legs I would take
the second:</p>
<ul class="tight">
<li><b>Table saw with a tapering jig</b> &mdash; a board with a stop that holds the
leg at an angle to the fence. Cut one face, rotate 90&deg;, cut the next. After
the first cut that face is no longer square, so the jig must ride on the faces
you haven't cut yet.</li>
<li><b>Saw close and plane to the line.</b> Mark the taper on both faces, saw
just outside it, then plane down. Removing 5/8&Prime; over 10&Prime; in pine is a
few minutes per face, it needs no jig, and there is nothing to go wrong at
speed.</li>
</ul>
<p>Ease every long edge lightly afterwards &mdash; a small chamfer or a couple of
plane strokes. Pine dents if you look at it, and a crisp arris will not survive
being moved around.</p>

<h3>Fixing them on</h3>
{figure(sbase, "Two glue blocks per leg, in the inner corner. Long grain to long grain against both the leg and the underside of the case, which is why this needs no hardware.")}
<p>Glue and rub the blocks into place, then check the piece stands without
rocking before the glue sets. If it rocks, trim the long foot <b>flat and
parallel to the floor</b>.</p>
</div></section>"""

    # Has to follow the piece: this is the browser tab, and it is the name the
    # published page carries around.  Both guides went out called "Wine Rack".
    html = f"""<title>{P["title"]} &mdash; Shop Build Guide</title>
<style>{CSS}</style>
<div class="wrap">
<header class="top">
  <p class="eyebrow">Shop build guide</p>
  <h1>{P["title"]}</h1>
  <p class="lede">{P["lede"]}</p>
  <ul class="specs">
    <li class="chip">Finished <b>{frac(W)} &times; {frac(DEPTH)} &times; {frac(OVERALL_H,8)} in</b></li>
    <li class="chip">Cells <b>{frac(OPENING_W)} &times; {frac(OPENING_H)} in</b></li>
    <li class="chip">Stock <b>{P["stock"]}</b></li>
    <li class="chip">Material <b>~{MATERIAL_FT:.0f} linear ft</b></li>
  </ul>
</header>

{figure(hero, "The piece as designed: stiles running full height, an egg-crate interior, and bought legs on angled plates.")}

<h3>What it is</h3>
{BLURB}

{figure(svg_elevation(), "Front elevation. The case is 29-1/4&Prime;; the legs set the rest of the height, so buy them first.", raster=False)}

{"".join(steps)}

{LEGS_SECTION}

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
    out = os.path.join(ROOT, "projects", PROJECT, "guide.html")
    with open(out, "w") as f:
        f.write(html)
    print(f"wrote {out}  ({len(html)/1024:.0f} KB)")


if __name__ == "__main__":
    build()
