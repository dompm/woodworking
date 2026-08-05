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
RES=${RES:-1400x1900}

S=lib/export_casework.scad
EXP=projects/wine-rack/exports
OUT=projects/wine-rack/renders

# One STL per board, so each gets its own object origin and therefore its own
# grain.  A single merged mesh would share one texture space across everything.
echo "exporting parts"
mkdir -p "$EXP/parts"
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

# The scandinavian variant is a different part set: square legs, glue blocks,
# no brass or steel.
echo "exporting scandi parts"
mkdir -p "$EXP/parts_scandi"
sx() {
  openscad -o "$EXP/parts_scandi/$1.stl" -D 'mode="none"' \
           -D "PART=\"$2\"" -D "PART_I=$3" \
           -D 'LEG_STYLE="square"' -D DEPTH=9.25 "$S" >/dev/null 2>&1
}
for i in 0 1; do sx "stile$i" stile $i; done
for i in 0 1 2 3 4 5 6; do sx "horiz$i" horiz $i; done
sx divider divider 0
for i in 0 1 2 3; do sx "leg$i" leg $i; done
sx blocks blocks 0
sx bottles bottles 0

for wood in walnut cherry; do
  echo "rendering $wood"
  "$BLENDER" -b -P lib/scene.py -- \
    --wood "$wood" --parts "$EXP/parts" --view hero \
    --samples "$SAMPLES" --res "$RES" \
    --out "$OUT/beauty_${wood}.png" 2>&1 | grep -E 'Saved|Error' || true
done

echo "rendering pine (scandinavian)"
"$BLENDER" -b -P lib/scene.py -- \
  --wood pine --parts "$EXP/parts_scandi" --view hero \
  --samples 300 --res 1200x1650 \
  --out "$OUT/beauty_pine.png" 2>&1 | grep -E 'Saved|Error' || true

echo "rendering detail"
"$BLENDER" -b -P lib/scene.py -- \
  --wood walnut --parts "$EXP/parts" --view detail \
  --samples "$SAMPLES" --res 1600x1200 \
  --out "$OUT/beauty_detail.png" 2>&1 | grep -E 'Saved|Error' || true

echo done
