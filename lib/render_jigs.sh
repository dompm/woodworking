#!/usr/bin/env bash
# Shop jig drawings.  These belong to no single project -- the same T-square,
# U-jig and rip sled build the wine rack, the document unit and whatever comes
# next -- so they render out of lib/ and every guide pulls from here.
set -euo pipefail
cd "$(dirname "$0")/.."             # repo root

S=lib/jigs.scad
OUT=lib/renders/jigs
mkdir -p "$OUT"
. lib/cameras.sh

# jig <name> <imgsize> <eye-camera-inches>
jig() {
  local name=$1 size=$2 camera=$3
  echo "  $name"
  openscad -o "$OUT/${name}.png" --imgsize="$size" --projection=p $OPTS \
           --camera="$(ecam "$camera")" -D 'mode="none"' -D "JIG=\"$name\"" \
           "$S" >/dev/null 2>&1
}

echo "rendering jigs"
jig dado                 1250,980   24,-20,26,8.5,4.2,0.4
jig dado_pass2           1250,980   24,-20,26,8.5,4.2,0.4
jig dado_pair            1300,1000  34,-30,29,7.5,9,0.4
jig slot                 1300,1000  19,27,26,4.6,4.5,0.4
jig ujig                 1250,980   22,-19,27,8.7,4.2,0.4
jig ujig_bearing         1250,980   22,-19,27,8.7,4.2,0.4
# Close in and low, looking along the fence: the point of this one is the
# bearing riding the template, so the section has to fill the frame.
jig ujig_bearing_section 1250,820   10.9,-4.2,2.9,9.35,6.5,0.95
jig ripsled              1250,880   46,-56,40,13,0,1
jig stopblock            1250,880   26,-58,40,-1.6,-3.5,1

echo done
