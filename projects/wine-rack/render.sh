#!/usr/bin/env bash
# Wine rack: working drawings + meshes, via OpenSCAD (seconds).
#
#   ./render.sh          # all views + STL/3MF
#   ./render_beauty.sh   # per-part STLs + Cycles beauty shots (minutes)
#
# Camera arguments are in inches; lib/cameras.sh scales them to the model's
# output units on the way to OpenSCAD.
set -euo pipefail
cd "$(dirname "$0")/../.."          # repo root

S=lib/casework.scad
OUT=projects/wine-rack/renders
EXP=projects/wine-rack/exports
mkdir -p "$OUT" "$EXP"
. lib/cameras.sh

echo "rendering wine rack"
r hero          1100,1500 p 5.125,4.5,9.25,65,0,28,105
r persp         1100,1500 p 5.125,4.5,9.25,65,0,28,105 -D show_bottles=false
r front          600,1450 o 5.125,4.5,9.25,90,0,0,115  -D show_bottles=false
r side           600,1450 o 5.125,4.5,9.25,90,0,90,115 -D show_bottles=false
r side_bottles   900,1450 o 5.125,4.5,9.25,90,0,90,115
r top            760,700  o 5.125,4.5,29.25,0,0,0,45   -D show_bottles=false -D show_legs=false
r exploded      1300,1500 p 5.125,4.5,9.25,68,0,32,140 -D 'mode="exploded"'
r joint         1100,900  p 1.6,4.0,29.5,74,0,25,20    -D 'mode="joint"'
r corner_top    1100,900  p 1.6,4.0,28.6,66,0,30,17    -D show_bottles=false -D show_legs=false
r base          1100,850  p 5.125,4.5,-3,74,0,30,30    -D show_bottles=false
re lap          1150,900    20,-22,17,5.1,4.5,0.4      -D 'mode="lap"'
re eggcrate     1150,1250   52,-50,44,5.1,7,14.6       -D 'mode="eggcrate"'
re motion       1200,1000   30,-34,44,5.125,4.5,28.6   -D 'mode="motion"'
re stile         800,1350   66,-40,34,0.375,4.5,14.6   -D 'mode="stile"'

# The scandinavian practice variant: square made legs glued into the corners,
# no hardware, and 1x pine at its actual 9-1/4 width rather than hardwood
# planed to 9.  Low camera, because the whole point of the view is the blocks.
re scandi_base  1100,850    20,-17,8,5.125,4.6,-3.4 \
    -D show_bottles=false -D 'LEG_STYLE="square"' -D DEPTH=9.25

# Mesh export.  With UNIT = 25.4 the model is emitted in millimetres, which is
# what every downstream tool assumes.
echo "  meshes"
openscad -o "$EXP/wine_rack.stl" -D show_bottles=false "$S" >/dev/null 2>&1
openscad -o "$EXP/wine_rack.3mf" -D show_bottles=false "$S" >/dev/null 2>&1 || true

# Jig drawings are shared by every project, so they live in lib/ and are
# rendered by lib/render_jigs.sh.  Run that if a jig model changed.
echo done
