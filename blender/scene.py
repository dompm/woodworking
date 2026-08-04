"""
Beauty render of the wine rack.

Imports the per-part STLs written by export_parts.scad, builds a procedural
wood shader (no external texture files), lights a small studio set and renders
with Cycles.

    /Applications/Blender.app/Contents/MacOS/Blender -b -P blender/scene.py -- \
        --wood walnut --out renders/beauty_walnut.png --samples 256

Grain runs along each board's own long axis.  Every carcass part has its 9"
dimension front to back, so the growth rings always band across Y; only the
length axis changes, which is why there are just two wood materials.
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
ap.add_argument("--out", default="renders/beauty.png")
ap.add_argument("--samples", type=int, default=256)
ap.add_argument("--res", default="1400x1900")
ap.add_argument("--parts", default="exports/parts")
ap.add_argument("--view", default="hero", choices=["hero", "front", "detail"])
ap.add_argument("--bottles", default="1")
args = ap.parse_args(argv)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTS = os.path.join(ROOT, args.parts)
RES_X, RES_Y = (int(v) for v in args.res.split("x"))

# Two wood species, as (early/light, late/dark) linear-ish sRGB pairs.
# sRGB, as you would sample them off a finished board.  These get converted to
# linear below -- do not start from already-dark values or the render comes out
# looking like bog oak.
WOODS = {
    #            lighter grain          darker grain
    # keep the two tones close -- walnut figure is a soft tonal shift, not the
    # stripe of a zebrawood, and too much spread reads as a toy
    "walnut": ((0.375, 0.272, 0.198), (0.225, 0.150, 0.104)),
    "cherry": ((0.630, 0.372, 0.232), (0.450, 0.242, 0.150)),
    # nordic pine: pale, and the grain contrast is HIGHER than in a hardwood --
    # soft earlywood against hard latewood is exactly what makes pine look like
    # pine rather than like a blonde hardwood
    "pine":   ((0.855, 0.735, 0.540), (0.600, 0.440, 0.268)),
}
LIGHT, DARK = WOODS[args.wood]


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
scene.view_settings.exposure = 0.0


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


GROUPS = {
    "wood_z": ["stile0", "stile1", "divider", "leg0", "leg1", "leg2", "leg3", "blocks"],
    "wood_x": ["horiz%d" % i for i in range(7)],
    "brass": ["brass"],
    "steel": ["steel"],
    "glass": ["bottles"],
}
SMOOTH = {"leg0", "leg1", "leg2", "leg3", "brass", "bottles"}

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


def wood_material(name, length_axis):
    """length_axis: 'X' or 'Z' -- the direction the board is long."""
    mat, nt, bsdf = new_mat(name)

    coord = nt.nodes.new("ShaderNodeTexCoord")
    objinfo = nt.nodes.new("ShaderNodeObjectInfo")

    # push the texture around per object so no two boards share a pattern
    off = nt.nodes.new("ShaderNodeVectorMath")
    off.operation = "SCALE"
    off.inputs["Scale"].default_value = 7.0

    combine = nt.nodes.new("ShaderNodeCombineXYZ")
    nt.links.new(objinfo.outputs["Random"], combine.inputs["X"])
    nt.links.new(objinfo.outputs["Random"], combine.inputs["Y"])
    nt.links.new(objinfo.outputs["Random"], combine.inputs["Z"])
    nt.links.new(combine.outputs["Vector"], off.inputs[0])

    mapping = nt.nodes.new("ShaderNodeMapping")
    # stretch the pattern along the length of the board, keep it tight across
    # the 9" width, which always runs along Y
    if length_axis == "X":
        mapping.inputs["Scale"].default_value = (0.30, 1.0, 0.55)
    else:
        mapping.inputs["Scale"].default_value = (0.55, 1.0, 0.30)
    nt.links.new(coord.outputs["Object"], mapping.inputs["Vector"])
    nt.links.new(off.outputs["Vector"], mapping.inputs["Location"])

    # Warp the coordinate before the bands.  The wave's own distortion only
    # ripples it; without a proper vector warp the result is dead-regular and
    # reads as corduroy rather than timber.
    warp_noise = nt.nodes.new("ShaderNodeTexNoise")
    warp_noise.inputs["Scale"].default_value = 1.7
    warp_noise.inputs["Detail"].default_value = 5.0
    warp_noise.inputs["Roughness"].default_value = 0.55
    nt.links.new(mapping.outputs["Vector"], warp_noise.inputs["Vector"])

    centre = nt.nodes.new("ShaderNodeVectorMath")
    centre.operation = "SUBTRACT"
    centre.inputs[1].default_value = (0.5, 0.5, 0.5)
    nt.links.new(warp_noise.outputs["Color"], centre.inputs[0])

    amount = nt.nodes.new("ShaderNodeVectorMath")
    amount.operation = "SCALE"
    amount.inputs["Scale"].default_value = 0.40
    nt.links.new(centre.outputs["Vector"], amount.inputs[0])

    warped = nt.nodes.new("ShaderNodeVectorMath")
    warped.operation = "ADD"
    nt.links.new(mapping.outputs["Vector"], warped.inputs[0])
    nt.links.new(amount.outputs["Vector"], warped.inputs[1])

    # Two scales of figure.  One wave alone gives corrugated cardboard -- real
    # timber has broad growth rings with much finer grain lines riding on them.
    def band(scale, distortion, detail, detail_scale):
        w = nt.nodes.new("ShaderNodeTexWave")
        w.wave_type = "BANDS"
        w.bands_direction = "Y"     # the 9" width always runs along Y
        w.wave_profile = "SIN"
        w.inputs["Scale"].default_value = scale
        w.inputs["Distortion"].default_value = distortion
        w.inputs["Detail"].default_value = detail
        w.inputs["Detail Scale"].default_value = detail_scale
        nt.links.new(warped.outputs["Vector"], w.inputs["Vector"])
        return w

    figure = band(5.0, 2.5, 2.0, 1.0)     # broad growth rings / cathedrals
    lines = band(24.0, 1.0, 1.0, 1.0)     # fine grain lines

    m1 = nt.nodes.new("ShaderNodeMath")
    m1.operation = "MULTIPLY"
    m1.inputs[1].default_value = 0.90
    nt.links.new(figure.outputs["Fac"], m1.inputs[0])

    m2 = nt.nodes.new("ShaderNodeMath")
    m2.operation = "MULTIPLY"
    m2.inputs[1].default_value = 0.10
    nt.links.new(lines.outputs["Fac"], m2.inputs[0])

    grain = nt.nodes.new("ShaderNodeMath")
    grain.operation = "ADD"
    nt.links.new(m1.outputs["Value"], grain.inputs[0])
    nt.links.new(m2.outputs["Value"], grain.inputs[1])

    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.interpolation = "B_SPLINE"
    ramp.color_ramp.elements[0].position = 0.12
    ramp.color_ramp.elements[0].color = srgb_to_linear(DARK)
    ramp.color_ramp.elements[1].position = 0.92
    ramp.color_ramp.elements[1].color = srgb_to_linear(LIGHT)
    nt.links.new(grain.outputs["Value"], ramp.inputs["Fac"])
    wave = grain   # downstream nodes drive roughness off the combined grain

    # broad colour drift so a board is not uniform end to end
    drift = nt.nodes.new("ShaderNodeTexNoise")
    drift.inputs["Scale"].default_value = 2.2
    drift.inputs["Detail"].default_value = 3.0
    nt.links.new(mapping.outputs["Vector"], drift.inputs["Vector"])

    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.blend_type = "MULTIPLY"
    mix.inputs["Factor"].default_value = 0.16
    nt.links.new(ramp.outputs["Color"], mix.inputs[6])
    nt.links.new(drift.outputs["Fac"], mix.inputs[7])
    nt.links.new(mix.outputs[2], bsdf.inputs["Base Color"])

    # satin oil finish: roughness follows the grain a little
    rough = nt.nodes.new("ShaderNodeMapRange")
    rough.inputs["To Min"].default_value = 0.44
    rough.inputs["To Max"].default_value = 0.64
    nt.links.new(wave.outputs["Value"], rough.inputs["Value"])
    nt.links.new(rough.outputs["Result"], bsdf.inputs["Roughness"])
    bsdf.inputs["Specular IOR Level"].default_value = 0.25

    # open pores, very subtle
    pores = nt.nodes.new("ShaderNodeTexNoise")
    pores.inputs["Scale"].default_value = 900.0
    pores.inputs["Detail"].default_value = 2.0
    nt.links.new(mapping.outputs["Vector"], pores.inputs["Vector"])
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.03
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
    "wood_z": wood_material("wood_z", "Z"),
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


target = Vector((CX, CY, TOP * 0.46))
area_light("key", (CX + 1.7, CY - 2.2, TOP * 0.66), target, 1.3, 150,
           (1.0, 0.96, 0.90))
area_light("fill", (CX - 2.1, CY - 1.7, TOP * 0.60), target, 1.2, 55,
           (0.90, 0.94, 1.0))
area_light("rim", (CX - 1.3, CY + 2.1, TOP * 0.70), target, 1.0, 80,
           (1.0, 0.98, 0.95))


# --------------------------------------------------------------------------
# camera
# --------------------------------------------------------------------------
VIEWS = {
    # (azimuth deg from -Y, elevation deg, distance m, focal mm, aim height frac)
    "hero":   (34, 6, 3.2, 85, 0.46),
    "front":  (4, 6, 3.2, 105, 0.50),
    "detail": (40, -4, 1.3, 85, 0.13),
}
az, el, dist, focal, aim = VIEWS[args.view]
aim_pt = Vector((CX, CY, TOP * aim))
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
