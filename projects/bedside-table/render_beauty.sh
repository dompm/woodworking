#!/usr/bin/env bash
# Bedside table: photoreal beauty renders via Blender / Cycles.
#
#   ./render.sh          # OpenSCAD drawings + meshes  (fast)
#   ./render_beauty.sh   # Per-part STLs + Cycles beauty shots (seconds/minutes)
set -euo pipefail
cd "$(dirname "$0")/../.."          # repo root

BLENDER=${BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}
SAMPLES=${SAMPLES:-256}
RES=${RES:-1800x1350}

S=projects/bedside-table/export_parts.scad
PARTS=projects/bedside-table/exports/parts
OUT=projects/bedside-table/renders
mkdir -p "$PARTS" "$OUT"

echo "exporting per-part STLs for Cycles"
rm -f "$PARTS"/*.stl

ex() {
  echo "  $1"
  openscad -o "$PARTS/$1.stl" -D 'mode="none"' -D "PART=\"$1\"" "$S" >/dev/null 2>&1
}

ex top
ex bottom
ex left
ex right
ex legs
ex glides

b() { # b <view> <res> <out>
  local view=$1 res=$2 out=$3
  echo "rendering Cycles beauty ($view)"
  "$BLENDER" -b -P lib/scene.py -- \
    --model bedside --parts "$PARTS" --wood yellow_birch \
    --view "$view" --res "$res" --samples "$SAMPLES" --out "$out" \
    2>&1 | grep -E 'Saved|Error' || true
}

b bedside_hero  "$RES" "$OUT/beauty_yellow_birch.png"
b bedside_front "$RES" "$OUT/beauty_front.png"

echo done
