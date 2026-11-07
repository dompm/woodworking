"""Blender / Cycles scene. Every product mesh is exported from yahtzee_box.scad."""
import argparse
import json
import math
from pathlib import Path
import sys
import bpy
from mathutils import Vector

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'lib'))
import render_style
ap=argparse.ArgumentParser()
ap.add_argument('--samples',type=int,default=64)
ap.add_argument('--resolution',type=int,default=1400)
ap.add_argument('--only',choices=['finger','butt','finger_strips'])
args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])

def simple(name, color, metal=0):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=.42;p.inputs['Metallic'].default_value=metal
    return m

def timber(axis, plywood=True):
    m=simple(('ply_' if plywood else 'maple_')+axis,(.57,.40,.23));n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
    geom=n.new('ShaderNodeNewGeometry')
    scale=n.new('ShaderNodeVectorMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=(550,16,250)
    l.new(geom.outputs['Position'],scale.inputs[0])
    noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=1;noise.inputs['Detail'].default_value=2
    l.new(scale.outputs['Vector'],noise.inputs['Vector'])
    grain=n.new('ShaderNodeValToRGB');grain.color_ramp.elements[0].position=.15;grain.color_ramp.elements[0].color=(.48,.32,.16,1)
    grain.color_ramp.elements[1].position=.85;grain.color_ramp.elements[1].color=(.76,.59,.36,1)
    l.new(noise.outputs['Fac'],grain.inputs[0])
    color=grain.outputs['Color']
    if plywood:
        sep=n.new('ShaderNodeSeparateXYZ');l.new(geom.outputs['Position'],sep.inputs[0])
        mult=n.new('ShaderNodeMath');mult.operation='MULTIPLY';mult.inputs[1].default_value=math.tau/.00254
        l.new(sep.outputs[axis],mult.inputs[0])
        wave=n.new('ShaderNodeMath');wave.operation='SINE';l.new(mult.outputs[0],wave.inputs[0])
        bands=n.new('ShaderNodeValToRGB');bands.color_ramp.elements[0].color=(.28,.16,.075,1);bands.color_ramp.elements[1].color=(.67,.48,.26,1)
        l.new(wave.outputs[0],bands.inputs[0])
        norm=n.new('ShaderNodeSeparateXYZ');l.new(geom.outputs['Normal'],norm.inputs[0])
        absolute=n.new('ShaderNodeMath');absolute.operation='ABSOLUTE';l.new(norm.outputs[axis],absolute.inputs[0])
        face=n.new('ShaderNodeMath');face.operation='GREATER_THAN';face.inputs[1].default_value=.8;l.new(absolute.outputs[0],face.inputs[0])
        mix=n.new('ShaderNodeMixRGB');l.new(face.outputs[0],mix.inputs[0]);l.new(bands.outputs[0],mix.inputs[1]);l.new(grain.outputs[0],mix.inputs[2]);color=mix.outputs[0]
    l.new(color,p.inputs['Base Color'])
    bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.12;bump.inputs['Distance'].default_value=.000035
    l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
    return m

def text_obj(text,loc,size,material,rotation=(0,0,0)):
    c=bpy.data.curves.new('printed score text','FONT');c.body=text;c.size=size;c.align_x='LEFT';c.extrude=0
    o=bpy.data.objects.new(text,c);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=rotation;c.materials.append(material)
    return o

def line_obj(a,b,mat,r=.0001):
    c=bpy.data.curves.new('printed score rule','CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=0
    sp=c.splines.new('POLY');sp.points.add(1);sp.points[0].co=(*a,1);sp.points[1].co=(*b,1)
    o=bpy.data.objects.new('printed rule',c);bpy.context.collection.objects.link(o);c.materials.append(mat)

def render(label,view,hardwood=False):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene=bpy.context.scene
    render_style.configure(scene,samples=args.samples,width=args.resolution,height=round(args.resolution*.8))
    manifest=json.loads((HERE/'exports'/f'parts_{label}'/'manifest.json').read_text())
    W,L,H=[v*.0254 for v in manifest['dimensions'][:3]]
    wood={a:timber(a) for a in 'XYZ'};hard={a:timber(a,False) for a in 'XYZ'}
    mats={'paper':simple('warm paper',(.87,.85,.77)),'ivory':simple('ivory dice',(.83,.77,.61)),
          'ink':simple('graphite',(.017,.023,.022)),'pencil':simple('brushed silver',(.5,.54,.57),.85),'rail':hard['Y']}
    objects={}
    for part in manifest['parts']:
        name=part['name']
        bpy.ops.wm.stl_import(filepath=str(HERE/'exports'/f'parts_{label}'/f'{name}.stl'),global_scale=.001)
        obj=bpy.context.object;obj.name=name;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        material=part['material']
        obj.data.materials.append((hard if hardwood and material=='wall' else wood)[part['axis']] if material in ('wall','ply') else mats[material])
        if material in ('wall','ply','rail'):
            bevel=obj.modifiers.new('lightly eased edges','BEVEL');bevel.width=.00016;bevel.segments=2
            obj.modifiers.new('face normals','WEIGHTED_NORMAL')
        if name=='lid' and view=='open':obj.location=(W+.022,0,-part['position'][2]*.0254)
        objects[name]=obj
    ink=mats['ink'];pad=next(p for p in manifest['parts'] if p['name']=='scorepad')
    px,py,pz=[v*.0254 for v in pad['position']];pw,pl,ph=[v*.0254 for v in pad['size']];z=pz+ph+.00006
    text_obj('OUR TRAVEL YAHTZEE',(px+.006,py+pl-.014,z),.0041,ink)
    text_obj('PLACE: ____________________',(px+.006,py+pl-.023,z),.0024,ink)
    rows=['ACES','TWOS','THREES','FOURS','FIVES','SIXES','BONUS','THREE OF A KIND','FOUR OF A KIND','FULL HOUSE','SMALL STRAIGHT','LARGE STRAIGHT','YAHTZEE','CHANCE','TOTAL']
    for i,title in enumerate(rows):
        yy=py+pl-.034-i*.0075;text_obj(title,(px+.006,yy,z),.0021,ink)
        line_obj((px+.005,yy-.002,z),(px+pw-.005,yy-.002,z),ink,.00006)
    for j in range(4):
        xx=px+.047+j*.014;line_obj((xx,py+.008,z),(xx,py+pl-.029,z),ink,.00006)
    # Thin side rules distinguish a paper stack from a single thick slab.
    for k in range(1,9):
        zz=pz+k*ph/10;line_obj((px,py,zz),(px+pw,py,zz),mats['paper'],.000045)
    if view.startswith('stage'):
        walls={'left','right','front','back'}
        stage=int(view[-2:])
        allowed=walls|({'base'} if stage!=2 else set())
        if stage>=4:allowed|={'dice_divider','pencil_divider','pencil_riser_bottom','pencil_riser_top'}
        if stage==5:allowed.add('lid')
        for name,obj in objects.items():obj.hide_render=name not in allowed
        for obj in list(scene.objects):
            if obj.type in ('FONT','CURVE'):obj.hide_render=True
        if stage==1:
            for name,delta in {'left':(-.025,0,0),'right':(.025,0,0),'front':(0,-.03,0),'back':(0,.03,0)}.items():objects[name].location=delta
        if stage==4:
            for name in ('dice_divider','pencil_divider'):objects[name].location.z=.032
            for name in ('pencil_riser_bottom','pencil_riser_top'):objects[name].location.z=.014
        if stage==5:objects['lid'].location.y=-L*.35
    target=Vector((W*.95 if view=='open' else W/2,L*.48,H*.45))
    render_style.studio(scene,target)
    camdata=bpy.data.cameras.new('Camera');cam=bpy.data.objects.new('Camera',camdata);bpy.context.collection.objects.link(cam);scene.camera=cam
    if view.startswith('stage'):
        target=Vector((W/2,L*.42,H*.8));cam.location=target+Vector((.25,-.38,.43));camdata.type='ORTHO';camdata.ortho_scale=.39
    elif view=='top':
        target=Vector((W/2,L/2,0));cam.location=target+Vector((0,0,.6));camdata.type='ORTHO';camdata.ortho_scale=.29
        objects['lid'].hide_render=True
    elif view=='detail':
        target=Vector((W*.20,L*.90,H*.55));cam.location=target+Vector((-.14,.16,.12));camdata.type='ORTHO';camdata.ortho_scale=.105
    else:
        cam.location=target+Vector((.25,-.38,.43));camdata.type='ORTHO';camdata.ortho_scale=.405 if view=='open' else .32
    cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
    suffix='_hardwood' if hardwood else ''
    out=HERE/'renders'/f'{label}_{view}{suffix}.png';scene.render.filepath=str(out)
    if label=='finger' and view=='open' and not hardwood:
        bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'yahtzee_box.blend'))
    bpy.ops.render.render(write_still=True)
    print('PRODUCT_RENDER',out,flush=True)

if __name__=='__main__':
    for label in ('finger','butt'):
        if args.only is None or args.only==label:
            for view in ('open','closed','detail','top'):render(label,view)
    if args.only is None or args.only=='finger':render('finger','open',True)
    if args.only is None or args.only=='finger_strips':render('finger_strips','open')
