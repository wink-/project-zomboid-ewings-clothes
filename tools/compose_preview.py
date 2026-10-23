from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import argparse
R=Path(__file__).resolve().parents[1];P=R/'preview'
im=Image.new('RGB',(1500,1330),'#11151F');d=ImageDraw.Draw(im)
ap=argparse.ArgumentParser();ap.add_argument('--bold-font',required=True);ap.add_argument('--regular-font',required=True);options=ap.parse_args();font=ImageFont.truetype(options.bold_font,34);small=ImageFont.truetype(options.regular_font,24)
d.text((44,27),"Ewing's Clothes  |  One Job",font=font,fill='white')
d.text((44,76),'1.0.0  /  OFFLINE UV PREVIEW  /  Project Zomboid 42.21',font=small,fill='#C0C6D3')
for row,sex in enumerate(['male','female']):
 for col,side in enumerate(['front','back']):
  x=col*750;y=130+row*570
  im.paste(Image.open(P/f'{sex}-{side}.png').convert('RGB'),(x,y))
  d.text((x+30,y+16),f'{sex.title()} / {side.title()}',font=small,fill='white')
d.text((44,1280),'Local Blender render using native UVs and original art. Equip, animation and MP tests not run.',font=small,fill='#C0C6D3')
im.save(P/'EwingsClothes-1.0.0-front-back-preview.png')
print(P/'EwingsClothes-1.0.0-front-back-preview.png')
