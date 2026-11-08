"""Project 71222 / Jet 0231: shared review mesh, mm, Z up.
Measured footprint + graphical steel layout; unmeasured sections are rendering proxies.
"""
from pathlib import Path
import math,json
import numpy as np
P=Path(__file__).resolve().parents[1];O=P/'model';D=P/'drawings'
A=json.loads((P/'interpretation/parameters.json').read_text());Q=A['visual_proxies'];CB=A['sections']['castellated']
V=[];F=[];G=[];M=[]
C={'timber':(.48,.35,.25),'brick':(.52,.29,.23),'render':(.80,.78,.70),'roof':(.66,.68,.66),'metal':(.77,.80,.79),'dark':(.17,.18,.18),'glass':(.24,.34,.38),'PV':(.13,.23,.32),'PV_grid':(.56,.64,.68),'paving':(.72,.70,.66),'white':(.88,.89,.86)}
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
W=A['width_mm'];L=A['nominal_depth_mm'];SPAN=A['main_span_depth_mm'];Z=Q['roof_level'];T=Q['roof_deck_thickness'];S=Z-T;H=Q['gallery_clear_height'];FLOOR=S-H
# Simple theatre massing follows the plan/aerial topology. No source engineering dimensions implied.
box(-13000,-9000,0,13000,50500,7500,'context_west_foyer','render')
box(-13000,-12500,0,23000,12500,7500,'context_south_entrance','render')
box(W,0,0,7000,41500,6000,'context_east_service','brick')
box(-13000,41500,0,W+20000,9000,10000,'context_rear_blocks','render')
# Auditorum mass and gently pitched roof behind the fly tower.
box(0,L,0,W,29000,14500,'context_auditorium','brick')
face([(0,L,14500),(W,L,14500),(W,L+29000,15000),(0,L+29000,15000)],'context_auditorium_roof','roof')
for x,y,l,w,z in [(-13000,-9000,13000,50500,7500),(-13000,-12500,23000,12500,7500),(W,0,7000,41500,6000),(-13000,41500,W+20000,9000,10000)]:box(x-150,y-150,z,l+300,w+300,180,'context_roof_coping','metal')
# Glazed frontage and repetitive windows, visual interpretation of photographs.
for y in np.arange(-8500,41000,2200):
 box(-13035,y,500,35,1900,4400,'context_plaza_glazing','glass');box(-13060,y,500,65,55,4500,'context_glazing_mullions','dark')
for x in np.arange(-12500,9000,2200):
 box(x,-12535,500,1900,35,4400,'context_south_glazing','glass')
 box(x,-12535,5300,1100,35,1500,'context_upper_windows','glass')
face([(-30000,-15000,-20),(-13000,-15000,-20),(-13000,51000,-20),(-30000,51000,-20)],'context_plaza','paving')
# Timber-clad fly tower; brick base and unmeasured wall build-up are visual envelopes only.
for side in ['S','N','E','W']:
 def uv(s,z,offset=0):
  if side=='S':return(s-150,-150-offset,z)
  if side=='N':return(W+150-s,L+150+offset,z)
  if side=='E':return(W+150+offset,s-150,z)
  return(-150-offset,L+150-s,z)
 length=(W if side in ['S','N'] else L)+300
 face([uv(0,0),uv(length,0),uv(length,10000),uv(0,10000)],'flytower_brick_'+side,'brick')
 face([uv(0,10000),uv(length,10000),uv(length,Z),uv(0,Z)],'flytower_timber_'+side,'timber')
 for x in np.arange(0,length+1,1500):beam(uv(x,10000,30),uv(x,Z,30),45,45,'timber_vertical_joints','dark')
 for z in np.arange(10100,Z,500):beam(uv(0,z,10),uv(length,z,10),10,10,'timber_board_joints','timber')
# Concrete/block inner faces are separate visual enclosure, not classified roof support walls.
for side in ['N','E']:
 if side=='N':pts=[(0,L-30,FLOOR),(W,L-30,FLOOR),(W,L-30,S),(0,L-30,S)]
 else:pts=[(W-30,0,FLOOR),(W-30,L,FLOOR),(W-30,L,S),(W-30,0,S)]
 face(pts,'inside_wall_'+side,'dark')
# Metal deck split around opening proxies so the roof access hatch remains open.
# Opening size/upstand and horizontal offsets are supplied; north datum remains provisional.
E=A['equipment'];openings=E['openings'];ROOFN=E['outer_north_y_mm']
# Hatch sizes describe overall upstands, not unsupported1300 clear apertures.
clear_openings=[(x+100,y+100,l-200,w-200,k) for x,y,l,w,k in openings]
xs=sorted(set([0,W]+[q[0] for q in clear_openings]+[q[0]+q[2] for q in clear_openings]));ys=sorted(set([0,ROOFN]+[q[1] for q in clear_openings]+[q[1]+q[3] for q in clear_openings]))
for x0,x1 in zip(xs,xs[1:]):
 for y0,y1 in zip(ys,ys[1:]):
  if any(a<(x0+x1)/2<a+c and b<(y0+y1)/2<b+d for a,b,c,d,_ in clear_openings):continue
  box(x0,y0,S,x1-x0,y1-y0,T,'metal_roof_deck','roof')
for y in np.arange(0,L,400):beam((0,y,S-2),(W,y,S-2),8,8,'deck_profile_ribs','metal')
# Low roof perimeter and coping; not an invented measured parapet height.
for x,y,l,w in [(0,0,W,300),(0,ROOFN-300,W,300),(0,300,300,ROOFN-600),(W-300,300,300,ROOFN-600)]:box(x,y,Z,l,w,300,'roof_edge_upstand','render')
# Safety line is a location path only; do not invent an unmeasured physical barrier height.
for a,b in zip(E['safety_path_mm'],E['safety_path_mm'][1:]):beam((*a,Z+12),(*b,Z+12),45,20,'roof_safety_line','dark')
for x,y,l,w,kind in openings:
 for xx,yy,ll,ww in [(x,y,l,100),(x,y+w-100,l,100),(x,y+100,100,w-200),(x+l-100,y+100,100,w-200)]:box(xx,yy,Z,ll,ww,300,'roof_'+kind+'_upstand','white')
 if kind=='skylight':face([(x+100,y+100,Z+300),(x+l-100,y+100,Z+300),(x+l-100,y+w-100,Z+300),(x+100,y+w-100,Z+300)],'roof_skylight_glass','glass')
 else:
  face([(x+l,y,Z+300),(x+l,y+w,Z+300),(x+l-150,y+w,Z+1600),(x+l-150,y,Z+1600)],'roof_hatch_open_lid','white')
# Three existing PV rows; module subdivisions are illustrative only.
for row,(y,yend) in enumerate(E['PV_rows_north_to_south'][::-1],1):
 x0=E['PV_x0_mm'];x1=E['PV_x1_mm'];dep=yend-y;rise=480
 for j in range(12):
  xa=x0+j*(x1-x0)/12;xb=x0+(j+1)*(x1-x0)/12-(20 if j<11 else 0)
  pts=[(xa,y,Z+200),(xb,y,Z+200),(xb,y+dep,Z+200+rise),(xa,y+dep,Z+200+rise)]
  face(pts,f'PV_row_{row}','PV')
  for a,b in zip(pts,pts[1:]+pts[:1]):beam(a,b,25,25,'PV_aluminium_frames','metal')
  for k in range(1,6):
   xx=xa+(xb-xa)*k/6;beam((xx,y,Z+205),(xx,y+dep,Z+205+rise),4,4,'PV_cell_grid','PV_grid')
 for x in np.arange(x0,x1+1,2600):
  for a,b in [((x,y,Z+80),(x,y,Z+200)),((x,y+dep,Z+80),(x,y+dep,Z+rise+200)),((x,y,Z+180),(x,y+dep,Z+100)),((x,y,Z+180),(x,y+dep,Z+rise+180))]:beam(a,b,40,40,'PV_support_frames','metal')
  for yy in [y,y+dep]:box(x-220,yy-220,Z,440,440,80,'PV_support_bases','dark')
# CBdepth/flanges and I-beam sizes are supplied; web/flange proxies are recorded separately.
def ibeam(a,b,h,bf,tf,g):
 a=np.array(a,float);b=np.array(b,float)
 for z in [-h/2+tf/2,h/2-tf/2]:beam(a+[0,0,z],b+[0,0,z],bf,tf,g,'metal')
 beam(a,b,8,h-2*tf,g,'metal')
def webprism(x,poly,tw,g):
 left=[(x-tw/2,y,z) for y,z in poly];right=[(x+tw/2,y,z) for y,z in poly]
 face(left[::-1],g,'metal');face(right,g,'metal')
 for i in range(len(poly)):j=(i+1)%len(poly);face([left[i],left[j],right[j],right[i]],g,'metal')
def castellated(x):
 h=CB['depth_mm'];bf=CB['flange_width_mm'];tf=CB['flange_thickness_mm'];tw=Q['castellated_web_thickness'];base=S-h;mid=S-h/2
 for z in [base, S-tf]:box(x-bf/2,0,z,bf,SPAN,tf,'castellated_flanges','metal')
 n=12;pitch=SPAN/n;hw=150*h/450;hh=130*h/450 # hole pattern is a visual proxy, not surveyed
 for i in range(n):
  cy=(i+.5)*pitch;yl=i*pitch;yr=(i+1)*pitch;hl=cy-hw;hr=cy+hw;zl=mid-hh;zh=mid+hh
  polys=[[(yl,base+tf),(yr,base+tf),(yr,zl),(yl,zl)],[(yl,zh),(yr,zh),(yr,S-tf),(yl,S-tf)],[(yl,zl),(hl,zl),(hl,zh),(yl,zh)],[(hr,zl),(yr,zl),(yr,zh),(hr,zh)],[(hl,mid),(cy-hw/2,zh),(hl,zh)],[(cy+hw/2,zh),(hr,mid),(hr,zh)],[(hl,zl),(cy-hw/2,zl),(hl,mid)],[(cy+hw/2,zl),(hr,zl),(hr,mid)]]
  for poly in polys:webprism(x,poly,tw,'castellated_webs')
for f in A['castellated_axes_x_fraction']:castellated(f*W)
for y in [0,SPAN]:ibeam((0,y,Z-750-125),(20800,y,Z-750-125),250,200,12,'primary_I_end_frames')
ibeam((0,0,Z-750-125),(0,SPAN,Z-750-125),250,200,12,'primary_I_side_frames')
for x in A['B2_axes_x_mm']:ibeam((x,0,Z-350-100),(x,SPAN,Z-350-100),200,150,12,'B2_I_beams')
# Full-web end beam retains the castellated family envelope, without hexagonal openings.
ibeam((20800,0,S-CB['depth_mm']/2),(20800,SPAN,S-CB['depth_mm']/2),CB['depth_mm'],CB['flange_width_mm'],CB['flange_thickness_mm'],'full_web_castellated_end_beam')
# All additional orange cross-members are B1, below the CHS tie plane.
for y in A['lower_B1_west_y_mm']:
 ibeam((0,y,Z-750-125),(4700,y,Z-750-125),250,200,12,'B1_west_lower_cross_members')
for y in A['lower_B1_east_y_mm']:
 ibeam((16700,y,Z-750-125),(20800,y,Z-750-125),250,200,12,'B1_east_lower_cross_members')
# West diagonal bay retains upper CHS. Central bays use lower beam level.
# The east side beyond the last castellated beam contains I-beams only.
chsz=S-CB['flange_thickness_mm']-45
nodes=[0]+A['castellated_axes_x_mm']
for y in A['secondary_axes_y_mm']:
 for j,(xa,xb) in enumerate(zip(nodes,nodes[1:])):
  start=xa+(75 if j==0 else Q['castellated_web_thickness']/2);end=xb-Q['castellated_web_thickness']/2
  level=chsz if j==0 else Z-750-125
  tube((start,y,level),(end,y,level),45,'CHS_transverse_braces','metal')
for aa,bb in [((0,SPAN),(4700,8900)),((0,5400),(4700,8900)),((0,5400),(4700,1900)),((0,0),(4700,1900))]:
 tube((*aa,chsz),(bb[0]-Q['castellated_web_thickness']/2,bb[1],chsz),45,'CHS_plan_braces','metal')
for x,y in [(0,0),(0,5400),(0,SPAN),(20800,0),(20800,SPAN)]:beam((x,y,FLOOR),(x,y,S),150,150,'roof_support_posts','metal')
# Technical cutaway floor is a context proxy, not the stage fly system.
face([(0,0,FLOOR),(W,0,FLOOR),(W,L,FLOOR),(0,L,FLOOR)],'upper_gallery_floor','roof')
# Same graphic north rotation is used for roof and theatre context.
a=math.radians(A['north_from_local_y_deg']);ca,sa=math.cos(a),math.sin(a)
for q in V:q[0],q[1]=q[0]*ca-q[1]*sa,q[0]*sa+q[1]*ca
mesh={'vertices':V,'faces':F,'groups':G,'materials':M,'colors':C,'units':'mm','up_axis':'Z','geometry_status':'CB800x210 flange18; west CHS upper, central CHS at lower B1 level, east I-beams only; unmeasured details/context visual only'}
(O/'mesh.json').write_text(json.dumps(mesh,separators=(',',':')));(O/'parameters.json').write_text(json.dumps(A,indent=2)+'\n')
import ezdxf
cad=ezdxf.new('R2000');cad.units=4
for g in sorted(set(G)):cad.layers.new(g,dxfattribs={'color':7})
for ids,g in zip(F,G):
 if g in ['PV_cell_grid','timber_board_joints','timber_vertical_joints']:continue
 pts=[V[i-1] for i in ids]
 for q in ([pts] if len(pts)<=4 else [[pts[0],pts[k],pts[k+1]] for k in range(1,len(pts)-1)]):cad.modelspace().add_3dface(q,dxfattribs={'layer':g})
assert not cad.audit().errors;cad.saveas(D/'71222-visual-model.dxf')
import cadquery as cq
parts={}
for ids,g in zip(F,G):
 if g in ['PV_cell_grid','timber_board_joints','timber_vertical_joints']:continue
 pts=[cq.Vector(*V[i-1]) for i in ids]
 try:parts.setdefault(g,[]).append(cq.Face.makeFromWires(cq.Wire.makePolygon(pts,close=True)))
 except Exception:
  for k in range(1,len(pts)-1):parts.setdefault(g,[]).append(cq.Face.makeFromWires(cq.Wire.makePolygon([pts[0],pts[k],pts[k+1]],close=True)))
a=cq.Assembly(name='71222_Jet_0231')
for g,fs in parts.items():a.add(cq.Compound.makeCompound(fs),name=g)
a.save(str(D/'71222-visual-model.step'))
print(len(V),'vertices;',len(F),'surfaces exported',flush=True)
