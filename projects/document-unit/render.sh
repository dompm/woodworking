#!/usr/bin/env bash
# Document unit: working drawings + meshes, via OpenSCAD (seconds).
#
#   ./render.sh          # all views + STL/3MF
#   ./render_beauty.sh   # per-part STLs + Cycles beauty shots (minutes)
#
# Same model as the wine rack -- PIECE="documents" swaps the cell grid from
# 2x6 of 4" squares to 2x5 of 12 x 3-1/2 flats and drops the legs.  DEPTH is
# 9.25 because 1x10 pine comes 9-1/4 actual and there is no reason to lose it.
set -euo pipefail
cd "$(dirname "$0")/../.."          # repo root

S=lib/casework.scad
OUT=projects/document-unit/renders
EXP=projects/document-unit/exports
mkdir -p "$OUT" "$EXP"
. lib/cameras.sh

D=(-D 'PIECE="documents"' -D DEPTH=9.25)

echo "rendering document unit"
re hero      1250,950    44,-40,30,13.1,4.6,10          "${D[@]}"
r  front     1150,1000 o 13.125,4.6,11,90,0,0,72        "${D[@]}"
re exploded  1250,1000   50,-46,36,13.1,4.6,10          "${D[@]}" -D 'mode="exploded"'

echo "  meshes"
openscad -o "$EXP/document_unit.stl" "${D[@]}" "$S" >/dev/null 2>&1
openscad -o "$EXP/document_unit.3mf" "${D[@]}" "$S" >/dev/null 2>&1 || true

echo done
