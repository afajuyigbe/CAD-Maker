"""River House whole-building visual surface mesh. Survey dimensions constrain roof;
photographs constrain facade form; unmeasured facade/equipment details approximate."""
from pathlib import Path
import runpy,json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
P=Path(__file__).parent;O=P/'outputs';O.mkdir(exist_ok=True)
V=[];F=[];G=[];M=[]
colors={'concrete':(.61,.60,.55),'concrete_light':(.76,.75,.69),'glass_a':(.20,.32,.42),'glass_b':(.24,.37,.47),'glass_c':(.28,.40,.49),'frame':(.16,.18,.19),'roof':(.23,.25,.25),'metal':(.58,.62,.63),'white':(.82,.84,.82),'dark':(.23,.25,.26),'vent':(.15,.18,.18),'C1':(.63,.65,.66),'C2_exposed':(.71,.72,.72),'main_beam':(.62,.63,.64),'B1':(.45,.48,.5),'B2':(.59,.63,.66),'connection_symbol':(.25,.27,.28),'column_glazed':(.49,.57,.60)}
def face(points,g,m):
 ids=[]
 for p in points:V.append(tuple(map(float,p)));ids.append(len(V))
 F.append(ids);G.append(g);M.append(m)
def box(x,y,z,l,w,h,g,m):
 p=[(x,y,z),(x+l,y,z),(x+l,y+w,z),(x,y+w,z),(x,y,z+h),(x+l,y,z+h),(x+l,y+w,z+h),(x,y+w,z+h)]
 for ix in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:face([p[i] for i in ix],g,m)
def beam(a,b,w,g,m='metal'):
 a=np.array(a,dtype=float);b=np.array(b,dtype=float);u=b-a;u/=np.linalg.norm(u);t=np.cross(u,[0,0,1])
 if np.linalg.norm(t)<.1:t=np.cross(u,[0,1,0])
 t=t/np.linalg.norm(t)*w/2;s=np.cross(u,t);p=[a-t-s,a+t-s,a+t+s,a-t+s,b-t-s,b+t-s,b+t+s,b-t+s]
 for ix in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:face([p[i] for i in ix],g,m)
def cylinder(x,y,z,r,h,g,m,n=12):
 base=[(x+r*math.cos(2*math.pi*i/n),y+r*math.sin(2*math.pi*i/n),z) for i in range(n)];top=[(a,b,z+h) for a,b,_ in base]
 for i in range(n):face([base[i],base[(i+1)%n],top[(i+1)%n],top[i]],g,m)
 face(base[::-1],g,m);face(top,g,m)
L,W,main,upper=44.65,14.6,38.,41.57
FRONT,REAR=-.23,W+.23
COLUMN_AXES=[0,6.15,11.65,17.15,22.65,28.15,33.65,39.15,44.65]
# Rectangle and heights are survey-constrained. Facade panel grids are approximate.
face([(0,FRONT,0),(L,FRONT,0),(L,REAR,0),(0,REAR,0)][::-1],'ground_envelope','dark')
face([(0,FRONT,38),(L,FRONT,38),(L,REAR,38),(0,REAR,38)],'main_roof_surface','roof')
# Street curtain wall: opaque material colours, individual planar glass panels.
face([(0,FRONT,0),(L,FRONT,0),(L,FRONT,upper),(0,FRONT,upper)],'street_curtain_wall_frame','frame')
# Three glazing modules per structural bay: primary column lines align with
# the survey grid, while the smaller mullions remain subordinate.
nz=28
for bay,(ca,cb) in enumerate(zip(COLUMN_AXES,COLUMN_AXES[1:])):
 for module in range(3):
  for j in range(nz):
   a,b=ca+module*(cb-ca)/3+.025,ca+(module+1)*(cb-ca)/3-.025
   lo,hi=j*upper/nz+.025,(j+1)*upper/nz-.025
   face([(a,FRONT-.025,lo),(b,FRONT-.025,lo),(b,FRONT-.025,hi),(a,FRONT-.025,hi)],'street_glazing',['glass_a','glass_b','glass_c'][(bay+module)%3])
# Full-height columns behind the curtain wall. C2 uses its observed exposed
# 380 x 300 portion only; no assumption of a hidden full section is added.
for x in COLUMN_AXES:
 for y in [0,W]:box(x-.19,y-.15,0,.38,.30,38.,f'facade_column_to_ground_{x}_{y}','C2_exposed')
 box(x-.19,W/2-.19,0,.38,.38,38.,f'central_column_to_ground_{x}','C1')
# Tinted surface ribbons depict the columns visible THROUGH the glazing,
# without falsely turning them into new external concrete pilasters.
for x in COLUMN_AXES:
 a,b=max(0,x-.19),min(L,x+.19)
 if b>a:
  face([(a,FRONT-.031,0),(b,FRONT-.031,0),(b,FRONT-.031,upper),(a,FRONT-.031,upper)],'street_columns_seen_through_glass','column_glazed')
  a,b=max(0,x-.04),min(L,x+.04)
  face([(a,FRONT-.036,0),(b,FRONT-.036,0),(b,FRONT-.036,upper),(a,FRONT-.036,upper)],'primary_curtain_wall_mullions','frame')
# End facades: precast panel grid and darker roof-level band with narrow openings.
for x in [0,L]:
 for i in range(5):
  for j in range(12):
   a,b=FRONT+i*(REAR-FRONT)/5,FRONT+(i+1)*(REAR-FRONT)/5;lo,hi=j*38/12,(j+1)*38/12
   face([(x,a,lo),(x,b,lo),(x,b,hi),(x,a,hi)],f'end_concrete_{x}','concrete')
 face([(x,FRONT,38),(x,REAR,38),(x,REAR,upper),(x,FRONT,upper)],f'end_upper_band_{x}','dark')
 for i in range(7):
  a=1.5+i*1.65
  xx=x+(-.025 if x==0 else .025)
  face([(xx,a,39),(xx,a+.55,39),(xx,a+.55,40.2),(xx,a,40.2)],f'end_high_vents_{x}','white')
# Rear: two horizontal banks of glazing and a pale full-height central spine.
face([(0,REAR,0),(L,REAR,0),(L,REAR,upper),(0,REAR,upper)],'rear_cladding','concrete')
core0,core1=21.1,24.0
box(core0,REAR,0,core1-core0,.65,upper,'rear_service_spine','concrete_light')
for row in range(14):
 lo=1+row*2.67;hi=min(lo+1.82,37.6)
 for ba,bb in [(1.5,core0),(core1,L-1.5)]:
  for i in range(10):
   a=ba+i*(bb-ba)/10+.025;b=ba+(i+1)*(bb-ba)/10-.025
   face([(a,REAR+.025,lo),(b,REAR+.025,lo),(b,REAR+.025,hi),(a,REAR+.025,hi)],'rear_window_bands','glass_b')
# Rear columns are seen within the glazing bands; horizontal opaque
# spandrels conceal them between floors, as in the engineer-marked photo.
for x in COLUMN_AXES:
 if not (1.5<x<core0 or core1<x<L-1.5):continue
 for row in range(14):
  lo=1+row*2.67;hi=min(lo+1.82,37.6)
  face([(x-.19,REAR+.031,lo),(x+.19,REAR+.031,lo),(x+.19,REAR+.031,hi),(x-.19,REAR+.031,hi)],'rear_columns_seen_through_glass','column_glazed')
# Continuous fine facade joints register the column axes across the opaque
# spandrels, while the wider column visibility remains behind the window bands.
for x in COLUMN_AXES:
 if not (1.5<x<core0 or core1<x<L-1.5):continue
 face([(x-.04,REAR+.036,0),(x+.04,REAR+.036,0),(x+.04,REAR+.036,upper),(x-.04,REAR+.036,upper)],'rear_primary_column_axis_joints','frame')
for ba,bb in [(1.5,core0),(core1,L-1.5)]:
 for i in range(16):
  x=ba+(i+.5)*(bb-ba)/16
  face([(x-.1,REAR+.03,39.2),(x+.1,REAR+.03,39.2),(x+.1,REAR+.03,40.6),(x-.1,REAR+.03,40.6)],'rear_upper_vents','glass_c')
# Exterior frame corners, plinth, and approximate street-level entrances.
for x in [0,L]:
 for y in [FRONT,REAR]:box(x-.10,y-.10,0,.20,.20,upper,'corner_mullions','frame')
box(0,FRONT-.06,4.5,L,.10,.6,'street_fascia','frame')
for x in [10,32]:
 box(x,FRONT-.12,0,2.5,.12,3.2,'street_entry','dark')
 for xx in [x,x+1.25,x+2.5]:beam((xx,FRONT-.15,0),(xx,FRONT-.15,3.2),.045,'entrance_frame')
# Interior faces of high parapet/enclosing roof walls (top at upper roof level).
for y in [.18,W-.18]:
 face([(0,y,38),(L,y,38),(L,y,upper),(0,y,upper)],'roof_inner_perimeter','concrete')
for x in [.18,L-.18]:face([(x,0,38),(x,W,38),(x,W,upper),(x,0,upper)],'roof_inner_end','concrete')
for y in [0,W]:box(0,y-.12,upper-.08,L,.24,.08,'roof_coping','dark')
for x in [0,L]:box(x-.12,0,upper-.08,.24,W,.08,'roof_coping','dark')
# Roof-frame component from surveyed interpretation; ground datum applied once.
r=runpy.run_path(str(P.parent/'roof-support-3d/model.py'),init_globals={'EXPORT_APPROVED':False})
for ids,g,m in zip(r['F'],r['G'],r['M']):
 if g.startswith('C1_') and int(g.rsplit('_',1)[1]) not in [0,2,3,4,8]:continue
 face([(r['V'][i-1][0],r['V'][i-1][1],r['V'][i-1][2]+38) for i in ids],g,m)
# Plant-room enclosure occupies the upper framing zone. Slab shown as surface,
# with no invented slab thickness or hidden member/connection specifications.
for x in [11.65,22.65]:
 face([(x,0,38),(x,W,38),(x,W,upper),(x,0,upper)],'plant_room_enclosure','concrete_light')
face([(11.65,0,upper),(22.65,0,upper),(22.65,W,upper),(11.65,W,upper)],'plant_room_roof','roof')
for x in [11.65,22.65]:
 for y in [3,6,9,12]:
  xx=x+(-.025 if x==11.65 else .025)
  face([(xx,y,38.2),(xx,y+1.2,38.2),(xx,y+1.2,40.6),(xx,y,40.6)],'plant_louvres','vent')
# Grillage: only connection footprint measured. Profiles are schematic visuals.
for y in [.725,6.575]:box(11.65,y-.14,41.65,5.5,.28,.35,'telecom_grillage_schematic','metal')
for x in [11.65,14.4,17.15]:box(x-.14,.725,41.65,.28,5.85,.35,'telecom_grillage_schematic','metal')
# Triangular lattice stub tower and representative antenna panels.
cx,cy=14.4,3.65;z0=42.0;zt=49.4;rad=.75
legs=[(cx+rad*math.cos(a),cy+rad*math.sin(a)) for a in [0,2*math.pi/3,4*math.pi/3]]
for x,y in legs:beam((x,y,z0),(x,y,zt),.10,'stub_tower_legs')
for iz in range(6):
 lo=z0+iz*(zt-z0)/6;hi=z0+(iz+1)*(zt-z0)/6
 for i in range(3):
  a,b=legs[i],legs[(i+1)%3];beam((*a,lo),(*b,lo),.06,'stub_tower_rings');beam((*a,lo),(*b,hi),.045,'stub_tower_bracing')
for z in [45.5,48.1]:
 for i in range(3):
  a=2*math.pi*i/3;x=cx+1.2*math.cos(a);y=cy+1.2*math.sin(a)
  beam((cx,cy,z),(x,y,z),.06,'antenna_supports');box(x-.18,y-.13,z-.65,.36,.26,1.3,'tower_antenna_panels','white')
# Circular antenna support rings visible around the lattice stub.
for z in [45.3,48.0]:
 for i in range(16):
  a,b=2*math.pi*i/16,2*math.pi*(i+1)/16
  beam((cx+1.25*math.cos(a),cy+1.25*math.sin(a),z),(cx+1.25*math.cos(b),cy+1.25*math.sin(b),z),.05,'tower_circular_antenna_ring')
# Roof guarding around measured grillage footprint.
for y in [.3,7.0]:
 for z in [42.2,42.7]:beam((11.2,y,z),(17.6,y,z),.045,'plant_roof_guardrail')
 for x in np.linspace(11.2,17.6,5):beam((x,y,upper),(x,y,42.7),.045,'plant_roof_guardrail')
for x in [11.2,17.6]:
 for z in [42.2,42.7]:beam((x,.3,z),(x,7,z),.045,'plant_roof_guardrail')
# Engineer-confirmed paired corner antennas on a common yoke bracket.
# Hardware sizes/orientation are photo-based visual estimates.
for corner,(x,y) in enumerate([(1,.8),(43.5,.8),(43.5,13.8)]):
 normal=np.array([x-L/2,y-W/2,0.]);normal/=np.linalg.norm(normal)
 tangent=np.array([normal[1],-normal[0],0.]);centre=np.array([x,y,0.])
 beam((x,y,upper),(x,y,44.6),.10,f'corner_{corner}_mast')
 for z in [42.9,44.15]:
  a=centre+tangent*.65;a[2]=z;b=centre-tangent*.65;b[2]=z
  beam(a,b,.065,f'corner_{corner}_shared_yoke')
 for side in [-1,1]:
  foot=centre+side*tangent*.50;foot[2]=42.7
  beam(foot,foot+[0,0,1.7],.065,f'corner_{corner}_yoke_upright')
  c=foot+normal*.16+[0,0,.10];w,d,h=.30,.20,1.55
  origin=c-tangent*w/2-normal*d/2
  pts=[origin,origin+tangent*w,origin+tangent*w+normal*d,origin+normal*d,origin+[0,0,h],origin+tangent*w+[0,0,h],origin+tangent*w+normal*d+[0,0,h],origin+normal*d+[0,0,h]]
  for ix in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:face([pts[i] for i in ix],f'corner_{corner}_antenna_pair_{side}','white')
 for side in [-1,1]:
  anchor=centre+side*tangent*1.2;anchor[2]=upper
  beam(anchor,(x,y,43.1),.055,f'corner_{corner}_mast_brace')
# Main-roof equipment row, raised access cabin and simple circulation platform.
for i,x in enumerate(np.linspace(25,42,9)):
 box(x,11.7,38.15,1.4,1.25,1.5,f'HVAC_{i}','white')
 box(x+.05,11.65,38.25,1.3,.06,1.1,f'HVAC_grille_{i}','vent')
 cylinder(x+.7,12.32,39.65,.48,.30,f'HVAC_fan_{i}','white')
box(29,3.8,38.4,3.4,2.4,2.5,'raised_access_cabin','white');box(28.6,3.3,38.3,4.2,3.4,.10,'cabin_platform','metal')
box(29.2,3.74,38.45,1.0,.06,2.1,'cabin_door','dark')
for x in [28.6,32.8]:
 for z in [38.85,39.35]:beam((x,3.3,z),(x,6.7,z),.04,'platform_guardrail')
for i in range(3):box(29.3,2.1+i*.4,38+i*.1,1.2,.4,.10,'access_steps','metal')
for y in [3.0,10.8]:box(22.65,y,38.08,20,.22,.10,'roof_cable_tray','metal')
# Keep outward face normals correct for OBJ viewers with back-face culling.
for i,g in enumerate(G):
 pts=np.array([V[j-1] for j in F[i]])
 reverse=(g in ['rear_cladding','rear_window_bands','rear_upper_vents','rear_columns_seen_through_glass','rear_primary_column_axis_joints','end_concrete_0','end_upper_band_0','end_high_vents_0'])
 if g=='plant_room_enclosure' and abs(pts[:,0].mean()-11.65)<1e-6:reverse=True
 if g=='plant_louvres' and pts[:,0].mean()<12:reverse=True
 if g=='roof_inner_perimeter' and pts[:,1].mean()<1:reverse=True
 if g=='roof_inner_end' and pts[:,0].mean()>L-1:reverse=True
 if reverse:F[i]=list(reversed(F[i]))
# Export clean surface polygons. OBJ rotation is proper: world (X,Y,Z)->(X,Z,-Y).
stem='7078-river-house-building'
# Review geometry is built without issuing mesh/material exports. This gate
# follows the engineer's request to approve the 3D appearance first.
import sys
if '--export-approved' in sys.argv:
 approval=json.loads((P/'item.json').read_text()).get('approval_gate',{})
 if not approval.get('approved'):raise RuntimeError('Engineer approval is required before OBJ/MTL issue.')
 import hashlib
 geometry_hash=hashlib.sha256(json.dumps({'vertices':V,'faces':F,'groups':G,'materials':M,'colors':colors}).encode()).hexdigest()
 if geometry_hash!=approval.get('approved_geometry_sha256'):raise RuntimeError('Geometry differs from authorised correction; approval record must be resolved.')
 with (O/(stem+'.obj')).open('w') as f:
  f.write('# Entire-building visual mesh; metres; OBJ Y up; ground Y=0\nmtllib '+stem+'.mtl\n')
  for x,y,z in V:f.write(f'v {x:.6f} {z:.6f} {-y:.6f}\n')
  prev=None
  for ids,g,m in zip(F,G,M):
   if (g,m)!=prev:f.write(f'g {g}\nusemtl {m}\n');prev=(g,m)
   f.write('f '+' '.join(map(str,ids))+'\n')
 with (O/(stem+'.mtl')).open('w') as f:
  for m,c in colors.items():f.write(f'newmtl {m}\nKd {" ".join(map(str,c))}\nKa .15 .15 .15\nKs .10 .10 .10\nNs 18\nd 1\nillum 2\n\n')
assert all(np.isfinite(V).flat)
for ids in F:
 p=np.array([V[i-1] for i in ids]);assert np.linalg.norm(np.cross(p[1]-p[0],p[2]-p[0]))>1e-10
# Compact parameter/evidence record, separate measured facts from visual guesses.
record={'scope':'Entire building with rooftop support zone, plant room, tower, antennas and indicative roof equipment','measured_roof_values_m':{'length':44.65,'width':14.6,'main_roof':38,'upper_roof_parapet':41.57,'grillage_connections':[5.5,5.85]},'visual_estimates':['Facade grid and rear band spacing','Paired corner yoke brackets: dimensions and orientation photo-based','End cladding joints and upper vents','Core projection, entrances and cabin','Grillage profiles and tower/antenna geometry','HVAC/cable-tray locations and sizes'],'roof_centre_columns':'Shown above main roof in plant framing zone and at both roof-end wall centres, per final engineer markup; other upper central extensions not verified','C2':'Only exposed 380x300 portion shown in roof frame, hidden full section unverified','facade_mapping':'Glazed street long face; horizontal rear window banks and central service spine; two largely blank ends with upper vents, based on supplied photographs','omitted':['Neighbouring buildings, street furniture, trees and foreground fence','Unverified lower adjacent roof at +7m','Hidden internal floors and connections'],'model_format':'Polygon surface geometry; OBJ/MTL issue controlled by approval record; metres/Y up/ground 0','facade_column_expression':'Full-height perimeter and central columns follow the survey bay grid; tinted ribbons show perimeter columns through street glazing and rear window bands. Fine mullions remain distinct.','facade_standoff':'230 mm illustrative curtain-wall stand-off from nominal column grid; not a surveyed dimension','faces':len(F),'vertices':len(V),'groups':len(set(G)),'validation':'Finite coordinates, nondegenerate polygons, no texture dependencies; mostly quads'}
(O/'model-record.json').write_text(json.dumps(record,indent=2)+'\n')
# Save shared geometry for editable CAD projections and subsequent regeneration.
(O/'mesh.json').write_text(json.dumps({'vertices':V,'faces':F,'groups':G,'materials':M,'colors':colors}))
print(json.dumps(record))
