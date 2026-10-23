"""Standard-library offline checks + deterministic install/source ZIPs.
Run: python tools/validate_and_package.py [--game PATH]
Does not install, run the game, access saves, change settings or export assets.
"""
from pathlib import Path
import argparse,hashlib,json,re,struct,zlib,zipfile,xml.etree.ElementTree as ET,shutil
ROOT=Path(__file__).resolve().parents[1];STAGE=ROOT/'EwingsClothes';VERSION='1.0.0'
ap=argparse.ArgumentParser();ap.add_argument('--game',type=Path,required=True,help='Path to your own installed ProjectZomboid game directory');args=ap.parse_args();GAME=args.game
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,condition,detail=''):
 if not condition:raise AssertionError(name+': '+str(detail))
 checks.append({'check':name,'status':'PASS','detail':detail})
inputs=['projectzomboid.jar','media/scripts/generated/items/clothing.txt','media/clothing/clothingItems/Tshirt_DefaultTEXTURE.xml','media/clothing/clothingItems/Tshirt_WhiteTINT.xml','media/textures/Clothes/Shirt_Tshirt_Textures/TShirt_White.png','media/textures/ClothingTShirt.png','media/clothing/clothingDecals/TShirt_Rock_1.xml','media/models_X/Skinned/MaleBody.x','media/models_X/Skinned/FemaleBody.x','media/scripts/generated/models_characters.txt','media/scripts/generated/models_clothes.txt','media/lua/shared/NPCs/BodyLocations.lua','media/lua/shared/TimedActions/ISWearClothing.lua','media/fileGuidTable.xml','media/lua/shared/Translate/EN/ItemName.json']
before={p:sha(GAME/p) for p in inputs}
manifest=GAME.parents[1]/'appmanifest_108600.acf';build=re.search(r'"buildid"\s+"(\d+)"',manifest.read_text()).group(1)
check('installed Steam build',build=='25485521',build)
def png(p):
 b=p.read_bytes();check('PNG signature '+p.name,b[:8]==b'\x89PNG\r\n\x1a\n');o=8;raw=b'';w=h=None
 while o<len(b):
  n=int.from_bytes(b[o:o+4],'big');k=b[o+4:o+8];v=b[o+8:o+8+n];crc=int.from_bytes(b[o+8+n:o+12+n],'big');assert zlib.crc32(k+v)&0xffffffff==crc
  if k==b'IHDR':w,h,depth,color,_,_,inter=struct.unpack('>IIBBBBB',v);assert (depth,color,inter)==(8,6,0)
  if k==b'IDAT':raw+=v
  o+=n+12
 rows=[];d=zlib.decompress(raw);stride=w*4;prev=bytearray(stride)
 for y in range(h):
  q=y*(stride+1);f=d[q];row=bytearray(d[q+1:q+1+stride])
  for x in range(stride):
   a=row[x-4] if x>=4 else 0;b=prev[x];c=prev[x-4] if x>=4 else 0
   if f==1:val=a
   elif f==2:val=b
   elif f==3:val=(a+b)//2
   elif f==4:
    p0=a+b-c;ds=[abs(p0-a),abs(p0-b),abs(p0-c)];val=[a,b,c][ds.index(min(ds))]
   else:assert f==0;val=0
   row[x]=(row[x]+val)&255
  rows.append(row);prev=row
 return w,h,rows
info=dict(x.split('=',1) for x in (STAGE/'42/mod.info').read_text().splitlines() if '='in x)
check('stable mod identity/version/bounds',info['id']=='EwingsClothes' and info['modversion']==VERSION and info['name']=="Ewing's Clothes" and info['versionMin']==info['versionMax']=='42.21')
itempath=STAGE/'42/media/scripts/EwingsClothes_OneJobTShirt.txt';text=itempath.read_text();check('balanced item syntax',text.count('{')==text.count('}')==2)
check('one unique fully qualified item',re.findall(r'\bitem\s+(\w+)',text)==['OneJobTShirt'] and re.search(r'\bmodule\s+EwingsClothes\b',text) is not None)
props=dict(re.findall(r'([A-Za-z]+)\s*=\s*([^,\n]+),',text))
expected={'ItemType':'base:clothing','BodyLocation':'base:tshirt','BloodLocation':'Shirt','ClothingItem':'EwingsClothes_OneJobTShirt','Icon':'EwingsClothes_OneJobTShirt','FabricType':'Cotton','Insulation':'0.2','WindResistance':'0.05','Weight':'0.3','WorldStaticModel':'TShirt_Ground','Tags':'base:ripclothingcotton'}
check('supported native property contract',all(props.get(k)==v for k,v in expected.items()),expected)
check('no random recolor or dye script fields',not any(k in props for k in ['ColorRed','ColorGreen','ColorBlue','LuaCreate','OnCreate']) and 'canbedyed' not in text)
native=(GAME/'media/scripts/generated/items/clothing.txt').read_text();check('no native namespace/item collision','module EwingsClothes' not in native and 'item OneJobTShirt' not in native)
xmlpath=STAGE/'common/media/clothing/clothingItems/EwingsClothes_OneJobTShirt.xml';xml=ET.parse(xmlpath).getroot();guid=xml.findtext('m_GUID')
check('fixed tint/hue and native male/female body layer',xml.findtext('m_AllowRandomHue')==xml.findtext('m_AllowRandomTint')=='false' and not xml.findtext('m_MaleModel') and not xml.findtext('m_FemaleModel') and xml.findtext('m_Static')=='false')
tex=STAGE/'common/media/textures'/(xml.findtext('m_BaseTextures')+'.png');check('clothing XML texture resolves exactly',tex.is_file(),tex.relative_to(STAGE).as_posix())
table=ET.parse(STAGE/'common/media/fileGuidTable.xml').getroot();entries=table.findall('files');check('one matching native merged GUID registration',len(entries)==1 and entries[0].findtext('guid')==guid and entries[0].findtext('path')==xmlpath.relative_to(STAGE/'common').as_posix())
nativeguids={e.findtext('guid') for e in ET.parse(GAME/'media/fileGuidTable.xml').getroot().findall('files')};check('unique GUID',guid not in nativeguids,guid)
en=json.loads((STAGE/'42/media/lua/shared/Translate/EN/ItemName.json').read_text());check('English item-name JSON maps exact ID',en=={'EwingsClothes.OneJobTShirt':'One Job T-shirt'})
icon=STAGE/'common/media/textures'/('Item_'+props['Icon']+'.png');w,h,px=png(tex);check('runtime atlas RGBA dimensions',(w,h)==(1024,1024))
iw,ih,ipx=png(icon);check('runtime icon RGBA dimensions',(iw,ih)==(128,128));check('icon transparency',any(a==0 for r in ipx for a in r[3::4]) and any(a==255 for r in ipx for a in r[3::4]))
check('atlas alpha has cloth and transparency',any(a==0 for r in px for a in r[3::4]) and any(a==255 for r in px for a in r[3::4]))
yellow=[]
for y,row in enumerate(px):
 for x in range(w):
  r,g,b,a=row[x*4:x*4+4]
  if a>200 and r>180 and g>140 and b<100:yellow.append((x,y))
check('only front-chest print is yellow',len(yellow)>500 and all(424<=x<600 and 340<=y<374 for x,y in yellow),{'yellow_pixels':len(yellow),'print_box':[424,340,600,374]})
spec=json.loads((ROOT/'art/art-spec.json').read_text());check('exact words and original artwork source',spec['phrase']=='One Job' and spec['back']=='plain purple' and '>One Job<' in (ROOT/'art/OneJobTShirt-atlas-source.svg').read_text())
check('runtime/source atlas byte identity',sha(tex)==sha(ROOT/'art/OneJobTShirt-atlas-source.png'))
def mesh(path):
 t=path.read_text();s=t[re.search(r'(?m)^\s*Mesh\s+\w*\s*\{',t).end():];a=re.findall(r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?',s);n=int(a[0]);v=[tuple(map(float,a[i:i+3])) for i in range(1,1+3*n,3)];p=1+3*n;nf=int(a[p]);p+=1;f=[]
 for _ in range(nf):k=int(a[p]);p+=1;f.append(tuple(map(int,a[p:p+k])));p+=k
 s=t[re.search(r'(?m)^\s*MeshTextureCoords\s+\w*\s*\{',t).end():];a=re.findall(r'-?\d+(?:\.\d+)?',s);uv=[tuple(map(float,a[i:i+2])) for i in range(1,1+2*int(a[0]),2)]
 return v,f,uv
def position(u,w,v,f,uv):
 for face in f:
  a,b,c=[uv[i] for i in face];den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
  if abs(den)<1e-10:continue
  q=((b[1]-c[1])*(u-c[0])+(c[0]-b[0])*(w-c[1]))/den;r=((c[1]-a[1])*(u-c[0])+(a[0]-c[0])*(w-c[1]))/den;s=1-q-r
  if min(q,r,s)>=-1e-6:return tuple(q*v[face[0]][j]+r*v[face[1]][j]+s*v[face[2]][j] for j in range(3))
 return None
uvresults={}
for sex in ['Male','Female']:
 v,f,uv=mesh(GAME/f'media/models_X/Skinned/{sex}Body.x');hits=[]
 for yi in range(7):
  for xi in range(17):
   x=424.5+174*xi/16;y=340.5+32*yi/6;hit=position(x/1024,y/1024,v,f,uv);hits.append(hit)
 # The upper chest lateral edges can be slightly forward/back of native Z=0;
 # back panel is near Z=.06-.10. Front UV island + Z<.025 distinguishes it.
 check(sex+' print samples cover only front torso',all(a is not None and a[2]<.025 and .69<a[1]<.78 for a in hits),{'samples':len(hits),'vertices':len(v),'triangles':len(f)})
 left=position(425/1024,356/1024,v,f,uv);right=position(599/1024,356/1024,v,f,uv)
 check(sex+' UV text orientation monotonic front',left[0]<right[0],{'left_x':left[0],'right_x':right[0]})
 uvresults[sex]={'samples':len(hits),'min_z':min(a[2] for a in hits),'max_z':max(a[2] for a in hits),'print_island':'central front','back_print_pixels':0}
check('native ground-model reference exists','model TShirt_Ground' in (GAME/'media/scripts/generated/models_clothes.txt').read_text() and (GAME/'media/models_X/WorldItems/Clothing/Bob_TShirt_Ground.fbx').is_file())
check('no executable runtime code, recipe, distribution or model files',not any(p.suffix.lower() in ['.lua','.class','.jar','.exe','.dll','.fbx','.x','.blend','.obj'] for p in STAGE.rglob('*') if p.is_file()))
check('preview images present',all((ROOT/'preview'/f'{sex}-{side}.png').is_file() for sex in ['male','female'] for side in ['front','back']) and (ROOT/'preview/EwingsClothes-1.0.0-front-back-preview.png').is_file())
check('selected installed inputs unchanged during checks',before=={p:sha(GAME/p) for p in inputs})
report={'mod':"Ewing's Clothes",'mod_id':'EwingsClothes','item_id':'EwingsClothes.OneJobTShirt','version':VERSION,'inspected_game_version':'42.21','steam_build':build,'date':'2026-10-22','method':'Static standard-library contract/reference/PNG/UV/package validation; local Blender preview separately viewed','checks':checks,'uv':uvresults,'inspected_input_sha256':before,'not_run':['game loading','debug item browser','actual equip and game render','animation/layering','ground render','damage/repair/washing','save/reload','multiplayer'],'scope':'Only workspace-created files written; no installation/settings/saves/publication; unrelated projects unopened','skill_bundled_validator':'unavailable companion resource; explicit project validator used'}
(ROOT/'docs/VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
# Keep installation documentation alongside the portable mod.
for name in ['README.md','CHANGELOG.md','NOTICE.md']:shutil.copy2(ROOT/name,STAGE/name)
(STAGE/'docs').mkdir(exist_ok=True)
for name in ['INSPECTION.md','DISPOSABLE_TEST_CHECKLIST.md','VALIDATION.json','PUBLICATION_VALIDATION.json']:shutil.copy2(ROOT/'docs'/name,STAGE/'docs'/name)
dist=ROOT/'dist';dist.mkdir(exist_ok=True)
def archive(path,members):
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p,name in sorted(members,key=lambda a:a[1]):
   zi=zipfile.ZipInfo(name,(2026,10,22,0,0,0));zi.compress_type=zipfile.ZIP_DEFLATED;zi.external_attr=0o100644<<16;z.writestr(zi,p.read_bytes())
 digest=sha(path);path.with_suffix(path.suffix+'.sha256').write_text(digest+'  '+path.name+'\n')
 with zipfile.ZipFile(path) as z:
  assert z.testzip() is None
  assert len(z.namelist())==len(set(z.namelist()))
  for p,name in members:assert z.read(name)==p.read_bytes()
 return {'file':path.name,'sha256':digest,'bytes':path.stat().st_size,'members':len(members),'verified':'CRC, unique safe paths, exact byte equality'}
install=archive(dist/f'EwingsClothes-{VERSION}-install.zip',[(p,'EwingsClothes/'+p.relative_to(STAGE).as_posix()) for p in STAGE.rglob('*') if p.is_file()])
with zipfile.ZipFile(dist/install['file']) as z:
 names=z.namelist();assert 'EwingsClothes/42/mod.info' in names and any(n.startswith('EwingsClothes/common/') for n in names);assert all(not n.startswith('/') and '..'not in n.split('/') for n in names)
sourcefiles=[]
for folder in ['art','tools','EwingsClothes','docs','preview']:
 for p in (ROOT/folder).rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ['.pyc','.blend','.x','.fbx','.obj','.jar','.class']:
   sourcefiles.append((p,'EwingsClothes-'+VERSION+'/'+p.relative_to(ROOT).as_posix()))
for n in ['README.md','CHANGELOG.md','NOTICE.md','README-BUILD.md']:sourcefiles.append((ROOT/n,'EwingsClothes-'+VERSION+'/'+n))
source=archive(dist/f'EwingsClothes-{VERSION}-source.zip',sourcefiles)
final={'version':VERSION,'install':install,'source':source,'checks_passed':len(checks),'validation':'All static checks PASS; runtime/MP not run'}
(dist/'PACKAGE_VERIFICATION.json').write_text(json.dumps(final,indent=2)+'\n');print(json.dumps(final,indent=2))
