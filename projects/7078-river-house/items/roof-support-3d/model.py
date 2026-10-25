"""Dimension-based roof-frame surface model. Main-roof top is local Z=0 (+38m)."""
from pathlib import Path
import json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
P=Path(__file__).parent;O=P/'outputs';O.mkdir(exist_ok=True)
V=[];F=[];G=[];M=[]
materials={'C1':(.63,.65,.66),'C2_exposed':(.71,.72,.72),'main_beam':(.62,.63,.64),'B1':(.45,.48,.5),'B2':(.59,.63,.66),'connection_symbol':(.25,.27,.28)}
# World X along survey length, Y across width; right-handed Z up.
def box(lengthpos,widthpos,z,l,w,h,group,mat):
 p=[(lengthpos,widthpos,z),(lengthpos+l,widthpos,z),(lengthpos+l,widthpos+w,z),(lengthpos,widthpos+w,z),(lengthpos,widthpos,z+h),(lengthpos+l,widthpos,z+h),(lengthpos+l,widthpos+w,z+h),(lengthpos,widthpos+w,z+h)]
 ids=[]
 for q in p:V.append(q);ids.append(len(V))
 for inds in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:F.append([ids[i] for i in inds]);G.append(group);M.append(mat)
ys=[0,6.15,11.65,17.15,22.65,28.15,33.65,39.15,44.65]
for width,rows,mat,sw in [(0,ys,'C2_exposed',.3),(14.6,ys,'C2_exposed',.3),(7.3,ys,'C1',.38)]:
 for i,y in enumerate(rows):box(y-.19,width-sw/2,-.5,.38,sw,4.07,f'{mat}_{width}_{i}',mat)
# Main-roof top +38m; section depth below roof datum.
for width in [0,14.6]:box(-.1625,width-.1625,-.3,44.975,.325,.3,f'main_longitudinal_{width}','main_beam')
for y in [0,44.65]:box(y-.1625,0,-.3,.325,14.6,.3,f'main_end_{y}','main_beam')
# Identified B1 beams and B2 secondary members at upper roof +41.57m.
for y in [11.65,17.15,22.65]:box(y-.19,0,3.19,.38,14.6,.38,f'B1_{y}','B1')
for width in [1.2,2.4,3.6,4.8,6.0]:box(11.65,width-.19,3.39,11,.38,.18,f'B2_left_{width}','B2')
for i,y in enumerate(np.arange(11.65,22.651,1.2)):box(float(y)-.19,7.3,3.39,.38,7.3,.18,f'B2_right_{i}','B2')
for y in [11.65,17.15]:
 for width in [.725,6.575]:box(y-.10,width-.10,3.57,.2,.2,.04,f'grillage_connection_symbol_{y}_{width}','connection_symbol')
stem='7078-river-house-roof-frame'
if globals().get('EXPORT_APPROVED',False):
 with (O/(stem+'.obj')).open('w') as f:
  f.write('# Roof support frame; metres; OBJ Y up. Y=0 is main roof +38m AGL.\nmtllib '+stem+'.mtl\n')
  for x,y,z in V:f.write(f'v {x:.6f} {z:.6f} {-y:.6f}\n')
  prev=None
  for ids,g,m in zip(F,G,M):
   if (g,m)!=prev:f.write(f'g {g}\nusemtl {m}\n');prev=(g,m)
   f.write('f '+' '.join(map(str,ids))+'\n')
 with (O/(stem+'.mtl')).open('w') as f:
  for m,c in materials.items():f.write(f'newmtl {m}\nKd {" ".join(map(str,c))}\nKa .15 .15 .15\nKs .05 .05 .05\nNs 10\nd 1\nillum 2\n\n')
assert all(np.isfinite(V).flat)
for ids in F:
 p=np.array([V[i-1] for i in ids]);assert np.linalg.norm(np.cross(p[1]-p[0],p[2]-p[0]))>1e-9
fig=plt.figure(figsize=(14,8));ax=fig.add_subplot(projection='3d');ax.add_collection3d(Poly3DCollection([[V[i-1] for i in ids] for ids in F],facecolors=[materials[m] for m in M],edgecolors='#24282b',linewidths=.27))
ax.set(xlim=(-1,46),ylim=(-1,16),zlim=(-.6,4.3));ax.set_box_aspect((47,17,4.9));ax.view_init(25,-57);ax.set_axis_off();fig.savefig(O/(stem+'-render.png'),dpi=170,bbox_inches='tight',pad_inches=.05);plt.close(fig)
record={'scope':'Confirmed roof-support frame; building envelope/grillage and tower details awaiting scope/photos','units':'metres','obj_up_axis':'Y','datum':'OBJ Y=0 at main roof +38.00m AGL; upper roof Y=3.57m','columns':'Symbolic 0.50m crop below main roof; column continuity below not modelled to ground','C2':'Only exposed 380x300 section shown; embedded/full section unknown','secondary_members':'Based on current survey interpretation, including 1200 spacing; final count/edge conditions require review','connections':'Markers identify four grillage connection points; no invented grillage member sizes or concealed bearing details','surface_faces':len(F),'vertices':len(V),'groups':len(set(G)),'validation':'Nondegenerate quad faces and finite coordinates; local MTL only, no external textures'}
(O/'model-record.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
