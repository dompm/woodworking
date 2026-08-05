#!/usr/bin/env bash
# Shared OpenSCAD camera helpers, sourced by each project's render.sh.
#
# Every camera argument in this repo is written in INCHES, because that is how
# the drawings and the cut lists are dimensioned and it is the only way the
# numbers stay readable.  The models emit millimetres (UNIT = 25.4), so the
# conversion happens here, once, instead of in every call site.
#
# Callers must set, before sourcing:
#   S    -- the .scad file to render
#   OUT  -- directory the .png files go into
#
# and may set OPTS (defaults to the Tomorrow colour scheme).

OPTS="${OPTS:---colorscheme=Tomorrow}"

# cam <tx,ty,tz,rx,ry,rz,dist>  -- gimbal camera; translations and distance in inches
cam() {
  awk -v u=25.4 -v a="$1" 'BEGIN{
    split(a, p, ",");
    printf "%.4f,%.4f,%.4f,%s,%s,%s,%.4f", p[1]*u, p[2]*u, p[3]*u, p[4], p[5], p[6], p[7]*u
  }'
}

# ecam <eyex,eyey,eyez,cx,cy,cz>  -- eye/centre camera, all six values in inches
ecam() {
  awk -v u=25.4 -v a="$1" 'BEGIN{
    split(a, p, ",");
    for (i = 1; i <= 6; i++) printf "%s%.4f", (i > 1 ? "," : ""), p[i]*u
  }'
}

# r <name> <imgsize> <projection> <gimbal-camera> [extra -D args...]
r() {
  local name=$1 size=$2 proj=$3 camera=$4; shift 4
  echo "  $name"
  openscad -o "$OUT/${name}.png" --imgsize="$size" --projection="$proj" \
           $OPTS --camera="$(cam "$camera")" "$@" "$S" >/dev/null 2>&1
}

# re <name> <imgsize> <eye-camera> [extra -D args...]   -- always perspective
re() {
  local name=$1 size=$2 camera=$3; shift 3
  echo "  $name"
  openscad -o "$OUT/${name}.png" --imgsize="$size" --projection=p \
           $OPTS --camera="$(ecam "$camera")" "$@" "$S" >/dev/null 2>&1
}
