"""Original vector/code-authored animal art. Never regenerates One Job assets."""
from pathlib import Path
from PIL import Image, ImageDraw
import math,json,hashlib
ROOT=Path(__file__).resolve().parents[1];ART=ROOT/'art/animals';ART.mkdir(exist_ok=True)
TEX=ROOT/'EwingsClothes/common/media/textures';OUT=TEX/'Clothes/EwingsClothes';OUT.mkdir(exist_ok=True)
class Art:
 def __init__(self,title):
  self.im=Image.new('RGBA',(1024,1024));self.d=ImageDraw.Draw(self.im);self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><title>{title}</title>'];self.edge='#382A30'
 def ellipse(self,b,fill,stroke=None,width=6):
  x,y,r,t=b;self.d.ellipse(tuple(v*4 for v in b),fill=fill,outline=stroke,width=width*4 if stroke else 1);self.svg.append(f'<ellipse cx="{(x+r)/2}" cy="{(y+t)/2}" rx="{(r-x)/2}" ry="{(t-y)/2}" fill="{fill}" stroke="{stroke or "none"}" stroke-width="{width}"/>')
 def poly(self,p,fill,stroke=None,width=6):
  self.d.polygon([(x*4,y*4) for x,y in p],fill=fill)
  if stroke:self.d.line([(x*4,y*4) for x,y in p+[p[0]]],fill=stroke,width=width*4,joint='curve')
  self.svg.append(f'<polygon points="{" ".join(str(x)+","+str(y) for x,y in p)}" fill="{fill}" stroke="{stroke or "none"}" stroke-width="{width}" stroke-linejoin="round"/>')
 def line(self,p,fill,width=5):
  self.d.line([(x*4,y*4) for x,y in p],fill=fill,width=width*4,joint='curve');self.svg.append(f'<polyline points="{" ".join(str(x)+","+str(y) for x,y in p)}" fill="none" stroke="{fill}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')
 def curve(self,pts,color,width=5):
  a,b,c,d=pts;p=[]
  for i in range(41):
   t=i/40;s=1-t;p.append(tuple(s**3*a[j]+3*s*s*t*b[j]+3*s*t*t*c[j]+t**3*d[j] for j in (0,1)))
  self.line(p,color,width)
 def save(self,key):
  (ART/f'{key}-graphic.svg').write_text('\n'.join(self.svg+['</svg>'])+'\n',encoding='utf8',newline='\n');self.im.resize((512,512),Image.Resampling.LANCZOS).save(ART/f'{key}-graphic.png')
  return self.im
def dog():
 a=Art('Original friendly dog portrait');E=a.edge
 a.ellipse((27,67,91,205),'#8D552F',E);a.ellipse((165,67,229,205),'#8D552F',E)
 a.ellipse((58,42,198,221),'#EDBA73',E)
 a.poly([(85,65),(104,34),(120,51),(140,31),(150,57),(173,61)],'#EDBA73',E,5)
 a.ellipse((109,54,148,142),'#FFF1CF')
 a.ellipse((82,125,174,202),'#FFF1CF')
 a.curve([(80,94),(87,85),(97,85),(104,91)],E,5);a.curve([(152,91),(160,85),(170,86),(176,95)],E,5)
 for x in [96,160]:
  a.ellipse((x-10,103,x+10,125),E);a.ellipse((x-5,105,x+1,112),'#FFFFFF')
 a.ellipse((113,143,143,162),E)
 a.line([(128,160),(128,176)],E,5)
 a.curve([(128,175),(117,188),(104,185),(100,177)],E,5);a.curve([(128,175),(139,188),(152,185),(156,177)],E,5)
 return a
def cat():
 a=Art('Original orange tabby cat portrait');E=a.edge
 a.poly([(52,113),(43,31),(99,65),(157,65),(213,31),(204,113)],'#F0B36A',E)
 a.poly([(57,56),(65,105),(91,80)],'#E8848F',E,4);a.poly([(199,56),(191,105),(165,80)],'#E8848F',E,4)
 a.ellipse((51,66,205,220),'#F0B36A',E)
 for p in [[(109,73),(113,94)],[(128,70),(128,98)],[(147,73),(143,94)]]:a.line(p,'#955437',7)
 a.ellipse((80,140,128,191),'#FFF1D4');a.ellipse((128,140,176,191),'#FFF1D4')
 for x in [94,162]:
  a.ellipse((x-12,111,x+12,135),E);a.ellipse((x-7,113,x-1,121),'#FFFFFF')
 a.poly([(116,149),(140,149),(128,162)],'#B84F64',E,3)
 a.line([(128,163),(128,174)],E,4)
 a.curve([(128,174),(118,185),(108,182),(104,177)],E,4);a.curve([(128,174),(138,185),(148,182),(152,177)],E,4)
 for p in [[(72,153),(23,143)],[(70,167),(21,171)],[(184,153),(233,143)],[(186,167),(235,171)]]:a.line(p,E,5)
 return a
spec={}
for key,builder,color in [('Dog',dog,'#216A68'),('Cat',cat,'#2B3857')]:
 graphic=builder().save(key)
 # Reuse only the already-original One Job alpha silhouette, never its RGB art.
 original=Image.open(OUT/'EwingsClothes_OneJobTShirt.png').convert('RGBA')
 atlas=Image.new('RGBA',(1024,1024),color);atlas.putalpha(original.getchannel('A'))
 atlas.alpha_composite(graphic.resize((144,144),Image.Resampling.LANCZOS),(440,340))
 atlas.save(OUT/f'EwingsClothes_{key}TShirt.png');atlas.save(ART/f'{key}TShirt-atlas-source.png')
 icon=Image.new('RGBA',(512,512));d=ImageDraw.Draw(icon)
 shape=[(182,66),(128,85),(38,159),(104,229),(146,195),(146,438),(366,438),(366,195),(408,229),(474,159),(384,85),(330,66),(309,100),(203,100)]
 d.polygon(shape,fill=color);d.line(shape+[shape[0]],fill='#172A35',width=9,joint='curve');d.arc((182,43,330,126),0,180,fill='#172A35',width=12)
 icon.alpha_composite(graphic.resize((172,172),Image.Resampling.LANCZOS),(170,171));icon.save(ART/f'{key}TShirt-icon-source.png');icon.resize((128,128),Image.Resampling.LANCZOS).save(TEX/f'Item_EwingsClothes_{key}TShirt.png')
 spec[key]={'shirt_color':color,'item_id':f'EwingsClothes.{key}TShirt','print_box':[440,340,584,484],'base_alpha':'original mod-owned One Job silhouette, unchanged','art':'original vector/code-authored portrait; no slogan, native photo pixels or external image assets','back':'plain'}
(ART/'animals-spec.json').write_text(json.dumps({'version':'1.1.0','designs':spec},indent=2)+'\n',newline='\n')
print('Created original Dog and Cat vector/raster artwork and runtime atlases/icons; One Job files untouched.')
