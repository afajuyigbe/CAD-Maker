"""Issue OBJ/MTL only from the exact geometry authorised by the engineer."""
from pathlib import Path
import json,hashlib,numpy as np,zipfile
P=Path(__file__).parent;O=P/'outputs';raw=(O/'mesh.json').read_bytes();digest=hashlib.sha256(raw).hexdigest();approval=json.loads((P/'item.json').read_text())['approval_gate']
assert approval.get('approved') and approval.get('approved_geometry_sha256')==digest,'Geometry not authorised for export'
d=json.loads(raw);V=np.array(d['vertices']);F=d['faces'];G=d['groups'];M=d['materials'];C=d['colors'];stem='7078-river-house-building'
N=[]
for f in F:
 p=V[np.array(f)-1];n=np.cross(p[1]-p[0],p[2]-p[0]);n/=np.linalg.norm(n);N.append(n)
with (O/(stem+'.obj')).open('w') as f:
 f.write('# River House 7078; approved with requested column corrections completed\n# Units metres; Y up; ground Y=0; X along roof length, -Z across roof width\nmtllib '+stem+'.mtl\no River_House_7078\ns off\n')
 for x,y,z in V:f.write(f'v {x:.6f} {z:.6f} {-y:.6f}\n')
 for x,y,z in N:f.write(f'vn {x:.8f} {z:.8f} {-y:.8f}\n')
 prev=None
 for index,(face,g,m) in enumerate(zip(F,G,M),1):
  if (g,m)!=prev:f.write(f'g {g}\nusemtl {m}\n');prev=(g,m)
  f.write('f '+' '.join(f'{i}//{index}' for i in face)+'\n')
with (O/(stem+'.mtl')).open('w') as f:
 for m,c in C.items():f.write(f'newmtl {m}\nKd {" ".join(map(str,c))}\nKa 0.15 0.15 0.15\nKs 0.10 0.10 0.10\nNs 18\nd 1\nillum 2\n\n')
# Independent parse and geometric/material readback against the approved source.
verts=[];normals=[];faces=[];uses=[];materials={l.split()[1] for l in (O/(stem+'.mtl')).read_text().splitlines() if l.startswith('newmtl ')}
for line in (O/(stem+'.obj')).read_text().splitlines():
 if line.startswith('v '):verts.append(list(map(float,line.split()[1:])))
 elif line.startswith('vn '):normals.append(list(map(float,line.split()[1:])))
 elif line.startswith('f '):faces.append([tuple(map(int,t.split('//'))) for t in line.split()[1:]])
 elif line.startswith('usemtl '):uses.append(line.split()[1])
 elif line.startswith('mtllib '):assert (O/line.split()[1]).is_file()
expected=V[:,[0,2,1]]*np.array([1,1,-1]);assert np.allclose(verts,expected,atol=.00000051)
assert all(m in materials for m in uses);assert len(faces)==len(F)
for old,new in zip(F,faces):assert old==[a for a,b in new] and all(1<=b<=len(normals) for a,b in new)
assert np.allclose(np.linalg.norm(normals,axis=1),1,atol=1e-6)
assert {'C1_7.3_0','C1_7.3_8'}<=set(G)
assert len([g for g in set(G) if '_antenna_pair_' in g])==6
for group in ['C1_7.3_0','C1_7.3_8']:
 pts=np.array([V[i-1] for face,g in zip(F,G) if g==group for i in face]);assert np.isclose(pts[:,2].max(),41.57)
# Engineer correction: all three B1 reach the opposite perimeter.
for group in ['B1_11.65','B1_17.15','B1_22.65']:
 pts=np.array([V[i-1] for face,g in zip(F,G) if g==group for i in face])
 assert np.isclose(pts[:,1].min(),0) and np.isclose(pts[:,1].max(),14.6)
# The marked rear column and its continuous facade register both exist.
assert 'facade_column_to_ground_17.15_14.6' in G
joints=[V[np.array(face)-1] for face,g in zip(F,G) if g=='rear_primary_column_axis_joints'];assert any(np.isclose(p[:,0].mean(),17.15) and p[:,2].min()==0 and np.isclose(p[:,2].max(),41.57) for p in joints)
report={'status':'passed','approved_geometry_sha256':digest,'vertices':len(verts),'surface_faces':len(faces),'unit_normals':len(normals),'materials':len(materials),'coordinate_readback':'matches approved mesh within 0.00000051 m','up_axis':'Y','units':'metres','ground_y':0,'external_textures':False,'roof_end_central_columns':'both restored','rear_17_15m_column':'continuous to ground and visible across facade bands','B1_spans':'3 beams span full 14.6 m building width','corner_antenna_mounts':'3 paired yokes / 6 panels'}
(O/'export-validation.json').write_text(json.dumps(report,indent=2)+'\n')
readme='''7078 River House – OBJ surface model + MTL

Keep 7078-river-house-building.obj and 7078-river-house-building.mtl together in the same directory. Import units: METRES. Y is vertical; ground Y=0. X follows the building length; negative Z follows the survey width. The MTL uses flat opaque colours with no bitmap textures. Select wireframe/feature-edge display in your software as required. Explicit normals and polygon faces are supplied; some importers triangulate polygons internally.

Geometry is exported from the corrected 3D model authorised by the engineer after the marked missing-column corrections. All three B1 beams extend across the full 14.6 m building width per the engineer correction of 25 October 2026. The roof-end central columns are restored; rear column continuity and paired corner yoke antennas are included. Facade grids and unmeasured equipment dimensions remain photograph-based approximations. The observed C2 section does not establish its hidden embedded full size. This is a visual surface model, not a structural analysis/fabrication model.
'''
(O/'MODEL-README.txt').write_text(readme)
with zipfile.ZipFile(O/(stem+'-obj-mtl.zip'),'w',zipfile.ZIP_DEFLATED) as z:
 for name in [stem+'.obj',stem+'.mtl','MODEL-README.txt','export-validation.json']:z.write(O/name,name)
print(json.dumps(report))
