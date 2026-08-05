#!/usr/bin/env bash
# Coffee table: working drawings + meshes, via OpenSCAD (seconds).
#
#   ./render.sh          # all views + STL/3MF
#   ./render_beauty.sh   # per-part STLs + Cycles beauty shots (minutes)
#
# Camera arguments are in inches; lib/cameras.sh scales them to the model's
# output units on the way to OpenSCAD.
set -euo pipefail
cd "$(dirname "$0")/../.."          # repo root

S=projects/coffee-table/coffee_table.scad
OUT=projects/coffee-table/renders
EXP=projects/coffee-table/exports
mkdir -p "$OUT" "$EXP"
. lib/cameras.sh

echo "rendering coffee table"
r hero        1600,1050 p 24,10.5,7.0,70,0,26,100
r persp_end   1250,1000 p 24,10.5,7.0,72,0,66,128
r front       1700,600  o 24,10.5,7.5,90,0,0,52
r side         900,700  o 24,10.5,7.5,90,0,90,50
r top         1600,780  o 24,10.5,15,0,0,0,62
r exploded    1450,1300 p 24,10.5,13.0,66,0,34,180 -D 'mode="exploded"'
r base        1500,900  p 24,10.5,5.0,72,0,26,92   -D show_top=false
r parts       1450,1000 p 32,17,1,60,0,22,145      -D 'mode="parts"'
r edge        1500,760  o 24,3.0,13.15,90,0,90,9.8 -D 'mode="edge"' -D show_shelf=false
re joint      1350,1050   36,-34,26,8,4,7.5        -D 'mode="joint"'

# Mesh export.  With UNIT = 25.4 the model is emitted in millimetres, which is
# what every downstream tool assumes.
echo "  meshes"
openscad -o "$EXP/coffee_table.stl" "$S" >/dev/null 2>&1
openscad -o "$EXP/coffee_table.3mf" "$S" >/dev/null 2>&1 || true

echo done
