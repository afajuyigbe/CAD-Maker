"""Orthographic shared-mesh projection with depth buffer and feature edges."""
from pathlib import Path
import json,math
import numpy as np
from PIL import Image
P=Path(__file__).parent;O=P/'outputs';d=json.loads((O/'mesh.json').read_text());VV=np.array(d['vertices']);FF=d['faces'];CC=d['colors'];MM=d['materials'];GG=d['groups']
def render(name,az,elev,size,selector=lambda g:True):
 fs=[(f,m,g) for f,m,g in zip(FF,MM,GG) if selector(g)];ids=sorted(set(i for f,m,g in fs for i in f));V=VV[np.array(ids)-1]
 width,height=size;a,e=map(math.radians,[az,elev]);right=np.array([-math.sin(a),math.cos(a),0]);up=np.array([-math.sin(e)*math.cos(a),-math.sin(e)*math.sin(a),math.cos(e)]);depth=np.array([math.cos(e)*math.cos(a),math.cos(e)*math.sin(a),math.sin(e)])
 proj=np.column_stack([VV@right,VV@up]);lo=np.array([V@right,V@up]).min(1);hi=np.array([V@right,V@up]).max(1);scale=min((width-30)/(hi[0]-lo[0]),(height-30)/(hi[1]-lo[1]));off=(np.array([width,height])-(hi-lo)*scale)/2;xy=(proj-lo)*scale+off;xy[:,1]=height-xy[:,1];zz=VV@depth
 image=np.full((height,width,3),255,dtype=np.uint8);zbuf=np.full((height,width),-np.inf);adj={};light=np.array([-.5,-.65,.7]);light/=np.linalg.norm(light)
 for f,mat,g in fs:
  ix=np.array(f)-1;p=xy[ix];z=zz[ix];normal=np.cross(VV[ix[1]]-VV[ix[0]],VV[ix[2]]-VV[ix[0]]);normal/=np.linalg.norm(normal);shade=.72+.28*max(0,normal@light);rgb=np.clip(np.array(CC[mat])*255*shade,0,255).astype(np.uint8)
  for ia,ib in zip(ix,np.roll(ix,-1)):
   key=tuple(sorted([tuple(np.round(VV[ia],3)),tuple(np.round(VV[ib],3))]));adj.setdefault(key,[]).append((ia,ib,normal,mat,g))
  for j in range(1,len(ix)-1):
   q=p[[0,j,j+1]];qd=z[[0,j,j+1]];xmin=max(0,int(np.floor(q[:,0].min())));xmax=min(width-1,int(np.ceil(q[:,0].max())));ymin=max(0,int(np.floor(q[:,1].min())));ymax=min(height-1,int(np.ceil(q[:,1].max())))
   if xmin>xmax or ymin>ymax:continue
   den=(q[1,1]-q[2,1])*(q[0,0]-q[2,0])+(q[2,0]-q[1,0])*(q[0,1]-q[2,1])
   if abs(den)<1e-9:continue
   xx,yy=np.meshgrid(np.arange(xmin,xmax+1)+.5,np.arange(ymin,ymax+1)+.5);w0=((q[1,1]-q[2,1])*(xx-q[2,0])+(q[2,0]-q[1,0])*(yy-q[2,1]))/den;w1=((q[2,1]-q[0,1])*(xx-q[2,0])+(q[0,0]-q[2,0])*(yy-q[2,1]))/den;w2=1-w0-w1;dep=w0*qd[0]+w1*qd[1]+w2*qd[2];sub=zbuf[ymin:ymax+1,xmin:xmax+1];mask=(w0>=-1e-6)&(w1>=-1e-6)&(w2>=-1e-6)&(dep>=sub-1e-6);sub[mask]=dep[mask];image[ymin:ymax+1,xmin:xmax+1][mask]=rgb
 visible=[]
 for entries in adj.values():
  ia,ib,n,mat,g=entries[0]
  if len(entries)>1:
   # Suppress coplanar edges and smooth cylinder tessellation; preserve creases, silhouettes and material boundaries.
   keep=any(n@q[2]<math.cos(math.radians(18)) or mat!=q[3] or (n@depth)*(q[2]@depth)<-1e-8 for q in entries[1:])
   if not keep:continue
  a,b=xy[ia],xy[ib];npts=max(2,int(np.linalg.norm(b-a)*1.6));tt=np.linspace(0,1,npts);ps=a[None,:]*(1-tt[:,None])+b[None,:]*tt[:,None];zs=zz[ia]*(1-tt)+zz[ib]*tt;px=np.rint(ps[:,0]).astype(int);py=np.rint(ps[:,1]).astype(int);valid=(px>=0)&(px<width)&(py>=0)&(py<height);vis=np.zeros(npts,bool);vis[valid]=zs[valid]>=zbuf[py[valid],px[valid]]-24
  image[py[vis],px[vis]]=[48,49,46];start=None
  for k,ok in enumerate(np.r_[vis,False]):
   if ok and start is None:start=k
   elif not ok and start is not None:
    if k-start>=2:visible.append([(ps[start]/[width,height]).tolist(),(ps[k-1]/[width,height]).tolist()])
    start=None
 Image.fromarray(image).save(O/f'{name}.png');(O/f'{name}-projection.json').write_text(json.dumps({'edges':visible,'right':right.tolist(),'up':up.tolist(),'lo':lo.tolist(),'scale':scale,'offset':off.tolist(),'size':size,'world_units':'mm'}));print(name,len(visible),flush=True)
if __name__=='__main__':
 render('south-elevation',-90,0,(1000,1650));render('east-elevation',0,0,(1000,1650))
 render('roof-plan',-90,90,(1400,1400))
 def support(g):return g.startswith(('perimeter_column','inner_projection','radial_beam')) or g in ['central_shaft','bottom_ring']
 render('support-plan',-90,90,(1400,1400),support)
 render('tower-3d',-105,18,(1350,1800))
 render('roof-3d',-65,53,(1500,1250),lambda g: not g.startswith(('perimeter_column','inner_projection','radial_beam','shaft_vent','vertical_cable')) and g not in ['central_shaft','ground_door','bottom_ring','tank_underside','tank_external_wall','tank_horizontal_joints'] and not 'lower_ring' in g and not g.startswith('EMA_'))
