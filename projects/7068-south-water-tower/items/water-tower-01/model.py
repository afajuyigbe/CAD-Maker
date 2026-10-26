"""7068 survey-controlled surface geometry, millimetres, Z up. No OBJ/MTL until approval."""
from pathlib import Path
import math,json,hashlib
import numpy as np
P=Path(__file__).parent;O=P/'outputs';O.mkdir(exist_ok=True)
D_IN=4700/math.sin(math.pi/8);D_OUT=D_IN+1200;D_CORE=D_OUT-9600
R=D_OUT/2;RC=D_CORE/2;PCD=D_IN+600
PARAM={'sectors':8,'inner_face_chord':4700,'inner_face_diameter':D_IN,'column_pcd':PCD,'outside_diameter':D_OUT,'core_diameter':D_CORE,'column_section':[600,600],'inner_projection_depth':250,'radial_beam_section':[200,450],'levels':{'ground':0,'ring_underside':15600,'ring_top':16500,'roof':22000,'parapet_lower_top':22120,'parapet_top':22210,'core_cap_top':23900},'roof_slab':150,'ring_section':[600,900]}
V=[];F=[];G=[];M=[]
C={'concrete':(.63,.61,.54),'core':(.64,.62,.56),'metal':(.61,.65,.66),'light_metal':(.78,.79,.76),'dark':(.23,.25,.24),'groove':(.34,.33,.29),'door':(.30,.25,.20),'glass':(.18,.23,.24),'cable':(.12,.14,.14)}
def face(pts,g,m):
 ids=[]
 for p in pts:V.append(list(map(float,p)));ids.append(len(V))
 F.append(ids);G.append(g);M.append(m)
def box(x,y,z,l,w,h,g,m='concrete',a=0):
 pts=np.array([[0,0,0],[l,0,0],[l,w,0],[0,w,0],[0,0,h],[l,0,h],[l,w,h],[0,w,h]],float);c,s=math.cos(a),math.sin(a);pts[:,:2]=pts[:,:2]@np.array([[c,s],[-s,c]]);pts+=np.array([x,y,z])
 for inds in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:face(pts[list(inds)],g,m)
def radialbox(r,a,z,depth,width,height,g,m='concrete'):
 c,s=math.cos(a),math.sin(a);x,y=r*c+width/2*s,r*s-width/2*c;box(x,y,z,depth,width,height,g,m,a)
def ring(ro,ri,z,h,g,m='concrete',n=96):
 for i in range(n):
  a,b=2*math.pi*i/n,2*math.pi*(i+1)/n
  p=lambda r,t,k:(r*math.cos(t),r*math.sin(t),k)
  face([p(ro,a,z),p(ro,b,z),p(ro,b,z+h),p(ro,a,z+h)],g,m)
  if ri>0:
   face([p(ri,b,z),p(ri,a,z),p(ri,a,z+h),p(ri,b,z+h)],g,m)
   face([p(ri,a,z+h),p(ro,a,z+h),p(ro,b,z+h),p(ri,b,z+h)],g,m)
   face([p(ri,b,z),p(ro,b,z),p(ro,a,z),p(ri,a,z)],g,m)
  else:
   face([(0,0,z+h),p(ro,a,z+h),p(ro,b,z+h)],g,m)
   face([(0,0,z),p(ro,b,z),p(ro,a,z)],g,m)
def beam(a,b,width,g,m='metal'):
 a,b=np.array(a,float),np.array(b,float);u=b-a;u/=np.linalg.norm(u);t=np.cross(u,[0,0,1])
 if np.linalg.norm(t)<.1:t=np.cross(u,[0,1,0])
 t=t/np.linalg.norm(t)*width/2;s=np.cross(u,t);pts=[a-t-s,a+t-s,a+t+s,a-t+s,b-t-s,b+t-s,b+t+s,b-t+s]
 for inds in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:face([pts[i] for i in inds],g,m)
def panel(r,a,z,w,h,g,m='light_metal',depth=180):radialbox(r,a,z,depth,w,h,g,m)
def disk(p,a,r,g):
 # Shallow circular dish, outward normal radial in XY, approximate hardware.
 p=np.array(p);u=np.array([0,0,1]);v=np.array([-math.sin(a),math.cos(a),0]);n=np.array([math.cos(a),math.sin(a),0]);N=32
 back=p-n*110
 for i in range(N):
  aa,bb=2*math.pi*i/N,2*math.pi*(i+1)/N;q=p+u*r*math.cos(aa)+v*r*math.sin(aa);t=p+u*r*math.cos(bb)+v*r*math.sin(bb)
  face([p,q,t],g,'light_metal');face([back,t,q],g,'metal')
# Ground-to-ring columns and central core, all eight stations follow accepted equal-sector derivation.
for i in range(8):
 a=math.radians(22.5+45*i)
 radialbox(D_IN/2,a,0,600,600,15600,f'perimeter_column_{i+1}')
 radialbox(RC,a,0,250,450,15600,f'inner_projection_{i+1}','core')
 radialbox(RC+250,a,15600,D_IN/2-RC-250,200,450,f'radial_beam_{i+1}')
# Central shaft wall external envelope. Door openings physically cut from cylindrical envelope at south.
n=96;da=math.asin(450/RC)
for i in range(n):
 a,b=2*math.pi*i/n,2*math.pi*(i+1)/n;mid=(a+b)/2;isdoor=abs(math.atan2(math.sin(mid+math.pi/2),math.cos(mid+math.pi/2)))<da
 spans=[(2100,22000)] if isdoor else [(0,22000)]
 for lo,hi in spans:face([(RC*math.cos(a),RC*math.sin(a),lo),(RC*math.cos(b),RC*math.sin(b),lo),(RC*math.cos(b),RC*math.sin(b),hi),(RC*math.cos(a),RC*math.sin(a),hi)],'central_shaft','core')
 # rooftop core to cap underside, door faces south, opening height 1750 (visual estimate)
 lo=23750 if isdoor else 22000
 if lo<23750:face([(RC*math.cos(a),RC*math.sin(a),lo),(RC*math.cos(b),RC*math.sin(b),lo),(RC*math.cos(b),RC*math.sin(b),23750),(RC*math.cos(a),RC*math.sin(a),23750)],'rooftop_core','core')
# door leaves stand inward; no assumed structural wall thickness
box(-430,-RC+100,0,860,40,2050,'ground_door','glass');box(-430,-RC+100,22000,860,40,1750,'roof_door','door')
for zz in list(range(2500,15100,1700)):
 for xx in [-850,850]:
  y=-math.sqrt(RC**2-xx**2)-5;disk((xx,y,zz),-math.pi/2,80,f'shaft_vent_{xx}_{zz}')
# Bottom ring, visible underside envelope and tank exterior. Hidden wall/bottom thickness not inferred.
ring(R,R-600,15600,900,'bottom_ring');ring(R,RC,16050,0,'tank_underside')
ring(R,R-1,16500,5350,'tank_external_wall')
for zz in [17300,18300,19300,20300,21150]:ring(R+2,R,zz,18,'tank_horizontal_joints','groove')
ring(R,0,21850,150,'roof_lid');ring(R,R-180,22000,120,'parapet_lower');ring(R,R-180,22120,90,'parapet_upper','core')
ring(RC+220,0,23750,150,'core_cap')
# 1100 handrail source GA. Hardware sections and roof parapet width are schematic.
rr=R-170
for zz in [22550,23100]:ring(rr+20,rr-20,zz,40,'roof_guardrails','metal')
for i in range(32):
 a=2*math.pi*i/32;x,y=rr*math.cos(a),rr*math.sin(a);beam((x,y,22210),(x,y,23130),40,'guardrail_posts')
# Telecom groups schematically positioned from existing GA, not proposed replacements.
EMA=[]
for k,degrees in enumerate([40,170,300],1):
 a=math.radians(degrees);n=np.array([math.cos(a),math.sin(a),0]);t=np.array([-math.sin(a),math.cos(a),0]);r=R+350;p=n*r
 beam((*p[:2],15800),(*p[:2],24500),80,f'EMA_{k}_mast')
 # Both lower ring and upper lid/parapet connections explicitly modelled.
 for label,zz in [('lower_ring',16050),('top_lid_parapet',22120)]:
  beam(tuple(n*(R-150)+np.array([0,0,zz])),tuple(n*r+np.array([0,0,zz])),100,f'EMA_{k}_{label}_bracket')
  for side in [-1,1]:beam(tuple(n*(R-130)+t*side*300+np.array([0,0,zz])),tuple(n*r+np.array([0,0,zz+200])),55,f'EMA_{k}_{label}_brace')
 # paired exterior panels on shared yokes as existing GA
 for zz in [20100,21600]:beam(tuple(p-t*650+np.array([0,0,zz])),tuple(p+t*650+np.array([0,0,zz])),65,f'EMA_{k}_yoke')
 for side in [-1,1]:
  q=p+t*side*380;box(*(q[:2]+n[:2]*65-t[:2]*210),19900,200,420,2100,f'EMA_{k}_antenna_{side}','light_metal',a)
 # roof radio frame near perimeter inside guardrail
 q=n*(R-850);beam((*q[:2],22000),(*q[:2],23500),75,f'radio_{k}_frame')
 for j in [-1,0,1]:
  loc=q+t*j*350;box(*(loc[:2]-t[:2]*140),22300,250,280,1000,f'radio_{k}_{j}','light_metal',a)
 EMA.append({'id':k,'angle_degrees_ccw_from_east':degrees,'connections':['bottom ring','lid/parapet'],'positions':'schematic from existing GA'})
# Other operators' simple pole antennas and dishes observed on tank wall/roof.
for k,deg in enumerate([90,112,220,270,0]):
 a=math.radians(deg);n=np.array([math.cos(a),math.sin(a),0]);p=n*(R+210)
 beam((*p[:2],15800),(*p[:2],24000),65,f'OLO_{k}_mast')
 for zz,label in [(16050,'lower_ring'),(22120,'top_lid_parapet')]:beam(tuple(n*(R-100)+[0,0,zz]),tuple(p+[0,0,zz]),65,f'OLO_{k}_{label}_bracket')
 panel(R+220,a,22200,180,1700,f'OLO_{k}_antenna',depth=100)
 if k in [0,2,3]:disk(tuple(n*(R+350)+[0,0,23100]),a,220,f'OLO_{k}_dish')
# Major rooftop dish on spreader frame, visual approximate dimensions.
a=math.radians(190);n=np.array([math.cos(a),math.sin(a),0]);q=n*4000
for off in [-550,550]:box(q[0]-700,q[1]+off,22000,1400,100,100,'dish_spreader','metal')
beam((q[0],q[1],22100),(q[0],q[1],23300),100,'dish_support')
disk((q[0],q[1],23400),a,650,'rooftop_large_dish')
# Covered roof features from photos: schematic, not inferred internal penetrations.
for k,(x,y,l,w) in enumerate([(2800,-1300,1400,1100),(2800,200,850,750),(3800,-1800,800,650),(3900,-650,900,700),(2700,1400,800,650)]):
 box(x,y,22000,l,w,230,f'roof_plinth_{k}','concrete');box(x-45,y-45,22230,l+90,w+90,100,f'roof_cover_{k}','metal')
# Perimeter cable tray and two vertical cable routes; schematic external detail.
ring(R-260,R-400,22170,250,'perimeter_cable_tray','dark')
for deg in [67.5,292.5]:
 a=math.radians(deg);r=R+45
 for j in [-65,0,65]:
  x=r*math.cos(a)-j*math.sin(a);y=r*math.sin(a)+j*math.cos(a);beam((x,y,50),(x,y,22250),35,'vertical_cable_routes','cable')
# No final exchange mesh exported here.
mesh={'vertices':V,'faces':F,'groups':G,'materials':M,'colors':C,'units':'mm','up_axis':'Z','parameters':PARAM,'EMA_register':EMA}
# Remove intentionally zero-depth internal surfaces that collapsed; ring h=0 top/bottom are duplicated but finite triangles retained once.
valid=[]
for i,f in enumerate(F):
 p=np.array([V[j-1] for j in f]);
 if np.linalg.norm(np.cross(p[1]-p[0],p[2]-p[0]))>1e-7:valid.append(i)
mesh.update(faces=[F[i] for i in valid],groups=[G[i] for i in valid],materials=[M[i] for i in valid])
(O/'mesh.json').write_text(json.dumps(mesh,separators=(',',':')))
(O/'parameters.json').write_text(json.dumps(PARAM,indent=2)+'\n')
print(json.dumps({'vertices':len(V),'faces':len(valid),'parameters':PARAM,'sha256':hashlib.sha256((O/'mesh.json').read_bytes()).hexdigest()}))
