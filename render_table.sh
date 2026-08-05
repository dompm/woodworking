#!/usr/bin/env bash
# Coffee table: working drawings + meshes, via OpenSCAD (seconds).
#
#   ./render_table.sh          # all views + STL/3MF
#   ./render_table_beauty.sh   # per-part STLs + Cycles beauty shots (minutes)
#
# Camera arguments below are written in INCHES for readability and scaled to
# the model's output units (mm) on the way to OpenSCAD.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p renders exports

S=coffee_table.scad
U=25.4
OPTS="--colorscheme=Tomorrow"

# ecam <eyex,eyey,eyez,cx,cy,cz>  -- 6-value eye/centre camera, in inches
ecam() {
  awk -v u="$U" -v a="$1" 'BEGIN{
    n = split(a, p, ",");
    for (i = 1; i <= 6; i++) printf "%s%.4f", (i > 1 ? "," : ""), p[i]*u
  }'
}
# cam <tx,ty,tz,rx,ry,rz,dist>  -- translations and distance given in inches
cam() {
  awk -v u="$U" -v a="$1" 'BEGIN{
    n = split(a, p, ",");
    printf "%.4f,%.4f,%.4f,%s,%s,%s,%.4f", p[1]*u, p[2]*u, p[3]*u, p[4], p[5], p[6], p[7]*u
  }'
}

re() { # re <name> <imgsize> <eye-camera-inches> [extra -D args...]
  local name=$1 size=$2 camera=$3; shift 3
  echo "  table_${name}"
  openscad -o "renders/table_${name}.png" --imgsize="$size" --projection=p \
           $OPTS --camera="$(ecam "$camera")" "$@" "$S" >/dev/null 2>&1
}

r() { # r <name> <imgsize> <projection> <camera-inches> [extra -D args...]
  local name=$1 size=$2 proj=$3 camera=$4; shift 4
  echo "  table_${name}"
  openscad -o "renders/table_${name}.png" --imgsize="$size" --projection="$proj" \
           $OPTS --camera="$(cam "$camera")" "$@" "$S" >/dev/null 2>&1
}

echo "rendering"
r hero        1600,1050 p 24,10.5,7.0,70,0,26,100
r persp_end   1250,1000 p 24,10.5,7.0,72,0,66,128
r front       1700,600  o 24,10.5,7.5,90,0,0,52
r side         900,700  o 24,10.5,7.5,90,0,90,50
r top         1600,780  o 24,10.5,15,0,0,0,62
r exploded    1450,1300 p 24,10.5,13.0,66,0,34,180 -D 'mode="exploded"'
r base        1500,900  p 24,10.5,5.0,72,0,26,92   -D show_top=false
r parts       1450,1000 p 32,17,1,60,0,22,145      -D 'mode="parts"'
r edge        1500,760  o 24,3.0,13.15,90,0,90,9.8  -D 'mode="edge"' -D show_shelf=false
re joint      1350,1050   36,-34,26,8,4,7.5        -D 'mode="joint"'

# Mesh export.  With UNIT = 25.4 the model is emitted in millimetres, which is
# what every downstream tool assumes.
echo "  meshes"
openscad -o exports/coffee_table.stl "$S" >/dev/null 2>&1
openscad -o exports/coffee_table.3mf "$S" >/dev/null 2>&1 || true

echo "done"
