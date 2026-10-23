"""Validate staged 1.1.0 and build deterministic ZIPs; never installs/publishes."""
from pathlib import Path
import argparse,json,hashlib,zipfile,re,struct,xml.etree.ElementTree as ET,shutil,platform,ast
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];MOD=ROOT/'EwingsClothes';VERSION='1.1.0'
ap=argparse.ArgumentParser();ap.add_argument('--game',type=Path,required=True);args=ap.parse_args();G=args.game
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def check(name,ok,detail=None):
 assert ok,name
 checks.append({'check':name,'status':'PASS','detail':detail})
check('authorized host',platform.node().upper()=='DESKTOP-CS2AF0J',platform.node())
manifest=G.parents[1]/'appmanifest_108600.acf';check('inspected Steam build',re.search(r'"buildid"\s+"25485521"',manifest.read_text()) is not None)
old=json.loads((ROOT/'docs/history/1.0.0/VALIDATION.json').read_text());check('same inspected 42.21 game JAR',sha(G/'projectzomboid.jar')==old['inspected_input_sha256']['projectzomboid.jar'])
base=json.loads((ROOT/'docs/PRESERVATION_BASELINE.json').read_text());check('all protected One Job original files unchanged',all(sha(ROOT/p)==h for p,h in base['sha256'].items()),len(base['sha256']))
info=dict(l.split('=',1) for l in (MOD/'42/mod.info').read_text().splitlines() if '='in l);check('stable mod ID and consistent version bounds',info['id']=='EwingsClothes' and info['modversion']==VERSION and info['versionMin']==info['versionMax']=='42.21')
ids=['OneJobTShirt','DogTShirt','CatTShirt'];definitions=[]
for p in (MOD/'42/media/scripts').glob('*.txt'):definitions+=re.findall(r'\bitem\s+([A-Za-z][A-Za-z0-9_]*)\s*\{',p.read_text())
check('three unique item definitions',sorted(definitions)==sorted(ids))
table=ET.parse(MOD/'common/media/fileGuidTable.xml').getroot();guids=[e.findtext('guid') for e in table.findall('files')];check('three unique clothing GUIDs',len(guids)==len(set(guids))==3)
native_guids={e.findtext('guid') for e in ET.parse(G/'media/fileGuidTable.xml').getroot().findall('files')};check('no native GUID collisions',not(set(guids)&native_guids))
for item in ids:
 key='EwingsClothes_'+item;xml=ET.parse(MOD/f'common/media/clothing/clothingItems/{key}.xml').getroot()
 check(item+' fixed native texture-layer definition',xml.findtext('m_AllowRandomTint')==xml.findtext('m_AllowRandomHue')=='false' and not xml.findtext('m_MaleModel') and not xml.findtext('m_FemaleModel'))
 tex=MOD/'common/media/textures'/(xml.findtext('m_BaseTextures')+'.png');im=Image.open(tex);check(item+' runtime texture RGBA/size/alpha',im.mode=='RGBA' and im.size==(1024,1024) and im.getchannel('A').getextrema()==(0,255))
 icon=Image.open(MOD/f'common/media/textures/Item_{key}.png');check(item+' icon RGBA and 128px',icon.mode=='RGBA' and icon.size==(128,128))
 script=(MOD/f'42/media/scripts/{key}.txt').read_text();check(item+' native equip/model/stat references',all(x in script for x in ['ItemType = base:clothing','BodyLocation = base:tshirt','BloodLocation = Shirt','WorldStaticModel = TShirt_Ground','Weight = 0.3','Insulation = 0.2']) and 'canbedyed' not in script)
 if item!='OneJobTShirt':
  animal=item[:-6];spec=json.loads((ROOT/'art/animals/animals-spec.json').read_text())['designs'][animal];rgb=tuple(bytes.fromhex(spec['shirt_color'][1:]));pixels=im.load();points=[]
  for y in range(1024):
   for x in range(1024):
    r,g,b,a=pixels[x,y]
    if a>200 and (abs(r-rgb[0])+abs(g-rgb[1])+abs(b-rgb[2]))>15:points.append((x,y))
  check(item+' graphic only inside central front print box',len(points)>500 and all(440<=x<584 and 340<=y<484 for x,y in points),{'art_pixels':len(points),'print_box':[440,340,584,484]})
  check(item+' runtime/source atlas byte equality',sha(tex)==sha(ROOT/f'art/animals/{animal}TShirt-atlas-source.png'))
  check(item+' original vector art included',(ROOT/f'art/animals/{animal}-graphic.svg').is_file())
recipes=(MOD/'42/media/scripts/EwingsClothes_AnimalRecipes.txt').read_text();check('exactly two craft recipes',re.findall(r'craftRecipe\s+(\w+)',recipes)==['EwingsClothesPrintDogTShirt','EwingsClothesPrintCatTShirt'])
check('matching photo and brush retained in each recipe',recipes.count('item 1 [Base.Photo] mode:keep')==2 and recipes.count('item 1 [Base.Paintbrush;Base.PaintbrushCrafted] mode:keep')==2)
check('native unworn state-copy flags on consumed blanks',recipes.count('item 1 [Base.Tshirt_DefaultTEXTURE;Base.Tshirt_WhiteTINT] flags[IsNotWorn;CopyClothing]')==2)
check('no invented fluids or whole-can destruction','-fluid' not in recipes and 'mode:destroy' not in recipes and recipes.count('item 1 [Base.Paint')==10)
native=(G/'media/scripts/generated/items/drainable.txt').read_text()
for paint in ['PaintTurquoise','PaintBrown','PaintBlue','PaintOrange','PaintWhite','PaintBlack']:
 body=re.search(r'\bitem '+paint+r'\s*\{([^}]+)\}',native).group(1);check(paint+' verified native drainable use', 'ItemType = base:drainable' in body and 'UseDelta = 0.1' in body)
names=json.loads((MOD/'42/media/lua/shared/Translate/EN/ItemName.json').read_text());check('all item names with preserved One Job entry',names=={'EwingsClothes.OneJobTShirt':'One Job T-shirt','EwingsClothes.DogTShirt':'Dog T-shirt','EwingsClothes.CatTShirt':'Cat T-shirt'})
native_parser=json.loads((ROOT/'.validation/native-parser-result.json').read_text());parser_summary={}
for animal in ['Dog','Cat']:
 out=native_parser[animal];lines=out['stdout'].strip().splitlines();check(animal+' executed native craft parser',out['exit_code']==0 and lines[:2]==['7','1'] and lines[-3:]==['true','true','EwingsClothesRecipeChecks.'+animal.lower()+'Photo'])
 check(animal+' native photo/tool keep modes and quantities','item 1 [Base.Photo] mode:keep\n1\ntrue' in out['stdout'] and 'item 1 [Base.Paintbrush;Base.PaintbrushCrafted] mode:keep\n1\ntrue' in out['stdout'])
 parser_summary[animal]={'status':'PASS','inputs':7,'outputs':1,'photo_retained':True,'brush_retained':True,'input_flags':['IsNotWorn','CopyClothing'],'callback':'EwingsClothesRecipeChecks.'+animal.lower()+'Photo'}
behavior=json.loads((ROOT/'docs/BEHAVIOR_CHECKS.json').read_text());check('executed native Kahlua photo/loot/state checks',len(behavior['results'])==3 and all(r['status']=='PASS' for r in behavior['results'].values()))
check('offline previews present and inspected',all((ROOT/f'preview/animals/EwingsClothes-1.1.0-{a}-front-back.png').is_file() for a in ['dog','cat']))
for p in (ROOT/'tools').glob('*.py'):ast.parse(p.read_text())
check('active Python development scripts parse',True)
files=[p for p in MOD.rglob('*') if p.is_file()]
check('no proprietary binaries/models/fonts/runtime executables',not any(p.suffix.lower() in ['.jar','.class','.dll','.exe','.fbx','.x','.obj','.blend','.ttf','.otf'] for p in files))
report={'version':VERSION,'mod_id':'EwingsClothes','items':['EwingsClothes.'+i for i in ids],'target':{'hostname':platform.node(),'game':'42.21','steam_build':'25485521'},'checks':checks,'native_parser':parser_summary,'native_kahlua':behavior['results'],'one_job_protected_file_count':len(base['sha256']),'not_run':['game or server launch','actual crafting inventory/UI selection','equip/animation/game rendering','loot in a world','save/reload','multiplayer'],'limits':'Native parser/VM routines and isolated mock tables are offline tests, not gameplay certification. Native clothing-pool literal tests cover three target pools and two unchanged native clothing pools; not complete world bootstrap.','bundled_skill_validator':'companion resources unavailable; explicit project validator used'}
(ROOT/'docs/VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',newline='\n')
# Replace obsolete staged documentation, never any runtime asset.
for p in (MOD/'docs').glob('*'):
 if p.is_file():p.unlink()
for n in ['README.md','NOTICE.md','CHANGELOG.md']:shutil.copy2(ROOT/n,MOD/n)
for n in ['ANIMAL_RECIPES.md','DISPOSABLE_TEST_CHECKLIST.md','PRESERVATION_BASELINE.json','VALIDATION.json','BEHAVIOR_CHECKS.json']:shutil.copy2(ROOT/'docs'/n,MOD/'docs'/n)
dist=ROOT/'dist';dist.mkdir(exist_ok=True)
def pack(path,members):
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p,name in sorted(members,key=lambda x:x[1]):
   zi=zipfile.ZipInfo(name,(2026,10,23,0,0,0));zi.compress_type=zipfile.ZIP_DEFLATED;zi.external_attr=0o100644<<16;z.writestr(zi,p.read_bytes())
 digest=sha(path);path.with_suffix('.zip.sha256').write_text(digest+'  '+path.name+'\n',newline='\n')
 with zipfile.ZipFile(path) as z:
  assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
  for p,name in members:assert z.read(name)==p.read_bytes()
 return {'file':path.name,'sha256':digest,'members':len(members),'bytes':path.stat().st_size}
install=pack(dist/f'EwingsClothes-{VERSION}-install.zip',[(p,'EwingsClothes/'+p.relative_to(MOD).as_posix()) for p in MOD.rglob('*') if p.is_file()])
members=[]
for folder in ['EwingsClothes','art','preview','docs','tools']:
 for p in (ROOT/folder).rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ['.pyc','.class','.jar','.x','.fbx','.blend']:
   members.append((p,f'EwingsClothes-{VERSION}/'+p.relative_to(ROOT).as_posix()))
for n in ['README.md','README-BUILD.md','NOTICE.md','CHANGELOG.md']:members.append((ROOT/n,f'EwingsClothes-{VERSION}/'+n))
source=pack(dist/f'EwingsClothes-{VERSION}-source.zip',members)
for p in dist.glob('*.zip'):
 with zipfile.ZipFile(p) as z:
  assert not any(any(bad in n for bad in ['.validation/','.git/','stdlib.lua','isolated-home','native-parser-result']) for n in z.namelist())
check('protected originals still unchanged after packaging',all(sha(ROOT/p)==h for p,h in base['sha256'].items()))
result={'version':VERSION,'offline_checks_passed':len(checks),'install':install,'source':source,'native_parser':'PASS (2 recipes)','native_kahlua':'PASS (photo predicates, additive pools/reload, actual native copy routine with mocks)','in_game_tests':'NOT RUN','installed_or_published':False}
(dist/'PACKAGE_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n',newline='\n');print(json.dumps(result,indent=2))
