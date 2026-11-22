#!/usr/bin/env bash
# Wine rack: photoreal renders, via Blender/Cycles.
#
#   ./render.sh          # OpenSCAD working drawings + meshes  (fast)
#   ./render_beauty.sh   # per-part STLs + Cycles beauty shots (slow)
#
#   SAMPLES=800 RES=2000x2700 ./render_beauty.sh
set -euo pipefail
cd "$(dirname "$0")/../.."          # repo root

BLENDER=${BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}
SAMPLES=${SAMPLES:-400}
RES=${RES:-1800x1350}

S=lib/export_casework.scad
EXP=projects/wine-rack/exports
OUT=projects/wine-rack/renders

# One STL per board, so each gets its own object origin and therefore its own
# grain.  A single merged mesh would share one texture space across everything.
echo "exporting parts"
mkdir -p "$EXP/parts"
rm -f "$EXP/parts"/*.stl
ex() {
  openscad -o "$EXP/parts/$1.stl" -D 'mode="none"' \
           -D "PART=\"$2\"" -D "PART_I=$3" "$S" >/dev/null 2>&1
}
for i in 0 1; do ex "stile$i" stile $i; done
for i in 0 1 2 3 4 5 6; do ex "horiz$i" horiz $i; done
ex divider divider 0
for i in 0 1 2 3; do ex "leg$i" leg $i; done
ex brass brass 0
ex steel steel 0
ex bottles bottles 0

# The pine variant uses splayed tapered square legs on a slim recessed base
# frame (no glue blocks, no brass or steel hardware).
echo "exporting pine frame parts"
mkdir -p "$EXP/parts_scandi"
rm -f "$EXP/parts_scandi"/*.stl
sx() {
  openscad -o "$EXP/parts_scandi/$1.stl" -D 'mode="none"' \
           -D "PART=\"$2\"" -D "PART_I=$3" \
           -D 'LEG_STYLE="square"' -D DEPTH=9.25 "$S" >/dev/null 2>&1
}
for i in 0 1; do sx "stile$i" stile $i; done
for i in 0 1 2 3 4 5 6; do sx "horiz$i" horiz $i; done
sx divider divider 0
for i in 0 1 2 3; do sx "leg$i" leg $i; done
sx frame_x frame_x 0
sx frame_y frame_y 0
sx bottles bottles 0

# The metal-leg variant uses bought splayed tapered steel legs welded to flat
# 4-hole mounting plates with rounded black foot caps.
echo "exporting metal-leg parts"
mkdir -p "$EXP/parts_metal"
rm -f "$EXP/parts_metal"/*.stl
mx() {
  openscad -o "$EXP/parts_metal/$1.stl" -D 'mode="none"' \
           -D "PART=\"$2\"" -D "PART_I=$3" \
           -D 'LEG_STYLE="metal"' "$S" >/dev/null 2>&1
}
for i in 0 1; do mx "stile$i" stile $i; done
for i in 0 1 2 3 4 5 6; do mx "horiz$i" horiz $i; done
mx divider divider 0
for i in 0 1 2 3; do mx "leg$i" leg $i; done
mx steel steel 0
mx bottles bottles 0

for wood in walnut cherry; do
  echo "rendering $wood"
  "$BLENDER" -b -P lib/scene.py -- \
    --wood "$wood" --parts "$EXP/parts" --view hero \
    --samples "$SAMPLES" --res "$RES" \
    --out "$OUT/beauty_${wood}.png"
done

echo "rendering pine (recessed frame + splayed square legs)"
"$BLENDER" -b -P lib/scene.py -- \
  --wood pine --parts "$EXP/parts_scandi" --view hero \
  --samples "$SAMPLES" --res "$RES" \
  --out "$OUT/beauty_pine.png"

echo "rendering ash with metal legs"
"$BLENDER" -b -P lib/scene.py -- \
  --wood ash --legs metal --parts "$EXP/parts_metal" --view hero \
  --samples "$SAMPLES" --res "$RES" \
  --out "$OUT/beauty_ash_metal.png"

echo "rendering detail"
"$BLENDER" -b -P lib/scene.py -- \
  --wood walnut --parts "$EXP/parts" --view detail \
  --samples "$SAMPLES" --res "$RES" \
  --out "$OUT/beauty_detail.png"

echo done
