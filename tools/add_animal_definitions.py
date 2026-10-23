"""Stage additive data definitions only; never installs or runs the game."""
from pathlib import Path
import json,uuid,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];MOD=ROOT/'EwingsClothes'
items=MOD/'42/media/scripts';items.mkdir(parents=True,exist_ok=True)
guids=ET.parse(MOD/'common/media/fileGuidTable.xml').getroot()
for animal in ['Dog','Cat']:
 key=f'EwingsClothes_{animal}TShirt';guid=str(uuid.uuid5(uuid.NAMESPACE_URL,'EwingsClothes.'+animal+'TShirt@1'))
 script=f'''module EwingsClothes
{{
    item {animal}TShirt
    {{
        DisplayName = {animal} T-shirt,
        DisplayCategory = Clothing,
        ItemType = base:clothing,
        Icon = {key},
        BloodLocation = Shirt,
        BodyLocation = base:tshirt,
        ClothingItem = {key},
        FabricType = Cotton,
        Insulation = 0.2,
        WindResistance = 0.05,
        Weight = 0.3,
        WorldStaticModel = TShirt_Ground,
        Tags = base:ripclothingcotton,
    }}
}}
'''
 (items/f'{key}.txt').write_text(script,newline='\n')
 xml=f'''<?xml version="1.0" encoding="utf-8"?>
<clothingItem>
    <m_GUID>{guid}</m_GUID>
    <m_MaleModel></m_MaleModel>
    <m_FemaleModel></m_FemaleModel>
    <m_Static>false</m_Static>
    <m_AllowRandomHue>false</m_AllowRandomHue>
    <m_AllowRandomTint>false</m_AllowRandomTint>
    <m_AttachBone></m_AttachBone>
    <m_BaseTextures>Clothes/EwingsClothes/{key}</m_BaseTextures>
</clothingItem>
'''
 (MOD/f'common/media/clothing/clothingItems/{key}.xml').write_text(xml,newline='\n')
 if not any(e.findtext('guid')==guid for e in guids.findall('files')):
  e=ET.SubElement(guids,'files');ET.SubElement(e,'path').text=f'media/clothing/clothingItems/{key}.xml';ET.SubElement(e,'guid').text=guid
ET.indent(guids,space='    ');ET.ElementTree(guids).write(MOD/'common/media/fileGuidTable.xml',encoding='utf-8',xml_declaration=True)
names=MOD/'42/media/lua/shared/Translate/EN/ItemName.json';en=json.loads(names.read_text());en.update({f'EwingsClothes.{a}TShirt':f'{a} T-shirt' for a in ['Dog','Cat']});names.write_text(json.dumps(en,indent=4)+'\n',newline='\n')
recipes=MOD/'42/media/lua/shared/Translate/EN/Recipes.json';recipes.write_text(json.dumps({'EwingsClothesPrintDogTShirt':'Paint Dog T-shirt (Reusable Dog Photo)','EwingsClothesPrintCatTShirt':'Paint Cat T-shirt (Reusable Cat Photo)'},indent=4)+'\n',newline='\n')
recipe='module EwingsClothes\n{\n'
for animal,base,portrait in [('Dog','Turquoise','Brown'),('Cat','Blue','Orange')]:
 recipe+=f'''    craftRecipe EwingsClothesPrint{animal}TShirt
    {{
        timedAction = MixingBucket,
        time = 180,
        Tags = AnySurfaceCraft,
        category = Tailoring,
        AllowBatchCraft = false,
        OnTest = EwingsClothesRecipeChecks.{animal.lower()}Photo,
        inputs
        {{
            item 1 [Base.Tshirt_DefaultTEXTURE;Base.Tshirt_WhiteTINT] flags[IsNotWorn;CopyClothing],
            item 1 [Base.Photo] mode:keep,
            item 1 [Base.Paintbrush;Base.PaintbrushCrafted] mode:keep,
            item 1 [Base.Paint{base}],
            item 1 [Base.Paint{portrait}],
            item 1 [Base.PaintWhite],
            item 1 [Base.PaintBlack],
        }}
        outputs
        {{
            item 1 EwingsClothes.{animal}TShirt,
        }}
    }}
'''
recipe+='}\n';(items/'EwingsClothes_AnimalRecipes.txt').write_text(recipe,newline='\n')
info=MOD/'42/mod.info';t=info.read_text().replace('modversion=1.0.0','modversion=1.1.0');t=t[:t.index('description=')]+"description=Three fixed-design shirts: One Job, Dog and Cat. Reusable matching-photo animal recipes and rare additive clothing loot. Target game 42.21; in-game tests pending.\n";info.write_text(t,newline='\n')
print('Staged new items, stable GUIDs, retained-photo recipes, names and mod version 1.1.0')
