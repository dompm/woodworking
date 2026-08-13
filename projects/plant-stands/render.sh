#!/usr/bin/env bash
# Plant stands: working drawings + meshes, via OpenSCAD (seconds).
#
# NOTE: the four-leg stand is built from a corner (centre 6,6); the three-leg
# one is built around the origin.  Different camera targets.
set -euo pipefail
cd "$(dirname "$0")/../.."          # repo root

S=projects/plant-stands/plant_stand.scad
OUT=projects/plant-stands/renders
EXP=projects/plant-stands/exports
mkdir -p "$OUT" "$EXP"
. lib/cameras.sh

echo "rendering four"
re four_hero   1000,1150   44,-40,34,6,6,9      -D 'STAND="four"'
re four_persp   950,1050   38,-34,20,6,6,8      -D 'STAND="four"'
r  four_front  1000,1050 o 6,6,9,90,0,0,60      -D 'STAND="four"'
openscad -o "$EXP/stand_four.stl" -D 'STAND="four"' "$S" >/dev/null 2>&1

echo "rendering three"
re three_hero  1000,1150   38,-34,30,0,0,9      -D 'STAND="three"'
re three_persp  950,1050   32,-28,16,0,0,8      -D 'STAND="three"'
r  three_front 1000,1050 o 0,0,9,90,0,0,60      -D 'STAND="three"'
openscad -o "$EXP/stand_three.stl" -D 'STAND="three"' "$S" >/dev/null 2>&1

echo done
