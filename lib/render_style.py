"""Shared studio presentation. Geometry, wood materials and cameras belong to projects."""
import math
import bpy
from mathutils import Vector

# Linear material/light values, not CSS/sRGB colors.
FLOOR_COLOR = (.12, .145, .14, 1)
WORLD_COLOR = (.65, .70, .80, 1)
EXPOSURE = -.6
LIGHTS = (
    ('large softbox', (-.22, -.16, .47), 10, .36),
    ('fill', (.48, .05, .30), 4, .30),
    ('rim', (.12, .44, .45), 7, .25),
)


def configure(scene, *, samples=64, width=1600, height=1280):
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    scene.cycles.device = 'CPU'
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        prefs.compute_device_type = 'METAL'
        prefs.get_devices()
        devices = [device for device in prefs.devices if device.type == 'METAL']
        for device in prefs.devices:
            device.use = device in devices
        if devices:
            scene.cycles.device = 'GPU'
    except (KeyError, TypeError, RuntimeError):
        pass
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.film_transparent = False
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.exposure = EXPOSURE
    scene.world = bpy.data.worlds.new('studio')
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes['Background']
    background.inputs['Color'].default_value = WORLD_COLOR
    background.inputs['Strength'].default_value = .4


def area_light(name, location, target, power, size):
    data = bpy.data.lights.new(name, type='AREA')
    data.energy = power
    data.shape = 'DISK'
    data.size = size
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()
    return obj


def studio(scene, target, *, scale=1, origin=(0, 0, 0), floor_z=-.0004):
    """Scale the 22-cm reference set uniformly; square power scaling preserves exposure.

    Inputs use Blender metres. Origin places the rig, independently of the camera
    target. Do not scale only by height: low, wide objects need a wide light rig.
    """
    if scale <= 0:
        raise ValueError('Studio scale must be positive')
    bpy.ops.mesh.primitive_plane_add(size=200*scale, location=(*origin[:2], floor_z))
    floor = bpy.context.object
    floor.name = 'studio floor'
    mat = bpy.data.materials.new('studio floor')
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = FLOOR_COLOR
    shader.inputs['Roughness'].default_value = .42
    floor.data.materials.append(mat)
    # Low camera angles see above the ground plane. A tangent cove carries the
    # ground into a backdrop without exposing a world/ground horizon.
    radius=.3*scale
    profile=[(origin[1]+.7*scale+radius*math.sin(a),floor_z+radius*(1-math.cos(a)))
             for a in (i*math.pi/64 for i in range(33))]
    profile.append((profile[-1][0],floor_z+3*scale))
    vertices=[(origin[0]+side*100*scale,y,z) for y,z in profile for side in (-1,1)]
    faces=[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(profile)-1)]
    mesh=bpy.data.meshes.new('studio cove')
    mesh.from_pydata(vertices,[],faces)
    mesh.update()
    cove=bpy.data.objects.new('studio cove',mesh)
    scene.collection.objects.link(cove)
    cove.data.materials.append(mat)
    for face in mesh.polygons:face.use_smooth=True
    for name, location, power, size in LIGHTS:
        position = Vector(origin) + Vector(location)*scale
        area_light(name, position, target, power*scale**2, size*scale)
    return floor
