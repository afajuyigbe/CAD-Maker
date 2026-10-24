"""Compose two A3 sheets and editable CAD sheet projections from shared mesh."""
from pathlib import Path
import json,fitz,ezdxf,subprocess,zipfile
from ezdxf.enums import TextEntityAlignment
P=Path(__file__).parent;O=P/'drawings';W=P/'interpretation';B=P/'items/building-visual-01/outputs';PT=72/25.4
# Reuse the exact reviewed KA sheet border/branding/title block.
source=fitz.open(O/'7078-river-house-roof-review.pdf');out=fitz.open();out.insert_pdf(source);out.insert_pdf(source);pg=out[1]
for r in [(15.3,20.3,330.7,279.7),(343,16,414,164),(343,237,414,247),(378,280,414,287)]:pg.add_redact_annot(fitz.Rect(*(v*PT for v in r)),fill=(1,1,1))
pg.apply_redactions(images=0,graphics=2,text=0)
def pdftext(x,y,s,h=2.2,bold=False):pg.insert_text((x*PT,y*PT),s,fontsize=h*PT,fontname='hebo' if bold else 'helv',color=(0,0,0))
pdftext(345,240,'Drawing Title:',1.9);pdftext(345,245,'Building 3D Model',3,True);pdftext(380,283,'Drawing: 7078-02',2.1)
rects={'street':(20,55,172,248.454545),'rear':(176,55,328,248.454545)}
for name,r in rects.items():pg.insert_image(fitz.Rect(*(v*PT for v in r)),filename=str(B/f'7078-river-house-building-{name}.png'),keep_proportion=True)
# Circled view number, underlined title and scale beneath as agreed.
for num,x,title in [(1,28,'Street frontage and roof'),(2,184,'Rear elevation and roof')]:
 pg.draw_circle((x*PT,265*PT),2.5*PT,color=(0,0,0),width=.15*PT);pdftext(x-.8,265.8,str(num),2.1)
 pdftext(x+5,264.5,title,2.4);pg.draw_line(((x+5)*PT,266*PT),((x+120)*PT,266*PT),width=.15*PT);pdftext(x+5,269,'3D View / NTS',1.9)
out.set_metadata({'title':'7078 River House - Roof Support Layout and Building 3D Model','author':'AT','subject':'Checked KS; revision 1; 3D facade/equipment details approximate'})
out.save(O/'7078-river-house-drawing-set-review.pdf',garbage=4,deflate=True);out.close();source.close()
preview=fitz.open(O/'7078-river-house-drawing-set-review.pdf');preview[1].get_pixmap(matrix=fitz.Matrix(1.7,1.7)).save(O/'7078-river-house-3d-sheet-review.png');preview.close()
# CAD sheet blocks and named paper layouts. Drawing 02 uses depth-tested visible
# edge projections from the same mesh: editable vector linework, no linked PNG.
cad=ezdxf.readfile(W/'7078-river-house-roof-review.dxf');ms=cad.modelspace();roof=cad.blocks.new('SHEET_01_ROOF')
for e in list(ms):ms.unlink_entity(e);roof.add_entity(e)
model=cad.blocks.new('SHEET_02_BUILDING_3D')
def dv(p):return (p[0],297-p[1])
def addtext(x,y,s,h=2.2):model.add_text(s,dxfattribs={'height':h,'layer':'TEXT'}).set_placement(dv((x,y)))
# Keep external frame, side table and logos. Replace drawing-area content, notes/key.
for e in roof:
 layer=e.dxf.get('layer','')
 if layer in ['GA_REFERENCE','MAIN_ROOF','UPPER_ROOF','COLUMNS','DIMENSIONS']:continue
 if e.dxftype()=='TEXT':
  p=e.dxf.insert;x,y=p.x,297-p.y
  if x<342 or y<165:continue
  c=e.copy()
  if 'Roof Support Layout' in c.dxf.text:c.dxf.text='Building 3D Model'
  if '7078-01' in c.dxf.text:c.dxf.text=c.dxf.text.replace('7078-01','7078-02')
  model.add_entity(c)
 elif layer=='SHEET' and e.dxftype()=='LINE':
  a=e.dxf.start;b=e.dxf.end
  if min(a.x,b.x)>343 and 16<min(297-a.y,297-b.y) and max(297-a.y,297-b.y)<165:continue
  # Delete compass/internal key symbols; retain plot border and sheet framework.
  if max(a.x,b.x)<342:
   vals=[(a.x,297-a.y),(b.x,297-b.y)]
   border=any(abs(vals[0][j]-v)<1e-4 and abs(vals[1][j]-v)<1e-4 for j,v in [(0,5),(0,15),(0,331),(1,7),(1,20),(1,280),(1,290)])
   if not border:continue
  model.add_entity(e.copy())
 elif layer=='BRANDING':model.add_entity(e.copy())
addtext(345,12,'ALL DIMENSIONS IN mm UNLESS STATED OTHERWISE',1.8)
if 'MODEL_3D_VIEW' not in cad.layers:cad.layers.new('MODEL_3D_VIEW',dxfattribs={'color':7,'lineweight':9})
for name,r in rects.items():
 x0,y0,x1,y1=r
 for a,b in json.loads((B/f'{name}-visible-edges.json').read_text()):
  aa=(x0+a[0]*(x1-x0),y0+a[1]*(y1-y0));bb=(x0+b[0]*(x1-x0),y0+b[1]*(y1-y0))
  model.add_line(dv(aa),dv(bb),dxfattribs={'layer':'MODEL_3D_VIEW','lineweight':9})
for num,x,title in [(1,28,'Street frontage and roof'),(2,184,'Rear elevation and roof')]:
 model.add_circle(dv((x,265)),2.5,dxfattribs={'layer':'SHEET'});addtext(x-.8,265.8,str(num),2.1);addtext(x+5,264.5,title,2.4);model.add_line(dv((x+5,266)),dv((x+120,266)),dxfattribs={'layer':'SHEET'});addtext(x+5,269,'3D View / NTS',1.9)
# Retain full editable face geometry in an uninserted, clearly named metre block.
# It can be inserted by CAD users; paper drawings remain A3 sheet millimetres.
mesh=json.loads((B/'mesh.json').read_text());geo=cad.blocks.new('BUILDING_SURFACE_METRES')
if 'BUILDING_SURFACE' not in cad.layers:cad.layers.new('BUILDING_SURFACE',dxfattribs={'color':8})
for ids,mat in zip(mesh['faces'],mesh['materials']):
 pts=[mesh['vertices'][i-1] for i in ids];rgb=tuple(int(v*255) for v in mesh['colors'][mat]);attrs={'layer':'BUILDING_SURFACE','true_color':ezdxf.colors.rgb2int(rgb)}
 if len(pts)<=4:geo.add_3dface(pts,dxfattribs=attrs)
 else:
  for i in range(1,len(pts)-1):geo.add_3dface([pts[0],pts[i],pts[i+1]],dxfattribs=attrs)
ms.add_blockref('SHEET_01_ROOF',(0,0));ms.add_blockref('SHEET_02_BUILDING_3D',(460,0))
old_layouts=[n for n in cad.layouts.names() if n!='Model']
for n,block in [('01 Roof Support Layout','SHEET_01_ROOF'),('02 Building 3D Model','SHEET_02_BUILDING_3D')]:
 lay=cad.layouts.new(n);lay.page_setup(size=(420,297),margins=(0,0,0,0),units='mm');lay.add_blockref(block,(0,0))
for n in old_layouts:cad.layouts.delete(n)
assert not cad.audit().errors
cad.saveas(W/'7078-drawing-set-review.dxf')
print('Two-page PDF and editable CAD sheet set composed.')
