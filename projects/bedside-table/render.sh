#!/usr/bin/env bash
# Bedside table: working drawings + meshes via OpenSCAD (seconds).
#
# Camera arguments are in inches; lib/cameras.sh scales them to the model's
# output units (UNIT = 25.4) on the way to OpenSCAD.
set -euo pipefail
cd "$(dirname "$0")/../.."          # repo root

S=projects/bedside-table/bedside_table.scad
OUT=projects/bedside-table/renders
EXP=projects/bedside-table/exports
mkdir -p "$OUT" "$EXP"
. lib/cameras.sh

echo "rendering bedside table"

# Whole piece: cx=8, cy=6, cz=-3.5 (from z=-14 to z=+7, total height 21")
# Carcass alone: cx=8, cy=6, cz=3.5 (from z=0 to z=+7)

# Hero perspective: three-quarter view from above, perfectly framed
re hero           1600,1200   48,-46,22,8,6,-4.5

# Eye-level perspective (standing or sitting beside the bed)
re eye            1500,1100   42,-48,6,8,6,-4.5

# Orthographic elevations
r front           1500,1100 o 8,6,-3.5,90,0,0,64
r side            1200,1100 o 8,6,-3.5,90,0,90,58
r top             1400,1100 o 8,6,3.5,0,0,0,32

# Carcass alone (for joinery & cut sizing)
r carcass         1400,950  p 8,6,3.5,70,0,32,40      -D 'mode="carcass"'
r carcass_front   1400,850  o 8,6,3.5,90,0,0,24       -D 'mode="carcass"'

# Exploded view showing 4 boards and legs
re exploded       1600,1300   54,-50,26,8,6,-5.5      -D 'mode="exploded"'

# Close-up corner joint
re joint          1300,950    12,-16,12,0.5,2.5,6.8   -D 'mode="joint"'

# Board cutting layout (45" total length)
r waterfall       1600,600  o 22.5,6,0.375,0,0,0,52   -D 'mode="waterfall"'

# Mesh exports
echo "  meshes"
openscad -o "$EXP/bedside_table.stl" "$S" >/dev/null 2>&1
openscad -o "$EXP/bedside_table.3mf" "$S" >/dev/null 2>&1 || true

echo done
