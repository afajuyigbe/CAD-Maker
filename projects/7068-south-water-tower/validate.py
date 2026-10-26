"""Review validation: measured/derived geometry, approval gate and real DWG readback."""
from pathlib import Path
import json,hashlib,math,collections,subprocess
import numpy as np,ezdxf,fitz
P=Path(__file__).parent;O=P/'drawings';W=P/'interpretation';B=P/'items/water-tower-01/outputs';conv=Path('/tmp/river-libredwg-build')
m=json.loads((B/'mesh.json').read_text());v=np.array(m['vertices']);p=m['parameters'];groups=set(m['groups'])
assert np.isfinite(v).all();assert min(v[:,2])==0
assert abs(p['inner_face_diameter']*math.sin(math.pi/8)-4700)<1e-6
assert abs(p['outside_diameter']-p['inner_face_diameter']-1200)<1e-6
assert abs(p['outside_diameter']-p['core_diameter']-9600)<1e-6
for i in range(1,9):
 assert f'perimeter_column_{i}' in groups and f'radial_beam_{i}' in groups
 pts=np.array([v[j-1] for f,g in zip(m['faces'],m['groups']) if g==f'perimeter_column_{i}' for j in f]);assert pts[:,2].min()==0 and pts[:,2].max()==15600
for i in range(1,4):
 assert f'EMA_{i}_lower_ring_bracket' in groups and f'EMA_{i}_top_lid_parapet_bracket' in groups
for f in m['faces']:
 assert min(f)>=1 and max(f)<=len(v);pp=v[np.array(f)-1];assert np.linalg.norm(np.cross(pp[1]-pp[0],pp[2]-pp[0]))>1e-8
assert p['levels']['roof']==22000 and p['levels']['core_cap_top']==23900
assert p['levels']['parapet_top']-p['levels']['roof']==210
assert p['levels']['parapet_top']-p['levels']['parapet_lower_top']==90
item=json.loads((P/'items/water-tower-01/item.json').read_text());assert not item['approval_gate']['approved'];assert not list(P.rglob('*.obj')) and not list(P.rglob('*.mtl'))
pdf=fitz.open(O/'7068-south-water-tower-review.pdf');assert len(pdf)==2
for pg in pdf:
 t=pg.get_text();assert all(s in t for s in ['ST','AF','Revision: 1','7068-0']);assert '7078' not in t and 'Ancore' not in t
 assert abs(pg.rect.width*25.4/72-420)<.001
assert '4700 - INNER-FACE CENTRES' in pdf[0].get_text();assert '13482' in pdf[0].get_text();assert '+23.900' in pdf[1].get_text()
dwg=O/'7068-south-water-tower-review.dwg';back=W/'7068-roundtrip.dxf';dwg.unlink(missing_ok=True);back.unlink(missing_ok=True)
for exe,args in [('dxf2dwg',['--as','r2000','-o',str(dwg),str(W/'7068-south-water-tower-review.dxf')]),('dwg2dxf',['-o',str(back),str(dwg)])]:
 r=subprocess.run([str(conv/exe),*args],capture_output=True,text=True);(W/(exe+'.log')).write_text(r.stdout+r.stderr);assert (dwg if exe=='dxf2dwg' else back).exists()
assert dwg.read_bytes()[:6]==b'AC1015'
a=ezdxf.readfile(W/'7068-south-water-tower-review.dxf');b=ezdxf.readfile(back);audit=b.audit();assert not audit.errors;counts={}
for name in ['SHEET_01','SHEET_02','TOWER_SURFACE_MM']:
 aa=a.blocks[name];bb=b.blocks[name];ca=collections.Counter(e.dxftype() for e in aa);cb=collections.Counter(e.dxftype() for e in bb);assert ca==cb,(name,ca,cb);counts[name]=dict(cb)
 key=lambda es:collections.Counter((e.dxf.text,round(e.dxf.get('rotation',0),5)) for e in es.query('TEXT'))
 assert key(aa)==key(bb)
 for old,new in zip(aa.query('LINE'),bb.query('LINE')):assert np.allclose(old.dxf.start,new.dxf.start,atol=1e-6) and np.allclose(old.dxf.end,new.dxf.end,atol=1e-6)
for name in ['01 Plans','02 Elevations and 3D']:assert len(b.layouts.get(name).query('INSERT'))==1
assert len(a.blocks['TOWER_SURFACE_MM'].query('3DFACE'))==len(m['faces'])
# Explicit geometric scales: source project maps each mm to1/100 and1/150 sheet mm.
for name,S in [('roof-plan',100),('south-elevation',150),('east-elevation',150)]:
 q=json.loads((B/f'{name}-projection.json').read_text());assert q['world_units']=='mm' and q['scale']>0
report={'status':'passed','paper':'2 x A3 landscape','revision':'1','author':'ST','checker':'AF','client':'Jet Network Solutions','surface_mesh_sha256':hashlib.sha256((B/'mesh.json').read_bytes()).hexdigest(),'mesh':{'vertices':len(v),'faces':len(m['faces']),'perimeter_columns':8,'radial_beams':8,'EMA_groups_with_upper_and_lower_brackets':3},'diameters_mm':{k:p[k] for k in ['inner_face_diameter','column_pcd','outside_diameter','core_diameter']},'DWG':'AutoCAD2000 AC1015, two named paper layouts, editable vector views','cad_units':'mm; scaled A3 sheet blocks; uninserted TOWER_SURFACE_MM is full-size3Dmm','DWG_roundtrip_audit_errors':0,'DWG_entity_counts':counts,'DWG_geometry_and_text':'retained through conversion','OBJ_MTL':'Not generated; held pending engineer model approval','geometry_limits':'See item record and README: survey approximations, schematic telecom hardware, unmeasured core cap/parapet width and inner projection width'}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
# Inspect converted CAD visually after the geometry readback.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import RenderContext,Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import Configuration,BackgroundPolicy
for i,name in enumerate(['01 Plans','02 Elevations and 3D'],1):
 fig=plt.figure(figsize=(14,9.9));ax=fig.add_axes([0,0,1,1]);Frontend(RenderContext(b),MatplotlibBackend(ax),config=Configuration(background_policy=BackgroundPolicy.WHITE)).draw_layout(b.layouts.get(name),finalize=True);fig.savefig(W/f'cad-roundtrip-sheet-{i}.png',dpi=120);plt.close(fig)
