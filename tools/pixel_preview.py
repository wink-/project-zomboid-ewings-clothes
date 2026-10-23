"""Offline CPU UV rasterization only. Reads installed body meshes in memory.
No application window, game code, extracted model or native skin is used/saved.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import argparse,re,numpy as np,json
ROOT=Path(__file__).resolve().parents[1]
def mesh(path):
 t=path.read_text();s=t[re.search(r'(?m)^\s*Mesh\s+\w*\s*\{',t).end():];a=re.findall(r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?',s);n=int(a[0]);v=np.array(list(map(float,a[1:1+3*n]))).reshape(-1,3);p=1+3*n;nf=int(a[p]);p+=1;f=[]
 for _ in range(nf):k=int(a[p]);p+=1;f.append(list(map(int,a[p:p+k])));p+=k
 s=t[re.search(r'(?m)^\s*MeshTextureCoords\s+\w*\s*\{',t).end():];a=re.findall(r'-?\d+(?:\.\d+)?',s);uv=np.array(list(map(float,a[1:1+2*int(a[0])]))).reshape(-1,2)
 return v,np.array(f),uv
def render(game,animal,sex,back=False):
 v,f,uv=mesh(game/f'media/models_X/Skinned/{sex}Body.x')
 tex=np.asarray(Image.open(ROOT/f'EwingsClothes/common/media/textures/Clothes/EwingsClothes/EwingsClothes_{animal}TShirt.png').convert('RGBA'))/255.
 width,height=750,480;scale=700;proj=np.column_stack((375+v[:,0]*scale*(-1 if back else 1),60+(.96-v[:,1])*scale));depth=v[:,2]*(1 if back else -1)
 image=np.empty((height,width,3));image[:]=[.115,.14,.18];zbuffer=np.full((height,width),-1e9);printpixels=0
 for face in f:
  a,b,c=proj[face];lo=np.maximum(np.floor(np.min([a,b,c],axis=0)).astype(int),[0,0]);hi=np.minimum(np.ceil(np.max([a,b,c],axis=0)).astype(int),[width-1,height-1])
  if np.any(hi<lo):continue
  den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
  if abs(den)<1e-6:continue
  yy,xx=np.mgrid[lo[1]:hi[1]+1,lo[0]:hi[0]+1];xx=xx+.5;yy=yy+.5
  q=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den;r=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den;s=1-q-r
  z=q*depth[face[0]]+r*depth[face[1]]+s*depth[face[2]];subz=zbuffer[lo[1]:hi[1]+1,lo[0]:hi[0]+1];take=(q>=-1e-5)&(r>=-1e-5)&(s>=-1e-5)&(z>subz)
  if not np.any(take):continue
  u=q*uv[face[0],0]+r*uv[face[1],0]+s*uv[face[2],0];w=q*uv[face[0],1]+r*uv[face[1],1]+s*uv[face[2],1]
  tx=np.clip((u*1024).astype(int),0,1023);ty=np.clip((w*1024).astype(int),0,1023);rgba=tex[ty,tx]
  normal=np.cross(v[face[1]]-v[face[0]],v[face[2]]-v[face[0]]);shade=.68+.30*abs(normal[2])/max(np.linalg.norm(normal),1e-9)
  rgb=(rgba[:,:,:3]*rgba[:,:,3:4]+np.array([.64,.70,.77])*(1-rgba[:,:,3:4]))*shade
  target=image[lo[1]:hi[1]+1,lo[0]:hi[0]+1];target[take]=rgb[take];subz[take]=z[take]
 return Image.fromarray(np.uint8(np.clip(image,0,1)*255))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--game',type=Path,required=True);ap.add_argument('--font',type=Path,required=True);args=ap.parse_args();out=ROOT/'preview/animals';out.mkdir(exist_ok=True);font=ImageFont.truetype(str(args.font),27);small=ImageFont.truetype(str(args.font),21)
 for animal in ['Dog','Cat']:
  board=Image.new('RGB',(1500,1120),'#111823');d=ImageDraw.Draw(board);d.text((30,22),f"Ewing's Clothes 1.1.0 | {animal} shirt | OFFLINE UV PIXEL PREVIEW",font=font,fill='white')
  for row,sex in enumerate(['Male','Female']):
   for col,back in enumerate([False,True]):
    tile=render(args.game,animal,sex,back);tile.save(out/f'{animal.lower()}-{sex.lower()}-{"back" if back else "front"}.png');x=col*750;y=80+row*480;board.paste(tile,(x,y));d.text((x+18,y+12),sex+' / '+('Back' if back else 'Front'),font=small,fill='white')
  d.text((30,1070),'Original vector art; native UV coordinates, neutral gray mannequin. No game/render/MP tests run.',font=small,fill='#CBD5E5');board.save(out/f'EwingsClothes-1.1.0-{animal.lower()}-front-back.png')
 print('Wrote CPU pixel previews; no windows or proprietary assets exported.')
