#!/usr/bin/env bash
# Footrest: working drawings + mesh, via OpenSCAD (seconds).
#
# Camera arguments are in inches; lib/cameras.sh scales them to the model's
# output units on the way to OpenSCAD.
set -euo pipefail
cd "$(dirname "$0")/../.."          # repo root

S=projects/footrest/footrest.scad
OUT=projects/footrest/renders
EXP=projects/footrest/exports
mkdir -p "$OUT" "$EXP"
. lib/cameras.sh

echo "rendering footrest"
# NOTE: x is DEPTH (front to back) here and y is WIDTH -- the opposite of the
# casework.  So the wedge profile is the view along Y.
re hero      1500,1050   26,-24,17,5.2,8.5,2.6
re persp     1300,1000   22,-19,11,5.2,8.5,2.2
r  profile   1100,620  o 5.2,8.5,2.75,90,0,0,24
r  front     1400,560  o 5.2,8.5,2.75,90,0,90,34
r  top       1300,850  o 5.2,8.5,2.75,0,0,0,26
re exploded  1500,1150   28,-26,19,5.2,8.5,2.6         -D 'mode="exploded"'
r  sidepart  1100,620  o 5.2,0.4,2.4,90,0,0,24         -D 'mode="side"'

echo "  mesh"
openscad -o "$EXP/footrest.stl" "$S" >/dev/null 2>&1
openscad -o "$EXP/footrest.3mf" "$S" >/dev/null 2>&1 || true

echo done
