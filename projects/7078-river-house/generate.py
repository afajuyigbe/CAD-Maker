"""River House review sheet. Written survey values; GA graphic fit is not measurement."""
from pathlib import Path
import json,math,fitz,numpy as np,ezdxf
from ezdxf.enums import TextEntityAlignment
from PIL import Image
P=Path(__file__).parent;O=P/'drawings';W=P/'interpretation';O.mkdir(exist_ok=True)
PT=72/25.4;doc=fitz.open();pg=doc.new_page(width=420*PT,height=297*PT)
cad=ezdxf.new('R2000');cad.units=4;ms=cad.modelspace()
for name,col in [('GA_REFERENCE',253),('MAIN_ROOF',7),('UPPER_ROOF',7),('COLUMNS',7),('DIMENSIONS',7),('TEXT',7),('SHEET',7),('BRANDING',7)]:cad.layers.new(name,dxfattribs={'color':col})
if 'UPPER' not in cad.linetypes:cad.linetypes.new('UPPER',dxfattribs={'description':'Upper level framing','pattern':[3,2,-1]})
def cv(p):return (p[0]*PT,p[1]*PT)
def dv(p):return (p[0],297-p[1])
def line(a,b,w=.18,layer='SHEET',gray=0,dash=False):
 pg.draw_line(cv(a),cv(b),color=(gray,)*3,width=w*PT,dashes='[5.67 2.835] 0' if dash else None)
 attrs={'layer':layer,'lineweight':int(round(w*100)),'true_color':ezdxf.colors.rgb2int((int(gray*255),)*3)}
 if dash:attrs['linetype']='UPPER'
 ms.add_line(dv(a),dv(b),dxfattribs=attrs)
def rect(x,y,w,h,lw=.18,layer='SHEET',fill=False):
 pts=[(x,y),(x+w,y),(x+w,y+h),(x,y+h)]
 for a,b in zip(pts,pts[1:]+pts[:1]):line(a,b,lw,layer)
 if fill:
  pg.draw_rect(fitz.Rect(x*PT,y*PT,(x+w)*PT,(y+h)*PT),color=None,fill=(0,0,0))
  ms.add_solid([dv(p) for p in [pts[0],pts[1],pts[3],pts[2]]],dxfattribs={'layer':layer})
def text(x,y,s,h=2.2,bold=False,align='left',layer='TEXT'):
 # Baseline text, same positions/height in PDF and editable DXF.
 width=fitz.get_text_length(s,fontname='hebo' if bold else 'helv',fontsize=h*PT)
 px=x*PT-(width/2 if align=='center' else width if align=='right' else 0)
 pg.insert_text((px,y*PT),s,fontname='hebo' if bold else 'helv',fontsize=h*PT,color=(0,0,0))
 t=ms.add_text(s,dxfattribs={'height':h,'layer':layer,'style':'Standard'})
 t.set_placement(dv((x,y)),align={'left':TextEntityAlignment.LEFT,'center':TextEntityAlignment.CENTER,'right':TextEntityAlignment.RIGHT}[align])
def wrap(x,y,s,widthchars=45,h=2.05):
 import textwrap
 for row in textwrap.wrap(s,width=widthchars):text(x,y,row,h);y+=h*1.35
 return y
# KA sheet skeleton
rect(5,7,410,283);rect(15,20,316,260);line((342,7),(342,290))
text(345,12,'ALL DIMENSIONS IN mm UNLESS STATED OTHERWISE',1.8,bold=True);line((342,15),(415,15))
text(345,21,'NOTES:',2.5,bold=True)
notes=['1. Main roof +38.00 m; plant-room roof +41.57 m. Levels supplied by engineer.','2. Columns continue from ground through main roof to plant-room roof / parapet level.','3. Upper B1/B2 framing is projected dashed onto the main-roof plan.','4. Member material, local bearings and dimension datums remain for confirmation.','5. X = grillage connection; pairs 5850 apart, centred in 7300 half-width.']
y=27
for s in notes:y=wrap(345,y,s,44,1.95)+2.2
text(345,103,'STRUCTURAL MEMBER KEY',2.5,bold=True)
key=[('Main-roof beam', '325 wide x 300 deep',False,.5),('B1: plant-room roof beam','380 x 380',True,.45),('B2: plant-room roof beam','380 wide x 180 deep',True,.2),('Columns: C1 380 x 380','C2 380 x 300; ID locations TBC',False,.35),('GA reference geometry','Light background',False,.09)]
y=110
for a,b,d,w in key:
 line((346,y),(355,y),w,dash=d,gray=.65 if w==.09 else 0);text(358,y+.8,a,2.05);text(358,y+4,b,1.9);y+=10
# issue / branding / title block
for yy in [165,171,178,185,212,235,248,266,278,290]:line((342,yy),(415,yy))
for xx in [351,376,386,396]:line((xx,165),(xx,185))
for xx,s in [(344,'Rev'),(353,'Issue'),(378,'Drawn'),(388,'Chkd'),(398,'Date')]:text(xx,184,s,1.7)
for xx,s in [(344,'TBC'),(353,'REVIEW'),(378,'AT'),(388,'KS'),(398,'24-10-26')]:text(xx,176,s,1.8)
text(345,190,'Consultant:',1.9)
logo=Path('assets/branding/ka-logo-survey-source.jpeg')
if logo.exists():
 r=fitz.Rect(360*PT,192*PT,398*PT,210*PT);pg.insert_image(r,filename=str(logo),keep_proportion=True)
 # Self-contained CAD logo from the same registered raster, as colour scan strips.
 im=Image.open(logo).convert('RGB');im.thumbnail((150,72));iw,ih=im.size;sc=min(38/iw,18/ih);ox=379-iw*sc/2;oy=201-ih*sc/2
 for yy in range(ih):
  xx=0
  while xx<iw:
   rgb=im.getpixel((xx,yy));q=tuple((v//48)*48 for v in rgb)
   if min(rgb)>225:xx+=1;continue
   end=xx+1
   while end<iw and tuple((v//48)*48 for v in im.getpixel((end,yy)))==q:end+=1
   x0,y0=ox+xx*sc,oy+yy*sc;x1,y1=ox+end*sc,y0+sc
   ms.add_solid([dv(t) for t in [(x0,y0),(x1,y0),(x0,y1),(x1,y1)]],dxfattribs={'layer':'BRANDING','true_color':ezdxf.colors.rgb2int(q)})
   xx=end
else:text(350,202,'KA ENGINEERING GROUP',3,bold=True)
text(345,217,'Client:',1.9);text(345,227,'Ancore',3)
text(345,240,'Drawing Title:',1.9);text(345,245,'Roof Support Layout',3,bold=True)
text(345,253,'Site / Address:',1.9)
for yy,s in [(258,'RIVER HOUSE'),(261,'48 HIGH STREET, BELFAST'),(264,'COUNTY ANTRIM, BT1 2DR')]:text(345,yy,s,2.2)
text(345,271,'Drawn: AT    Checked: KS',2);text(345,276,'Scale: NTS / DO NOT SCALE',2)
text(345,283,'Project: 7078',2.3);text(380,283,'Drawing: 7078-01',2.1);text(345,288,'Revision: TBC',2.1)
# Survey coordinate X across width; Y along length, top end of supplied sketch.
S=.0060
def m(x,y):return (38+y*S,77+(14600-x)*S)
# GA vector graphic alignment, with separate surveyed dimension labels.
origin=np.array([608.34,317.0]);across=np.array([-54.78,-66.84]);along=np.array([194.58,-159.48]);inv=np.linalg.inv(np.column_stack([across,along]))
def gapt(p):
 uv=inv@(np.array(p)-origin);return (uv[0]*14600,uv[1]*44650)
def clip(a,b):
 a=np.array(a);b=np.array(b);v=b-a;lo,hi=0.,1.
 for pp,qq in [(-v[0],a[0]),(v[0],14600-a[0]),(-v[1],a[1]),(v[1],44650-a[1])]:
  if abs(pp)<1e-12:
   if qq<0:return None
  elif pp<0:lo=max(lo,qq/pp)
  else:hi=min(hi,qq/pp)
  if lo>hi:return None
 return a+lo*v,a+hi*v
count=0;shape=pg.new_shape()
for d in json.loads((W/'ga-vector-selection.json').read_text()):
 for it in d['items']:
  if it[0]=='l':pairs=[(it[1],it[2])]
  elif it[0]=='re':
   x0,y0,x1,y1=it[1];ps=[(x0,y0),(x1,y0),(x1,y1),(x0,y1)];pairs=list(zip(ps,ps[1:]+ps[:1]))
  else:continue
  for a,b in pairs:
   seg=clip(gapt(a),gapt(b))
   if seg is None:continue
   a,b=[m(*t) for t in seg];shape.draw_line(cv(a),cv(b));ms.add_line(dv(a),dv(b),dxfattribs={'layer':'GA_REFERENCE','true_color':ezdxf.colors.rgb2int((204,204,204)),'lineweight':5});count+=1
shape.finish(color=(.80,.80,.80),width=.07*PT);shape.commit()
# Main perimeter beams; retain measured survey frame without inventing walls.
for xx in [0,14600]:line(m(xx,0),m(xx,44650),.55,'MAIN_ROOF')
for yy in [0,44650]:line(m(0,yy),m(14600,yy),.55,'MAIN_ROOF')
# Central column spine repeats all perimeter bay positions, per engineer correction.
# Individual C1/C2 section assignments remain unresolved.
ys=[0,6150,11650,17150,22650,28150,33650,39150,44650]
for xx,rows in [(0,ys),(14600,[q for q in ys if q!=17150]),(7300,ys)]:
 for yy in rows:
  cx,cy=m(xx,yy);rect(cx-1.05,cy-1.05,2.1,2.1,.25,'COLUMNS',fill=True)
# Blue upper framing converted to black dashed linework.
for yy in [11650,17150,22650]:
 line(m(0,yy),m(7300,yy),.45,'UPPER_ROOF',dash=True)
 a=m(3600,yy);text(a[0]-1,a[1]-1.4,'B1',2.3,bold=True)
for xx in [1200,2400,3600,4800,6000]:line(m(xx,11650),m(xx,22650),.18,'UPPER_ROOF',dash=True)
for yy in range(11650,22651,1200):line(m(7300,yy),m(14600,yy),.18,'UPPER_ROOF',dash=True)
for xx in [0,7300,14600]:line(m(xx,11650),m(xx,22650),.3,'UPPER_ROOF',dash=True)
text(*m(3300,14500),'B2',2.3,bold=True);text(*m(10500,16400),'B2',2.3,bold=True)
# Grillage connection symbols: 5850 spacing confirmed. Placement across B1
# is engineer-confirmed centred: (7300 - 5850) / 2 = 725 mm.
for yy in [11650,17150]:
 for xx in [725,6575]:
  cx,cy=m(xx,yy)
  line((cx-1.2,cy-1.2),(cx+1.2,cy+1.2),.42,'COLUMNS')
  line((cx-1.2,cy+1.2),(cx+1.2,cy-1.2),.42,'COLUMNS')
# Label roof levels beside plan, not over GA equipment.
text(38,66,'MAIN ROOF +38.00 m',2.6,bold=True)
text(108,175,'PLANT-ROOM ROOF ABOVE +41.57 m',2.3,bold=True)
# Dimension arrow helper: no INT / EXT suffixes.
def dim(a,b,offset,label):
 a=np.array(a);b=np.array(b);v=b-a;L=np.linalg.norm(v);u=v/L;n=np.array([-u[1],u[0]]);aa=a+n*offset;bb=b+n*offset
 for p,q in [(a,aa+n*np.sign(offset)*1.3),(b,bb+n*np.sign(offset)*1.3)]:line(p+n*np.sign(offset)*.7,q,.10,'DIMENSIONS')
 line(aa,bb,.12,'DIMENSIONS')
 for tip,dr in [(aa,u),(bb,-u)]:
  for side in [-1,1]:line(tip,tip+dr*1.4+n*side*.42,.12,'DIMENSIONS')
 mid=(aa+bb)/2
 text(mid[0],mid[1]-.9,label,2.05,align='center')
for ya,yb in zip(ys,ys[1:]):dim(m(14600,ya),m(14600,yb),-8,str(yb-ya))
dim(m(0,44650),m(7300,44650),9,'7300');dim(m(7300,44650),m(14600,44650),9,'7300')
# Upper secondary framing spacing (representative interval, repeat as noted).
dim(m(725,11650),m(6575,11650),-14,'5850');dim(m(1200,11650),m(2400,11650),-4,'1200');dim(m(14600,12850),m(14600,14050),-5,'1200')
# Compass from GA north transformed by same affine graphic fit.
n=np.array(gapt(origin+np.array([0,-10])))-np.array(gapt(origin));nn=np.array([n[1],-n[0]]);nn/=np.linalg.norm(nn);cc=np.array([29,36]);side=np.array([-nn[1],nn[0]])
# KA-style compass rose with cardinal labels and a fine ring.
for j in range(32):
 ang1=2*math.pi*j/32;ang2=2*math.pi*(j+1)/32
 line(cc+np.array([math.cos(ang1),math.sin(ang1)])*4.2,cc+np.array([math.cos(ang2),math.sin(ang2)])*4.2,.08)
for v,l in [(nn,'N'),(-nn,'S'),(side,'E'),(-side,'W')]:
 tip=cc+v*6;perp=np.array([-v[1],v[0]])
 line(cc+perp*.85,tip,.13);line(tip,cc-perp*.85,.13);line(cc-perp*.85,cc+perp*.85,.10)
 if l in ['N','E']:line(cc,tip,.4)
 text(*(cc+v*8.2),l,2,align='center')
# Regression: source PDF -> final sheet must preserve orientation (positive
# determinant in the common image coordinate convention). North/east use that map.
origin_sheet=np.array(m(*gapt(origin)))
source_to_sheet=np.column_stack([np.array(m(*gapt(origin+[1,0])))-origin_sheet,np.array(m(*gapt(origin+[0,1])))-origin_sheet])
assert np.linalg.det(source_to_sheet)>0, 'Mirrored GA transform'
expected_north=source_to_sheet@np.array([0,-1.0]);expected_north/=np.linalg.norm(expected_north)
assert np.allclose(nn,expected_north)
orientation_check={'source_to_sheet_determinant':float(np.linalg.det(source_to_sheet)),'north_sheet_xy':nn.tolist(),'status':'orientation preserved','central_column_count':len(ys),'central_column_positions_mm':ys}
(W/'orientation-check.json').write_text(json.dumps(orientation_check,indent=2)+'\n')
# Short vertical load-path/continuity diagram; no hidden connection design implied.
text(40,203,'LEVEL / COLUMN CONTINUITY',2.5,bold=True)
for xx in [57,115]:line((xx,212),(xx,262),.5,'COLUMNS')
line((52,225),(120,225),.45,'UPPER_ROOF',dash=True);line((52,249),(120,249),.5,'MAIN_ROOF')
line((64,218),(108,218),.35);line((78,218),(83,207),.25);line((94,218),(89,207),.25)
text(127,219,'Telecom grillage / stub tower (schematic)',2.1)
text(127,226,'Plant-room roof +41.57 m: B1 / B2',2.1)
text(127,250,'Main roof +38.00 m: 325 x 300 beams',2.1)
text(127,258,'Columns continue below to ground',2.1)
text(40,270,'Local bearings and C1/C2 identification require confirmation.',2.0)
# Store explicit draft limits outside the engineering plotting area.
pg.set_rotation(0);doc.set_metadata({'title':'7078 River House - Roof Support Layout - Review','author':'KA Engineering Group','subject':'Review draft; issue metadata and local support details to confirm'})
pdf=O/'7078-river-house-roof-review.pdf';doc.save(pdf,garbage=4,deflate=True);pg.get_pixmap(matrix=fitz.Matrix(1.8,1.8)).save(O/'7078-river-house-roof-review.png');cad.saveas(W/'7078-river-house-roof-review.dxf')
assert not cad.audit().errors
(W/'ga-placement.json').write_text(json.dumps({'source_page':8,'source_sector':'B underlying grayscale vectors','origin_pdf':origin.tolist(),'width_vector_pdf':across.tolist(),'length_vector_pdf':along.tolist(),'dimensions':'survey values; graphic fit does not measure the GA','background_segments':count},indent=2))
print(json.dumps({'pdf':str(pdf),'dxf_entities':len(ms),'ga_segments':count,'cad_space':'A3 sheet-space millimetres, NTS','audit_errors':0}))
