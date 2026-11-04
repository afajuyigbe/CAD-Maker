"""7145 Saffron Walden Tower review geometry. mm; Z up; GA-aligned axes.
Unmeasured facade envelopes are photo interpretations, not fabrication dimensions.
"""
from pathlib import Path
import json,math
import numpy as np
from wall_profile import segments,thickness,COURSE_PITCH,COURSES_PER_STEP,OFFSET,BASE_RETURN,TOP_ENVELOPE,BASE_EXTERNAL,BASE_WALL,PLINTH_TOP
P=Path(__file__).resolve().parents[1];O=P/'model';D=P/'drawings';O.mkdir(exist_ok=True);D.mkdir(exist_ok=True)
V=[];F=[];G=[];M=[]
C={'brick':(.52,.34,.22),'trim':(.62,.46,.31),'recess':(.28,.22,.17),'glass':(.24,.30,.31),'steel':(.56,.61,.61),'proposed':(.60,.48,.35),'roof':(.69,.69,.64),'concrete':(.73,.73,.69),'tank':(.42,.27,.18),'tank_rib':(.50,.34,.23),'pipe':(.25,.26,.23),'wood':(.34,.26,.17),'mortar':(.53,.39,.28),'guard':(.45,.49,.48)}
def face(pts,g,m):
 a=np.array(pts,float)
 if np.linalg.norm(np.cross(a[1]-a[0],a[2]-a[0]))<1e-7:return
 ix=[]
 for p in a:V.append(p.tolist());ix.append(len(V))
 F.append(ix);G.append(g);M.append(m)
def box(x,y,z,l,w,h,g,m='steel'):
 q=[(x,y,z),(x+l,y,z),(x+l,y+w,z),(x,y+w,z),(x,y,z+h),(x+l,y,z+h),(x+l,y+w,z+h),(x,y+w,z+h)]
 for ix in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:face([q[i] for i in ix],g,m)
def beam(a,b,width,depth,g,m='steel'):
 a=np.array(a,float);b=np.array(b,float);u=b-a;u=u/np.linalg.norm(u);v=np.cross(u,[0,0,1])
 if np.linalg.norm(v)<.01:v=np.array([1.,0,0])
 v=v/np.linalg.norm(v)*width/2;w=np.cross(u,v);w=w/np.linalg.norm(w)*depth/2
 pts=[a-v-w,a+v-w,a+v+w,a-v+w,b-v-w,b+v-w,b+v+w,b-v+w]
 for ids in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:face([pts[i] for i in ids],g,m)
def tube(a,b,r,g,m='steel',n=10):
 a=np.array(a,float);b=np.array(b,float);u=b-a;u/=np.linalg.norm(u);v=np.cross(u,[0,0,1])
 if np.linalg.norm(v)<.1:v=np.array([1.,0,0])
 v/=np.linalg.norm(v);w=np.cross(u,v);q=[a+r*(v*math.cos(i*2*math.pi/n)+w*math.sin(i*2*math.pi/n)) for i in range(n)];t=[p+b-a for p in q]
 face(q[::-1],g,m);face(t,g,m)
 for i in range(n):face([q[i],q[(i+1)%n],t[(i+1)%n],t[i]],g,m)
W=5200.;ROOF=25000.;SLAB=175.;F4=ROOF-SLAB-4100.;SOFFIT=ROOF-SLAB
# Exterior envelope follows photographs: broader stepped base and strong projecting cornices.
# Wall envelope not a surveyed thickness; only5200internal and175roof slab are dimensioned.
profiles=segments(ROOF)
for z0,z1,t in profiles:
 for side in ['S','N','E','W']:
  if side=='S':pts=[(-t,-t,z0),(W+t,-t,z0),(W+t,-t,z1),(-t,-t,z1)]
  if side=='N':pts=[(W+t,W+t,z0),(-t,W+t,z0),(-t,W+t,z1),(W+t,W+t,z1)]
  if side=='E':pts=[(W+t,-t,z0),(W+t,W+t,z0),(W+t,W+t,z1),(W+t,-t,z1)]
  if side=='W':pts=[(-t,W+t,z0),(-t,-t,z0),(-t,-t,z1),(-t,W+t,z1)]
  face(pts,'tower_wall_'+side,'brick')
 # Modest course texture: face edges suppressed by renderer.
 for z in np.arange(z0+COURSE_PITCH,z1,COURSE_PITCH):
  for side in ['S','N','E','W']:
   if side=='S':pts=[(-t,-t-2,z),(W+t,-t-2,z),(W+t,-t-2,z+3),(-t,-t-2,z+3)]
   if side=='N':pts=[(W+t,W+t+2,z),(-t,W+t+2,z),(-t,W+t+2,z+3),(W+t,W+t+2,z+3)]
   if side=='E':pts=[(W+t+2,-t,z),(W+t+2,W+t,z),(W+t+2,W+t,z+3),(W+t+2,-t,z+3)]
   if side=='W':pts=[(-t-2,W+t,z),(-t-2,-t,z),(-t-2,-t,z+3),(-t-2,W+t,z+3)]
   face(pts,'cosmetic_courses','mortar')
# Horizontal masonry returns close the widening wall envelope at every course-count step.
for (lo,hi,t),(nlo,nhi,nt) in zip(profiles,profiles[1:]):
 for points in [
  [(-t,-t,hi),(W+t,-t,hi),(W+nt,-nt,hi),(-nt,-nt,hi)],
  [(-t,W+t,hi),(-nt,W+nt,hi),(W+nt,W+nt,hi),(W+t,W+t,hi)],
  [(-t,-t,hi),(-nt,-nt,hi),(-nt,W+nt,hi),(-t,W+t,hi)],
  [(W+t,-t,hi),(W+t,W+t,hi),(W+nt,W+nt,hi),(W+nt,-nt,hi)]]:face(points,'masonry_wall_returns','brick')
def ring(z,h,t,project,g):
 for x,y,l,w in [(-t-project,-t-project,W+2*(t+project),180),(-t-project,W+t+project-180,W+2*(t+project),180),(-t-project,-t-project,180,W+2*(t+project)),(W+t+project-180,-t-project,180,W+2*(t+project))]:box(x,y,z,l,w,h,g,'trim')
for z,t in [(300,950),(5200,950),(10200,800),(16200,650),(19800,550),(24500,500)]:
 t=thickness(z);ring(z,140,t,80,'cornice_lower');ring(z+140,160,t,160,'cornice_middle');ring(z+300,110,t,230,'cornice_coping')
# Upper corbel course, discrete projecting masonry brackets.
for side in range(4):
 for x in np.linspace(200,W-200,7):
  if side==0:box(x-130,-790,20000,260,350,450,'upper_corbels','trim')
  if side==1:box(x-130,W+440,20000,260,350,450,'upper_corbels','trim')
  if side==2:box(-790,x-130,20000,350,260,450,'upper_corbels','trim')
  if side==3:box(W+440,x-130,20000,350,260,450,'upper_corbels','trim')
def arched(side,c,z,width,height,t,glazed,g):
 radius=width/2;spring=z+height-radius
 def xyz(s,zz,off,t=None):
  if t is None:t=thickness(zz)
  if side=='S':return(c+s,-t-off,zz)
  if side=='N':return(W-c-s,W+t+off,zz)
  if side=='E':return(W+t+off,c+s,zz)
  return(-t-off,W-c-s,zz)
 def panel(poly,name,mat,off):
  def clip(q,z,up):
   out=[]
   for a,b in zip(q,q[1:]+q[:1]):
    ina=a[1]>=z if up else a[1]<=z;inb=b[1]>=z if up else b[1]<=z
    if ina:out.append(a)
    if ina!=inb:
     v=(z-a[1])/(b[1]-a[1]);out.append((a[0]+v*(b[0]-a[0]),z))
   return out
  for lo,hi,t in profiles:
   q=clip(poly,lo,True)
   if q:q=clip(q,hi,False)
   if len(q)>=3:face([xyz(x,z,off,t) for x,z in q],name,mat)
 def bar(a,b,name):
  cuts=sorted(set([a[1],b[1]]+[z for z,_,_ in profiles if min(a[1],b[1])<z<max(a[1],b[1])]))
  if a[1]==b[1]:beam(xyz(*a,32),xyz(*b,32),24,24,name,'steel');return
  for z0,z1 in zip(cuts,cuts[1:]):
   zz=(z0+z1)/2;t=thickness(zz)
   x0=a[0]+(b[0]-a[0])*(z0-a[1])/(b[1]-a[1]);x1=a[0]+(b[0]-a[0])*(z1-a[1])/(b[1]-a[1])
   beam(xyz(x0,z0,32,t),xyz(x1,z1,32,t),24,24,name,'steel')
 arc=[(radius*math.cos(a),spring+radius*math.sin(a)) for a in np.linspace(0,math.pi,17)]
 q=[(-radius,z),(radius,z)]+arc
 panel(q,g,'glass' if glazed else 'recess',12)
 # Arch ring and vertical jambs are geometry, not painted rectangular window outlines.
 for a,b in zip(np.linspace(0,math.pi,17),np.linspace(0,math.pi,17)[1:]):
  rr=radius+95;panel([(radius*math.cos(a),spring+radius*math.sin(a)),(rr*math.cos(a),spring+rr*math.sin(a)),(rr*math.cos(b),spring+rr*math.sin(b)),(radius*math.cos(b),spring+radius*math.sin(b))],g+'_arch','trim',28)
 for xx in [-radius-95,radius]:panel([(xx,z),(xx+95,z),(xx+95,spring),(xx,spring)],g+'_jamb','trim',28)
 if glazed:
  for zz in np.arange(z+300,spring,450):bar((-radius,zz),(radius,zz),g+'_glazing_bars')
  bar((0,z),(0,spring+radius),g+'_glazing_bars')
for side in ['S','N','E','W']:
 glazed=side in ['S','N']
 for c in [1650,3550]:
  arched(side,c,6200,860,3600,800,glazed,'lower_arch_'+side)
  arched(side,c,11100,1050,4700,650,glazed,'main_arch_'+side)
 for c in [1150,2600,4050]:arched(side,c,16900,680,2300,550,glazed,'upper_arch_'+side)
 for c in [800,2000,3200,4400]:arched(side,c,21300,620,2800,500,False,'tank_level_arch_'+side)
 # Brick pilasters distinguish the paired tall recessed panels.
 for c in [400,2600,4800]:
  for lo,hi,t in profiles:
   z0=max(lo,10400);z1=min(hi,16100)
   if z1<=z0:continue
   if side=='S':box(c-90,-t-45,z0,180,50,z1-z0,'facade_pilasters','trim')
   if side=='N':box(c-90,W+t-5,z0,180,50,z1-z0,'facade_pilasters','trim')
   if side=='E':box(W+t-5,c-90,z0,50,180,z1-z0,'facade_pilasters','trim')
   if side=='W':box(-t-45,c-90,z0,50,180,z1-z0,'facade_pilasters','trim')
arched('W',2600,100,1200,3300,950,False,'ground_entry')
# Roof concrete; four perimeter strips preserve roof access opening.
for x,y,l,w in [(0,0,W,1800),(0,3200,W,W-3200),(0,1800,2200,1400),(3200,1800,W-3200,1400)]:box(x,y,SOFFIT,l,w,SLAB,'roof_slab','roof')
T=TOP_ENVELOPE
for x,y,l,w in [(-T,-T,W+2*T,T),(-T,W,W+2*T,T),(-T,0,T,W),(W,0,T,W)]:box(x,y,ROOF,l,w,550,'roof_parapet','brick')
for x,y in [(-T,-T),(W,-T),(W,W),(-T,W)]:box(x,y,ROOF,T,T,550,'roof_corner_piers','trim')
# Seven internal embedded beam axes, not fabricated section dimensions.
for i in range(1,8):
 yy=650*i;face([(0,yy-12,SOFFIT-5),(W,yy-12,SOFFIT-5),(W,yy+12,SOFFIT-5),(0,yy+12,SOFFIT-5)],f'embedded_beam_{i}','steel')
def ibeam(a,b,h,bf,tf,tw,g):
 a=np.array(a,float);b=np.array(b,float)
 for zz in [-h/2+tf/2,h/2-tf/2]:beam(a+[0,0,zz],b+[0,0,zz],bf,tf,g)
 beam(a,b,tw,h-2*tf,g)
# Measured exposed members, with the measurement-based profile retained rather than a false standard label.
for xx in [W/3,2*W/3]:ibeam((xx,0,SOFFIT-76),(xx,W,SOFFIT-76),152,125,9,7,'exposed_roof_member')
ibeam((0,2600,F4-255),(W,2600,F4-255),510,190,20,10,'primary_fourth_floor_floor_EW')
# Fourth-floor STEEL floor / third-floor roof; no invented 175mm concrete slab here.
# Primary beam lies BELOW this floor, not at the roof above the fourth floor.
# Steel deck thickness is unmeasured: use a surface with no asserted build-up.
# The flanged pipe is not a structural column.
for x,y,l,w in [(0,0,W,1700),(0,3500,W,1700),(0,1700,2000,1800),(3300,1700,1900,1800)]:face([(x,y,F4),(x+l,y,F4),(x+l,y+w,F4),(x,y+w,F4)],'fourth_floor_steel_deck','steel')
tube((3900,3000,F4),(3900,3000,SOFFIT),170,'service_pipe','pipe')
for zz in [F4+600,F4+2800]:tube((3900,3000,zz),(3900,3000,zz+65),230,'service_pipe_flanges','pipe')
# Decommissioned tank panels, four rows with raised cross ribs and circular bosses.
for side in ['N','S','E','W']:
 def uv(s,z,off):
  if side=='S':return(s,off,z)
  if side=='N':return(W-s,W-off,z)
  if side=='E':return(W-off,s,z)
  return(off,W-s,z)
 for j in range(4):
  for k in range(4):
   lo=j*1300+12;hi=(j+1)*1300-12;zb=F4+k*925+12;zt=F4+(k+1)*925-12;centre=((lo+hi)/2,(zb+zt)/2)
   face([uv(lo,zb,35),uv(hi,zb,35),uv(hi,zt,35),uv(lo,zt,35)],'tank_panels_'+side,'tank')
   for a,b in [((lo,zb),(hi,zb)),((hi,zb),(hi,zt)),((hi,zt),(lo,zt)),((lo,zt),(lo,zb)),((lo,zb),(hi,zt)),((lo,zt),(hi,zb))]:beam(uv(*a,70),uv(*b,70),24,24,'tank_ribs_'+side,'tank_rib')
   cp=np.array(uv(*centre,95));axis=np.array([0,1,0]) if side in ['N','S'] else np.array([1,0,0]);tube(cp-axis*15,cp+axis*15,80,'tank_bosses_'+side,'tank_rib',12)
# Interior masonry band above the former 3700mm tank; actual room geometry.
for side in ['N','E']:
 def inner(s,z,off=1):return (s,W-off,z) if side=='N' else (W-off,s,z)
 face([inner(0,F4+3700),inner(W,F4+3700),inner(W,SOFFIT),inner(0,SOFFIT)],'interior_brick_band_'+side,'brick')
 for z in np.arange(F4+3700+75,SOFFIT,75):face([inner(0,z,3),inner(W,z,3),inner(W,z+3,3),inner(0,z+3,3)],'interior_brick_joints_'+side,'mortar')
 for row,z in enumerate(np.arange(F4+3700,SOFFIT,75)):
  for x in np.arange(0 if row%2 else 112.5,W,225):face([inner(x,z,4),inner(x+3,z,4),inner(x+3,min(z+75,SOFFIT),4),inner(x,min(z+75,SOFFIT),4)],'interior_brick_joints_'+side,'mortar')
# View-only unbroken floor surface for the explanatory interior illustration.
# It is not exported as an invented physical floor over the surveyed access hole.
face([(0,0,F4),(W,0,F4),(W,W,F4),(0,W,F4)],'interior_review_floor','concrete')
# Timber access stair and elevated hatch landing.
for x,y in [(2100,1800),(3200,1800),(2100,3300),(3200,3300)]:box(x-55,y-55,F4,110,110,1900,'timber_access_frame','wood')
for i in range(11):box(2100,1750+i*130,F4+i*175,1100,180,55,'timber_stair_treads','wood')
box(2100,3000,F4+1850,1100,450,100,'timber_landing','wood')
for x in [2120,3150]:beam((x,3100,F4+1850),(x,3100,ROOF),60,60,'hatch_ladder','steel')
for z in np.arange(F4+2000,ROOF,280):beam((2120,3100,z),(3150,3100,z),35,35,'hatch_ladder','steel')
face([(2200,1800,ROOF+30),(3200,1800,ROOF+30),(3200,3000,ROOF+1200),(2200,3000,ROOF+1200)],'open_roof_hatch','roof')
# Perimeter mesh guarding and cable tray, from supplied rooftop photograph.
for a,b in [((-300,-300),(W+300,-300)),((W+300,-300),(W+300,W+300)),((W+300,W+300),(-300,W+300)),((-300,W+300),(-300,-300))]:
 for z in [ROOF+100,ROOF+1050]:tube((*a,z),(*b,z),20,'roof_guard','guard')
 for t in np.linspace(0,1,18):
  q=np.array(a)*(1-t)+np.array(b)*t;beam((*q,ROOF+80),(*q,ROOF+1050),10,10,'roof_guard_mesh','guard')
 aa=np.array(a)*.94+np.array([W/2,W/2])*.06;bb=np.array(b)*.94+np.array([W/2,W/2])*.06;beam((*aa,ROOF+100),(*bb,ROOF+100),160,75,'roof_cable_tray','steel')
# Allocated TEF equipment: three sectors, single long panel plus two stacked short panels.
sectors=[('S1',0,(1300,W+T+50),(3900,W+T+50)),('S2',120,(W+T+50,1300),(4350,-T-50)),('S3',240,(-T-50,1300),(850,-T-50))]
for sec,az,solo,pair in sectors:
 fwd=np.array([math.sin(math.radians(az)),math.cos(math.radians(az))]);right=np.array([fwd[1],-fwd[0]])
 for k,centre in enumerate([solo,pair]):
  c=np.array(centre,float);tube((*c,21900),(*c,24700),57.15,sec+'_wall_carrier','proposed')
  for z in [22300,24000]:
   inner=c-fwd*450;beam((*inner,z),(*c,z),85,85,sec+'_wall_mount','proposed');box(inner[0]-100,inner[1]-100,z-100,200,200,30,sec+'_wall_plate','proposed')
 for j,(c,cz,h,w) in enumerate([(solo,23250,2000,400),(pair,23960,780,420),(pair,22640,780,420)]):
  c=np.array(c,float)+fwd*110;dep=180;pp=[]
  for z in [cz-h/2,cz+h/2]:
   for rr,ff in [(-w/2,-dep/2),(w/2,-dep/2),(w/2,dep/2),(-w/2,dep/2)]:pp.append((*(c+right*rr+fwd*ff),z))
  for ix in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:face([pp[i] for i in ix],sec+'_allocated_antenna_'+str(j),'proposed')
# Allocated internal RRUs: GA three groups of five on N/W/E internal rails.
for side in ['N','W','E']:
 for j in range(5):
  c=650+j*240
  if side=='N':box(c,W-200,20700,200,160,420,'allocated_RRU_'+side+'_'+str(j),'steel')
  elif side=='W':box(40,c,20700,160,200,420,'allocated_RRU_'+side+'_'+str(j),'steel')
  else:box(W-200,c,20700,160,200,420,'allocated_RRU_'+side+'_'+str(j),'steel')
# Allocated 300mm dish on existing west-wall pole; bearing not specified by GA.
tube((-650,1000,18100),(-650,1000,19100),45,'allocated_dish_existing_pole','steel')
tube((-680,1000,18600),(-760,1000,18600),150,'allocated_300mm_dish','roof',20)
# Retained OLO roof installations, visually distinct from allocated wall-mounted TEF panels.
for k,(x,y) in enumerate([(4400,4400),(4400,700),(700,700)]):
 tube((x,y,ROOF),(x,y,28300),57,'retained_roof_mast_'+str(k),'steel')
 for dx,dy in [(1200,0),(0,1200)]:beam((x-dx,y-dy,ROOF+100),(x,y,ROOF+1500),55,55,'retained_roof_bracing','steel')
 box(x-150,y+70,26750,300,140,1500,'retained_OLO_antenna_'+str(k),'roof')
 if k==0:tube((x,y+120,27400),(x,y+200,27400),220,'retained_dish','roof',20)
# Apply the GA plan's small rotation consistently; preserve right-handed Xeast/Ynorth.
angle=math.atan2(9.78,176.88);ca,sa=math.cos(angle),math.sin(angle)
for q in V:q[0],q[1]=q[0]*ca-q[1]*sa,q[0]*sa+q[1]*ca
mesh={'vertices':V,'faces':F,'groups':G,'materials':M,'colors':C,'units':'mm','up_axis':'Z','view_only_groups':['interior_review_floor']}
(O/'mesh.json').write_text(json.dumps(mesh,separators=(',',':')))
(O/'parameters.json').write_text(json.dumps({'internal_clear':5200,'roof_level':25000,'slab_thickness':175,'parapet':550,'fourth_floor_level_from_roof_and_clear_height':F4,'fourth_floor_clear_height':4100,'primary_beam_level':'Fourth-floor floor / third-floor roof','primary_beam_top':F4,'primary_beam_soffit':F4-510,'fourth_floor_floor_type':'Steel; deck build-up unmeasured','tank_panel_height':3700,'beam_count':7,'beam_spacing':650,'spaces':8,'edge_beams':False,'roof_embedded_section':'Not measured; position bands only','measured_profiles':[{'depth':510,'width':190,'flange':20},{'depth':152,'width':125,'flange':9}],'rotation_deg':math.degrees(angle),'wall_profile':{'outward_step_mm':OFFSET,'small_step_count':3,'location':'Lower plinth below lowest arched openings','courses_per_step':COURSES_PER_STEP,'base_return_mm':BASE_RETURN,'visual_course_pitch_mm':COURSE_PITCH,'course_pitch_status':'Unmeasured; visual model proxy only','base_external_width_mm':BASE_EXTERNAL,'base_wall_mm':BASE_WALL,'plinth_top_first_floor_mm':PLINTH_TOP,'top_wall_envelope_mm':TOP_ENVELOPE,'first_floor_wall_approx_mm':[550,600],'top_wall_envelope_status':'Nominal 650 closes exact base/clear widths and returns; first-floor thickness described approximately 550/600' },'visual_only':['External wall envelope/facade proportions','Arch sizes and recess depths','Hatch/stair and tank panel modules','Unmeasured steel web thicknesses'], 'clear_height_note':'Survey floor-to-ceiling readings retained separately; not forced into GA floor-to-floor levels'},indent=2)+'\n')
import ezdxf
cad=ezdxf.new('R2000');cad.units=4
for g in sorted(set(G)):cad.layers.new(g,dxfattribs={'color':7})
for f,g in zip(F,G):
 if g.startswith(('cosmetic','interior_review')):continue
 q=[V[i-1] for i in f]
 for poly in ([q] if len(q)<=4 else [[q[0],q[j],q[j+1]] for j in range(1,len(q)-1)]):cad.modelspace().add_3dface(poly,dxfattribs={'layer':g})
cad.saveas(D/'7145-tower-model.dxf')
import cadquery as cq
parts={}
for f,g in zip(F,G):
 if g.startswith(('cosmetic','interior_review')):continue
 pts=[cq.Vector(*V[i-1]) for i in f]
 try:parts.setdefault(g,[]).append(cq.Face.makeFromWires(cq.Wire.makePolygon(pts,close=True)))
 except Exception:
  for j in range(1,len(pts)-1):parts.setdefault(g,[]).append(cq.Face.makeFromWires(cq.Wire.makePolygon([pts[0],pts[j],pts[j+1]],close=True)))
a=cq.Assembly(name='7145_Saffron_Walden_Tower')
for g,fs in parts.items():a.add(cq.Compound.makeCompound(fs),name=g)
a.save(str(D/'7145-tower-model.step'))
print(len(V),'vertices',len(F),'faces; model exported',flush=True)
