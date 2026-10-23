"""Native parser/Kahlua checks using installed game JAR and its existing JRE.
Emits tiny original JVM test runners without downloading a compiler. No game
entry point is used. All generated files and user.home stay in .validation/.
"""
from pathlib import Path
import argparse,struct,subprocess,json,re,shutil
ROOT=Path(__file__).resolve().parents[1];WORK=ROOT/'.validation';WORK.mkdir(exist_ok=True)
u2=lambda x:struct.pack('>H',x);u4=lambda x:struct.pack('>I',x)
class Class:
 def __init__(self,name):self.name=name;self.cp=[];self.keys={};self.methods=[]
 def add(self,k,b):
  if k not in self.keys:self.cp.append(b);self.keys[k]=len(self.cp)
  return self.keys[k]
 def utf(self,s):b=s.encode();return self.add(('utf',s),b'\x01'+u2(len(b))+b)
 def cls(self,s):return self.add(('class',s),b'\x07'+u2(self.utf(s)))
 def string(self,s):return self.add(('str',s),b'\x08'+u2(self.utf(s)))
 def ref(self,c,n,d,field=False):
  owner=self.cls(c);nt=self.add(('nt',n,d),b'\x0c'+u2(self.utf(n))+u2(self.utf(d)))
  return self.add(('ref',field,c,n,d),bytes([9 if field else 10])+u2(owner)+u2(nt))
 def call(self,c,n,d,op=0xb6):return bytes([op])+u2(self.ref(c,n,d))
 def field(self,c,n,d,op=0xb2):return bytes([op])+u2(self.ref(c,n,d,True))
 def new(self,c):return b'\xbb'+u2(self.cls(c))+b'\x59'+self.call(c,'<init>','()V',0xb7)
 def ldc(self,s):return b'\x13'+u2(self.string(s))
 def method(self,name,desc,code,access=9,stack=12,locals=8):
  self.methods.append((access,self.utf(name),self.utf(desc),code,stack,locals))
 def readarg(self,i):
  return b'\x2a'+bytes([3+i] if i<6 else [0x10,i])+b'\x32\x03\xbd'+u2(self.cls('java/lang/String'))+self.call('java/nio/file/Paths','get','(Ljava/lang/String;[Ljava/lang/String;)Ljava/nio/file/Path;',0xb8)+self.call('java/nio/file/Files','readString','(Ljava/nio/file/Path;)Ljava/lang/String;',0xb8)
 def println(self,code,desc='Ljava/lang/String;'):
  return self.field('java/lang/System','out','Ljava/io/PrintStream;')+code+self.call('java/io/PrintStream','println','('+desc+')V')
 def save(self,path):
  me=self.cls(self.name);sup=self.cls('java/lang/Object');codeidx=self.utf('Code');data=b'\xca\xfe\xba\xbe'+u2(0)+u2(49)+u2(len(self.cp)+1)+b''.join(self.cp)+u2(0x21)+u2(me)+u2(sup)+u2(0)+u2(0)+u2(len(self.methods))
  for access,name,desc,code,stack,locals in self.methods:
   body=u2(stack)+u2(locals)+u4(len(code))+code+u2(0)+u2(0)
   data+=u2(access)+u2(name)+u2(desc)+u2(1)+u2(codeidx)+u4(len(body))+body
  path.write_bytes(data+u2(0))
def lua_runner(n):
 c=Class('EwingsLuaCheck');P='se/krka/kahlua/j2se/J2SEPlatform';T='se/krka/kahlua/vm/KahluaTable';K='se/krka/kahlua/vm/KahluaThread'
 b=c.call(P,'getInstance','()L'+P+';',0xb8)+b'\x4c\x2b'+c.call(P,'newEnvironment','()L'+T+';')+b'\x4d'
 b+=b'\xbb'+u2(c.cls(K))+b'\x59\x2b\x2c'+c.call(K,'<init>','(Lse/krka/kahlua/vm/Platform;L'+T+';)V',0xb7)+b'\x4e'
 b+=b'\x13'+u2(c.cls(K))+c.ldc('debugOwnerThread')+c.call('java/lang/Class','getDeclaredField','(Ljava/lang/String;)Ljava/lang/reflect/Field;')+b'\x3a\x04\x19\x04\x04'+c.call('java/lang/reflect/Field','setAccessible','(Z)V')
 b+=b'\x19\x04\x2d'+c.call('java/lang/Thread','currentThread','()Ljava/lang/Thread;',0xb8)+c.call('java/lang/reflect/Field','set','(Ljava/lang/Object;Ljava/lang/Object;)V')
 for i in range(n):
  b+=b'\x2d'+c.readarg(i)+c.ldc('check-'+str(i))+b'\x2c'+c.call('se/krka/kahlua/luaj/compiler/LuaCompiler','loadstring','(Ljava/lang/String;Ljava/lang/String;L'+T+';)Lse/krka/kahlua/vm/LuaClosure;',0xb8)+b'\x03\xbd'+u2(c.cls('java/lang/Object'))+c.call(K,'pcall','(Ljava/lang/Object;[Ljava/lang/Object;)[Ljava/lang/Object;')+c.call('java/util/Arrays','toString','([Ljava/lang/Object;)Ljava/lang/String;',0xb8)+b'\x3a\x04'+c.println(b'\x19\x04')
 c.method('main','([Ljava/lang/String;)V',b+b'\xb1');c.save(WORK/'EwingsLuaCheck.class')
def parser_runner():
 c=Class('EwingsRecipeCheck');M='zombie/scripting/objects/ScriptModule';R='zombie/scripting/entity/components/crafting/CraftRecipe';I='zombie/scripting/entity/components/crafting/InputScript'
 b=c.new(M)+b'\x4c\x2b'+c.ldc('EwingsClothes')+c.field(M,'name','Ljava/lang/String;',0xb5)
 b+=c.new(R)+b'\x4d\x2c\x2b'+c.call(R,'setModule','(L'+M+';)V')
 # Set the native parser's isolated vanilla load context; do not scan mod dirs.
 b+=b'\x13'+u2(c.cls('zombie/scripting/ScriptManager'))+c.ldc('currentLoadFileMod')+c.call('java/lang/Class','getDeclaredField','(Ljava/lang/String;)Ljava/lang/reflect/Field;')+b'\x3a\x04\x19\x04\x04'+c.call('java/lang/reflect/Field','setAccessible','(Z)V')
 b+=b'\x19\x04\x01'+c.ldc('pz-vanilla')+c.call('java/lang/reflect/Field','set','(Ljava/lang/Object;Ljava/lang/Object;)V')
 b+=b'\x2c'+c.ldc('AnimalCheck')+c.call(R,'InitLoadPP','(Ljava/lang/String;)V')
 b+=b'\x2c'+c.ldc('AnimalCheck')+c.readarg(0)+c.call(R,'Load','(Ljava/lang/String;Ljava/lang/String;)V')
 b+=c.println(b'\x2c'+c.call(R,'getInputs','()Ljava/util/ArrayList;')+c.call('java/util/ArrayList','size','()I'),'I')
 b+=c.println(b'\x2c'+c.call(R,'getOutputs','()Ljava/util/ArrayList;')+c.call('java/util/ArrayList','size','()I'),'I')
 for i in range(7):
  b+=b'\x2c'+c.call(R,'getInputs','()Ljava/util/ArrayList;')+bytes([3+i] if i<6 else [0x10,i])+c.call('java/util/ArrayList','get','(I)Ljava/lang/Object;')+b'\xc0'+u2(c.cls(I))+b'\x4e'
  b+=c.println(b'\x2d'+c.call(I,'getOriginalLine','()Ljava/lang/String;'))
  b+=c.println(b'\x2d'+c.call(I,'getIntAmount','()I'),'I')+c.println(b'\x2d'+c.call(I,'isKeep','()Z'),'Z')
 iflag='zombie/entity/components/crafting/InputFlag'
 for flag in ['CopyClothing','IsNotWorn']:
  b+=b'\x2c'+c.call(R,'getInputs','()Ljava/util/ArrayList;')+b'\x03'+c.call('java/util/ArrayList','get','(I)Ljava/lang/Object;')+b'\xc0'+u2(c.cls(I))+b'\x4e'
  b+=c.println(b'\x2d'+c.field(iflag,flag,'L'+iflag+';')+c.call(I,'hasFlag','(L'+iflag+';)Z'),'Z')
 lc=R+'$LuaCall';b+=c.println(b'\x2c'+c.field(lc,'OnTest','L'+lc+';')+c.call(R,'getLuaCallString','(L'+lc+';)Ljava/lang/String;'))
 c.method('main','([Ljava/lang/String;)V',b+b'\xb1');c.save(WORK/'EwingsRecipeCheck.class')
def run(game,klass,args):
 # Kahlua expects its own standard library in cwd. This private test copy is
 # excluded from every artifact and must never be redistributed.
 shutil.copyfile(game/'stdlib.lua',WORK/'stdlib.lua')
 cp=';'.join(map(str,[WORK,game/'projectzomboid.jar',game]));java=game/'jre64/bin/java.exe'
 return subprocess.run([str(java),'-Djava.awt.headless=true','-Duser.home='+str(WORK/'isolated-home'),'-cp',cp,klass]+list(map(str,args)),cwd=WORK,capture_output=True,text=True,timeout=45)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--game',type=Path,required=True);ap.add_argument('--lua',type=Path,nargs='*');args=ap.parse_args();game=args.game
 if args.lua:
  lua_runner(len(args.lua));r=run(game,'EwingsLuaCheck',args.lua);print(r.stdout);print(r.stderr)
  assert r.returncode==0 and len(re.findall(r'^\[true(?:,|\])',r.stdout,re.M))==len(args.lua),(r.returncode,r.stdout,r.stderr)
  raise SystemExit(0)
 parser_runner();results={}
 text=(ROOT/'EwingsClothes/42/media/scripts/EwingsClothes_AnimalRecipes.txt').read_text()
 for animal in ['Dog','Cat']:
  match=re.search(r'craftRecipe EwingsClothesPrint'+animal+r'TShirt\s*\{',text);start=match.start();depth=0;end=None
  for i in range(text.index('{',start),len(text)):
   depth+=1 if text[i]=='{' else -1 if text[i]=='}' else 0
   if depth==0:end=i+1;break
  f=WORK/f'{animal}-recipe.txt';f.write_text(text[start:end]);r=run(game,'EwingsRecipeCheck',[f]);results[animal]={'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr};print(animal,r.returncode,r.stdout[-300:],r.stderr[-600:])
 (WORK/'native-parser-result.json').write_text(json.dumps(results,indent=2))
