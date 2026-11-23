"""Run in Blender; reuses the product meshes for intermediate build stages."""
import importlib.util
import os
from pathlib import Path
import subprocess
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('product_scene',HERE/'render_scene.py')
product=importlib.util.module_from_spec(spec);spec.loader.exec_module(product)
if os.environ.get('YAHTZEE_TABLE_ONLY')!='1':
    for step in range(1,6):product.render('butt',f'stage{step:02}')

folder=HERE/'exports'/'parts_router_table';folder.mkdir(exist_ok=True)
names=('structure','plate','fence','router','guard','controls','clamps')
for name in names:
    result=subprocess.run(['openscad','-o',str(folder/f'{name}.stl'),'-D',f'PART="{name}"',str(HERE/'router_table.scad')],capture_output=True,text=True)
    if result.returncode or 'ERROR:' in result.stderr or 'WARNING:' in result.stderr:raise RuntimeError(result.stderr)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
product.render_style.configure(scene,samples=product.args.samples,width=1600,height=1250)
materials={'structure':product.timber('Z'),'fence':product.timber('Y'),'plate':product.simple('phenolic',(.035,.045,.05)),
 'router':product.simple('generic router envelope',(.03,.18,.19)), 'guard':product.simple('guard',(.35,.6,.65)),
 'controls':product.simple('paddle switch',(.6,.035,.02)), 'clamps':product.simple('bench clamps',(.85,.25,.03))}
for name in names:
    bpy.ops.wm.stl_import(filepath=str(folder/f'{name}.stl'),global_scale=.001)
    obj=bpy.context.object;obj.name=name;obj.data.materials.append(materials[name]);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if name=='structure':
        obj.data.materials.append(product.timber('X'));obj.data.materials.append(product.timber('Y'))
        # Panel face/edge orientation differs across the combined stand mesh.
        for face in obj.data.polygons:
            x,y,z=[v/.0254 for v in face.center]
            if .7499<z<14.0001 and (.9999<=x<=1.7501 or 24.2499<=x<=25.0001):face.material_index=1
            elif 4.9999<=z<=11.0001 and 18.9999<=y<=19.7501:face.material_index=2
    b=obj.modifiers.new('eased edges','BEVEL');b.width=.001;b.segments=2
    if name=='guard':
        p=materials[name].node_tree.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=.8;p.inputs['Roughness'].default_value=.15
# Thin bench slab shows what the clamps attach to; tool beneath is schematic.
bpy.ops.mesh.primitive_cube_add(size=1,location=(.33,.25,-.025));bench=bpy.context.object;bench.scale=(.85,.75,.05);bench.data.materials.append(product.simple('bench',(.18,.21,.20)))
target=Vector((.33,.28,.23))
product.render_style.studio(scene,target,scale=3.2,floor_z=-.051)
camdata=bpy.data.cameras.new('Camera');cam=bpy.data.objects.new('Camera',camdata);scene.collection.objects.link(cam);scene.camera=cam
cam.location=(1.2,-1.25,1.1);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();camdata.type='ORTHO';camdata.ortho_scale=1.08
scene.render.filepath=str(HERE/'renders'/'router_table_overview.png');bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'router_table_concept.blend'))
