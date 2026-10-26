"""7068: model-derived A3 plans, elevations and technical 3D review sheets."""
from pathlib import Path
import json,math,textwrap,fitz,ezdxf,numpy as np
from ezdxf.enums import TextEntityAlignment
from PIL import Image
P=Path(__file__).parent;O=P/'drawings';W=P/'interpretation';B=P/'items/water-tower-01/outputs';O.mkdir(exist_ok=True)
PAR=json.loads((B/'parameters.json').read_text());PT=72/25.4;doc=fitz.open();cad=ezdxf.new('R2000');cad.units=4
for name in ['SHEET','TEXT','DIMENSIONS','GEOMETRY','BRANDING','SCHEMATIC']:cad.layers.new(name,dxfattribs={'color':7})
TEXT_QUEUE=[]
def cv(p):return(p[0]*PT,p[1]*PT)
def dv(p):return(p[0],297-p[1])
def line(a,b,w=.18,layer='SHEET',gray=0,dash=False):
 pg.draw_line(cv(a),cv(b),color=(gray,)*3,width=w*PT,dashes='[5 3] 0' if dash else None)
 attrs={'layer':layer,'lineweight':int(round(w*100)),'true_color':ezdxf.colors.rgb2int((int(gray*255),)*3)}
 ms.add_line(dv(a),dv(b),dxfattribs=attrs)
def rect(x,y,w,h,lw=.18,layer='SHEET',fill=False):
 pts=[(x,y),(x+w,y),(x+w,y+h),(x,y+h)]
 for a,b in zip(pts,pts[1:]+pts[:1]):line(a,b,lw,layer)
 if fill:
  pg.draw_rect(fitz.Rect(x*PT,y*PT,(x+w)*PT,(y+h)*PT),color=None,fill=(0,0,0));ms.add_solid([dv(p) for p in [pts[0],pts[1],pts[3],pts[2]]],dxfattribs={'layer':layer})
def text(x,y,s,h=2.2,bold=False,align='left',layer='TEXT',angle=0):TEXT_QUEUE.append((x,y,str(s),h,bold,align,layer,angle))
def circle(c,r,w=.2,layer='GEOMETRY'):
 pg.draw_circle(cv(c),r*PT,color=(0,0,0),width=w*PT);ms.add_circle(dv(c),r,dxfattribs={'layer':layer,'lineweight':int(w*100)})
def wrap(x,y,s,widthchars=44,h=2.05):
 for row in textwrap.wrap(s,widthchars):text(x,y,row,h);y+=h*1.4
 return y

def finish_text():
 # Actual CAD line gaps avoid unreliable white-mask conversion to DWG.
 bounds_all=[]
 for x,y,s,h,bold,align,layer,angle in TEXT_QUEUE:
  width=fitz.get_text_length(s,fontname='hebo' if bold else 'helv',fontsize=h*PT)/PT
  left=x-(width/2 if align=='center' else width if align=='right' else 0)
  bounds_all.append((x-h*1.08-.1,y-width/2-.4,x+.25,y+width/2+.4) if angle==90 else (left-.4,y-h*1.08-.1,left+width+.4,y+.25))
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
  a=(e.dxf.start.x,297-e.dxf.start.y);b=(e.dxf.end.x,297-e.dxf.end.y)
  xmin,xmax=sorted([a[0],b[0]]);ymin,ymax=sorted([a[1],b[1]])
  ranges=[]
  for r in bounds_all:
   if r[2]<xmin or r[0]>xmax or r[3]<ymin or r[1]>ymax:continue
   hit=interval(a,b,r)
   if hit and hit[1]-hit[0]>1e-9:ranges.append(hit)
  if not ranges:continue
  merged=[]
  for lo,hi in sorted(ranges):
   if merged and lo<=merged[-1][1]:merged[-1][1]=max(hi,merged[-1][1])
   else:merged.append([lo,hi])
  attrs=e.dxf.all_existing_dxf_attribs();attrs={k:v for k,v in attrs.items() if k not in ['handle','owner','start','end']}
  cursor=0.;kept=[]
  for lo,hi in merged:
   if lo>cursor+1e-8:kept.append((cursor,lo))
   cursor=max(cursor,hi)
  if cursor<1-1e-8:kept.append((cursor,1.))
  ms.delete_entity(e)
  for lo,hi in kept:
   aa=(a[0]+(b[0]-a[0])*lo,a[1]+(b[1]-a[1])*lo);bb=(a[0]+(b[0]-a[0])*hi,a[1]+(b[1]-a[1])*hi)
   ms.add_line(dv(aa),dv(bb),dxfattribs=attrs)
 # PDF clearances remain white; CAD geometry already has corresponding gaps.
 for x,y,s,h,bold,align,layer,angle in TEXT_QUEUE:
  width=fitz.get_text_length(s,fontname='hebo' if bold else 'helv',fontsize=h*PT)/PT
  left=x-(width/2 if align=='center' else width if align=='right' else 0)
  bounds=(x-h*1.08-.1,y-width/2-.4,x+.25,y+width/2+.4) if angle==90 else (left-.4,y-h*1.08-.1,left+width+.4,y+.25)
  pg.draw_rect(fitz.Rect(*(v*PT for v in bounds)),color=None,fill=(1,1,1))
  x0,y0,x1,y1=bounds
  pg.insert_text((x*PT,(y+width/2)*PT) if angle==90 else (left*PT,y*PT),s,fontname='hebo' if bold else 'helv',fontsize=h*PT,color=(0,0,0),rotate=angle)
  t=ms.add_text(s,dxfattribs={'height':h,'layer':layer,'style':'Standard','rotation':angle})
  t.set_placement(dv((x,y)),align={'left':TextEntityAlignment.LEFT,'center':TextEntityAlignment.CENTER,'right':TextEntityAlignment.RIGHT}[align])
def logo(path,area,rotate=0):
 x,y,w,h=area;im=Image.open(path).convert('RGB')
 if rotate:im=im.rotate(rotate,expand=True)
 im.thumbnail((180,100));iw,ih=im.size;sc=min(w/iw,h/ih);ox=x+(w-iw*sc)/2;oy=y+(h-ih*sc)/2
 # PDF uses original source pixels; CAD scan strips keep branding self-contained.
 pg.insert_image(fitz.Rect(x*PT,y*PT,(x+w)*PT,(y+h)*PT),filename=str(path),rotate=rotate,keep_proportion=True)
 for yy in range(ih):
  xx=0
  while xx<iw:
   rgb=im.getpixel((xx,yy));q=tuple((v//48)*48 for v in rgb)
   if min(rgb)>220:xx+=1;continue
   end=xx+1
   while end<iw and tuple((v//48)*48 for v in im.getpixel((end,yy)))==q:end+=1
   x0,y0=ox+xx*sc,oy+yy*sc;x1,y1=ox+end*sc,y0+sc
   ms.add_solid([dv(t) for t in [(x0,y0),(x1,y0),(x0,y1),(x1,y1)]],dxfattribs={'layer':'BRANDING','true_color':ezdxf.colors.rgb2int(q)});xx=end

def frame(number,title,scale):
 rect(5,7,410,283);rect(15,20,316,260);line((342,7),(342,290));line((342,15),(415,15));text(345,12,'ALL DIMENSIONS IN mm; LEVELS IN m AGL',1.95,bold=True)
 text(345,23,'DRAWING NOTES',2.5,True);y=30
 notes=['1. Eight equal sectors adopted from the survey and agreed diameter derivation. Dimensions derived from approximate readings are marked approx.',
 '2. Main roof +22.00; top of core +23.90. Approximate vertical survey chain totals 21.75; confirmed roof level governs.',
 '3. Telecoms shown as existing. All external antenna mounting assemblies connect at bottom ring and top lid/parapet. Brackets schematic.',
 '4. Parapet: 120 lower + 90 upper = 210 high. Width, core-cap projection/thickness and roof equipment sizes schematic.',
 '5. Tank wall/floor thickness, foundations, reinforcement and concealed connections not established. External geometry only.']
 for s in notes:y=wrap(345,y,s,43,1.9)+2.2
 text(345,139,'MEMBER / LEVEL KEY',2.4,True)
 for yy,s in [(145,'Columns: 600 x 600'),(150,'Inner column projection: 250 radial'),(155,'Radial beams: 200 x 450 (survey)'),(160,'Bottom ring: 900 high x 600 radial')]:text(345,yy,s,1.95)
 for yy in [166,173,185,212,235,251,267,279,290]:line((342,yy),(415,yy))
 for xx in [351,376,386,396]:line((xx,166),(xx,185))
 for xx,s in [(344,'Rev'),(353,'Issue'),(378,'Drawn'),(388,'Chkd'),(398,'Date')]:text(xx,171,s,1.65)
 for xx,s in [(344,'1'),(353,'REVIEW'),(378,'ST'),(388,'AF'),(398,'26-10-26')]:text(xx,180,s,1.8)
 text(345,190,'Consultant:',1.9);logo(Path('assets/branding/ka-logo-survey-source.jpeg'),(357,192,43,18))
 text(345,217,'Client:',1.9);logo(Path('assets/branding/jet-logo-ga-source.jpeg'),(349,220,59,12),90)
 text(345,240,'Drawing Title:',1.9);text(345,247,title,2.5,True)
 text(345,256,'SOUTH WATER TOWER',2.25,True);text(345,261,'SOUTH ROAD, BECCLES, NORFOLK',1.9);text(345,265,'NR34 9NZ',1.9)
 text(345,272,'Drawn: ST    Checked: AF',2);text(345,277,scale,2)
 text(345,284,'Project: 7068',2.25);text(380,284,f'Dwg: 7068-0{number}',2.15);text(345,288,'Revision: 1',2)

def projection(name,cx,cy,S=None,area=None,shaded=False):
 d=json.loads((B/f'{name}-projection.json').read_text());size=np.array(d['size']);sc=d['scale'];lo=np.array(d['lo']);off=np.array(d['offset']);right=np.array(d['right']);up=np.array(d['up'])
 uv0=(np.array([0,0])-lo)*sc+off;uv0[1]=size[1]-uv0[1]
 if area is None:
  wh=size/sc/S;xy=np.array([cx,cy])-uv0/sc/S
 else:
  x,y,w,h=area;wh=size*min(w/size[0],h/size[1]);xy=np.array([x+(w-wh[0])/2,y+(h-wh[1])/2])
 if shaded:pg.insert_image(fitz.Rect(*(np.r_[xy,xy+wh]*PT)),filename=str(B/f'{name}.png'))
 shape=pg.new_shape()
 for a,b in d['edges']:
  aa=xy+np.array(a)*wh;bb=xy+np.array(b)*wh
  if not shaded:shape.draw_line(cv(aa),cv(bb))
  ms.add_line(dv(aa),dv(bb),dxfattribs={'layer':'GEOMETRY','lineweight':13})
 if not shaded:shape.finish(color=(0,0,0),width=.13*PT);shape.commit()
 def world(p):
  uv=(np.array([np.dot(p,right),np.dot(p,up)])-lo)*sc+off;uv[1]=size[1]-uv[1];return xy+uv/size*wh
 return world

def arrow(p,v):
 p=np.array(p);v=np.array(v);v=v/np.linalg.norm(v);t=np.array([-v[1],v[0]])
 for side in [-1,1]:line(p,p+v*1.5+t*side*.45,.14,'DIMENSIONS')
def dim(a,b,offset,label,angle=0):
 a,b=np.array(a),np.array(b);u=b-a;u=u/np.linalg.norm(u);n=np.array([-u[1],u[0]]);aa=a+n*offset;bb=b+n*offset
 for p,q in [(a,aa),(b,bb)]:line(p+n*np.sign(offset)*.7,q+n*np.sign(offset)*1.5,.10,'DIMENSIONS')
 line(aa,bb,.13,'DIMENSIONS');arrow(aa,u);arrow(bb,-u);mid=(aa+bb)/2
 if angle==90:text(mid[0]-1.2,mid[1],label,2.05,align='center',layer='DIMENSIONS',angle=90)
 else:text(mid[0],mid[1]-1.1,label,2.05,align='center',layer='DIMENSIONS')
def leader(p,elbow,end,label):
 line(p,elbow,.12,'DIMENSIONS');line(elbow,end,.12,'DIMENSIONS');arrow(p,np.array(elbow)-p);text(end[0],end[1]-1,label,2.05)
def caption(x,y,n,title,sub,w=100):
 circle((x+2.1,y),2.1,.18,'SHEET');text(x+2.1,y+.75,n,2,align='center');line((x+4.3,y),(x+w,y),.18)
 text(x+7,y-1.3,title,2.5,True);text(x+7,y+3.4,sub,1.9)
def north(x,y):
 circle((x,y),4,.13);line((x,y+6),(x,y-8),.18);arrow((x,y-8),(0,1));text(x,y-10,'N',2.3,True,align='center')

def new_sheet(number,title,scale):
 global pg,ms,TEXT_QUEUE
 TEXT_QUEUE=[];pg=doc.new_page(width=420*PT,height=297*PT);ms=cad.blocks.new(f'SHEET_0{number}');frame(number,title,scale)
R=PAR['outside_diameter']/2;RC=PAR['core_diameter']/2;RI=PAR['inner_face_diameter']/2
# Plan sheet: roof equipment and separate support arrangement expose different levels.
new_sheet(1,'Water Tower - Plans','Plans 1:100 at A3')
roof=projection('roof-plan',92,109,100);supp=projection('support-plan',252,109,100)
north(28,34);north(190,34)
dim(roof((-R,0,22000)),roof((R,0,22000)),81,'13482 approx. - OUTSIDE DIA.')
# Dashed core wall below its overhanging cap, exact radius from shared parameters.
for i in range(48):
 a=2*math.pi*i/48;b=a+math.pi/48
 line(roof((RC*math.cos(a),RC*math.sin(a),22000)),roof((RC*math.cos(b),RC*math.sin(b),22000)),.12,'GEOMETRY')
leader(roof((RC/math.sqrt(2),RC/math.sqrt(2),22000)),(131,74),(133,74),'Core dia. 3882 approx.')
caption(24,201,1,'Roof Plan','1 : 100 | Existing telecom arrangement',141)
caption(184,201,2,'Support Arrangement','1 : 100 | Tank and lid omitted to show framing',141)
# Column cut footprints extracted from the actual shared mesh, not hidden by ring top.
mesh=json.loads((B/'mesh.json').read_text())
for k in range(1,9):
 for ids,g in zip(mesh['faces'],mesh['groups']):
  if g==f'perimeter_column_{k}':
   pp=np.array([mesh['vertices'][i-1] for i in ids])
   if np.allclose(pp[:,2],15600):
    for a,b in zip(pp,np.roll(pp,-1,axis=0)):line(supp(a),supp(b),.3,'GEOMETRY')
leader(supp((RI*math.cos(math.pi/8),-RI*math.sin(math.pi/8),15600)),(298,151),(298,151),'600 x 600 typical')
# chord centre points on adjacent inner faces, per user's specified conversion.
a=np.array([-RI*math.sin(math.pi/8),RI*math.cos(math.pi/8),15600]);b=np.array([RI*math.sin(math.pi/8),RI*math.cos(math.pi/8),15600]);dim(supp(a),supp(b),-12,'4700 - INNER-FACE CENTRES')
leader(supp((0,0,15600)),(277,126),(280,126),'Core dia. 3882 approx.')
# radial depth chain follows column station at 22.5deg; annotate exact selected geometry.
a=math.radians(22.5);n=np.array([math.cos(a),math.sin(a),0]);p1=supp(n*RC);p2=supp(n*R);dim(p1,p2,10,'4800 approx.')
text(26,220,'DIMENSION BASIS',2.5,True)
for i,s in enumerate(['Inner-face chord: 4100 clear + 600 column width = 4700 (engineer convention).',
 'Inner-face circle dia. = 4700 / sin 22.5 deg = 12282 approx.; column PCD = 12882 approx.',
 'Outside dia. = 12282 + 2 x 600 = 13482 approx.; core dia. = 13482 - 2 x 4800 = 3882 approx.',
 'Radial clear gap derives as 3950; survey reads 3900. Difference retained as rounding, not a new measured value.']):text(26,227+i*5.3,s,2.1)
text(26,254,'SUPPORT DETAILS',2.5,True)
text(26,261,'8 columns 600 x 600; inner projections 250 radial; radial members 200 x 450; bottom ring 900 high x 600 radial.',2.05)
text(26,267,'Roof slab 150 thick. Inner projection width 450 shown schematically; exact hidden connections not surveyed.',2.05)
finish_text()
# Elevations and overall render, same model geometry and common ground datum.
new_sheet(2,'Water Tower - Elevations / 3D','Elevations 1:150 at A3 / 3D NTS')
south=projection('south-elevation',69,242,150);east=projection('east-elevation',173,242,150)
projection('tower-3d',0,0,area=(233,42,96,205),shaded=True)
for project,cx in [(south,69),(east,173)]:
 p=project((-R,0,0)) if project is south else project((0,-R,0));q=project((R,0,0)) if project is south else project((0,R,0));line((cx-48,242),(cx+48,242),.16,'GEOMETRY')
 # Short datum ticks and labels in each view, positioned clear of the model.
 for zz,label in [(0,'0.000'),(15600,'+15.600'),(16500,'+16.500'),(22000,'+22.000'),(23900,'+23.900')]:
  y=242-zz/150;line((cx-48,y),(cx-43,y),.12,'DIMENSIONS');text(cx-48,y-1,label,1.8)
# Dimension actual levels, keeping vertical labels parallel to their lines.
dim(south((R,0,16500)),south((R,0,22000)),8,'5500 adopted',90)
dim(east((0,RC,22000)),east((0,RC,23900)),32,'1900',90)
caption(23,256,1,'South Elevation','1 : 150 | Doorway side; roof door schematic',92)
caption(127,256,2,'East Elevation','1 : 150 | GA orientation',92)
caption(237,256,3,'3D View','NTS | Model for review / approval',88)
# Ring/body/lid level dimensions use identified faces, not canopy tops.
dim(south((-R,0,0)),south((-R,0,15600)),-10,'15600',90)
text(25,274,'Tank lid +22.00 m controls model; 5.25 m survey height is approximate. Parapet top +22.210 m.',2)
finish_text()
# Two independent paper sheets, full-size model in mm as an uninserted editable surface block.
old=cad.layouts.names()[1:]
for i,name in enumerate(['01 Plans','02 Elevations and 3D'],1):
 lay=cad.layouts.new(name);lay.page_setup(size=(420,297),margins=(0,0,0,0),units='mm');lay.add_blockref(f'SHEET_0{i}',(0,0))
 cad.modelspace().add_blockref(f'SHEET_0{i}',((i-1)*450,0))
for name in old:cad.layouts.delete(name)
mesh=json.loads((B/'mesh.json').read_text());blk=cad.blocks.new('TOWER_SURFACE_MM')
for face_ids in mesh['faces']:
 pts=[mesh['vertices'][i-1] for i in face_ids]
 if len(pts)<=4:blk.add_3dface(pts,dxfattribs={'layer':'GEOMETRY'})
 else:
  for j in range(1,len(pts)-1):blk.add_3dface([pts[0],pts[j],pts[j+1]],dxfattribs={'layer':'GEOMETRY'})
assert not cad.audit().errors
cad.saveas(W/'7068-south-water-tower-review.dxf');doc.save(O/'7068-south-water-tower-review.pdf',garbage=4,deflate=True);doc.close()
doc=fitz.open(O/'7068-south-water-tower-review.pdf')
for i,pg in enumerate(doc):pg.get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False).save(O/f'7068-sheet-{i+1:02}.png')
print('Two A3 sheets; plan/elevations/3D from common model; revision 1 ST/AF.')
