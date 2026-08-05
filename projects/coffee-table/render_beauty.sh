#!/usr/bin/env bash
# Coffee table: photoreal renders, via Blender/Cycles.
#
#   ./render.sh          # OpenSCAD working drawings + meshes  (fast)
#   ./render_beauty.sh   # per-part STLs + Cycles beauty shots (slow)
#
#   SAMPLES=800 RES=2600x1700 ./render_beauty.sh
#
# KNOWN ISSUE: the wood shader still bands into visible stripes on the big
# panels (top, shelf) despite --rings 0.12.  The multiplier is plumbed through
# correctly and the grain axis is right; the cause is downstream of it.
set -euo pipefail
cd "$(dirname "$0")/../.."          # repo root

BLENDER=${BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}
SAMPLES=${SAMPLES:-400}
RES=${RES:-2000x1300}

S=projects/coffee-table/export_parts.scad
PARTS=projects/coffee-table/exports/parts
OUT=projects/coffee-table/renders

# One STL per board, so each gets its own object origin and therefore its own
# grain.  A single merged mesh would share one texture space across everything.
echo "exporting parts"
mkdir -p "$PARTS"
rm -f "$PARTS"/*.stl
ex() {
  openscad -o "$PARTS/$1.stl" -D 'mode="none"' \
           -D "PART=\"$2\"" -D "PART_I=$3" "$S" >/dev/null 2>&1
}
ex top top 0
ex shelf shelf 0
ex tenons tenons 0
ex buttons buttons 0
for i in 0 1; do
  ex "rail$i"  rail  $i
  ex "xrail$i" xrail $i
done
for i in 0 1 2 3; do ex "leg$i" leg $i; done

b() { # b <view> <res> <out>
  echo "rendering $1"
  "$BLENDER" -b -P lib/scene.py -- \
    --model table --parts "$PARTS" --wood walnut --rings 0.12 \
    --view "$1" --res "$2" --samples "$SAMPLES" --out "$3" \
    2>&1 | grep -E 'Saved|Error' || true
}

b table        "$RES"     "$OUT/beauty_walnut.png"
b table_end    1500x1300  "$OUT/beauty_end.png"
b table_detail 1800x1300  "$OUT/beauty_detail.png"

echo done
