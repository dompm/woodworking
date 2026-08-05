#!/usr/bin/env bash
# Document unit: photoreal render, via Blender/Cycles.
#
#   SAMPLES=400 RES=2000x1600 ./render_beauty.sh
set -euo pipefail
cd "$(dirname "$0")/../.."          # repo root

BLENDER=${BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}
SAMPLES=${SAMPLES:-200}
RES=${RES:-1400x1100}

S=lib/export_casework.scad
PARTS=projects/document-unit/exports/parts
OUT=projects/document-unit/renders

# One STL per board, so each gets its own object origin and therefore its own
# grain.  A single merged mesh would share one texture space across everything.
echo "exporting parts"
mkdir -p "$PARTS"
rm -f "$PARTS"/*.stl
ex() {
  openscad -o "$PARTS/$1.stl" -D 'mode="none"' \
           -D "PART=\"$2\"" -D "PART_I=$3" \
           -D 'PIECE="documents"' -D DEPTH=9.25 "$S" >/dev/null 2>&1
}
for i in 0 1; do ex "stile$i" stile $i; done
for i in 0 1 2 3 4 5; do ex "horiz$i" horiz $i; done
ex divider divider 0

# --view wide, not hero: the hero rig is framed for a tall narrow rack and
# crops a case that is wider than it is high.  --bottles 0 because there are
# none, and pine because that is what this one gets built from.
echo "rendering pine"
"$BLENDER" -b -P lib/scene.py -- \
  --wood pine --parts "$PARTS" --view wide --bottles 0 \
  --samples "$SAMPLES" --res "$RES" --out "$OUT/beauty_documents.png" \
  2>&1 | grep -E 'Saved|Error' || true

echo done
