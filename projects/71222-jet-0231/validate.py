"""Verify current review geometry and PDF/DWG content; report unresolved engineering data separately."""
from pathlib import Path
import json,collections,math
import fitz,ezdxf,numpy as np
from ezdxf.addons.drawing import Frontend,RenderContext,pymupdf,layout,config
P=Path(__file__).resolve().parent;D=P/'drawings';R=P/'interpretation/dwg-roundtrip';report={}
for src in sorted(D.glob('*.dxf')):
 a=ezdxf.readfile(src);assert not a.audit().errors
 b=ezdxf.readfile(R/src.name)
 kinds=['LINE','TEXT','SOLID','CIRCLE','3DFACE','IMAGE','IMAGEDEF','INSERT']
 count=lambda d:collections.Counter(e.dxftype() for e in d.entitydb.values() if e.is_alive and e.dxftype() in kinds)
 assert count(a)==count(b),(src.name,count(a),count(b))
 assert collections.Counter(e.dxf.text for e in a.query('TEXT'))==collections.Counter(e.dxf.text for e in b.query('TEXT'))
 assert a.layouts.names()==b.layouts.names() and a.units==b.units==4
 line_styles=lambda d:collections.Counter((e.dxf.layer,e.dxf.linetype.upper(),e.dxf.lineweight) for e in d.query('LINE'))
 assert line_styles(a)==line_styles(b)
 audit=b.audit();assert not audit.errors
 refs=[e.dxf.filename for e in b.objects.query('IMAGEDEF')];assert all((D/x).is_file() for x in refs)
 report[src.name]={'entities':dict(count(a)),'text_and_layouts_retained':True,'units':'mm','audit_errors':len(audit.errors),'readback_material_placeholder_fixes':len(audit.fixes),'relative_images':refs}
 if src.stem in ['71222-01','71222-02','71222-03']:
  for im in b.objects.query('IMAGEDEF'):im.dxf.filename=str(D/im.dxf.filename)
  out=pymupdf.PyMuPdfBackend();Frontend(RenderContext(b),out,config=config.Configuration(background_policy=config.BackgroundPolicy.WHITE)).draw_layout(b.modelspace(),finalize=True)
  pdf=out.get_pdf_bytes(layout.Page(420,297));f=P/'interpretation'/f'{src.stem}-cad-check.pdf';f.write_bytes(pdf)
  doc=fitz.open(stream=pdf,filetype='pdf');doc[0].get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(f.with_suffix('.png'))
pdf=fitz.open(D/'71222-review-drawing-set.pdf');assert len(pdf)==3
for n,p in enumerate(pdf,1):
 assert np.allclose([p.rect.width,p.rect.height],np.array([420,297])*72/25.4,atol=.01)
 text=p.get_text();assert f'71222-0{n}' in text and 'Jansen SL' in text and 'S.T.' in text and 'K.S.' in text
 assert not any(x in text for x in ['7145','5166','JetNSL','SAFFRON','TADWORTH','AT    Checked: AF'])
 for block in p.get_text('blocks'):assert p.rect.contains(fitz.Rect(block[:4])),(n,block)
text=pdf[0].get_text();assert all(x in text for x in ['21300','12500','10600','1900'])
assert text.splitlines().count('3000')==4  # Four measured bays between five castellated axes.
assert not any('Scan Locations' in p.get_text() for p in pdf)
a=json.loads((P/'interpretation/parameters.json').read_text());assert a['main_depth_mm']+a['corridor_depth_mm']==a['nominal_depth_mm']==12500
assert a['width_mm']==21300 and np.allclose(np.diff(a['castellated_axes_x_mm']),3000)
assert len(a['castellated_axes_x_mm'])==5
mesh=json.loads((P/'model/mesh.json').read_text());v=np.array(mesh['vertices']);assert np.isfinite(v).all()
assert set(g for g in mesh['groups'] if g.startswith('PV_row_'))=={'PV_row_1','PV_row_2','PV_row_3'}
assert not any('telecom' in g.lower() or 'antenna' in g.lower() for g in mesh['groups'])
for f in mesh['faces']:
 assert len(f)>=3 and all(1<=i<=len(v) for i in f)
 q=v[np.array(f)-1];assert np.linalg.norm(np.cross(q[1]-q[0],q[2]-q[0]))>1e-7
angle=math.radians(a['north_from_local_y_deg']);rot=np.array([[math.cos(angle),math.sin(angle)],[-math.sin(angle),math.cos(angle)]])
assert abs(np.linalg.det(rot)-1)<1e-9
ids=sorted(set(i for f,g in zip(mesh['faces'],mesh['groups']) if g=='castellated_flanges' for i in f));xy=v[np.array(ids)-1,:2]@rot.T
xs=np.unique(np.round(xy[:,0],5));assert len(xs)==10
centres=(xs[::2]+xs[1::2])/2;assert np.allclose(centres,a['castellated_axes_x_mm'],atol=1e-4)
assert abs(xy[:,1].min())<1e-5 and abs(xy[:,1].max()-10600)<1e-5
ids=sorted(set(i for f,g in zip(mesh['faces'],mesh['groups']) if g=='CHS_transverse_braces' for i in f));xy=v[np.array(ids)-1,:2]@rot.T
row=xy[(xy[:,1]>1800)&(xy[:,1]<2000),1];assert abs(row.max()-row.min()-90)<1e-5
assert sum(a['width_chain_mm'])==21300
assert a['B2_axes_x_mm'][-1]==20500 and a['full_web_castellated_axis_x_mm']==20800
assert a['full_web_castellated_axis_x_mm']-a['B2_axes_x_mm'][-1]==300
assert a['width_mm']-a['full_web_castellated_axis_x_mm']==500
assert 'End offset to confirm' not in text and '300' in text and '500' in text
# Independently check the moved full-web geometry and the added B2 line in local coordinates.
for name,expected in [('full_web_castellated_end_beam',[20800]),('B2_I_beams',[2200,19200,20500])]:
 ids=sorted(set(i for f,g in zip(mesh['faces'],mesh['groups']) if g==name for i in f));xy=v[np.array(ids)-1,:2]@rot.T
 xs=np.unique(np.round(xy[:,0],5))
 for x in expected:assert np.any(np.isclose(xs,x-105 if name.startswith('full_web') else x-75))
# Confirmed section and corrected vertical arrangement, checked against exported mesh vertices.
S=a['visual_proxies']['roof_level']-a['visual_proxies']['roof_deck_thickness'];Z=a['visual_proxies']['roof_level'];CB=a['sections']['castellated']
assert (CB['depth_mm'],CB['flange_width_mm'],CB['flange_thickness_mm'])==(800,210,18)
ids=sorted(set(i for f,g in zip(mesh['faces'],mesh['groups']) if g=='castellated_flanges' for i in f));fl=v[np.array(ids)-1];zs=np.unique(np.round(fl[:,2],6))
assert np.allclose(zs,[S-800,S-782,S-18,S])
xx=fl[:,:2]@rot.T
for c in a['castellated_axes_x_mm']:
 points=xx[np.abs(xx[:,0]-c)<200,0];assert np.allclose([points.min(),points.max()],[c-105,c+105])
ids=sorted(set(i for f,g in zip(mesh['faces'],mesh['groups']) if g=='CHS_transverse_braces' for i in f));q=v[np.array(ids)-1];xy=q[:,:2]@rot.T
assert xy[:,0].max()<16700 and xy[:,0].min()>0
west=q[xy[:,0]<4700-1e-5,2];central=q[xy[:,0]>4700+1e-5,2]
# The first central segment starts just east of the first castellated web.
assert abs((west.min()+west.max())/2-(S-18-45))<1e-6
assert abs((central.min()+central.max())/2-(Z-750-125))<1e-6
ids=sorted(set(i for f,g in zip(mesh['faces'],mesh['groups']) if g=='CHS_plan_braces' for i in f));diag=v[np.array(ids)-1];dxy=diag[:,:2]@rot.T
assert dxy[:,0].max()<4700+90 and abs((diag[:,2].min()+diag[:,2].max())/2-(S-18-45))<1e-6
ch=diag[:,2]
for group,stations in [('B1_west_lower_cross_members',[1900,5400,8900]),('B1_east_lower_cross_members',[1900,3650,5400,7150,8900])]:
 ids=sorted(set(i for f,g in zip(mesh['faces'],mesh['groups']) if g==group for i in f));q=v[np.array(ids)-1];xy=q[:,:2]@rot.T
 ys=np.unique(np.round(xy[:,1],5));assert len(ys)==len(stations)*4
 assert np.allclose(ys.reshape(-1,4).mean(1),stations)
 assert np.allclose([q[:,2].min(),q[:,2].max()],[Z-1000,Z-750]) and q[:,2].max()<ch.min()
ids=sorted(set(i for f,g in zip(mesh['faces'],mesh['groups']) if g=='B2_I_beams' for i in f));q=v[np.array(ids)-1];xy=q[:,:2]@rot.T
xs=np.unique(np.round(xy[:,0],5));assert len(xs)==12 and np.allclose(xs.reshape(3,4).mean(1),[2200,19200,20500])
assert q[:,2].max()<ch.min()
assert 'section TBC' not in text and 'top/bottom CB' not in text
assert all(t in text for t in ['800','210','18'])
# Distinct member patterns survive the native drawing; labels are not the classifier.
roof=ezdxf.readfile(D/'71222-01.dxf')
style={}
for layer in ['CASTELLATED','I_BEAMS','B2_BEAMS','CHS_BRACES','FULL_WEB']:
 entities=[e for e in roof.query('LINE') if e.dxf.layer==layer]
 assert entities
 style[layer]=sorted(set((e.dxf.linetype.upper(),e.dxf.lineweight) for e in entities))
assert style['CASTELLATED']==[('CB_LONG_DASH',50)]
assert style['CHS_BRACES']==[('CHS_DASH_DOT',30)]
assert style['FULL_WEB']==[('CONTINUOUS',80)]
assert all(x[0]=='CONTINUOUS' for x in style['I_BEAMS'])
assert style['B2_BEAMS']==[('B2_SHORT_DASH',40)]
assert len({tuple(x) for x in style.values()})==5
for block in pdf[0].get_text('blocks'):
 if block[0]<330*72/25.4:assert not any(t in block[4].splitlines() for t in ['CB','FW','B1','B2'])
E=a['equipment'];equipment_text=pdf[1].get_text()
assert all(t in equipment_text for t in ['3500','2900','12800','4000','3200','1500','1300','300','2100','1850','1950','1350','1650'])
assert '*' not in equipment_text and 'closure' not in equipment_text.lower() and 'confirm' not in equipment_text.lower()
assert sum(E['PV_vertical_chain_mm'])==E['outer_north_y_mm']==12500
assert sum(a['main_depth_chain_mm'])==10600
assert E['openings'][0][0]==12800 and E['openings'][1][0]-(12800+1300)==4000
assert 21300-E['openings'][1][0]==3200
assert E['openings'][0][1]==12500-1500
assert E['PV_x0_mm']==3500 and 21300-E['PV_x1_mm']==2900
assert E['parapet_width_mm']==E['parapet_height_mm']==300
assert E['hatch_size_mm']==[1300,1300] and E['opening_upstand_mm']==300
assert E['safety_path_mm'][0][1]==12500-1500 and E['safety_path_mm'][1][0]==21300-1500 and E['safety_path_mm'][-1][1]==1500
for n,ys in enumerate(E['PV_rows_north_to_south'][::-1],1):
 ids=sorted(set(i for f,g in zip(mesh['faces'],mesh['groups']) if g==f'PV_row_{n}' for i in f));xy=v[np.array(ids)-1,:2]@rot.T
 assert np.allclose([xy[:,0].min(),xy[:,0].max()],[3500,18400],atol=1e-5)
 assert np.allclose([xy[:,1].min(),xy[:,1].max()],ys,atol=1e-5)
assert mesh['groups'].count('roof_skylight_glass')==2
import cadquery as cq
bb=cq.importers.importStep(str(D/'71222-visual-model.step')).val().BoundingBox()
assert np.allclose([bb.xmin,bb.ymin,bb.zmin],v.min(0),atol=1e-5) and np.allclose([bb.xmax,bb.ymax,bb.zmax],v.max(0),atol=1e-5)
report['review_checks']={'status':'Review draft; unresolved engineering details listed below','PDF_pages':3,'metadata':'71222 / Jet 0231 / Jansen SL / S.T. / K.S. / Rev1','roof_depth_mm':12500,'main_depth_mm':10600,'corridor_mm':1900,'width_mm':21300,'castellated_beams':5,'castellated_profile_mm':{'depth':800,'flange_width':210,'flange_thickness':18},'CHS_level':'Upper west diagonal bay; lower central bays at B1 level; no CHS in east I-beam bay','B1_lower_cross_members':{'west':3,'east':5},'B2_members':3,'castellated_spaces_mm':[3000]*4,'width_chain_mm':a['width_chain_mm'],'last_B2_to_full_web_mm':300,'full_web_to_wall_mm':500,'CHS_outer_diameter_mm':90,'member_line_patterns':style,'equipment_setbacks_mm':{'PV_west':3500,'PV_east':2900,'hatch_west':12800,'skylight_east':3200,'safety':1500},'PV_depth_chain_mm':E['PV_vertical_chain_mm'],'opening_chain_mm':[12800,1300,4000,3200],'parapet_mm':[300,300],'upstand_mm':[1300,1300,300],'PV_rows':3,'telecoms':'Excluded as instructed','scan_locations':'Excluded as instructed','STEP_mesh_bounds':'Match','unresolved':['Unsupplied web/I-flange thicknesses and exact B1/B2 roof-offset reference','Unmeasured castellated hole geometry and connection details'],'model_limits':'Surrounding theatre heights, proxy steel thicknesses, PV/opening details and graphical north not surveyed'}
(P/'interpretation/validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['review_checks'],indent=2),flush=True)
