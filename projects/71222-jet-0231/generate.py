"""71222 Jet0231: roof-support review and theatre visual model sheets."""
from pathlib import Path
import json,math,textwrap,shutil
import fitz,ezdxf,numpy as np
from ezdxf.enums import TextEntityAlignment
P=Path(__file__).resolve().parent;O=P/'drawings';B=P/'model';PT=72/25.4
doc=fitz.open();cad=ezdxf.new('R2000');cad.units=4;cad.set_raster_variables(frame=0)
for layer in ['FRAME','TEXT','DIMENSIONS','EXISTING','PROPOSED','LOAD_BEARING_WALLS','OVERHANG_SUPPORT','BEAMS','PHOTO_COLUMNS','IMAGES','EMBEDDED_BEAMS','ROOF_MEMBERS','SCAN_SYMBOLS','STEEL_FLOOR','TIMBER_DECK','ELEVATION','CASTELLATED','I_BEAMS','B2_BEAMS','CHS_BRACES','PV','ROOF_OPENINGS','REFERENCE','FULL_WEB','SAFETY','PARAPET']:cad.layers.new(layer,dxfattribs={'color':7})
# Distinct member patterns are encoded identically in PDF and native CAD.
STYLES={'CASTELLATED':(.50,0.,(8.,2.2),'CB_LONG_DASH'),'CHS_BRACES':(.30,0.,(5.,1.,.5,1.),'CHS_DASH_DOT'),'FULL_WEB':(.80,0.,None,'Continuous'),'I_BEAMS':(.35,0.,None,'Continuous'),'B2_BEAMS':(.40,0.,(2.,1.2),'B2_SHORT_DASH'),'SAFETY':(.28,0.,(2.,1.,.4,1.,.4,1.),'SAFETY_CHAIN_2'),'PV':(.18,.4,None,'Continuous'),'ROOF_OPENINGS':(.30,0.,None,'Continuous'),'PARAPET':(.50,0.,None,'Continuous')}
for name,pattern in [('B2_SHORT_DASH',(2.,1.2)),('DASHED_REVIEW',(2.5,1.5)),('CB_LONG_DASH',(8.,2.2)),('CHS_DASH_DOT',(5.,1.,.5,1.)),('SAFETY_CHAIN_2',(2.,1.,.4,1.,.4,1.))]:
 signed=[v if i%2==0 else -v for i,v in enumerate(pattern)];cad.linetypes.new(name,dxfattribs={'pattern':[sum(pattern)]+signed})
queue=[];pdf_lines={};BEAM_SEGMENTS=[]
def line(a,b,w=.18,layer='FRAME',gray=0,dash=False):
 a=np.array(a,dtype=float);b=np.array(b,dtype=float)
 pattern=(2.5,1.5) if dash else None;lt='DASHED_REVIEW' if dash else 'Continuous'
 if layer in STYLES:w,gray,pattern,lt=STYLES[layer]
 pdf_lines.setdefault((w,gray,pattern),[]).append((a,b))
 ms.add_line((a[0],297-a[1]),(b[0],297-b[1]),dxfattribs={'layer':layer,'lineweight':round(w*100),'true_color':ezdxf.colors.rgb2int((int(gray*255),)*3),'color':8 if layer=='PV' else 254 if gray>=.5 else 250 if gray>0 else 7,'linetype':lt})
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
 for (w,gray,pattern),segments in pdf_lines.items():
  shape=pg.new_shape()
  for a,b in segments:shape.draw_line(tuple(a*PT),tuple(b*PT))
  shape.finish(color=(gray,)*3,width=w*PT,dashes=('['+' '.join(str(x*PT) for x in pattern)+'] 0') if pattern else None,closePath=False);shape.commit()
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

A=json.loads((P/'interpretation/parameters.json').read_text());W=A['width_mm'];L=A['nominal_depth_mm'];MAIN=A['main_depth_mm'];SCALE=.012
PLAN_ORIGIN=(38.,75.)
loc=lambda x,y:np.array([PLAN_ORIGIN[0]+x*SCALE,PLAN_ORIGIN[1]+(L-y)*SCALE])

def frame(n,title):
 global pg,ms
 pg=doc.new_page(width=420*PT,height=297*PT);ms=cad.blocks.new(f'SHEET_0{n}')
 rect(5,5,410,287,.35);rect(15,20,320,261,.22);line((341,5),(341,292),.3)
 text(344,10,'DIMENSIONS IN mm',1.8,True);line((341,13),(415,13),.18)
 text(345,23,'DRAWING NOTES',2.55,True)
 notes={2:[],1:['Metal deck roof; existing PV arrays in three rows.','Nominal overall depth includes the corridor strip.','Castellated beams 800 deep; flange 210 wide x 18 thick.','Equipment set-out is shown on sheet 71222-02.','CHS: upper in left diagonal bay; lower in central bays. Right bay: I-beams only.'],3:['Raised timber-clad fly tower is the roof in scope.','Surrounding theatre is visual context; building heights unmeasured.','Lower view omits roof decking and PV arrays to expose supports.','Fly-system bars, pulleys and cables are excluded from roof-support members.']}[n]
 if n==2:notes=['Existing PV arrays in three rows.','Hatch/skylight upstands: 1300 x 1300 x 300 high.','Safety line set back 1500 from building edge; parapet 300 x 300.','Setbacks are to outside building edges; opening gaps are face to face.']
 y=31
 for i,t in enumerate(notes,1):y=wrap(345,y,str(i)+'. '+t,n=42,h=1.95)+2
 text(345,101,'MEMBER KEY' if n==1 else 'ROOF KEY' if n==2 else 'VIEW KEY',2.5,True)
 if n==1:
  for yy,kind,spec,layer in [(110,'CB','800 deep; flange 210 x 18','CASTELLATED'),(120,'B1','I-beam 200 x 250','I_BEAMS'),(130,'B2','I-beam 200 x 150','B2_BEAMS'),(140,'CHS','90 dia; levels per note 5','CHS_BRACES'),(150,'FW','Full-web end beam','FULL_WEB')]:
   if layer in ['I_BEAMS','B2_BEAMS','CASTELLATED']:
    for dy in [-.55,.55]:line((345,yy-1+dy),(361,yy-1+dy),.35,layer)
   else:line((345,yy-1),(361,yy-1),.35,layer)
   text(364,yy,kind+'  '+spec,1.8)
 elif n==2:
  for yy,t,layer in [(111,'PV arrays','PV'),(121,'Safety line','SAFETY'),(131,'Parapet','PARAPET'),(141,'H hatch / SL skylight','ROOF_OPENINGS')]:line((345,yy-1),(361,yy-1),.25,layer);text(364,yy,t,1.9)

 else:
  for yy,t in [(111,'Brown: timber-clad fly tower'),(121,'Blue-grey: existing PV arrays'),(131,'White/grey: roof steel'),(141,'Roof openings: hatch / skylights'),(151,'CHS upper left / lower centre')]:text(345,yy,t,1.9)
 for yy in [162,171,184,211,237,255,272,282]:line((341,yy),(415,yy),.2)
 for xx in [353,378,391,402]:line((xx,162),(xx,184),.15)
 for xx,t in [(344,'Rev'),(355,'Issue'),(380,'Drawn'),(393,'Chkd'),(404,'Date')]:text(xx,168,t,1.65)
 for xx,t in [(344,'1'),(355,'REVIEW'),(380,'S.T.'),(393,'K.S.'),(403,'08-11-26')]:text(xx,179,t,1.7)
 text(345,190,'Consultant:',1.8);logo(Path('assets/branding/ka-logo-survey-source.jpeg'),(357,192,43,17))
 text(345,217,'Client:',1.9);text(378,229,'Jansen SL',4,True,align='center')
 text(345,243,'Drawing Title:',1.8);text(345,250,title,2.4,True)
 text(345,261,'JET 0231',3,True);text(345,266,'Gala Theatre & Cinema',2);text(345,270,'Millennium Square, Durham',1.8)
 text(345,278,'Drawn: S.T.    Checked: K.S.',1.95);text(345,287,'71222-0'+str(n)+'  |  Rev 1',2.2,True);text(409,287,'NTS',1.8,align='right')

def north(x,y):
 a=math.radians(A['north_from_local_y_deg']);v=np.array([math.sin(a),-math.cos(a)]);u=np.array([-v[1],v[0]]);c=np.array([x,y]);tip=c+v*9
 line(c-v*7,tip,.25);line(c-u*4,c+u*4,.15)
 pg.draw_circle(tuple(c*PT),3.2*PT,color=(0,0,0),width=.4);ms.add_circle((x,297-y),3.2,dxfattribs={'layer':'FRAME'})
 line(tip,tip-v*2+u*.7,.2);line(tip,tip-v*2-u*.7,.2);t=tip+v*3;text(t[0],t[1]+.6,'N',2.4,True,align='center')

def polygon(pts,w=.18,layer='EXISTING',gray=0,dash=False):
 for a,b in zip(pts,pts[1:]+pts[:1]):line(a,b,w,layer,gray,dash)

frame(1,'Roof Support Layout')
polygon([loc(0,0),loc(W,0),loc(W,L),loc(0,L)],.65,'EXISTING')
line(loc(0,MAIN),loc(W,MAIN),.30,'REFERENCE');q=loc(5700,12100);text(q[0],q[1]+.7,'CORRIDOR (included)',2.1,True,align='center')
# Main-space steel set-out; castellated spacing is engineer-confirmed 3000 c/c.
for x in A['castellated_axes_x_mm']:
 for dx in [-105,105]:line(loc(x+dx,0),loc(x+dx,MAIN),.45,'CASTELLATED',dash=True)
for y in [0,MAIN]:line(loc(0,y),loc(20800,y),.42,'I_BEAMS')
for dx in [-65,65]:line(loc(dx,0),loc(dx,MAIN),.35,'I_BEAMS')
for x in A['B2_axes_x_mm']:
 for dx in [-75,75]:line(loc(x+dx,0),loc(x+dx,MAIN),.40,'B2_BEAMS')
line(loc(20800,0),loc(20800,MAIN),.75,'FULL_WEB')
for y in A['secondary_axes_y_mm']:line(loc(0,y),loc(16700,y),.25,'CHS_BRACES')
# Paired continuous B1flanges below the chain-dot upperCHS, sharing their plan stations.
for y in A['lower_B1_west_y_mm']:
 for dy in [-65,65]:line(loc(0,y+dy),loc(4700,y+dy),.35,'I_BEAMS')
for y in A['lower_B1_east_y_mm']:
 for dy in [-65,65]:line(loc(16700,y+dy),loc(20800,y+dy),.35,'I_BEAMS')
for a,b in [((0,MAIN),(4700,8900)),((0,5400),(4700,8900)),((0,5400),(4700,1900)),((0,0),(4700,1900))]:line(loc(*a),loc(*b),.27,'CHS_BRACES')
for y in [0,5400,MAIN]:
 q=loc(0,y);rect(q[0]-1.3,q[1]-1.3,2.6,2.6,.4)
# Written dimensions: no values derived by measuring the screenshot.
dim(loc(0,L),loc(W,L),-17,'21300')
vdim(loc(0,L),loc(0,0),22,'12500')
for y0,y1,label in [(8900,10600,'1700'),(7150,8900,'1750'),(5400,7150,'1750'),(3650,5400,'1750'),(1900,3650,'1750'),(0,1900,'1900')]:vdim(loc(0,y0),loc(0,y1),29,label)
vdim(loc(W,MAIN),loc(W,L),309,'1900');vdim(loc(W,0),loc(W,MAIN),309,'10600')
for x0,x1,label in [(0,2200,'2200'),(2200,4700,'2500'),(4700,7700,'3000'),(7700,10700,'3000'),(10700,13700,'3000'),(13700,16700,'3000'),(16700,19200,'2500'),(19200,20500,'1300'),(20500,20800,'300'),(20800,21300,'500')]:dim(loc(x0,0),loc(x1,0),13,label)

north(318,38);caption(23,274,1,'Roof Support Layout','NTS',304);flush()

# Dimensioned external equipment layout: same footprint and source parameter record.
frame(2,'Roof Equipment Layout');E=A['equipment'];ex0=E['outer_west_x_mm'];ex1=E['outer_east_x_mm'];EN=E['outer_north_y_mm'];loc=lambda x,y:np.array([PLAN_ORIGIN[0]+x*SCALE,PLAN_ORIGIN[1]+(EN-y)*SCALE])
polygon([loc(ex0,0),loc(ex1,0),loc(ex1,EN),loc(ex0,EN)],.45,'PARAPET')
polygon([loc(300,300),loc(W-300,300),loc(W-300,EN-300),loc(300,EN-300)],.35,'PARAPET')
for y0,y1 in E['PV_rows_north_to_south']:
 for j in range(12):
  xa=E['PV_x0_mm']+j*(E['PV_x1_mm']-E['PV_x0_mm'])/12;xb=E['PV_x0_mm']+(j+1)*(E['PV_x1_mm']-E['PV_x0_mm'])/12-(20 if j<11 else 0)
  polygon([loc(xa,y0),loc(xb,y0),loc(xb,y1),loc(xa,y1)],.13,'PV')
for x,y,w,h,kind in E['openings']:
 polygon([loc(x,y),loc(x+w,y),loc(x+w,y+h),loc(x,y+h)],.28,'ROOF_OPENINGS');q=loc(x+w/2,y+h/2);text(q[0],q[1]+.7,'H' if kind=='hatch' else 'SL',2,True,align='center')
for a,b in zip(E['safety_path_mm'],E['safety_path_mm'][1:]):line(loc(*a),loc(*b),.28,'SAFETY')
# Horizontal equipment face references; verified offsets from the external sketch.
dim(loc(ex0,1650),loc(E['PV_x0_mm'],1650),27,'3500')
dim(loc(E['PV_x1_mm'],1650),loc(ex1,1650),27,'2900')
dim(loc(ex0,EN),loc(E['openings'][0][0],EN),-29,'12800')
h1,h2=E['openings'][:2];dim(loc(h1[0]+1300,EN),loc(h2[0],EN),-17,'4000')
dim(loc(h2[0],EN),loc(ex1,EN),-41,'3200')
dim(loc(h1[0],h1[1]+1300),loc(h1[0]+1300,h1[1]+1300),-6,'1300')
vdim(loc(h1[0],h1[1]),loc(h1[0],h1[1]+1300),loc(h1[0],0)[0]-5,'1300')
# Safety setback at south and east edges; north shown to current outer-edge reference.
vdim(loc(5500,0),loc(5500,1500),loc(5500,0)[0],'1500')
dim(loc(ex1-1500,4400),loc(ex1,4400),0,'1500')
vdim(loc(15500,EN-1500),loc(15500,EN),loc(15500,0)[0],'1500')
vdim(loc(h1[0]-1800,h1[1]),loc(h1[0]-1800,EN),loc(h1[0]-1800,0)[0],'1500')
# Readable row widths and clear gaps from the supplied chain; final south gap remains a query.
for y0,y1,label in [(8550,10400,'1850'),(6600,8550,'1950'),(4900,6600,'1700'),(3550,4900,'1350'),(1650,3550,'1900'),(0,1650,'1650')]:vdim(loc(ex0,y0),loc(ex0,y1),24,label)
vdim(loc(ex0,10400),loc(ex0,EN),24,'2100')

q=loc(ex1,650);line(q,q+np.array([6,8]),.13);text(q[0]+7,q[1]+9,'Parapet 300 x 300',1.8,align='right')
text(39,255,'H/SL: 1300 x 1300 overall; upstand 300 high',2.1)
rect(282,246,8,8,.4);dim((282,246),(290,246),-5,'300');vdim((290,246),(290,254),297,'300');text(286,263,'Parapet section',1.9,align='center')
north(318,38);caption(23,274,1,'Roof Equipment Set-out','NTS',304);flush()

# Crop only blank margins; preserve full model geometry and project the matching CAD edges.
def picture(name,target):
 from PIL import Image,ImageChops
 src=B/(name+'.png');im=Image.open(src).convert('RGB');old=im.size;r=ImageChops.difference(im,Image.new('RGB',im.size,'white')).getbbox();r=(max(0,r[0]-3),max(0,r[1]-3),min(im.width,r[2]+3),min(im.height,r[3]+3));im=im.crop(r);im.save(O/src.name);size=im.size
 x0,y0,x1,y1=target;sc=min((x1-x0)/size[0],(y1-y0)/size[1]);w,h=np.array(size)*sc;x=x0+(x1-x0-w)/2;y=y0+(y1-y0-h)/2
 pg.insert_image(fitz.Rect(x*PT,y*PT,(x+w)*PT,(y+h)*PT),filename=str(O/src.name));idef=cad.add_image_def(filename=src.name,size_in_pixel=size);ms.add_image(idef,(x,297-y-h),(w,h))
 data=json.loads((B/(name+'-projection.json')).read_text())
 for a,b in data['edges']:
  aa=(np.array(a)*old-np.array(r[:2]))*sc+np.array([x,y]);bb=(np.array(b)*old-np.array(r[:2]))*sc+np.array([x,y]);ms.add_line((aa[0],297-aa[1]),(bb[0],297-bb[1]),dxfattribs={'layer':'EXISTING','color':250,'lineweight':9})

frame(3,'3D Building / Roof Supports')
picture('71222-theatre-context',(21,27,330,146));caption(23,153,1,'Theatre Context - Target Fly Tower','3D NTS',304)
picture('71222-roof-supports',(21,167,219,263));picture('71222-roof-arrangement',(224,172,330,256))
caption(23,274,2,'Roof Supports - CHS Levels by Bay','3D NTS',194);caption(224,274,3,'Existing Roof','3D NTS',105);flush()
from ezdxf.addons import Importer
for n,title in enumerate(['Roof Support Layout','Roof Equipment Layout','3D Building and Roof'],1):
 lay=cad.layouts.new(f'0{n} '+title);lay.page_setup(size=(420,297),margins=(0,0,0,0),units='mm');lay.add_blockref(f'SHEET_0{n}',(0,0));cad.modelspace().add_blockref(f'SHEET_0{n}',((n-1)*450,0))
 pdf=fitz.open();pdf.insert_pdf(doc,from_page=n-1,to_page=n-1);pdf.save(O/f'71222-0{n}.pdf',garbage=4,deflate=True)
 c=ezdxf.new('R2000');c.units=4;c.set_raster_variables(frame=0);imp=Importer(cad,c);imp.import_block(f'SHEET_0{n}',rename=False);imp.finalize();c.modelspace().add_blockref(f'SHEET_0{n}',(0,0));la=c.layouts.new(title);la.page_setup(size=(420,297),margins=(0,0,0,0),units='mm');la.add_blockref(f'SHEET_0{n}',(0,0));c.layouts.delete('Layout1')
 if n==3:
  for oldim in cad.blocks['SHEET_03'].query('IMAGE'):
   pix=tuple(oldim.dxf.image_size);newdef=c.add_image_def(filename=oldim.image_def.dxf.filename,size_in_pixel=pix);c.blocks['SHEET_03'].add_image(newdef,tuple(oldim.dxf.insert),(oldim.dxf.u_pixel.magnitude*pix[0],oldim.dxf.v_pixel.magnitude*pix[1]))
 assert not c.audit().errors;c.saveas(O/f'71222-0{n}.dxf')
if 'Layout1' in cad.layouts.names():cad.layouts.delete('Layout1')
assert not cad.audit().errors;cad.saveas(O/'71222-drawing-set.dxf');doc.set_metadata({'title':'71222 Jet 0231 - Roof Support Review','author':'S.T.','subject':'Jansen SL; K.S.; revision 1; raised theatre fly-tower roof'});doc.save(O/'71222-review-drawing-set.pdf',garbage=4,deflate=True)
for i,pg in enumerate(doc,1):pg.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(O/f'71222-sheet-{i:02}.png')
print('Three A3 support/equipment/3D review sheets generated',flush=True)
