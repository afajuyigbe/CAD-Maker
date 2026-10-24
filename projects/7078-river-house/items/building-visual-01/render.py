"""Depth-buffered orthographic mesh render; edges use polygon boundaries only."""
from pathlib import Path
import json,math
import numpy as np
from PIL import Image
P=Path(__file__).parent;O=P/'outputs';d=json.loads((O/'mesh.json').read_text());V=np.array(d['vertices']);F=d['faces'];C=d['colors'];M=d['materials']
def render(az,elev=24,width=1100,height=1400):
 a,e=map(math.radians,[az,elev]);right=np.array([-math.sin(a),math.cos(a),0]);up=np.array([-math.sin(e)*math.cos(a),-math.sin(e)*math.sin(a),math.cos(e)]);depth=np.array([math.cos(e)*math.cos(a),math.cos(e)*math.sin(a),math.sin(e)])
 proj=np.column_stack([V@right,V@up]);lo=proj.min(0);hi=proj.max(0);scale=min((width-40)/(hi[0]-lo[0]),(height-40)/(hi[1]-lo[1]));off=np.array([(width-(hi[0]-lo[0])*scale)/2,(height-(hi[1]-lo[1])*scale)/2]);xy=(proj-lo)*scale+off;xy[:,1]=height-xy[:,1];zz=V@depth
 image=np.full((height,width,3),255,dtype=np.uint8);zbuf=np.full((height,width),-np.inf)
 light=np.array([-.4,-.6,.7]);light/=np.linalg.norm(light)
 for ids,mat in zip(F,M):
  ix=np.array(ids)-1;p=xy[ix];z=zz[ix];normal=np.cross(V[ix[1]]-V[ix[0]],V[ix[2]]-V[ix[0]]);normal/=np.linalg.norm(normal);shade=.84+.16*abs(normal@light);rgb=np.clip(np.array(C[mat])*255*shade,0,255).astype(np.uint8)
  for j in range(1,len(ix)-1):
   q=p[[0,j,j+1]];qd=z[[0,j,j+1]];xmin=max(0,int(np.floor(q[:,0].min())));xmax=min(width-1,int(np.ceil(q[:,0].max())));ymin=max(0,int(np.floor(q[:,1].min())));ymax=min(height-1,int(np.ceil(q[:,1].max())))
   if xmin>xmax or ymin>ymax:continue
   den=(q[1,1]-q[2,1])*(q[0,0]-q[2,0])+(q[2,0]-q[1,0])*(q[0,1]-q[2,1])
   if abs(den)<1e-9:continue
   xx,yy=np.meshgrid(np.arange(xmin,xmax+1)+.5,np.arange(ymin,ymax+1)+.5)
   w0=((q[1,1]-q[2,1])*(xx-q[2,0])+(q[2,0]-q[1,0])*(yy-q[2,1]))/den;w1=((q[2,1]-q[0,1])*(xx-q[2,0])+(q[0,0]-q[2,0])*(yy-q[2,1]))/den;w2=1-w0-w1;dep=w0*qd[0]+w1*qd[1]+w2*qd[2]
   sub=zbuf[ymin:ymax+1,xmin:xmax+1];mask=(w0>=-1e-6)&(w1>=-1e-6)&(w2>=-1e-6)&(dep>=sub-1e-9);sub[mask]=dep[mask];image[ymin:ymax+1,xmin:xmax+1][mask]=rgb
 # Draw visible boundary edges; no rasterisation triangulation is exported/drawn.
 visible=[];seen=set()
 for ids in F:
  ix=[i-1 for i in ids]
  for ia,ib in zip(ix,ix[1:]+ix[:1]):
   key=tuple(sorted([tuple(np.round(V[ia],5)),tuple(np.round(V[ib],5))]))
   if key in seen:continue
   seen.add(key);a,b=xy[ia],xy[ib];n=max(2,int(np.linalg.norm(b-a)*1.4));t=np.linspace(0,1,n);ps=a[None,:]*(1-t[:,None])+b[None,:]*t[:,None];zs=zz[ia]*(1-t)+zz[ib]*t;px=np.rint(ps[:,0]).astype(int);py=np.rint(ps[:,1]).astype(int);valid=(px>=0)&(px<width)&(py>=0)&(py<height)
   vis=np.zeros(n,dtype=bool);vis[valid]=zs[valid]>=zbuf[py[valid],px[valid]]-.065
   image[py[vis],px[vis]]=[45,51,54]
   # Retain visible intervals as editable 2D CAD segments in normalised image coords.
   start=None
   for k,ok in enumerate(np.r_[vis,False]):
    if ok and start is None:start=k
    elif not ok and start is not None:
     if k-start>=2:visible.append([(ps[start]/[width,height]).tolist(),(ps[k-1]/[width,height]).tolist()])
     start=None
 return Image.fromarray(image),visible
for name,az in [('street',-58),('rear',122)]:
 im,edges=render(az);im.save(O/f'7078-river-house-building-{name}.png');(O/f'{name}-visible-edges.json').write_text(json.dumps(edges));print(name,len(edges),flush=True)
