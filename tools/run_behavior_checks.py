"""Run actual installed Kahlua against photo predicates, loot and clothing copy."""
from pathlib import Path
import argparse,json,re
from native_checks import ROOT,WORK,lua_runner,run
ap=argparse.ArgumentParser();ap.add_argument('--game',type=Path,required=True);args=ap.parse_args();G=args.game
MOD=ROOT/'EwingsClothes/42/media/lua';results={}
def runfiles(name,files):
 lua_runner(len(files));r=run(G,'EwingsLuaCheck',files)
 lines=re.findall(r'^\[true(?:,.*)?\]$',r.stdout,re.M)
 assert r.returncode==0 and len(lines)==len(files),(name,r.returncode,r.stdout,r.stderr)
 results[name]={'status':'PASS','vm':'installed native Kahlua','results':lines[-1]};print(name,lines[-1])
runfiles('photo_predicates',[MOD/'shared/EwingsClothes_RecipeChecks.lua',ROOT/'tools/lua_assertions.lua'])
setup=WORK/'setup.lua';setup.write_text('require = function(name) return true end\nISBaseTimedAction = {derive=function(self,name) return {} end}\ninstanceof=function(item,name) return false end\nreturn "isolated test setup"\n')
snapshot=WORK/'snapshot.lua';snapshot.write_text('''
EwingsClothesTestBefore = {}
EwingsClothesTestUnrelated = {}
local targets={ClothingStoresShirts=true, ClothingStorageAllShirts=true, WardrobeGeneric=true}
local identities={}
for name in pairs(targets) do identities[ProceduralDistributions.list[name]]=true end
for name,pool in pairs(ProceduralDistributions.list) do
 local copy={identity=pool,rolls=pool.rolls}
 if pool.items then copy.items={};for i,value in ipairs(pool.items) do copy.items[i]=value end end
 if targets[name] then EwingsClothesTestBefore[name]=copy
 elseif not identities[pool] then EwingsClothesTestUnrelated[name]=copy end
end
return "native distribution snapshots recorded"
''')
dist=MOD/'server/Items/EwingsClothes_Distributions.lua'
# Load exact native clothing pool literals, not unrelated world bootstrap globals.
native=(G/'media/lua/server/Items/ProceduralDistributions.lua').read_text()
pooltext='ProceduralDistributions = {list={}}\n'
for name in ['ClothingStoresShirts','ClothingStorageAllShirts','WardrobeGeneric','ClothingStoresBoots','ClothingStoresJackets']:
 match=re.search(r'(?m)^\s*'+name+r'\s*=\s*\{',native);start=native.index('{',match.start());depth=0
 for i in range(start,len(native)):
  depth+=1 if native[i]=='{' else -1 if native[i]=='}' else 0
  if depth==0:break
 pooltext+='ProceduralDistributions.list.'+name+' = '+native[start:i+1]+'\n'
pools=WORK/'native-clothing-pools.lua';pools.write_text(pooltext)
clutter=sorted((G/'media/lua/server/Items').glob('Distribution_*Junk.lua'))
runfiles('additive_loot_repeated_load',[setup]+clutter+[pools,snapshot,dist,dist,ROOT/'tools/distribution_assertions.lua'])
# Execute the exact installed copyClothingItem routine with isolated table mocks.
state=WORK/'state.lua';state.write_text('''
local condition,wetness,dirt,blood,holes,patches=4,72,61,37,2,3
local visual={getTint=function() return "old random tint" end,getBaseTexture=function() return 0 end,getTextureChoice=function() return -1 end,getDecal=function() return nil end}
local copied={}
local newVisual={setTint=function(self,v) copied.tint=v end,setBaseTexture=function(self,v) copied.base=v end,setTextureChoice=function(self,v) copied.texture=v end,setDecal=function(self,v) copied.decal=v end,
copyDirt=function(self,v) assert(v==visual);copied.dirt=dirt end,copyBlood=function(self,v) assert(v==visual);copied.blood=blood end,copyHoles=function(self,v) assert(v==visual);copied.holes=holes end,copyPatches=function(self,v) assert(v==visual);copied.patches=patches end}
local original={getVisual=function() return visual end,getClothingItem=function() return {} end,IsInventoryContainer=function() return false end,getColor=function() return "old color" end,
copyPatchesTo=function(self,v) copied.patchTransfer=true end,getWetness=function() return wetness end,getFluidContainer=function() return nil end,getCondition=function() return condition end,
isFavorite=function() return true end,hasModData=function() return true end,getModData=function() return {userMark="kept"} end}
local output={getVisual=function() return newVisual end,IsInventoryContainer=function() return false end,setColor=function(self,v) copied.color=v end,IsClothing=function() return true end,
setWetness=function(self,v) copied.wetness=v end,getFluidContainer=function() return nil end,setCondition=function(self,v) copied.condition=v end,setFavorite=function(self,v) copied.favorite=v end,
copyModData=function(self,v) copied.modData=v end,synchWithVisual=function() copied.synchronized=true end}
copyClothingItem(original,output)
assert(copied.condition==condition and copied.wetness==wetness and copied.dirt==dirt and copied.blood==blood and copied.holes==holes and copied.patches==patches)
assert(copied.patchTransfer and copied.favorite and copied.modData.userMark=="kept" and copied.synchronized)
assert(copied.base==0 and copied.texture==-1 and copied.decal==nil)
return "native CopyClothing routine preserved damaged, dirty, bloody, wet, patched input state (isolated mocks)"
''')
runfiles('native_copy_clothing_state',[setup,G/'media/lua/shared/TimedActions/ISClothingExtraAction.lua',state])
(ROOT/'docs/BEHAVIOR_CHECKS.json').write_text(json.dumps({'results':results,'not_gameplay':'Native functions/VM executed with isolated test tables, not actual inventory, rendering or multiplayer'},indent=2)+'\n',newline='\n')
