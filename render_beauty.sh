#!/usr/bin/env bash
# Photoreal renders, via Blender/Cycles.
#
#   ./render.sh          # OpenSCAD working drawings + meshes  (fast)
#   ./render_beauty.sh   # per-part STLs + Cycles beauty shots (slow)
set -euo pipefail
cd "$(dirname "$0")"

BLENDER=${BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}
SAMPLES=${SAMPLES:-400}
RES=${RES:-1400x1900}

# One STL per board, so each gets its own object origin and therefore its own
# grain.  A single merged mesh would share one texture space across everything.
echo "exporting parts"
mkdir -p exports/parts
ex() {
  openscad -o "exports/parts/$1.stl" -D 'mode="none"' \
           -D "PART=\"$2\"" -D "PART_I=$3" export_parts.scad >/dev/null 2>&1
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
mkdir -p exports/parts_scandi
sx() {
  openscad -o "exports/parts_scandi/$1.stl" -D 'mode="none"' \
           -D "PART=\"$2\"" -D "PART_I=$3" \
           -D 'LEG_STYLE="square"' -D DEPTH=9.25 export_parts.scad >/dev/null 2>&1
}
for i in 0 1; do sx "stile$i" stile $i; done
for i in 0 1 2 3 4 5 6; do sx "horiz$i" horiz $i; done
sx divider divider 0
for i in 0 1 2 3; do sx "leg$i" leg $i; done
sx blocks blocks 0
sx bottles bottles 0

for wood in walnut cherry; do
  echo "rendering $wood"
  "$BLENDER" -b -P blender/scene.py -- \
    --wood "$wood" --view hero --samples "$SAMPLES" --res "$RES" \
    --out "renders/beauty_${wood}.png" 2>&1 | grep -E 'Saved|Error' || true
done

echo "rendering pine (scandinavian)"
"$BLENDER" -b -P blender/scene.py -- \
  --wood pine --parts exports/parts_scandi --view hero \
  --samples "$SAMPLES" --res "$RES" \
  --out renders/beauty_pine.png 2>&1 | grep -E 'Saved|Error' || true

echo "rendering detail"
"$BLENDER" -b -P blender/scene.py -- \
  --wood walnut --view detail --samples "$SAMPLES" --res 1600x1200 \
  --out renders/beauty_detail.png 2>&1 | grep -E 'Saved|Error' || true

echo done
