from pathlib import Path
import json,collections
import numpy as np,ezdxf,fitz
from ezdxf.addons.drawing import Frontend,RenderContext,pymupdf,layout,config
P=Path(__file__).resolve().parent;D=P/'drawings';R=P/'interpretation/dwg-roundtrip';report={}
for src in sorted(D.glob('*.dxf')):
 a=ezdxf.readfile(src);b=ezdxf.readfile(R/src.name)
 ca=collections.Counter(e.dxftype() for e in a.entitydb.values() if e.is_alive and e.dxftype() in ['LINE','TEXT','SOLID','CIRCLE','3DFACE','IMAGE','IMAGEDEF','INSERT'])
 cb=collections.Counter(e.dxftype() for e in b.entitydb.values() if e.is_alive and e.dxftype() in ca)
 ta=collections.Counter(e.dxf.text for e in a.query('TEXT'));tb=collections.Counter(e.dxf.text for e in b.query('TEXT'))
 assert ca==cb,(src.name,ca,cb)
 assert ta==tb,src.name
 assert a.layouts.names()==b.layouts.names(),src.name
 aud=b.audit();assert not aud.errors
 images=[e.dxf.filename for e in b.objects.query('IMAGEDEF')];assert all((D/x).exists() for x in images)
 report[src.name]={'entities':dict(ca),'text_preserved':True,'audit_errors':len(aud.errors),'audit_fixes':len(aud.fixes),'image_references':images,'units':b.units}
 if src.stem in ['7145-01','7145-02']:
  # Resolve the shipped relative image references for independent CAD rendering.
  for im in b.objects.query('IMAGEDEF'):im.dxf.filename=str(D/im.dxf.filename)
  backend=pymupdf.PyMuPdfBackend();cfg=config.Configuration(background_policy=config.BackgroundPolicy.WHITE)
  Frontend(RenderContext(b),backend,config=cfg).draw_layout(b.modelspace(),finalize=True)
  pdf=backend.get_pdf_bytes(layout.Page(420,297));out=P/'interpretation'/f'{src.stem}-cad-check.pdf';out.write_bytes(pdf)
  doc=fitz.open(stream=pdf,filetype='pdf');doc[0].get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(out.with_suffix('.png'))
pdf=fitz.open(D/'7145-review-drawing-set.pdf');assert len(pdf)==2
for i,p in enumerate(pdf):
 assert abs(p.rect.width-420*72/25.4)<.01 and abs(p.rect.height-297*72/25.4)<.01
 text=p.get_text();assert '7145-0'+str(i+1) in text and 'Drawn: AT' in text and 'Checked: AF' in text
 assert not any(x in text.lower() for x in ['tadworth','5166','skye','howmic','7092'])
 for b in p.get_text('blocks'):assert p.rect.contains(fitz.Rect(b[:4])),(i,b)
par=json.loads((P/'model/parameters.json').read_text());assert par['beam_count']==7 and par['spaces']==8 and par['beam_spacing']==650 and not par['edge_beams'];assert par['spaces']*par['beam_spacing']==par['internal_clear']
mesh=json.loads((P/'model/mesh.json').read_text());axes=set(g for g in mesh['groups'] if g.startswith('embedded_beam_'));assert len(axes)==7
assert len(set(g for g in mesh['groups'] if '_allocated_antenna_' in g))==9
assert len(set(g for g in mesh['groups'] if g.startswith('allocated_RRU_')))==15
assert (D/'7145-saffron-walden-tower.obj').is_file() and (D/'7145-saffron-walden-tower.mtl').is_file()
obj_report=json.loads((D/'obj-validation.json').read_text());assert obj_report['status']=='passed'
# Verify the corrected engineering datums, not only file counts.
elev=json.loads((P/'interpretation/elevation-datums.json').read_text())
heights=[x['value_mm'] for x in elev['clear_height_dimensions']]
assert heights==[5600,2400,2600,5500,2800,4100]
for d in elev['clear_height_dimensions']:
 assert abs((d['sheet_floor_y']-d['sheet_ceiling_y'])/.0085-d['value_mm'])<1e-7
 assert d['from']=='floor top' and d['to']=='ceiling soffit'
page1=pdf[0].get_text();page2=pdf[1].get_text()
assert '510' not in page1 and '152' in page1 and 'Soffit scan - location 1' in page1
assert page2.count('175')>=5 and all(str(x) in page2 for x in heights)
assert 'B1 - floor of fourth floor' not in page2 and 'B1: 510 x 190, flange 20' in page2
v=np.array(mesh['vertices']);beamids=set(i for f,g in zip(mesh['faces'],mesh['groups']) if g=='primary_fourth_floor_floor_EW' for i in f)
bz=v[np.array(sorted(beamids))-1,2]
assert abs(bz.max()-par['primary_beam_top'])<1e-7 and abs(bz.max()-bz.min()-510)<1e-7
assert par['roof_level']-par['slab_thickness']-par['primary_beam_top']==4100
assert 'fourth_floor_deck' not in mesh['groups'] and 'fourth_floor_steel_deck' in mesh['groups']
assert not any((D/x).exists() for x in ['7145-03.pdf','7145-03.dwg','7145-03.dxf'])
# Lower plinth has only the surveyed three small returns plus the base return.
import sys
sys.path.insert(0,str(P/'model'))
from wall_profile import segments,thickness
bands=segments()
assert [round(a[2]-b[2],6) for a,b in zip(bands,bands[1:])]==[300,150,150,150]
assert thickness(10000)==thickness(24000)
assert 'Roof support member' not in page1 and 'Wall offsets - survey profile' not in page1
roofsheet=ezdxf.readfile(D/'7145-01.dxf')
rooftext=[e.dxf.text for e in roofsheet.query('TEXT')]
assert not any('650' in x or 'no edge beams' in x or 'eight spaces' in x for x in rooftext)
assert par['wall_profile']['outward_step_mm']==150
assert 'Lower plinth:' not in page2 and 'Former water tank' in page2 and 'Brickwork' in page2
assert '510' not in [e.dxf.text for e in ezdxf.readfile(D/'7145-02.dxf').query('TEXT')]
# Check the visible illustration selects the real 3700mm tank / 4100mm room datums.
assert par['fourth_floor_clear_height']-par['tank_panel_height']==400
assert 'interior_brick_band_N' in mesh['groups'] and 'interior_brick_band_E' in mesh['groups']
for side in ['N','E']:
 ids=set(i for f,g in zip(mesh['faces'],mesh['groups']) if g=='interior_brick_band_'+side for i in f)
 bb=v[np.array(sorted(ids))-1,2];assert abs(bb.min()-(par['primary_beam_top']+3700))<1e-7 and abs(bb.max()-(par['roof_level']-175))<1e-7
assert par['wall_profile']['base_external_width_mm']==8000 and par['wall_profile']['base_wall_mm']==1400
assert abs(bands[0][2]-1400)<1e-7 and abs(bands[-1][2]-650)<1e-7
assert abs(5200+2*bands[0][2]-8000)<1e-7
assert abs(par['wall_profile']['plinth_top_first_floor_mm']-5775)<1e-7
assert '8000' in page2 and '1400' in page2 and 'Approx. 550-600' in page2
assert 'Approx. 500' not in page2
# Rotate the base masonry back to local axes and verify the actual outer faces.
a=np.deg2rad(par['rotation_deg']);inverse=np.array([[np.cos(a),np.sin(a)],[-np.sin(a),np.cos(a)]])
base_ids={i for f,g in zip(mesh['faces'],mesh['groups']) if g.startswith('tower_wall_') for i in f if abs(v[i-1,2])<1e-7}
base_xy=v[np.array(sorted(base_ids))-1,:2]@inverse.T
assert np.allclose(base_xy.max(0)-base_xy.min(0),[8000,8000],atol=1e-6)
# Independent STEP readback compares the actual current exports.
import cadquery as cq
step=cq.importers.importStep(str(D/'7145-tower-model.step')).val().BoundingBox()
assert np.allclose([step.xmin,step.ymin,step.zmin],v.min(0),atol=1e-5)
assert np.allclose([step.xmax,step.ymax,step.zmax],v.max(0),atol=1e-5)
report['review_checks']={'PDF_pages':2,'A3_landscape':True,'metadata_and_text_bounds':'pass','internal_clear_mm':5200,'base_external_width_mm':8000,'base_wall_mm':1400,'first_floor_wall_approx_mm':[550,600],'nominal_shaft_model_wall_mm':650,'plinth_top':'First-floor level, 5775 mm','embedded_beams':7,'spaces':8,'spacing_mm':650,'edge_beams':False,'scan_sheet':'Integrated on sheet 7145-01; no separate scan sheet','clear_heights_mm':heights,'wall_profile':'Lower plinth only: three 150 mm steps at 20-course intervals and 300 mm base return; upper shaft constant','roof_sheet_details':'Flange-9 section, standalone wall-offset detail, repeated 650 dimension chain and spacing note removed','interior_view':'Perspective: 3700 mm tank height, exposed brick band to roof soffit; no floor beams or access opening','slabs':'175 mm shown separately from clear heights','primary_beam_location':'Fourth-floor floor / third-floor roof','primary_beam_model_top_mm':float(bz.max()),'scan_locations':[{'number':1,'type':'soffit','target':'Roof over fourth floor'}],'allocated_panels':9,'allocated_RRUs':15,'allocated_dish_mm':300,'OBJ_MTL':'Export authorised by engineer; matching OBJ/MTL independently validated','STEP_mesh_bounds_match':True}
(P/'interpretation/validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['review_checks'],indent=2),flush=True)
