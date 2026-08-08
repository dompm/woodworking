#!/usr/bin/env bash
# Document unit: working drawings + meshes, via OpenSCAD (seconds).
#
#   ./render.sh          # all views + STL/3MF
#   ./render_beauty.sh   # per-part STLs + Cycles beauty shots (minutes)
#
# Same model as the wine rack -- PIECE="documents" swaps the cell grid from
# 2x6 of 4" squares to 2x5 of 12 x 3-1/2 flats and drops the legs.
#
# DEPTH is 11: a letter duo-tang is 9 to 9-1/2 wide, so a 1x10's 9-1/4 actual is
# too tight (the wide ones don't go in at all).  A 1x12 is 11-1/4 and gets both
# edges ripped square, landing at 11.  MEASURE what you actually get -- the lap
# slots are exactly half of it.
set -euo pipefail
cd "$(dirname "$0")/../.."          # repo root

S=lib/casework.scad
OUT=projects/document-unit/renders
EXP=projects/document-unit/exports
mkdir -p "$OUT" "$EXP"
. lib/cameras.sh

D=(-D 'PIECE="documents"' -D DEPTH=11)

echo "rendering document unit"
re hero      1250,950    46,-42,31,13.1,5.5,10          "${D[@]}"
r  front     1150,1000 o 13.125,5.5,11,90,0,0,72        "${D[@]}"
re exploded  1250,1000   52,-48,37,13.1,5.5,10          "${D[@]}" -D 'mode="exploded"'

echo "  meshes"
openscad -o "$EXP/document_unit.stl" "${D[@]}" "$S" >/dev/null 2>&1
openscad -o "$EXP/document_unit.3mf" "${D[@]}" "$S" >/dev/null 2>&1 || true

echo done
