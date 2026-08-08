#!/usr/bin/env bash
# Salt boxes: working drawings + meshes, via OpenSCAD (seconds).
set -euo pipefail
cd "$(dirname "$0")/../.."          # repo root

S=projects/salt-boxes/salt_box.scad
OUT=projects/salt-boxes/renders
EXP=projects/salt-boxes/exports
mkdir -p "$OUT" "$EXP"
. lib/cameras.sh

# two boxes: 1 middle layer for MSG, 2 for sugar
for n in 2 3; do
  L="-D LAYERS=$n"
  echo "rendering ${n}-layer"
  re "L${n}_hero"     900,800    14,-12,10,0.6,1.75,1.4   $L
  re "L${n}_open"     900,800    14,-12,10,0.6,1.75,1.4   $L -D 'mode="open"'
  re "L${n}_exploded" 900,1000  15,-13,12,1.75,1.75,2.2   $L -D 'mode="exploded"'
  re "L${n}_section"  900,750    12,-10,7,1.75,1.0,1.3   $L -D 'mode="section"'
  openscad -o "$EXP/salt_box_${n}layer.stl" $L "$S" >/dev/null 2>&1
done

echo done
