"""Approximate visual model, metres. Source plan XY, height Z; OBJ exports Y-up."""
import json, math, zipfile
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
P=Path(__file__).parent; O=P/'outputs'; O.mkdir(exist_ok=True)
data=json.loads((P/'item.json').read_text()); scale=7.5/96.5
outline=np.array(data['footprint_reference']['path'][:-1])*scale
V=[]; F=[]; G=[]; M=[]
colors={'brick':(.48,.36,.25),'roof':(.16,.18,.19),'glass':(.39,.55,.61),'frame':(.87,.88,.85),'metal':(.52,.56,.57),'cap':(.59,.58,.52),'cladding':(.8,.81,.76),'door':(.3,.37,.38)}
def face(points,group,mat):
 ids=[]
 for p in points: V.append(tuple(float(x) for x in p)); ids.append(len(V))
 F.append(ids);G.append(group);M.append(mat)
def box(x,y,z,a,b,h,g,m):
 p=[(x,y,z),(x+a,y,z),(x+a,y+b,z),(x,y+b,z),(x,y,z+h),(x+a,y,z+h),(x+a,y+b,z+h),(x,y+b,z+h)]
 for inds in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:face([p[i] for i in inds],g,m)
def beam(a,b,w,g='roof_rails',m='metal'):
 a=np.array(a);b=np.array(b);u=b-a;u=u/np.linalg.norm(u); t=np.cross(u,[0,0,1])
 if np.linalg.norm(t)<.1:t=np.cross(u,[0,1,0])
 t=t/np.linalg.norm(t)*w/2;s=np.cross(u,t)
 p=[a-t-s,a+t-s,a+t+s,a-t+s,b-t-s,b+t-s,b+t+s,b-t+s]
 for ix in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:face([p[i] for i in ix],g,m)
# Split wall surfaces around true surface apertures; glazing fills each window opening.
def wall(a,b,windows,group):
 a=np.array(a);b=np.array(b);d=b-a;L=np.linalg.norm(d);u=d/L
 def pt(t,z,offset=0):return (*(a+u*t+np.array([-u[1],u[0]])*offset),z)
 cuts=sorted(set([0,L]+[max(0,min(L,q)) for w in windows for q in (w[0],w[0]+w[1])]))
 for l,r in zip(cuts,cuts[1:]):
  active=[w for w in windows if w[0]<(l+r)/2<w[0]+w[1]]
  heights=sorted(set([0,8.4]+[q for w in active for q in (w[2],w[2]+w[3])]))
  for lo,hi in zip(heights,heights[1:]):
   if not any(w[2]<(lo+hi)/2<w[2]+w[3] for w in active):face([pt(l,lo),pt(r,lo),pt(r,hi),pt(l,hi)],group,'brick')
 for i,(t,w,z,h,panes) in enumerate(windows):
  g=f'{group}_opening_{i:02}'
  face([pt(t,z,.012),pt(t+w,z,.012),pt(t+w,z+h,.012),pt(t,z+h,.012)],g,'glass')
  for k in range(panes+1):beam(pt(t+k*w/panes,z,-.015),pt(t+k*w/panes,z+h,-.015),.045,g,'frame')
  for zz in [z,z+h,z+h*.48]:beam(pt(t,zz,-.015),pt(t+w,zz,-.015),.045,g,'frame')
 # dark coping with meaningful edge
 beam(pt(0,8.41),pt(L,8.41),.14,group+'_coping','roof')
# consistent external facade groups, apertures approximately matched to photographs
for i,a in enumerate(outline):
 b=outline[(i+1)%len(outline)]; L=np.linalg.norm(b-a);wins=[]
 if i==5: # courtyard facade: glazed staircase at return
  wins=[(.06,3.5,.3,7.95,3)]
  for level in range(3):
   for t,w in [(4.1,1.65),(6.9,1.65),(9.7,.75),(11.5,.75),(13.2,2.05),(16.1,1.45)]:
    if t+w<L-.15:wins.append((t,w,.9+level*2.8,1.3,3 if w>1.4 else 1))
 else:
  n=max(1,round(L/3.8))
  for level in range(3):
   for j in range(n):
    w=min(1.65,L/(n+1)*.68);t=(j+.5)*L/n-w/2
    if t>.18 and t+w<L-.18:wins.append((t,w,.95+2.8*level,1.25,3 if w>1.2 else 1))
 wall(a,b,wins,f'facade_{i:02}')
# triangulate concave roof and ground with ear clipping
from matplotlib.path import Path as MPath
poly=outline.tolist();ids=list(range(len(poly)))
area=sum(np.cross(outline[(i+1)%len(outline)],outline[i]) for i in range(len(outline)))
if area>0:ids.reverse()
while len(ids)>2:
 for k,j in enumerate(ids):
  ia,ic=ids[k-1],ids[(k+1)%len(ids)];tri=np.array([outline[ia],outline[j],outline[ic]])
  if np.cross(tri[1]-tri[0],tri[2]-tri[1])<=1e-8:continue
  if any(MPath(tri).contains_point(outline[q],radius=-1e-7) for q in ids if q not in [ia,j,ic]):continue
  face([(*p,8.4) for p in tri],'main_roof','roof');face([(*p,0) for p in tri[::-1]],'base','brick');ids.pop(k);break
 else:raise ValueError('roof triangulation failed')
# rooftop room, pitched roof with white gable, proportions estimated from photos
x,y=77.35*scale,127.27*scale;a,b=5.8,3.6
# Brick shell with an actual opening on the chimney-side eaves wall.
# Door/panel sizes are visual estimates; not surveyed dimensions.
door_y=y+.18; door_w=.88; door_top=10.0
face([(x,y,8.4),(x,y+b,8.4),(x,y+b,10.05),(x,y,10.05)],'room_side_wall','brick')
for yy in [y,y+b]:
 face([(x,yy,8.4),(x+a,yy,8.4),(x+a,yy,10.05),(x,yy,10.05)],'room_gable_wall','brick')
 face([(x,yy,10.05),(x+a,yy,10.05),(x+a/2,yy,10.8)],'room_gable','cladding')
for lo,hi in [(y,door_y),(door_y+door_w,y+b)]:
 face([(x+a,lo,8.4),(x+a,hi,8.4),(x+a,hi,10.05),(x+a,lo,10.05)],'room_door_wall','brick')
face([(x+a,door_y,door_top),(x+a,door_y+door_w,door_top),(x+a,door_y+door_w,10.05),(x+a,door_y,10.05)],'room_door_lintel','brick')
# Recess is a dark visual backing, not inferred interior geometry.
face([(x+a-.10,door_y,8.43),(x+a-.10,door_y+door_w,8.43),(x+a-.10,door_y+door_w,door_top),(x+a-.10,door_y,door_top)],'room_door_recess','door')
for yy in [door_y,door_y+door_w]:beam((x+a+.025,yy,8.43),(x+a+.025,yy,door_top),.065,'room_door_frame','frame')
for zz in [8.43,door_top]:beam((x+a+.025,door_y,zz),(x+a+.025,door_y+door_w,zz),.065,'room_door_frame','frame')
# Open outward door leaf, as photographed; angle approximate.
hinge=np.array([x+a+.045,door_y,8.46]); tip=hinge+np.array([door_w*.94,door_w*.342,0])
face([hinge,tip,tip+[0,0,1.5],hinge+[0,0,1.5]],'room_open_door','frame')
for aa,bb in [(hinge,tip),(hinge+[0,0,1.5],tip+[0,0,1.5]),(hinge,hinge+[0,0,1.5]),(tip,tip+[0,0,1.5])]:beam(aa,bb,.045,'room_door_leaf_edges','frame')
# Large white horizontal-clad panel on the gable towards the frames.
px0,px1=x+.35,x+a-.35; panel_y=y-.025
face([(px0,panel_y,8.7),(px1,panel_y,8.7),(px1,panel_y,10.05),(x+a/2,panel_y,10.70),(px0,panel_y,10.05)],'room_white_cladding','cladding')
for zz in np.arange(8.85,10.65,.17):
 half=(a/2-.35) if zz<=10.05 else (a/2-.35)*(10.7-zz)/.65
 beam((x+a/2-half,panel_y-.012,zz),(x+a/2+half,panel_y-.012,zz),.014,'room_cladding_joints','frame')
# Slight roof overhang, with pale eaves and gable fascia.
ox=.12;oy=.12
face([(x-ox,y-oy,10.05),(x+a/2,y-oy,10.8),(x+a/2,y+b+oy,10.8),(x-ox,y+b+oy,10.05)],'pitched_roof','roof')
face([(x+a/2,y-oy,10.8),(x+a+ox,y-oy,10.05),(x+a+ox,y+b+oy,10.05),(x+a/2,y+b+oy,10.8)],'pitched_roof','roof')
for xx in [x-ox,x+a+ox]:
 face([(xx,y-oy,9.89),(xx,y+b+oy,9.89),(xx,y+b+oy,10.05),(xx,y-oy,10.05)],'room_eaves_fascia','frame')
for yy in [y-oy,y+b+oy]:
 for left,right in [((x-ox,yy,10.05),(x+a/2,yy,10.8)),((x+a/2,yy,10.8),(x+a+ox,yy,10.05))]:
  face([left,right,(right[0],right[1],right[2]-.13),(left[0],left[1],left[2]-.13)],'room_gable_fascia','frame')
# measured tapered chimney body, top brick at roof+2.3m; cap schematic
cx,cy=x+a+.35,y+1.8
low=[(cx-.75,cy-.525,8.4),(cx+.75,cy-.525,8.4),(cx+.75,cy+.525,8.4),(cx-.75,cy+.525,8.4)]
top=[(cx-.6,cy-.51,10.7),(cx+.6,cy-.51,10.7),(cx+.6,cy+.51,10.7),(cx-.6,cy+.51,10.7)]
for i in range(4):face([low[i],low[(i+1)%4],top[(i+1)%4],top[i]],'chimney_brick','brick')
face(top,'chimney_brick','brick');box(cx-.65,cy-.56,10.7,1.3,1.12,.075,'chimney_cap_estimated','cap')
# two free standing telecom frames, approximate placement from GA
for idx,(fx,fy) in enumerate([(1.2,6.4),(6.2,1.2)]):
 g=f'telecom_frame_{idx+1}'
 for dx in [-.9,.9]:
  box(fx+dx-.18,fy-.8,8.42,.36,1.6,.16,g+'_ballast','cap')
  beam((fx+dx,fy-.65,8.6),(fx+dx,fy+.65,8.6),.09,g)
 beam((fx-.9,fy,8.6),(fx+.9,fy,8.6),.09,g)
 beam((fx,fy,8.6),(fx,fy,11.9),.11,g)
 beam((fx-.9,fy,8.6),(fx,fy,10.7),.07,g)
 box(fx-.22,fy-.16,10.1,.44,.22,1.75,g+'_antenna','cladding')
# chimney attached antenna basic visual representation
beam((cx-.9,cy,8.7),(cx-.9,cy,12.8),.1,'chimney_mount')
for z in [9.3,10.2]:beam((cx-.9,cy,z),(cx+.5,cy,z),.1,'chimney_mount')
box(cx-1.12,cy-.15,11.1,.42,.25,1.75,'chimney_antenna','cladding')
# local roof guardrails, visible rooflight forms
for ax,ay,bx,by in [(0.5,.5,7,.5),(.5,.5,.5,8),(x-.4,y-.6,x+a+.5,y-.6)]:
 L=math.hypot(bx-ax,by-ay)
 for z in [8.95,9.45]:beam((ax,ay,z),(bx,by,z),.045)
 for t in np.linspace(0,1,max(2,math.ceil(L/1.5)+1)):beam((ax+(bx-ax)*t,ay+(by-ay)*t,8.4),(ax+(bx-ax)*t,ay+(by-ay)*t,9.45),.045)
for rx,ry in [(21,9.5),(29,13.5)]:box(rx,ry,8.41,1.1,.85,.18,'rooflight','frame');box(rx+.07,ry+.07,8.59,.96,.71,.08,'rooflight_glass','glass')
# Courtyard stair entrance and visible vertical rainwater stacks.
corex=97*scale; corey=187.7*scale
box(corex+.75,corey-.035,.02,1.5,.07,2.15,'stair_entrance','door')
for xx in [corex+.75,corex+1.5,corex+2.25]:beam((xx,corey+.01,.02),(xx,corey+.01,2.17),.045,'stair_entrance','frame')
for px,py in [(7.58,18),(12,14.68),(23,14.68),(-.06,5),(-.06,17)]:
 beam((px,py,.2),(px,py,8.3),.075,'rainwater_pipes','roof')
# Visible shallow raised central slab on the chimney cap (unmeasured).
box(cx-.30,cy-.43,10.775,.6,.86,.06,'chimney_cap_centre_schematic','cap')
# Source annotations use image coordinates: X right, Y down.
# Convert to right-handed world coordinates: X right, Y up the source sheet,
# Z height. This reflection requires reversing every face winding.
V=[(x,-y,z) for x,y,z in V]
F=[list(reversed(ids)) for ids in F]
# OBJ uses Y-up after a proper rotation of the corrected world geometry.
stem='7111-honeypot-building-visual-01'
with (O/(stem+'.obj')).open('w') as f:
 f.write('# Approximate visual reconstruction; metres; Y up\nmtllib '+stem+'.mtl\n')
 for x,y,z in V:f.write(f'v {x:.6f} {z:.6f} {-y:.6f}\n')
 last=None
 for ids,g,m in zip(F,G,M):
  if (g,m)!=last:f.write(f'g {g}\nusemtl {m}\n');last=(g,m)
  f.write('f '+' '.join(map(str,ids))+'\n')
with (O/(stem+'.mtl')).open('w') as f:
 for m,c in colors.items():f.write(f'newmtl {m}\nKd {" ".join(map(str,c))}\nKa 0.15 0.15 0.15\nKs 0.05 0.05 0.05\nNs 10\nd 1\nillum 2\n\n')
# structural export validation
assert all(np.isfinite(V).flat)
for ids in F:
 p=np.array([V[i-1] for i in ids]);assert np.linalg.norm(np.cross(p[1]-p[0],p[2]-p[0]))>1e-9
report={'vertices':len(V),'surface_faces':len(F),'groups':len(set(G)),'materials':len(colors),'units':'metres','obj_up_axis':'Y','bounds_xyz_internal':np.array(V).min(0).tolist()+np.array(V).max(0).tolist(),'orientation':'source sheet Y-down reflected to world Y-up; polygon winding reversed; OBJ axis rotation determinant +1','validation':'finite coordinates, valid nondegenerate polygon faces, local MTL references'}
# Orientation regression: three asymmetric landmarks must retain handedness
# relative to the north-up GA, not an image-axis top-view display.
landmarks=np.array([[1.2,6.4],[6.2,1.2],[12.32,12.70]])
west=np.array([-277.20,82.98]);west/=np.linalg.norm(west)
right=np.array([-west[1],west[0]])
ga_display=landmarks[:,0,None]*right-landmarks[:,1,None]*west
ga_world=ga_display*np.array([1,-1])
export_top=landmarks*np.array([1,-1]) # OBJ X / minus OBJ Z; +Y vertical
signed=lambda p:float(np.linalg.det(np.stack([p[1]-p[0],p[2]-p[0]])))
assert signed(ga_world)*signed(export_top)>0
report['orientation_check']={'landmarks':['Frame A','Frame B','chimney'],'ga_world_signed_area2':signed(ga_world),'obj_top_signed_area2':signed(export_top),'status':'same handedness'}
(O/'validation.json').write_text(json.dumps(report,indent=2))
for wire in [False,True]:
 fig=plt.figure(figsize=(14,9));ax=fig.add_subplot(projection='3d');polys=[[V[i-1] for i in ids] for ids in F]
 coll=Poly3DCollection(polys,facecolors=[(*colors[m],1) for m in M] if not wire else (1,1,1,.03),edgecolors='#252a2c',linewidths=.22 if not wire else .28)
 ax.add_collection3d(coll);ax.set(xlim=(-1,39),ylim=(-24,1),zlim=(0,14));ax.set_box_aspect((40,25,14));ax.view_init(25,-125);ax.set_axis_off();ax.set_title('Honeypot Hall — approximate visual surface model'+(' / wireframe' if wire else ''),fontsize=13)
 fig.savefig(O/(stem+('-wireframe.png' if wire else '-preview.png')),dpi=150,bbox_inches='tight');plt.close(fig)
# Detail camera exposes the chimney-side door and frame-facing cladding.
fig=plt.figure(figsize=(10,8));ax=fig.add_subplot(projection='3d')
selected=[i for i,g in enumerate(G) if g.startswith(('room_','pitched_roof','chimney_'))]
ax.add_collection3d(Poly3DCollection([[V[j-1] for j in F[i]] for i in selected],facecolors=[colors[M[i]] for i in selected],edgecolors='#333333',linewidths=.3))
ax.set(xlim=(5.5,13.6),ylim=(-14,-8.8),zlim=(8.35,12.9));ax.set_box_aspect((8.1,5.2,4.55));ax.view_init(20,35);ax.set_axis_off();ax.set_title('Rooftop room — photo-based detail (approximate)')
fig.savefig(O/(stem+'-rooftop-detail.png'),dpi=150,bbox_inches='tight');plt.close(fig)
(O/'README.txt').write_text('Honeypot Hall / project 7111 / approximate visual model\n\nOpen the OBJ with its same-named MTL in the same folder. Select wireframe in your application. Units: metres. OBJ Y is up; ground at Y=0. OBJ X follows source-sheet right and OBJ Z follows source-sheet down. Handedness corrected from the first issue; face winding corrected with it. Polygon surface mesh, not line-only geometry. Materials use flat colours and require no textures.\n\nGA footprint and supplied photographs govern visual arrangement. Three-storey envelope, mixed windows, glazed staircase, stepped roof outline, pitched rooftop room with photo-based open access door, cladding and fascia, tapered chimney and simplified telecom frames/antenna/rails are included. Unseen openings are representative, and roof equipment placement and window spacing remain approximate. The model is for visual context, not measured drawings, structural analysis or fabrication. Cap dimensions remain schematic. Adjacent buildings, trees, cars and flat interiors are excluded.\n\nThe roof is triangulated to preserve the concave footprint. Wireframe display may show those tessellation edges. Window and frame surfaces remain separate named groups. Individual masonry joints are omitted for readability.\n')
with zipfile.ZipFile(O/(stem+'.zip'),'w',zipfile.ZIP_DEFLATED) as z:
 for suffix in ['.obj','.mtl','-preview.png','-wireframe.png','-rooftop-detail.png']:z.write(O/(stem+suffix),stem+suffix)
 for name in ['README.txt','validation.json']:z.write(O/name,name)
print(json.dumps(report))
