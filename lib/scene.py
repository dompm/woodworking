"""
Beauty render of a piece from this repo.

Imports the per-part STLs written by lib/export_casework.scad (wine rack,
document unit) or projects/coffee-table/export_parts.scad, builds a procedural
wood shader (no external texture files), lights a small studio set and renders
with Cycles.

--parts and --out are relative to the repo root, so a project's render_beauty.sh
points them inside its own directory.  Normally you would run that script rather
than calling this directly.

    /Applications/Blender.app/Contents/MacOS/Blender -b -P lib/scene.py -- \
        --parts projects/wine-rack/exports/parts --wood walnut \
        --out projects/wine-rack/renders/beauty_walnut.png --samples 256

    /Applications/Blender.app/Contents/MacOS/Blender -b -P lib/scene.py -- \
        --model table --parts projects/coffee-table/exports/parts \
        --view table --res 2000x1300 \
        --out projects/coffee-table/renders/beauty_walnut.png

Grain runs along each board's own long axis, so there is one material per axis.
The wine rack needs two: every carcass part has its 9" dimension front to back,
so the rings always band across Y and only the length axis changes.  The coffee
table needs all three -- the top and aprons are long in X, the breadboard ends
and the shelf rails are long in Y, the legs in Z.

The wine rack's defaults are untouched by the coffee table's arrival: --model
defaults to winerack, and its light rig, part groups and camera views are the
same numbers they always were.
"""
import argparse
import math
import os
import sys

import bpy
from mathutils import Vector

# --------------------------------------------------------------------------
# args
# --------------------------------------------------------------------------
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--wood", default="walnut", choices=["walnut", "cherry", "pine"])
ap.add_argument("--out", default="projects/wine-rack/renders/beauty.png")
ap.add_argument("--samples", type=int, default=256)
ap.add_argument("--res", default="1400x1900")
ap.add_argument("--parts", default="projects/wine-rack/exports/parts")
ap.add_argument("--view", default="hero",
                choices=["hero", "front", "detail", "wide",
                         "table", "table_end", "table_detail"])
ap.add_argument("--model", default="winerack", choices=["winerack", "table"])
# Ring scale multiplier.  The ring pitch that reads as walnut on a 9"-wide
# carcass board turns into moire on a 1-3/4" leg: same physical pitch, far
# fewer pixels across the part.  Coarser rings calm the legs down and, as a
# bonus, put some contrast back into a big flat top that was reading as paint.
ap.add_argument("--rings", type=float, default=1.0)
ap.add_argument("--bottles", default="1")
args = ap.parse_args(argv)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTS = os.path.join(ROOT, args.parts)
RES_X, RES_Y = (int(v) for v in args.res.split("x"))

# Per species.  The ring PROFILE and the knot density are what actually
# identify a wood -- more than its colour.
#
#   profile SAW : earlywood widens gradually, then the ring boundary is abrupt.
#                 That asymmetry is the signature of a softwood.
#   profile SIN : soft, low-contrast gradation, typical of a diffuse-porous
#                 hardwood like walnut or cherry.
#   stops       : where the ramp turns over.  Pushed late for pine, so most of
#                 the field is pale earlywood and the dark latewood is a narrow
#                 hard-edged line rather than half the surface.
WOODS = {
    "walnut": dict(light=(0.352, 0.252, 0.182), dark=(0.198, 0.130, 0.090),
                   knot=(0.13, 0.085, 0.06), profile="SIN", stops=(0.22, 0.84),
                   rings=300.0, knots=0.0, rough=(0.44, 0.64)),
    "cherry": dict(light=(0.630, 0.372, 0.232), dark=(0.450, 0.242, 0.150),
                   knot=(0.28, 0.14, 0.09), profile="SIN", stops=(0.14, 0.90),
                   rings=320.0, knots=0.0, rough=(0.42, 0.62)),
    # Pine: pale field, narrow dark latewood, and knots -- a clear pine board
    # reads as anonymous blonde hardwood, which is exactly what went wrong the
    # first time round.
    "pine":   dict(light=(0.885, 0.780, 0.590), dark=(0.430, 0.278, 0.148),
                   knot=(0.34, 0.215, 0.115), profile="SAW", stops=(0.78, 0.86),
                   rings=380.0, knots=1.0, rough=(0.40, 0.60)),
}
SPEC = WOODS[args.wood]
LIGHT, DARK = SPEC["light"], SPEC["dark"]


def srgb_to_linear(c):
    return tuple(
        (v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in c
    ) + (1.0,)


# --------------------------------------------------------------------------
# scene reset
# --------------------------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = args.samples
scene.cycles.use_denoising = True
scene.render.resolution_x = RES_X
scene.render.resolution_y = RES_Y
scene.render.film_transparent = False
scene.render.image_settings.file_format = "PNG"

# Metal GPU if this machine has one, otherwise CPU.
try:
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "METAL"
    prefs.get_devices()
    for d in prefs.devices:
        d.use = True
    scene.cycles.device = "GPU"
    print("cycles: GPU (metal)")
except Exception as exc:  # pragma: no cover - depends on the machine
    scene.cycles.device = "CPU"
    print("cycles: CPU (%s)" % exc)

# AgX desaturates bright values hard, which turns lit walnut into grey.
# Prefer the product-viz transform, which holds saturation into the highlights.
for vt in ("Khronos PBR Neutral", "Filmic", "AgX", "Standard"):
    try:
        scene.view_settings.view_transform = vt
        print("view transform:", vt)
        break
    except Exception:
        continue
# A big horizontal top faces the lights squarely and blows out where the wine
# rack's mostly vertical faces do not; half a stop down keeps the walnut brown
# instead of tan.
scene.view_settings.exposure = -0.35 if args.model == "table" else 0.0


# --------------------------------------------------------------------------
# import
# --------------------------------------------------------------------------
def import_stl(path):
    before = set(bpy.data.objects)
    if hasattr(bpy.ops.wm, "stl_import"):
        bpy.ops.wm.stl_import(filepath=path, global_scale=0.001)
    else:
        bpy.ops.import_mesh.stl(filepath=path, global_scale=0.001)
    new = list(set(bpy.data.objects) - before)
    return new[0] if new else None


def shade_smooth(obj, angle_deg=32):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()
    for op in ("shade_auto_smooth", "shade_smooth_by_angle"):
        if hasattr(bpy.ops.object, op):
            try:
                getattr(bpy.ops.object, op)(angle=math.radians(angle_deg))
                return
            except Exception:
                pass


MODELS = {
    "winerack": dict(
        groups={
            "wood_z": ["stile0", "stile1", "divider",
                       "leg0", "leg1", "leg2", "leg3", "blocks"],
            "wood_x": ["horiz%d" % i for i in range(7)],
            "brass": ["brass"],
            "steel": ["steel"],
            "glass": ["bottles"],
        },
        smooth={"leg0", "leg1", "leg2", "leg3", "brass", "bottles"},
    ),
    "table": dict(
        groups={
            # long in X: the top, both long rails, the shelf, the buttons
            "wood_xq": ["top", "rail0", "rail1", "shelf", "buttons"],
            # long in Y: the cross rails, and the loose tenons, whose grain runs
            # along the joint the same way
            "wood_y": ["xrail0", "xrail1", "tenons"],
            "wood_zq": ["leg0", "leg1", "leg2", "leg3"],
        },
        smooth=set(),
    ),
}
GROUPS = MODELS[args.model]["groups"]
SMOOTH = MODELS[args.model]["smooth"]

imported = {}
for group, names in GROUPS.items():
    if group == "glass" and args.bottles == "0":
        continue
    for name in names:
        path = os.path.join(PARTS, name + ".stl")
        if not os.path.exists(path):
            print("missing:", path)
            continue
        obj = import_stl(path)
        obj.name = name
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        # The STL importer applies global_scale to the OBJECT transform and
        # leaves the mesh in millimetres.  Object texture coordinates are taken
        # from mesh-local space, so without baking the scale in, the wood grain
        # is ~1000x too fine and averages out to flat colour.
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        # per-object origin so each board gets its own texture space
        bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
        if name in SMOOTH:
            shade_smooth(obj)
        imported.setdefault(group, []).append(obj)

all_objs = [o for objs in imported.values() for o in objs]
if not all_objs:
    raise SystemExit("nothing imported from %s" % PARTS)

# drop the whole assembly so the feet sit on z = 0
min_z = min(
    (o.matrix_world @ Vector(c)).z for o in all_objs for c in o.bound_box
)
for o in all_objs:
    o.location.z -= min_z
# matrix_world is cached; without this the bounds below are the pre-shift ones
# and every light and the camera get sized to the wrong height
bpy.context.view_layer.update()

xs = [(o.matrix_world @ Vector(c)).x for o in all_objs for c in o.bound_box]
ys = [(o.matrix_world @ Vector(c)).y for o in all_objs for c in o.bound_box]
zs = [(o.matrix_world @ Vector(c)).z for o in all_objs for c in o.bound_box]
CX, CY = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
TOP = max(zs)
print("bounds  x %.3f..%.3f  y %.3f..%.3f  z %.3f..%.3f"
      % (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)))


# --------------------------------------------------------------------------
# materials
# --------------------------------------------------------------------------
def new_mat(name):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat, nt, bsdf


def wood_material(name, length_axis, pith_d=0.110, warp=1.0, quarter=False):
    """Growth rings as concentric cylinders around a pith axis, which is what
    they physically are.  A board is then an off-centre slice through those
    cylinders, and the cathedral figure falls out of the geometry instead of
    being faked with wobbly parallel bands."""
    mat, nt, bsdf = new_mat(name)
    axis = length_axis                      # 'X', 'Y' or 'Z': the grain direction

    coord = nt.nodes.new("ShaderNodeTexCoord")
    objinfo = nt.nodes.new("ShaderNodeObjectInfo")

    # Per-object variation.  This has to be anisotropic: a big random offset
    # ALONG the grain just means the board was cut from further up the log,
    # which is what we want.  The same offset across the grain would move the
    # pith itself and destroy the ring geometry entirely.
    along = nt.nodes.new("ShaderNodeMath")
    along.operation = "MULTIPLY"
    along.inputs[1].default_value = 4.0
    nt.links.new(objinfo.outputs["Random"], along.inputs[0])

    cross = nt.nodes.new("ShaderNodeMath")          # +/- 15 mm on the pith
    cross.operation = "MULTIPLY_ADD"
    cross.inputs[1].default_value = 0.030
    cross.inputs[2].default_value = -0.015
    nt.links.new(objinfo.outputs["Random"], cross.inputs[0])

    comb = nt.nodes.new("ShaderNodeCombineXYZ")
    for ax in ("X", "Y", "Z"):
        src = along if ax == axis else cross
        nt.links.new(src.outputs["Value"], comb.inputs[ax])
    rnd = comb

    # Push the pith well outside the board, in the two axes that are NOT the
    # grain.  The board then sits on an arc of large radius: nearly straight
    # across its width, curving over its length.  Move the pith closer and the
    # board reads as quartersawn; further and it flattens out.
    # Flatsawn: the pith sits well below the WIDE face, so the board is a
    # shallow off-centre slice and the rings surface as nested arcs about the
    # centreline -- cathedral figure, derived rather than drawn.
    # For a Y board the wide face is still up, so the pith goes deep in Z and
    # only a little in X -- the same relationship an X board has, turned 90
    # degrees in plan.
    # Flatsawn: the pith sits below the WIDE face, so the board is a shallow
    # off-centre slice and the rings surface as nested arcs -- cathedral figure.
    # QUARTERSAWN: the pith sits off to the SIDE instead, so the rings stand on
    # edge in the board and reach the face as straight parallel lines.  That is
    # what the top of this table is specified as, and it is also the only way a
    # 21"-wide panel stops reading as corduroy: the lines are meant to be
    # straight, they just have to be at a believable pitch and not aliasing.
    pith = ({"X": (0.0, pith_d, 0.008),
             "Y": (pith_d, 0.0, 0.008),
             "Z": (pith_d, 0.008, 0.0)}[axis] if quarter else
            {"X": (0.0, 0.010, pith_d),
             "Y": (0.010, 0.0, pith_d),
             "Z": (pith_d, 0.010, 0.0)}[axis])
    off = nt.nodes.new("ShaderNodeVectorMath")
    off.operation = "ADD"
    off.inputs[1].default_value = pith
    nt.links.new(rnd.outputs["Vector"], off.inputs[0])

    base = nt.nodes.new("ShaderNodeVectorMath")
    base.operation = "ADD"
    nt.links.new(coord.outputs["Object"], base.inputs[0])
    nt.links.new(off.outputs["Vector"], base.inputs[1])

    # Warp the ring field.  Stretched hard ALONG the grain, so the wander is
    # long and slow -- that is what turns concentric rings into cathedrals
    # rather than into noise.
    stretch = nt.nodes.new("ShaderNodeMapping")
    stretch.inputs["Scale"].default_value = {
        "X": (0.10, 1.0, 1.0), "Y": (1.0, 0.10, 1.0), "Z": (1.0, 1.0, 0.10)}[axis]
    nt.links.new(base.outputs["Vector"], stretch.inputs["Vector"])

    warpn = nt.nodes.new("ShaderNodeTexNoise")
    warpn.inputs["Scale"].default_value = 9.0
    warpn.inputs["Detail"].default_value = 4.0
    warpn.inputs["Roughness"].default_value = 0.55
    nt.links.new(stretch.outputs["Vector"], warpn.inputs["Vector"])

    ctr = nt.nodes.new("ShaderNodeVectorMath")
    ctr.operation = "SUBTRACT"
    ctr.inputs[1].default_value = (0.5, 0.5, 0.5)
    nt.links.new(warpn.outputs["Color"], ctr.inputs[0])

    amt = nt.nodes.new("ShaderNodeVectorMath")
    amt.operation = "SCALE"
    # 20 mm of wander across a ring pitch under a millimetre is what turns
    # concentric circles into cathedral figure.  Parts that are meant to read as
    # riftsawn get a fraction of it (see wood_zq).
    amt.inputs["Scale"].default_value = 0.020 * warp
    nt.links.new(ctr.outputs["Vector"], amt.inputs[0])

    warped = nt.nodes.new("ShaderNodeVectorMath")
    warped.operation = "ADD"
    nt.links.new(base.outputs["Vector"], warped.inputs[0])
    nt.links.new(amt.outputs["Vector"], warped.inputs[1])

    # Knots: Voronoi feature points scattered through the board.  Near one, the
    # rings deflect (phase offset) and the colour darkens -- which is what a
    # branch actually does to the wood around it.
    flat = nt.nodes.new("ShaderNodeMapping")
    flat.inputs["Scale"].default_value = {
        "X": (1.0, 1.0, 0.0), "Y": (1.0, 1.0, 0.0), "Z": (0.0, 1.0, 1.0)}[axis]
    nt.links.new(base.outputs["Vector"], flat.inputs["Vector"])

    vor = nt.nodes.new("ShaderNodeTexVoronoi")
    vor.feature = "F1"
    vor.inputs["Scale"].default_value = 7.0
    vor.inputs["Randomness"].default_value = 1.0
    nt.links.new(flat.outputs["Vector"], vor.inputs["Vector"])

    # Voronoi reports Distance in SCALED units, where a cell is about 1 across
    # -- so the radius here is in cell fractions, not metres.
    knot = nt.nodes.new("ShaderNodeMapRange")          # 1 at the centre, 0 away
    knot.inputs["From Min"].default_value = 0.0
    knot.inputs["From Max"].default_value = 0.17
    knot.inputs["To Min"].default_value = 1.0
    knot.inputs["To Max"].default_value = 0.0
    knot.clamp = True
    nt.links.new(vor.outputs["Distance"], knot.inputs["Value"])

    # not every cell gets a knot -- a board with a knot every 5 inches reads
    # as a pallet, not as furniture stock
    gate = nt.nodes.new("ShaderNodeMath")
    gate.operation = "GREATER_THAN"
    gate.inputs[1].default_value = 0.62
    nt.links.new(vor.outputs["Color"], gate.inputs[0])

    gated = nt.nodes.new("ShaderNodeMath")
    gated.operation = "MULTIPLY"
    nt.links.new(knot.outputs["Result"], gated.inputs[0])
    nt.links.new(gate.outputs["Value"], gated.inputs[1])

    knot_amt = nt.nodes.new("ShaderNodeMath")
    knot_amt.operation = "MULTIPLY"
    knot_amt.inputs[1].default_value = SPEC["knots"]
    nt.links.new(gated.outputs["Value"], knot_amt.inputs[0])

    deflect = nt.nodes.new("ShaderNodeMath")
    deflect.operation = "MULTIPLY"
    deflect.inputs[1].default_value = 2.6
    nt.links.new(knot_amt.outputs["Value"], deflect.inputs[0])

    # the rings themselves, concentric about the grain axis
    rings = nt.nodes.new("ShaderNodeTexWave")
    rings.wave_type = "RINGS"
    rings.rings_direction = axis
    rings.wave_profile = SPEC["profile"]
    rings.inputs["Scale"].default_value = SPEC["rings"] * args.rings
    rings.inputs["Distortion"].default_value = 1.0
    rings.inputs["Detail"].default_value = 2.0
    rings.inputs["Detail Scale"].default_value = 0.8
    nt.links.new(warped.outputs["Vector"], rings.inputs["Vector"])
    nt.links.new(deflect.outputs["Value"], rings.inputs["Phase Offset"])

    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.interpolation = "EASE" if SPEC["profile"] == "SAW" else "B_SPLINE"
    ramp.color_ramp.elements[0].position = SPEC["stops"][0]
    ramp.color_ramp.elements[0].color = srgb_to_linear(LIGHT)
    ramp.color_ramp.elements[1].position = SPEC["stops"][1]
    ramp.color_ramp.elements[1].color = srgb_to_linear(DARK)
    nt.links.new(rings.outputs["Fac"], ramp.inputs["Fac"])

    # darken into the knot itself
    kmix = nt.nodes.new("ShaderNodeMix")
    kmix.data_type = "RGBA"
    kmix.inputs[6].default_value = (0, 0, 0, 1)
    kmix.inputs[7].default_value = srgb_to_linear(SPEC["knot"])
    nt.links.new(ramp.outputs["Color"], kmix.inputs[6])
    nt.links.new(knot_amt.outputs["Value"], kmix.inputs[0])
    nt.links.new(kmix.outputs[2], bsdf.inputs["Base Color"])

    # satin oil finish, roughness tracking the rings a little
    rough = nt.nodes.new("ShaderNodeMapRange")
    rough.inputs["To Min"].default_value = SPEC["rough"][0]
    rough.inputs["To Max"].default_value = SPEC["rough"][1]
    nt.links.new(rings.outputs["Fac"], rough.inputs["Value"])
    nt.links.new(rough.outputs["Result"], bsdf.inputs["Roughness"])
    bsdf.inputs["Specular IOR Level"].default_value = 0.25

    # open pores / fibre, very subtle
    pores = nt.nodes.new("ShaderNodeTexNoise")
    pores.inputs["Scale"].default_value = 900.0
    pores.inputs["Detail"].default_value = 2.0
    nt.links.new(stretch.outputs["Vector"], pores.inputs["Vector"])
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.04
    nt.links.new(pores.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


def brass_material():
    mat, nt, bsdf = new_mat("brass")
    bsdf.inputs["Base Color"].default_value = srgb_to_linear((0.82, 0.66, 0.32))
    bsdf.inputs["Metallic"].default_value = 1.0
    bsdf.inputs["Roughness"].default_value = 0.22
    return mat


def steel_material():
    mat, nt, bsdf = new_mat("steel")
    bsdf.inputs["Base Color"].default_value = srgb_to_linear((0.16, 0.17, 0.19))
    bsdf.inputs["Metallic"].default_value = 1.0
    bsdf.inputs["Roughness"].default_value = 0.45
    return mat


def glass_material():
    """Bottle glass.  The bottles are solid meshes, so plain transmission makes
    them glow like lanterns.  Volume absorption is what actually makes a wine
    bottle read as near-black with green edges."""
    mat, nt, bsdf = new_mat("glass")
    bsdf.inputs["Base Color"].default_value = srgb_to_linear((0.30, 0.42, 0.30))
    bsdf.inputs["Roughness"].default_value = 0.05
    bsdf.inputs["Transmission Weight"].default_value = 1.0
    bsdf.inputs["IOR"].default_value = 1.52
    out = [n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"][0]
    vol = nt.nodes.new("ShaderNodeVolumeAbsorption")
    vol.inputs["Color"].default_value = srgb_to_linear((0.16, 0.38, 0.18))
    vol.inputs["Density"].default_value = 55.0
    nt.links.new(vol.outputs["Volume"], out.inputs["Volume"])
    return mat


MATS = {
    "wood_x": wood_material("wood_x", "X"),
    "wood_y": wood_material("wood_y", "Y"),
    "wood_z": wood_material("wood_z", "Z"),
    # A LEG is riftsawn stock -- straight grain, no cathedral.  Modelled with
    # the pith eight times further out, so the board sits on an almost flat arc
    # and the rings run straight up the post.  Leave it at the flatsawn 110 mm
    # and the leg gets the cathedral figure of a wide board squeezed into
    # 1-3/4", which renders as a herringbone and looks like a printed veneer.
    #
    # The warp has to come down with it.  Two of the leg's four faces are
    # TANGENT to the ring cylinders, so the radius barely changes across them
    # and there is no ring gradient for the warp to perturb -- the warp becomes
    # the whole pattern, and 10 mm of it on a 1-3/4" face renders as a violent
    # chevron on one face while the face beside it stays perfectly straight.
    "wood_zq": wood_material("wood_zq", "Z", pith_d=0.90, warp=0.22),
    # The coffee table's top is 21" wide where the wine rack's boards are 9".
    # At the wine rack's pith distance the cathedrals get squeezed into tight
    # parallel bands and the whole panel reads as corduroy; pushing the pith
    # nearly four times further out gives long, lazy arcs instead -- broad in
    # the middle of the board and closing up toward the edges, which is what a
    # wide walnut top actually looks like.
    "wood_xq": wood_material("wood_xq", "X", pith_d=0.42),
    "brass": brass_material(),
    "steel": steel_material(),
    "glass": glass_material(),
}
for group, objs in imported.items():
    for o in objs:
        o.data.materials.clear()
        o.data.materials.append(MATS[group])


# --------------------------------------------------------------------------
# set
# --------------------------------------------------------------------------
bpy.ops.mesh.primitive_plane_add(size=14, location=(CX, CY, 0))
floor = bpy.context.object
floor.name = "floor"
fm, fnt, fb = new_mat("floor")
fb.inputs["Base Color"].default_value = srgb_to_linear((0.30, 0.29, 0.275))
fb.inputs["Roughness"].default_value = 0.55
floor.data.materials.append(fm)

world = bpy.data.worlds.new("world")
scene.world = world
world.use_nodes = True
wnt = world.node_tree
wnt.nodes.clear()
wout = wnt.nodes.new("ShaderNodeOutputWorld")
wbg = wnt.nodes.new("ShaderNodeBackground")
wbg.inputs["Color"].default_value = (0.075, 0.080, 0.092, 1.0)
wbg.inputs["Strength"].default_value = 1.6
wnt.links.new(wbg.outputs["Background"], wout.inputs["Surface"])


def area_light(name, loc, look_at, size, power, color=(1, 1, 1)):
    d = bpy.data.lights.new(name, type="AREA")
    d.size = size
    d.energy = power
    d.color = color
    o = bpy.data.objects.new(name, d)
    scene.collection.objects.link(o)
    o.location = loc
    direction = Vector(look_at) - Vector(loc)
    o.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    return o


# The rig is sized off the piece's own height, which works for the wine rack
# (1.0 m tall and narrow) and fails completely for a coffee table: 0.66 of a
# 0.39 m height puts the key light 26 cm off the floor, inside the piece.  A low
# wide piece gets absolute heights and a wider spread instead, and more power to
# pay for the extra distance.  SPREAD/SIZE/POWER are all 1 for the wine rack, so
# its numbers are exactly what they were.
if args.model == "table":
    AIM_Z = TOP + 0.08
    KEY_Z, FILL_Z, RIM_Z = 2.40, 1.90, 2.60
    SPREAD, SIZE, POWER = 1.0, 2.0, 0.85
else:
    AIM_Z = TOP * 0.46
    KEY_Z, FILL_Z, RIM_Z = TOP * 0.66, TOP * 0.60, TOP * 0.70
    SPREAD, SIZE, POWER = 1.0, 1.0, 1.0

target = Vector((CX, CY, AIM_Z))
area_light("key", (CX + 1.7 * SPREAD, CY - 2.2 * SPREAD, KEY_Z), target,
           1.3 * SIZE, 150 * POWER, (1.0, 0.96, 0.90))
area_light("fill", (CX - 2.1 * SPREAD, CY - 1.7 * SPREAD, FILL_Z), target,
           1.2 * SIZE, 55 * POWER, (0.90, 0.94, 1.0))
area_light("rim", (CX - 1.3 * SPREAD, CY + 2.1 * SPREAD, RIM_Z), target,
           1.0 * SIZE, 80 * POWER, (1.0, 0.98, 0.95))

# A coffee table is mostly UNDERSIDE from any normal viewpoint, and a rig built
# for a tall case leaves the shelf, the aprons and every joint in it black.  One
# broad, weak, low source from the front opens all of that without touching the
# top, which is already lit from above.
if args.model == "table":
    area_light("under", (CX + 0.5, CY - 2.2, 0.26),
               Vector((CX, CY, 0.17)), 2.6, 90, (1.0, 0.96, 0.90))


# --------------------------------------------------------------------------
# camera
# --------------------------------------------------------------------------
VIEWS = {
    # (azimuth deg from -Y, elevation deg, distance m, focal mm, aim height frac)
    "hero":   (34, 6, 3.2, 85, 0.46),
    "front":  (4, 6, 3.2, 105, 0.50),
    "detail": (40, -4, 1.3, 85, 0.13),
    # for a wide, low case rather than a tall narrow one
    "wide":   (32, 12, 2.15, 70, 0.50),
    # The coffee table: 1.27 m long and 0.39 m tall, so the camera has to be a
    # long way back and only a little above the top.  Drop below about 12
    # degrees of elevation and the shelf disappears behind the front apron.
    "table":        (34, 15, 2.95, 60, 0.62),
    "table_end":    (74, 13, 2.30, 70, 0.62),
    # a sixth element shifts the aim point along the length, as a fraction of
    # the half length -- the wine rack's views omit it and are unaffected
    "table_detail": (46, 4, 1.00, 85, 0.44, -0.74, -0.55),
}
_v = VIEWS[args.view]
az, el, dist, focal, aim = _v[:5]
aimx = _v[5] if len(_v) > 5 else 0.0
aimy = _v[6] if len(_v) > 6 else 0.0
aim_pt = Vector((CX + aimx * (max(xs) - min(xs)) / 2,
                 CY + aimy * (max(ys) - min(ys)) / 2,
                 TOP * aim))
cam_dir = Vector((
    math.sin(math.radians(az)) * math.cos(math.radians(el)),
    -math.cos(math.radians(az)) * math.cos(math.radians(el)),
    math.sin(math.radians(el)),
))
cam_data = bpy.data.cameras.new("cam")
cam_data.lens = focal
cam = bpy.data.objects.new("cam", cam_data)
scene.collection.objects.link(cam)
cam.location = aim_pt + cam_dir * dist
cam.rotation_euler = (aim_pt - cam.location).to_track_quat("-Z", "Y").to_euler()
scene.camera = cam

cam_data.dof.use_dof = True
cam_data.dof.focus_distance = dist
cam_data.dof.aperture_fstop = 8.0

out = os.path.join(ROOT, args.out)
os.makedirs(os.path.dirname(out), exist_ok=True)
scene.render.filepath = out
print("rendering %s -> %s" % (args.wood, out))
bpy.ops.render.render(write_still=True)
print("done")
