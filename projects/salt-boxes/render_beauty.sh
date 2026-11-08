#!/usr/bin/env bash
# Salt boxes: photoreal beauty renders via Blender / Cycles.
#
#   ./render.sh          # OpenSCAD drawings + meshes  (fast)
#   ./render_beauty.sh   # Per-part STLs + Cycles beauty shots (seconds/minutes)
set -euo pipefail
cd "$(dirname "$0")/../.."          # repo root

BLENDER=${BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}
SAMPLES=${SAMPLES:-256}
RES=${RES:-1800x1350}

S=projects/salt-boxes/export_parts.scad
PARTS=projects/salt-boxes/exports/parts
OUT=projects/salt-boxes/renders
mkdir -p "$PARTS" "$OUT"

echo "exporting per-part STLs for Cycles"
rm -f "$PARTS"/*.stl

ex() {
  echo "  $1"
  openscad -o "$PARTS/$1.stl" -D 'mode="none"' -D "PART=\"$1\"" "$S" >/dev/null 2>&1
}

ex short_bottom
ex short_mid0
ex short_mid1
ex short_lid
ex short_brass
ex short_steel
ex tall_bottom
ex tall_mid0
ex tall_mid1
ex tall_mid2
ex tall_lid
ex tall_brass
ex tall_steel

b() { # b <view> <res> <out>
  local view=$1 res=$2 out=$3
  echo "rendering Cycles beauty ($view)"
  "$BLENDER" -b -P lib/scene.py -- \
    --model saltbox --parts "$PARTS" --wood walnut \
    --view "$view" --res "$res" --samples "$SAMPLES" --out "$out"
}

b saltbox_hero   "$RES" "$OUT/beauty_walnut.png"
b saltbox_detail "$RES" "$OUT/beauty_detail.png"

echo done
