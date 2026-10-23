"""Run with installed Blender --background --factory-startup --python FILE.
Reads local vanilla body mesh in memory for preview only; never saves a blend,
exports a model, copies vanilla textures, installs anything, or starts the game.
"""
import bpy,math,re,sys,argparse
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'preview';OUT.mkdir(exist_ok=True)
ap=argparse.ArgumentParser();ap.add_argument('--game',type=Path,required=True);options=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);GAME=options.game
def mesh(path):
 t=path.read_text();s=t[re.search(r'(?m)^\s*Mesh\s+\w*\s*\{',t).end():];tokens=re.findall(r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?',s)
 n=int(tokens[0]);verts=[tuple(map(float,tokens[i:i+3])) for i in range(1,1+3*n,3)];p=1+3*n;nf=int(tokens[p]);p+=1;faces=[]
 for _ in range(nf):k=int(tokens[p]);p+=1;faces.append(tuple(map(int,tokens[p:p+k])));p+=k
 s=t[re.search(r'(?m)^\s*MeshTextureCoords\s+\w*\s*\{',t).end():];tokens=re.findall(r'-?\d+(?:\.\d+)?',s);n=int(tokens[0]);uv=[tuple(map(float,tokens[i:i+2])) for i in range(1,1+2*n,2)]
 return verts,faces,uv
def render(sex,side):
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 v,f,uv=mesh(GAME/f'media/models_X/Skinned/{sex}Body.x')
 # DirectX Y-up -> Blender Z-up. Native forward (-Z) becomes Blender -Y.
 me=bpy.data.meshes.new('PreviewOnly');me.from_pydata([(x,z,y) for x,y,z in v],[],[tuple(reversed(a)) for a in f]);me.update()
 ob=bpy.data.objects.new('Local neutral mannequin; original shirt texture',me);bpy.context.collection.objects.link(ob)
 layer=me.uv_layers.new(name='Native UV')
 for poly in me.polygons:
  poly.use_smooth=True
  for li in poly.loop_indices:
   u,w=uv[me.loops[li].vertex_index];layer.data[li].uv=(u,1-w)
 mat=bpy.data.materials.new('Original purple shirt / neutral gray mannequin');mat.use_nodes=True;n=mat.node_tree.nodes;n.clear();links=mat.node_tree.links
 out=n.new('ShaderNodeOutputMaterial');bs=n.new('ShaderNodeBsdfPrincipled');bs.inputs['Roughness'].default_value=.9
 tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(ROOT/'stage/EwingsClothes/common/media/textures/Clothes/EwingsClothes/EwingsClothes_OneJobTShirt.png'),check_existing=True)
 mix=n.new('ShaderNodeMixRGB');mix.blend_type='MIX';mix.inputs[1].default_value=(.27,.30,.35,1);links.new(tex.outputs['Alpha'],mix.inputs[0]);links.new(tex.outputs['Color'],mix.inputs[2]);links.new(mix.outputs[0],bs.inputs['Base Color']);links.new(bs.outputs[0],out.inputs[0]);ob.data.materials.append(mat)
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=32
 scene.render.resolution_x=750;scene.render.resolution_y=550;scene.render.resolution_percentage=100
 scene.world.color=(.2,.2,.2);scene.view_settings.view_transform='Standard'
 scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
 sign=-1 if side=='front' else 1
 bpy.ops.object.camera_add(location=(0,sign*3,.66));cam=bpy.context.object;target=Vector((0,0,.66));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=1.08;scene.camera=cam
 for x,y,z,power,size in [(-1,sign*1.8,2.5,100,2),(1,sign*1.2,1.5,65,1.6)]:
  bpy.ops.object.light_add(type='AREA',location=(x,y,z));lamp=bpy.context.object;lamp.data.energy=power;lamp.data.shape='DISK';lamp.data.size=size;lamp.rotation_euler=(Vector((0,0,.65))-lamp.location).to_track_quat('-Z','Y').to_euler()
 scene.render.filepath=str(OUT/f'{sex.lower()}-{side}.png');bpy.ops.render.render(write_still=True)
 print('PREVIEW',sex,side,'verts',len(v),'faces',len(f),'no geometry exported')
for sex in ['Male','Female']:
 for side in ['front','back']:render(sex,side)
