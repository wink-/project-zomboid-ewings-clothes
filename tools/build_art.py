"""Original garment art; no game texture or model data is read by this builder."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,argparse
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'art'; TEX=ROOT/'stage/EwingsClothes/common/media/textures'
ART.mkdir(parents=True,exist_ok=True); (TEX/'Clothes/EwingsClothes').mkdir(parents=True,exist_ok=True)
PURPLE='#7026A3'; YELLOW='#FFDA36'; S=4
# Coordinates in the native 256x256 body-atlas convention. These are original
# simple shapes designed from inspected UV coordinates, not traced pixels.
torso=[(51,66),(62,63),(83,54),(91,62),(103,70),(112,77),(144,77),(153,70),(165,62),(173,54),(194,63),(205,66),(205,146),(51,146)]
sleeves=[[(8,0),(47,0),(47,42),(8,42)],[(209,0),(248,0),(248,42),(209,42)]]
mask=Image.new('L',(1024,1024));d=ImageDraw.Draw(mask)
for poly in [torso]+sleeves:d.polygon([(x*S,y*S) for x,y in poly],fill=255)
im=Image.new('RGBA',mask.size,PURPLE);im.putalpha(mask)
ap=argparse.ArgumentParser();ap.add_argument('--font',type=Path,required=True,help='Path to a legally available bold font; original build used Arial Bold');font_path=ap.parse_args().font
font=ImageFont.truetype(str(font_path),57)
label=Image.new('RGBA',(300,90));ld=ImageDraw.Draw(label);bbox=ld.textbbox((0,0),'One Job',font=font)
ld.text((-bbox[0],-bbox[1]),'One Job',font=font,fill=YELLOW,stroke_width=0)
label=label.crop((0,0,bbox[2]-bbox[0],bbox[3]-bbox[1]))
# Upper chest, safely below neckline; central island only.
label=label.resize((176,34),Image.Resampling.LANCZOS)
im.alpha_composite(label,(424,340))
path=TEX/'Clothes/EwingsClothes/EwingsClothes_OneJobTShirt.png';im.save(path)
im.save(ART/'OneJobTShirt-atlas-source.png')
polystr=lambda p:' '.join(f'{x*4},{y*4}' for x,y in p)
svg='<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">\n<title>Ewing\'s Clothes - One Job original atlas</title>\n'
for p in [torso]+sleeves:svg+=f'<polygon points="{polystr(p)}" fill="{PURPLE}"/>\n'
svg+=f'<text x="512" y="373" text-anchor="middle" textLength="176" lengthAdjust="spacingAndGlyphs" font-family="Arial, sans-serif" font-weight="700" font-size="45" fill="{YELLOW}">One Job</text>\n</svg>\n'
(ART/'OneJobTShirt-atlas-source.svg').write_text(svg,encoding='utf8')
# Inventory art is an original front-view silhouette. Gray border is an icon
# edge, not an extra garment graphic. Only the words One Job appear on cloth.
icon=Image.new('RGBA',(512,512));dr=ImageDraw.Draw(icon)
shape=[(182,66),(128,85),(38,159),(104,229),(146,195),(146,438),(366,438),(366,195),(408,229),(474,159),(384,85),(330,66),(309,100),(203,100)]
dr.polygon(shape,fill=PURPLE);dr.line(shape+[shape[0]],fill='#321348',width=9,joint='curve')
dr.arc((182,43,330,126),0,180,fill='#40165E',width=12)
ifont=ImageFont.truetype(str(font_path),51); bb=dr.textbbox((0,0),'One Job',font=ifont)
dr.text(((512-(bb[2]-bb[0]))/2,181),'One Job',font=ifont,fill=YELLOW)
icon.save(ART/'OneJobTShirt-icon-source.png');icon.resize((128,128),Image.Resampling.LANCZOS).save(TEX/'Item_EwingsClothes_OneJobTShirt.png')
(ART/'art-spec.json').write_text(json.dumps({'version':'1.0.0','phrase':'One Job','purple':PURPLE,'yellow':YELLOW,'atlas_size':[1024,1024],'native_uv_reference_size':[256,256],'print_box_pixels':[424,340,600,374],'print_uv':[424/1024,340/1024,600/1024,374/1024],'font':'Arial Bold (system font rendered to raster; no font file redistributed)','back':'plain purple','generation':'Original polygons and typography; no extracted game pixels'},indent=2))
print('Built original 1024x1024 atlas, 128x128 icon, editable SVG/spec and raster sources')
