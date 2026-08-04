#!/usr/bin/env bash
# Re-render every view and export the mesh.  Requires OpenSCAD on PATH.
#
# Camera arguments below are written in INCHES for readability and scaled to
# the model's output units (mm) on the way to OpenSCAD.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p renders exports

S=wine_rack.scad
U=25.4
OPTS="--colorscheme=Tomorrow"

# cam <tx,ty,tz,rx,ry,rz,dist>  -- translations and distance given in inches
cam() {
  awk -v u="$U" -v a="$1" 'BEGIN{
    n = split(a, p, ",");
    printf "%.4f,%.4f,%.4f,%s,%s,%s,%.4f", p[1]*u, p[2]*u, p[3]*u, p[4], p[5], p[6], p[7]*u
  }'
}
# ecam <eyex,eyey,eyez,cx,cy,cz>  -- 6-value eye/centre camera, in inches
ecam() {
  awk -v u="$U" -v a="$1" 'BEGIN{
    n = split(a, p, ",");
    for (i = 1; i <= 6; i++) printf "%s%.4f", (i > 1 ? "," : ""), p[i]*u
  }'
}

re() { # re <name> <imgsize> <eye-camera-inches> [extra -D args...]
  local name=$1 size=$2 camera=$3; shift 3
  echo "  $name"
  openscad -o "renders/${name}.png" --imgsize="$size" --projection=p \
           $OPTS --camera="$(ecam "$camera")" "$@" "$S" >/dev/null 2>&1
}

r() { # r <name> <imgsize> <projection> <camera-inches> [extra -D args...]
  local name=$1 size=$2 proj=$3 camera=$4; shift 4
  echo "  $name"
  openscad -o "renders/${name}.png" --imgsize="$size" --projection="$proj" \
           $OPTS --camera="$(cam "$camera")" "$@" "$S" >/dev/null 2>&1
}

echo "rendering"
r hero          1100,1500 p 5.125,4.5,9.25,65,0,28,105
r persp         1100,1500 p 5.125,4.5,9.25,65,0,28,105 -D show_bottles=false
r front          600,1450 o 5.125,4.5,9.25,90,0,0,115  -D show_bottles=false
r side           600,1450 o 5.125,4.5,9.25,90,0,90,115 -D show_bottles=false
r side_bottles   900,1450 o 5.125,4.5,9.25,90,0,90,115
r top            760,700  o 5.125,4.5,29.25,0,0,0,45   -D show_bottles=false -D show_legs=false
r exploded      1300,1500 p 5.125,4.5,9.25,68,0,32,140 -D 'mode="exploded"'
r joint         1100,900  p 1.6,4.0,29.5,74,0,25,20    -D 'mode="joint"'
r corner_top    1100,900  p 1.6,4.0,28.6,66,0,30,17    -D show_bottles=false -D show_legs=false
r base          1100,850  p 5.125,4.5,-3,74,0,30,30    -D show_bottles=false
re lap          1150,900    20,-22,17,5.1,4.5,0.4      -D 'mode="lap"'
re eggcrate     1150,1250   52,-50,44,5.1,7,14.6       -D 'mode="eggcrate"'
re motion       1200,1000   30,-34,44,5.125,4.5,28.6   -D 'mode="motion"'
re stile         800,1350   66,-40,34,0.375,4.5,14.6   -D 'mode="stile"'

# Jig drawings (separate model)
echo "  jigs"
mkdir -p renders/jigs
JCAM="$(ecam 24,-20,26,8.5,4.2,0.4)"
for j in dado dado_pass2; do
  openscad -o "renders/jigs/$j.png" --imgsize=1250,980 --projection=p $OPTS \
           --camera="$JCAM" -D 'mode="none"' -D "JIG=\"$j\"" jigs.scad >/dev/null 2>&1
done
openscad -o renders/jigs/dado_pair.png --imgsize=1300,1000 --projection=p $OPTS \
         --camera="$(ecam 34,-30,29,7.5,9,0.4)" -D 'mode="none"' -D 'JIG="dado_pair"' jigs.scad >/dev/null 2>&1
openscad -o renders/jigs/slot.png --imgsize=1300,1000 --projection=p $OPTS \
         --camera="$(ecam 19,27,26,4.6,4.5,0.4)" -D 'mode="none"' -D 'JIG="slot"' jigs.scad >/dev/null 2>&1

# Mesh export.  With UNIT = 25.4 the model is emitted in millimetres, which is
# what every downstream tool assumes.
echo "  meshes"
openscad -o exports/wine_rack.stl -D show_bottles=false "$S" >/dev/null 2>&1
openscad -o exports/wine_rack.3mf -D show_bottles=false "$S" >/dev/null 2>&1 || true

echo "done"
