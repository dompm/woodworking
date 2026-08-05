#!/usr/bin/env bash
# Coffee table: photoreal renders, via Blender/Cycles.
#
#   ./render_table.sh          # OpenSCAD working drawings + meshes  (fast)
#   ./render_table_beauty.sh   # per-part STLs + Cycles beauty shots (slow)
#
#   SAMPLES=800 RES=2600x1700 ./render_table_beauty.sh
set -euo pipefail
cd "$(dirname "$0")"

BLENDER=${BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}
SAMPLES=${SAMPLES:-400}
RES=${RES:-2000x1300}

# One STL per board, so each gets its own object origin and therefore its own
# grain.  A single merged mesh would share one texture space across everything.
echo "exporting parts"
mkdir -p exports/table_parts
rm -f exports/table_parts/*.stl
ex() {
  openscad -o "exports/table_parts/$1.stl" -D 'mode="none"' \
           -D "PART=\"$2\"" -D "PART_I=$3" export_table_parts.scad >/dev/null 2>&1
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
  "$BLENDER" -b -P blender/scene.py -- \
    --model table --parts exports/table_parts --wood walnut --rings 0.12 \
    --view "$1" --res "$2" --samples "$SAMPLES" --out "$3" \
    2>&1 | grep -E 'Saved|Error' || true
}

b table        "$RES"     renders/table_beauty_walnut.png
b table_end    1500x1300  renders/table_beauty_end.png
b table_detail 1800x1300  renders/table_beauty_detail.png

echo done
