"""Export approved shared mesh to self-contained OBJ/MTL, mm and Z up."""
from pathlib import Path
import json,hashlib,collections,re
P=Path(__file__).resolve().parents[1];B=P/'model';O=P/'drawings'
d=json.loads((B/'mesh.json').read_text())
# Omit the explanatory floor proxy; retain the actual access opening and floor.
selected=[(f,g,m) for f,g,m in zip(d['faces'],d['groups'],d['materials']) if not g.startswith('interior_review')]
used_indices=sorted({i for f,g,m in selected for i in f});remap={old:i+1 for i,old in enumerate(used_indices)}
d['vertices']=[d['vertices'][i-1] for i in used_indices];d['faces']=[[remap[i] for i in f] for f,g,m in selected];d['groups']=[g for f,g,m in selected];d['materials']=[m for f,g,m in selected]
assert not any(g.startswith('interior_review') for g in d['groups'])
stem='7145-saffron-walden-tower';obj=O/(stem+'.obj');mtl=O/(stem+'.mtl')
with mtl.open('w') as f:
 f.write('# Project 7145 Saffron Walden Tower; flat colours; no external textures\n')
 for name,rgb in d['colors'].items():
  f.write(f'\nnewmtl {name}\nKa 0.15 0.15 0.15\nKd '+' '.join(f'{c:.8f}' for c in rgb)+'\nKs 0.05 0.05 0.05\nNs 10\nd 1\nillum 2\n')
parts=collections.defaultdict(list)
for face,group,material in zip(d['faces'],d['groups'],d['materials']):parts[(group,material)].append(face)
with obj.open('w') as f:
 f.write('# Project 7145 Saffron Walden Tower — Export authorised by engineer after requested corrections\n# Units:millimetres; Xeast,Ynorth,Zup; grounddatumZ0\n# Origin: southwest internal corner projected to ground, with GA plan rotation\nmtllib '+mtl.name+'\ns off\n')
 for v in d['vertices']:f.write('v '+' '.join(f'{x:.8f}' for x in v)+'\n')
 for (group,material),faces in parts.items():
  group=re.sub(r'[^A-Za-z0-9_]+','_',group);f.write(f'\no {group}\ng {group}\nusemtl {material}\n')
  for face in faces:f.write('f '+' '.join(str(i) for i in face)+'\n')
# Independent lexical readback of written files.
import numpy as np
verts=[];faces=[];used=set();groups=set();current_material=None;libraries=[]
for ln in obj.read_text().splitlines():
 t=ln.split()
 if not t or t[0].startswith('#'):continue
 if t[0]=='v':assert len(t)==4;verts.append([float(x) for x in t[1:]])
 elif t[0]=='f':
  ix=[int(x.split('/')[0]) for x in t[1:]];assert len(ix)>=3;faces.append(ix);assert current_material;used.add(current_material)
 elif t[0]=='usemtl':current_material=t[1]
 elif t[0]=='mtllib':libraries.append(t[1])
 elif t[0]=='g':groups.add(t[1])
materials={};cur=None
for ln in mtl.read_text().splitlines():
 t=ln.split()
 if not t or t[0].startswith('#'):continue
 if t[0]=='newmtl':cur=t[1];assert cur not in materials;materials[cur]={}
 elif t[0]=='Kd':assert cur;rgb=[float(c) for c in t[1:]];assert len(rgb)==3 and all(0<=c<=1 for c in rgb);materials[cur]['Kd']=rgb
 elif t[0].startswith('map_'):raise AssertionError('Unexpected external texture')
v=np.array(verts);assert np.isfinite(v).all();assert libraries==[mtl.name];assert used<=materials.keys()
assert len(verts)==len(d['vertices']) and len(faces)==len(d['faces']);assert np.allclose(v,np.array(d['vertices']),atol=1e-7,rtol=0)
original=collections.Counter(tuple(f) for f in d['faces']);assert collections.Counter(tuple(f) for f in faces)==original
for ix in faces:
 assert all(1<=i<=len(v) for i in ix);q=v[np.array(ix)-1];assert np.linalg.norm(np.cross(q[1]-q[0],q[2]-q[0]))>1e-5
report={'status':'passed','geometry_source_sha256':hashlib.sha256((B/'mesh.json').read_bytes()).hexdigest(),'vertices':len(verts),'polygon_faces':len(faces),'groups':len(groups),'materials_used':sorted(used),'units':'mm','axes':'Xeast/Ynorth/Zup','textures':'None; self-contained flat colours','readback':'Independent OBJ/MTL lexical readback: vertices, face multiset, valid indices, nonzero face area, materials and relative library path checked'}
report['excluded_view_only_groups']=['interior_review_floor']
(O/'obj-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
