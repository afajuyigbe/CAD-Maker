"""7145 review sheets: GA roof vectors, survey supports and common model views."""
from pathlib import Path
import json,math,textwrap,shutil
import fitz,ezdxf,numpy as np
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/"model"))
from wall_profile import segments as wall_segments,TOP_ENVELOPE,BASE_WALL,BASE_EXTERNAL
from ezdxf.enums import TextEntityAlignment
P=Path(__file__).resolve().parent;O=P/'drawings';B=P/'model';PT=72/25.4
source=fitz.open(P/'sources/CS_111051_TEF_8233_VF_75548_GA_REV_1A (1).pdf');doc=fitz.open();cad=ezdxf.new('R2000');cad.units=4;cad.set_raster_variables(frame=0)
for layer in ['FRAME','TEXT','DIMENSIONS','EXISTING','PROPOSED','LOAD_BEARING_WALLS','OVERHANG_SUPPORT','BEAMS','PHOTO_COLUMNS','IMAGES','EMBEDDED_BEAMS','ROOF_MEMBERS','SCAN_SYMBOLS','STEEL_FLOOR','TIMBER_DECK','ELEVATION']:cad.layers.new(layer,dxfattribs={'color':7})
cad.linetypes.new('DASHED_REVIEW',dxfattribs={'pattern':[4,2.5,-1.5]})
queue=[];pdf_lines={};BEAM_SEGMENTS=[]
def line(a,b,w=.18,layer='FRAME',gray=0,dash=False):
 a=np.array(a,dtype=float);b=np.array(b,dtype=float)
 if ms.name=='SHEET_01' and layer in ['EXISTING','LOAD_BEARING_WALLS','OVERHANG_SUPPORT'] and BEAM_SEGMENTS:
  # Remove only collinear solid geometry under beam dashes, leaving crossing walls intact.
  delta=b-a;den=float(delta@delta);hits=[]
  if den>1e-10:
   for c,d in BEAM_SEGMENTS:
    if abs(delta[0]*(d-c)[1]-delta[1]*(d-c)[0])>1e-5:continue
    if abs(delta[0]*(c-a)[1]-delta[1]*(c-a)[0])/np.sqrt(den)>.12:continue
    lo,hi=sorted([float((c-a)@delta/den),float((d-a)@delta/den)]);lo=max(0,lo);hi=min(1,hi)
    if hi>lo+1e-8:hits.append((lo,hi))
  if hits:
   merged=[]
   for lo,hi in sorted(hits):
    if merged and lo<=merged[-1][1]:merged[-1][1]=max(hi,merged[-1][1])
    else:merged.append([lo,hi])
   cursor=0.;pieces=[]
   for lo,hi in merged:
    if lo>cursor+1e-8:pieces.append((cursor,lo))
    cursor=max(cursor,hi)
   if cursor<1-1e-8:pieces.append((cursor,1))
   for lo,hi in pieces:
    aa=a+delta*lo;bb=a+delta*hi;pdf_lines.setdefault((w,gray,dash),[]).append((aa,bb))
    ms.add_line((aa[0],297-aa[1]),(bb[0],297-bb[1]),dxfattribs={'layer':layer,'lineweight':round(w*100),'true_color':ezdxf.colors.rgb2int((int(gray*255),)*3),'color':254 if gray>.5 else 250 if gray>0 else 7})
   return
 pdf_lines.setdefault((w,gray,dash),[]).append((a,b))
 ms.add_line((a[0],297-a[1]),(b[0],297-b[1]),dxfattribs={'layer':layer,'lineweight':round(w*100),'true_color':ezdxf.colors.rgb2int((int(gray*255),)*3),'color':254 if gray>.5 else 250 if gray>0 else 7,'linetype':'DASHED_REVIEW' if dash else 'Continuous'})
def text(x,y,t,h=2.25,bold=False,align='left',angle=0):queue.append((x,y,str(t),h,bold,align,angle))
def rect(x,y,w,h,lw=.18):
 pts=[(x,y),(x+w,y),(x+w,y+h),(x,y+h)]
 for a,b in zip(pts,pts[1:]+pts[:1]):line(a,b,lw)
def wrap(x,y,t,n=39,h=2.05):
 for s in textwrap.wrap(t,n):text(x,y,s,h);y+=h*1.5
 return y

def trim_labels():
 bounds=[]
 for x,y,t,h,bold,align,angle in queue:
  w=fitz.get_text_length(t,fontname='hebo' if bold else 'helv',fontsize=h*PT)/PT
  left=x-w/2 if align=='center' else x-w if align=='right' else x
  bounds.append((x-h*1.08-.1,y-w/2-.3,x+.25,y+w/2+.3) if angle==90 else (left-.3,y-h*1.08-.1,left+w+.3,y+.25))
 def interval(a,b,r):
  dx=b[0]-a[0];dy=b[1]-a[1];lo=0.;hi=1.
  for pp,qq in [(-dx,a[0]-r[0]),(dx,r[2]-a[0]),(-dy,a[1]-r[1]),(dy,r[3]-a[1])]:
   if abs(pp)<1e-12:
    if qq<0:return None
   elif pp<0:lo=max(lo,qq/pp)
   else:hi=min(hi,qq/pp)
   if lo>hi:return None
  return lo,hi
 for e in list(ms.query('LINE')):
  a=(e.dxf.start.x,297-e.dxf.start.y);b=(e.dxf.end.x,297-e.dxf.end.y);xmin,xmax=sorted([a[0],b[0]]);ymin,ymax=sorted([a[1],b[1]]);hits=[]
  for r in bounds:
   if r[2]<xmin or r[0]>xmax or r[3]<ymin or r[1]>ymax:continue
   hit=interval(a,b,r)
   if hit and hit[1]-hit[0]>1e-9:hits.append(hit)
  if not hits:continue
  merged=[]
  for lo,hi in sorted(hits):
   if merged and lo<=merged[-1][1]:merged[-1][1]=max(hi,merged[-1][1])
   else:merged.append([lo,hi])
  attrs={k:v for k,v in e.dxf.all_existing_dxf_attribs().items() if k not in ['handle','owner','start','end']};cursor=0.;kept=[]
  for lo,hi in merged:
   if lo>cursor+1e-8:kept.append((cursor,lo))
   cursor=max(cursor,hi)
  if cursor<1-1e-8:kept.append((cursor,1.))
  ms.delete_entity(e)
  for lo,hi in kept:
   aa=np.array(a)+(np.array(b)-a)*lo;bb=np.array(a)+(np.array(b)-a)*hi
   ms.add_line((aa[0],297-aa[1]),(bb[0],297-bb[1]),dxfattribs=attrs)
 return bounds
def flush():
 for (w,gray,dash),segments in pdf_lines.items():
  shape=pg.new_shape()
  for a,b in segments:shape.draw_line(tuple(a*PT),tuple(b*PT))
  shape.finish(color=(gray,)*3,width=w*PT,dashes='[5 3] 0' if dash else None,closePath=False);shape.commit()
 pdf_lines.clear()
 bounds=trim_labels()
 for r in bounds:pg.draw_rect(fitz.Rect(*(v*PT for v in r)),color=None,fill=(1,1,1))
 for x,y,t,h,bold,align,angle in queue:
  width=fitz.get_text_length(t,fontname='hebo' if bold else 'helv',fontsize=h*PT)/PT
  xx=x-width/2 if align=='center' else x-width if align=='right' else x
  if angle:
   pg.insert_text((x*PT,(y+width/2)*PT),t,fontsize=h*PT,fontname='hebo' if bold else 'helv',rotate=angle,color=(0,0,0))
  else:pg.insert_text((xx*PT,y*PT),t,fontsize=h*PT,fontname='hebo' if bold else 'helv',color=(0,0,0))
  e=ms.add_text(t,dxfattribs={'height':h,'layer':'TEXT','style':'Standard','rotation':angle,'true_color':0})
  e.set_placement((x,297-y),align=TextEntityAlignment.CENTER if align=='center' else TextEntityAlignment.RIGHT if align=='right' else TextEntityAlignment.LEFT)
 queue.clear()
def dim(a,b,offset,label):
 a=np.array(a,float);b=np.array(b,float);u=(b-a)/np.linalg.norm(b-a);v=np.array([-u[1],u[0]]);aa=a+v*offset;bb=b+v*offset
 for p,q in [(a,aa+v*np.sign(offset)*1.5),(b,bb+v*np.sign(offset)*1.5),(aa,bb)]:line(p,q,.13,'DIMENSIONS')
 for tip in [aa,bb]:
  tick=(u+v)*.35;line(tip-tick,tip+tick,.13,'DIMENSIONS')
 c=(aa+bb)/2;text(c[0],c[1]-1,label,2.2,align='center')
def vdim(a,b,x,label):
 a=np.array(a,float);b=np.array(b,float);aa=np.array([x,a[1]]);bb=np.array([x,b[1]])
 for p,q in [(a,aa+np.array([1.5 if x>a[0] else -1.5,0])),(b,bb+np.array([1.5 if x>b[0] else -1.5,0])),(aa,bb)]:line(p,q,.13,'DIMENSIONS')
 for tip in [aa,bb]:
  line(tip+np.array([-.35,.35]),tip+np.array([.35,-.35]),.13,'DIMENSIONS')
 text(x-.8,(aa[1]+bb[1])/2,label,2.7,align='center',angle=90)
def caption(x,y,n,title,scale,width):
 pg.draw_circle((x*PT,y*PT),2*PT,color=(0,0,0),width=.4);ms.add_circle((x,297-y),2,dxfattribs={'layer':'FRAME'})
 text(x,y+.7,n,1.8,align='center');text(x+5,y-1,title,2.7,True);line((x+5,y+1),(x+width,y+1),.15);text(x+5,y+4.6,scale,1.9)
def compass(x,y):
 line((x,y+10),(x,y-4),.25);line((x-4,y+3),(x+4,y+3),.15);pg.draw_circle((x*PT,(y+3)*PT),3.2*PT,color=(0,0,0),width=.4);ms.add_circle((x,297-y-3),3.2,dxfattribs={'layer':'FRAME'});line((x,y-4),(x-1,y-1),.2);line((x,y-4),(x+1,y-1),.2);text(x,y-6,'N',2.4,True,align='center')

def logo(path,target,rotate=0):
 from PIL import Image
 im=Image.open(path).convert('RGB')
 if rotate:im=im.rotate(rotate,expand=True)
 im.thumbnail((180,90));iw,ih=im.size;x,y,w,h=target;sc=min(w/iw,h/ih);ox=x+(w-iw*sc)/2;oy=y+(h-ih*sc)/2
 import io
 b=io.BytesIO();im.save(b,format='PNG');pg.insert_image(fitz.Rect(x*PT,y*PT,(x+w)*PT,(y+h)*PT),stream=b.getvalue())
 for yy in range(ih):
  xx=0
  while xx<iw:
   rgb=im.getpixel((xx,yy))
   if min(rgb)>210:xx+=1;continue
   end=xx+1
   while end<iw and min(im.getpixel((end,yy)))<=210:end+=1
   xa,xb=ox+xx*sc,ox+end*sc;ya,yb=297-oy-yy*sc,297-oy-(yy+1)*sc
   ms.add_solid([(xa,ya),(xb,ya),(xa,yb),(xb,yb)],dxfattribs={'layer':'FRAME','color':7});xx=end

def frame(n,title):
 global pg,ms
 pg=doc.new_page(width=420*PT,height=297*PT);ms=cad.blocks.new(f'SHEET_0{n}')
 rect(5,5,410,287,.35);rect(15,20,320,261,.22);line((341,5),(341,292),.3)
 text(344,10,'DIMENSIONS IN mm; LEVELS ABOVE GROUND',1.65,True);line((341,13),(415,13),.18)
 text(345,23,'DRAWING NOTES',2.55,True)
 notes={1:['Roof over fourth floor: slab 175 thick; parapet 550 high.','Exposed roof members: measured 152 x 125; flange 9.','Scan 1: soffit of roof over fourth floor.'],2:['All height dimensions are floor to ceiling; concrete slabs 175 thick shown separately.','B1: 510 x 190, flange 20; at fourth-floor FLOOR / third-floor ROOF.','Fourth-floor steel floor and intermediate timber-deck build-ups not measured.','Ribbed panels are the former water tank.']}[n]
 yy=31
 for i,t in enumerate(notes,1):yy=wrap(345,yy,str(i)+'. '+t,n=43,h=1.95)+2
 text(345,109,'ELEMENT KEY' if n!=3 else 'SCAN KEY',2.5,True)
 if n==1:
  for yy,w,dash,t in [(119,.65,False,'Masonry wall faces'),(129,.45,True,'Embedded roof beams'),(139,.4,False,'Exposed roof members')]:
   line((345,yy-1),(352,yy-1),w,'FRAME',dash=dash);text(355,yy,t,1.9)
  scanbox(349,150,False);text(356,151,'Soffit scan - location 1',1.9)
 else:
  for yy,w,dash,t in [(119,.45,False,'Concrete slab'),(129,.4,True,'Steel floor'),(139,.25,True,'Intermediate timber deck')]:
   line((345,yy-1),(352,yy-1),w,'FRAME',dash=dash);text(355,yy,t,1.9)
  text(345,151,'B1  Primary E/W beam at floor 4',1.9)
 for yy in [162,171,184,211,237,255,272,282]:line((341,yy),(415,yy),.2)
 for xx in [353,378,391,402]:line((xx,162),(xx,184),.15)
 for xx,t in [(344,'Rev'),(355,'Issue'),(380,'Drawn'),(393,'Chkd'),(404,'Date')]:text(xx,168,t,1.65)
 for xx,t in [(344,'1'),(355,'REVIEW'),(380,'AT'),(393,'AF'),(403,'04-11-26')]:text(xx,179,t,1.7)
 text(345,190,'Consultant:',1.8);logo(Path('assets/branding/ka-logo-survey-source.jpeg'),(357,192,43,17))
 text(345,217,'Client: JetNSL',1.9);logo(Path('assets/branding/jet-logo-ga-source.jpeg'),(361,219,40,16),90)
 text(345,243,'Drawing Title:',1.8);text(345,250,title,2.5,True)
 text(345,261,'SAFFRON WALDEN TOWER',2.4,True);text(345,266,'Mount Pleasant Road, Saffron Walden',1.8);text(345,270,'Essex CB11 4GA',1.8)
 text(345,278,'Drawn: AT    Checked: AF',1.95);text(345,287,'7145-0'+str(n)+'  |  Rev 1',2.3,True);text(409,287,'NTS',1.9,align='right')

def scanbox(x,y,number=True):
 r=2.7;rect(x-r,y-r,2*r,2*r,.22)
 # Opposite diagonal to topside: soffit hatch (rising left to right in page axes).
 for k in np.arange(-2*r,2*r+.01,1.3):
  aa=max(-r,k-r);bb=min(r,k+r)
  if bb>aa:line((x+aa,y+k-aa),(x+bb,y+k-bb),.13,'SCAN_SYMBOLS')
 if number:text(x,y-r-1,'1',2.6,True,align='center')

TL=np.array([450.06,281.12]);TR=np.array([626.94,271.34]);BL=np.array([459.90,458.0]);u=TR-TL;v=BL-TL
fx=lambda p:np.array([65+(p[0]-434.34),43+(p[1]-255.62)])
loc=lambda x,y:fx(TL+u*x/5200+v*(5200-y)/5200)
# GA crop includes the roof itself and wall-mounted allocated equipment; source labels excluded.
def plan():
 seen=set()
 for source_index,dr in enumerate(source[4].get_drawings()):
  if source_index>=7915 or source_index==7460:continue # GA outlined lettering and ground footprint are excluded
  co=dr['color'] or (0,0,0);sat=max(co)-min(co)>.18
  for it in dr['items']:
   pairs=[]
   if it[0]=='l':pairs=[(it[1],it[2])]
   elif it[0]=='re':
    r=it[1];pairs=[(r.tl,r.tr),(r.tr,r.br),(r.br,r.bl),(r.bl,r.tl)]
   elif it[0]=='qu':
    q=it[1];pairs=[(q.ul,q.ur),(q.ur,q.lr),(q.lr,q.ll),(q.ll,q.ul)]
   elif it[0]=='c':
    q=np.array([[p.x,p.y] for p in it[1:]]);poly=[(1-t)**3*q[0]+3*(1-t)**2*t*q[1]+3*(1-t)*t*t*q[2]+t**3*q[3] for t in np.linspace(0,1,7)];pairs=list(zip(poly,poly[1:]))
   for a,b in pairs:
    a=np.array(a);b=np.array(b)
    if not all(426<q[0]<662 and 250<q[1]<482 for q in [a,b]):continue
    key=tuple(np.round(np.r_[a,b],2))
    if key in seen:continue
    seen.add(key);line(fx(a),fx(b),.13 if sat else .10,'PROPOSED' if sat else 'EXISTING',.35 if sat else .7)
 # Actual internal faces and roof envelope from GA path; these are not beam axes.
 for corners,weight in [([TL,TR,TR+v,BL],.65),([np.array([434.34,267.08]),np.array([640.98,255.62]),np.array([652.44,462.26]),np.array([445.8,473.72])],.28)]:
  for a,b in zip(corners,corners[1:]+corners[:1]):line(fx(a),fx(b),weight,'LOAD_BEARING_WALLS' if weight>.5 else 'EXISTING')
 for i in range(1,8):line(loc(0,i*650),loc(5200,i*650),.45,'EMBEDDED_BEAMS',dash=True)
 # Solid member-reference 1 runs north/south, perpendicular to embedded axes.
 for xx in [5200/3,10400/3]:
  for dx in [-62.5,62.5]:line(loc(xx+dx,0),loc(xx+dx,5200),.35,'ROOF_MEMBERS')

def section(x,y,h,b,tf,title):
 sc=.075 if h>300 else .18;hh=h*sc;bb=b*sc;ff=tf*sc;ww=1.2
 pts=[(x-bb/2,y-hh/2),(x+bb/2,y-hh/2),(x+bb/2,y-hh/2+ff),(x+ww/2,y-hh/2+ff),(x+ww/2,y+hh/2-ff),(x+bb/2,y+hh/2-ff),(x+bb/2,y+hh/2),(x-bb/2,y+hh/2),(x-bb/2,y+hh/2-ff),(x-ww/2,y+hh/2-ff),(x-ww/2,y-hh/2+ff),(x-bb/2,y-hh/2+ff)]
 for a,bp in zip(pts,pts[1:]+pts[:1]):line(a,bp,.25,'ROOF_MEMBERS')
 dim((x-bb/2,y-hh/2),(x+bb/2,y-hh/2),-7,str(b));vdim((x-bb/2,y-hh/2),(x-bb/2,y+hh/2),x-bb/2-8,str(h))
 text(x,y+hh/2+7,'Flange '+str(tf),2.05,align='center');text(x,y+hh/2+12,title,2.1,True,align='center')

frame(1,'Roof Support Layout');plan();compass(320,36);scanbox(*loc(4000,2800))
dim(loc(0,5200),loc(5200,5200),-14,'5200');dim(loc(0,0),loc(0,5200),-15,'5200')

caption(23,274,1,'Roof Support Layout / Scan Location','NTS',304);flush()

frame(2,'Elevation / 3D Views')
def picture(name,target):
 from PIL import Image,ImageChops
 src=B/(name+'.png');im=Image.open(src).convert('RGB');original_size=im.size;bounds=ImageChops.difference(im,Image.new('RGB',im.size,'white')).getbbox();bounds=(max(0,bounds[0]-3),max(0,bounds[1]-3),min(im.width,bounds[2]+3),min(im.height,bounds[3]+3));im=im.crop(bounds);im.save(O/src.name);size=im.size
 x0,y0,x1,y1=target;sc=min((x1-x0)/size[0],(y1-y0)/size[1]);w,h=np.array(size)*sc;x=x0+(x1-x0-w)/2;y=y0+(y1-y0-h)/2
 pg.insert_image(fitz.Rect(x*PT,y*PT,(x+w)*PT,(y+h)*PT),filename=str(O/src.name))
 idef=cad.add_image_def(filename=src.name,size_in_pixel=size);ms.add_image(idef,(x,297-y-h),(w,h))
 # Editable visible feature edges accompany the image underlay in CAD.
 data=json.loads((B/(name+'-projection.json')).read_text())
 for a,b in data['edges']:
  a=[(a[0]*original_size[0]-bounds[0])/size[0],(a[1]*original_size[1]-bounds[1])/size[1]];b=[(b[0]*original_size[0]-bounds[0])/size[0],(b[1]*original_size[1]-bounds[1])/size[1]]
  ms.add_line((x+a[0]*w,297-y-a[1]*h),(x+b[0]*w,297-y-b[1]*h),dxfattribs={'layer':'EXISTING','color':250,'lineweight':9})
 def project_local(lx,ly,lz):
  angle=math.radians(json.loads((B/'parameters.json').read_text())['rotation_deg']);q=np.array([lx*math.cos(angle)-ly*math.sin(angle),lx*math.sin(angle)+ly*math.cos(angle),lz])
  if data.get('perspective'):
   centre=np.array(data['centre']);pr=np.array([(q-centre)@data['right'],(q-centre)@data['up']])*data['focal']/(data['camera_depth']-q@data['depth'])
  else:pr=np.array([q@data['right'],q@data['up']])
  pixel=(pr-np.array(data['lo']))*data['scale']+np.array(data['offset']);pixel[1]=original_size[1]-pixel[1]
  return np.array([x+(pixel[0]-bounds[0])*sc,y+(pixel[1]-bounds[1])*sc])
 return project_local

# Sectional elevation: dimensions terminate at floor tops and ceiling soffits.
# Unknown timber/steel build-ups are displayed schematically, without numeric thicknesses.
left,right=67.,111.2;scale=.0085;floor_y=257.;elevation_dimensions=[]
def hfloor(y,kind,thickness=None):
 if thickness is not None:
  top=y-thickness*scale
  for yy in [y,top]:line((left,yy),(right,yy),.35,'ELEVATION')
  for xx in np.arange(left,right,3):line((xx,y),(min(xx+1.5,right),top),.10,'ELEVATION')
  # Short dimensions use outward ticks so the separate 175 is legible at A3.
  xx=49
  for yy in [y,top]:line((xx-1,yy),(left,yy),.12,'DIMENSIONS')
  line((xx,y),(xx,top),.12,'DIMENSIONS');line((xx-.35,y+.35),(xx+.35,y-.35),.12,'DIMENSIONS');line((xx-.35,top+.35),(xx+.35,top-.35),.12,'DIMENSIONS')
  text(xx+1.5,(y+top)/2+.7,str(thickness),1.9)
  return top
 top=y-1.3
 for yy in [y,top]:line((left,yy),(right,yy),.30,'STEEL_FLOOR' if kind=='steel' else 'TIMBER_DECK',dash=True)
 return top
levels={};line((left-7,floor_y),(right+7,floor_y),.4,'ELEVATION');levels['Ground-floor floor']=floor_y
for name,height,kind in [('Ground floor',5600,'concrete'),('First floor - lower',2400,'timber'),('First floor - upper',2600,'concrete'),('Second floor',5500,'concrete'),('Third floor',2800,'steel'),('Fourth floor',4100,'concrete')]:
 ceiling_y=floor_y-height*scale
 vdim((left,floor_y),(left,ceiling_y),35,str(height))
 elevation_dimensions.append({'room':name,'value_mm':height,'from':'floor top','to':'ceiling soffit','sheet_floor_y':floor_y,'sheet_ceiling_y':ceiling_y})
 levels[name+' ceiling']=ceiling_y
 top=hfloor(ceiling_y,kind,175 if kind=='concrete' else None)
 if name=='Ground floor':levels['First-floor floor']=top
 if name=='First floor - lower':levels['Intermediate timber deck']=top
 if name=='First floor - upper':levels['Second-floor floor']=top
 if name=='Second floor':levels['Third-floor floor']=top
 if name=='Third floor':levels['Fourth-floor floor']=top
 if name=='Fourth floor':levels['Roof top']=top
 floor_y=top
roof_top=levels['Roof top'];parapet_top=roof_top-550*scale
# Widen both outer wall faces with the survey's course-count offset pattern.
# Clear inner faces remain 5200 apart. Course pitch is unmeasured, so vertical
# step positions are graphical/NTS and are not issued as mm height dimensions.
section_wall_bands=wall_segments((257-roof_top)/scale)
for side in [-1,1]:
 inner=left if side<0 else right
 line((inner,257),(inner,parapet_top),.5,'ELEVATION')
 previous=None
 for lo,hi,t in section_wall_bands:
  x=inner+side*t*scale;y0=257-lo*scale;y1=257-hi*scale
  line((x,y0),(x,y1),.5,'ELEVATION')
  if previous is not None:line((previous,y0),(x,y0),.5,'ELEVATION')
  previous=x
 line((previous,roof_top),(previous,parapet_top),.5,'ELEVATION');line((previous,parapet_top),(inner,parapet_top),.35,'ELEVATION')
vdim((left,roof_top),(left,parapet_top),35,'550')
dim((left,257),(right,257),6,'5200')
dim((left-BASE_WALL*scale,257),(right+BASE_WALL*scale,257),12,'8000')
dim((left-BASE_WALL*scale,251),(left,251),-5,'1400')
# Engineer-marked approximate shaft-wall thickness, at the second-floor zone.
wall_y=(levels['First-floor floor']+levels['Intermediate timber deck'])/2;wall_outer=right+TOP_ENVELOPE*scale
line((right,wall_y),(wall_outer,wall_y),.13,'DIMENSIONS')
for xx in [right,wall_outer]:line((xx-.35,wall_y+.35),(xx+.35,wall_y-.35),.13,'DIMENSIONS')
line((wall_outer,wall_y),(121,wall_y),.13,'DIMENSIONS');text(123,wall_y+.8,'Approx. 550-600',2.1)
for label,y in [('Ground floor',257),('First floor',levels['First-floor floor']),('Timber deck',levels['Intermediate timber deck']),('Second floor',levels['Second-floor floor']),('Third floor',levels['Third-floor floor'])]:
 line((right+1,y),(121,y),.12,'ELEVATION');text(123,y+.8,label,1.9)
f4=levels['Fourth-floor floor'];roof_soffit=levels['Fourth floor ceiling']
line((right+1,f4),(121,f4),.12,'ELEVATION');text(123,f4-2,'Fourth-floor floor',1.9,True);text(123,f4+1.5,'/ third-floor roof',1.9)
line((right+1,roof_top),(121,roof_top),.12,'ELEVATION');text(123,roof_top+.8,'Roof over fourth floor',1.9)
# B1 is a downstand at the fourth-floor FLOOR, wholly separate from roof-above supports.
beam_bottom=f4+510*scale
for yy in [f4,beam_bottom]:line((left,yy),(right,yy),.55,'STEEL_FLOOR')
line((left,beam_bottom),(left,f4),.35,'STEEL_FLOOR');line((right,beam_bottom),(right,f4),.35,'STEEL_FLOOR')
line((right,beam_bottom),(145,beam_bottom+4),.15,'ELEVATION');text(146,beam_bottom+5,'B1 (E/W)',1.9,True)
# Tank height is a separate object dimension, not a storey or slab measurement.
tank_top=f4-3700*scale
for xx in [left+3,right-3]:
 line((xx,f4),(xx,tank_top),.25,'ELEVATION')
 for yy in np.linspace(tank_top,f4,5):line((xx-1,yy),(xx+1,yy),.13,'ELEVATION')
vdim((right-3,f4),(right-3,tank_top),120,'3700')
text((left+right)/2,f4-14,'Former tank',1.8,align='center')
# Roof member and embedded axes shown at the roof slab soffit, not at B1 level.
for xx in [left+(right-left)/3,left+2*(right-left)/3]:rect(xx-125*scale/2,roof_soffit,125*scale,152*scale,.28)
text(76,40,'SECTIONAL ELEVATION',2.3,True);text(76,44,'Clear heights and slab thicknesses',1.8)
(P/'interpretation/elevation-datums.json').write_text(json.dumps({'sheet':2,'scale_status':'NTS','clear_height_dimensions':elevation_dimensions,'concrete_slab_thickness_mm':175,'unknown_build_ups':['Intermediate timber deck','Fourth-floor steel deck'],'primary_beam_location':'Fourth-floor floor / third-floor roof','levels_sheet_y':levels,'wall_profile':{'outward_step_mm':150,'small_step_count':3,'location':'Lower plinth below lowest arched openings','courses_per_step':20,'base_return_mm':300,'vertical_step_positions':'Course-based; visual/NTS pitch only, not surveyed heights'},'base_external_width_mm':8000,'base_wall_mm':1400,'first_floor_wall_approx_mm':[550,600],'model_nominal_shaft_wall_mm':650,'no_cumulative_AGL_levels_inferred':True},indent=2)+'\n')
picture('7145-tower-view',(167,28,244,151))
caption(169,160,2,'Tower','3D NTS',157)
project=picture('7145-fourth-floor-interior',(167,172,329,263))
par=json.loads((B/'parameters.json').read_text());level=par['primary_beam_top']
a=project(0,5200,level);b=project(0,5200,level+3700)
vdim(a,b,min(a[0],b[0])-5,'3700')
q=project(1600,5200,level+3900);text(q[0],q[1]+.7,'Brickwork',1.75,True,align='center')
q=project(2600,5200,level+1800);text(q[0],q[1],'Former water tank',1.9,True,align='center')
caption(23,274,1,'Sectional Elevation','NTS',141);caption(168,274,3,'Fourth-Floor Interior','3D NTS',160);flush()

from ezdxf.addons import Importer
for n,title in enumerate(['Roof Support Layout','Elevation and 3D Views'],1):
 lay=cad.layouts.new(f'0{n} '+title);lay.page_setup(size=(420,297),margins=(0,0,0,0),units='mm');lay.add_blockref(f'SHEET_0{n}',(0,0));cad.modelspace().add_blockref(f'SHEET_0{n}',((n-1)*450,0))
 single=fitz.open();single.insert_pdf(doc,from_page=n-1,to_page=n-1);single.save(O/f'7145-0{n}.pdf',garbage=4,deflate=True)
 # Standalone sheets maintain IMAGEDEF relative filenames and editable entities.
 c=ezdxf.new('R2000');c.units=4;imp=Importer(cad,c);imp.import_block(f'SHEET_0{n}',rename=False);imp.finalize();c.modelspace().add_blockref(f'SHEET_0{n}',(0,0));la=c.layouts.new(title);la.page_setup(size=(420,297),margins=(0,0,0,0),units='mm');la.add_blockref(f'SHEET_0{n}',(0,0));c.layouts.delete('Layout1')
 if n==2:
  for oldim in cad.blocks['SHEET_02'].query('IMAGE'):
   idef=oldim.image_def;pix=tuple(oldim.dxf.image_size);newdef=c.add_image_def(filename=idef.dxf.filename,size_in_pixel=pix);c.blocks['SHEET_02'].add_image(newdef,tuple(oldim.dxf.insert), (oldim.dxf.u_pixel.magnitude*pix[0],oldim.dxf.v_pixel.magnitude*pix[1]))
 assert not c.audit().errors
 c.saveas(O/f'7145-0{n}.dxf')
 if n==2:
  # ezdxf Importer does not import IMAGE resources; full set retains them and standalone has vector view edges.
  pass
if 'Layout1' in cad.layouts.names():cad.layouts.delete('Layout1')
assert not cad.audit().errors
cad.saveas(O/'7145-drawing-set.dxf');doc.set_metadata({'title':'7145 Saffron Walden Tower - Review','author':'AT','subject':'Roof support with scan marker; dimensioned elevation and 3D; Rev 1'});doc.save(O/'7145-review-drawing-set.pdf',garbage=4,deflate=True)
for i,pg in enumerate(doc,1):pg.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(O/f'7145-sheet-{i:02}.png')
print('Two A3 review sheets generated',flush=True)
