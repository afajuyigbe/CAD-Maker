"""Publish only this project's review files, preserving the existing repository history."""
from pathlib import Path
import subprocess,os,json,tempfile
ROOT=Path(__file__).resolve().parents[2];os.chdir(ROOT);P=Path('projects/7068-south-water-tower')
assert json.loads((P/'drawings/validation.json').read_text())['status']=='passed'
assert not json.loads((P/'items/water-tower-01/item.json').read_text())['approval_gate']['approved']
assert not list(P.rglob('*.obj')) and not list(P.rglob('*.mtl'))
files=[str(f) for f in P.rglob('*') if f.is_file() and f.suffix not in ['.pyc','.log'] and '__pycache__' not in str(f) and f.name!='7068-roundtrip.dxf']
files+=['assets/branding/ka-logo-survey-source.jpeg','assets/branding/jet-logo-ga-source.jpeg','docs/bespoke-site-items-workflow.md','docs/bespoke-site-items-rules.json','docs/drawing-sheet-standard.md','docs/whole-building-visual-model-workflow.md','templates/bespoke-site-item.json']
def git(*args,env=None,input=None):return subprocess.check_output(['git',*args],env=env,input=input).decode().strip()
branch='review/7068-south-water-tower';existing=git('ls-remote','origin','refs/heads/'+branch)
git('fetch','origin',branch if existing else 'main');parent=git('rev-parse','FETCH_HEAD')
with tempfile.TemporaryDirectory(dir='/tmp') as tmp:
 env=os.environ.copy();env['GIT_INDEX_FILE']=tmp+'/index';git('read-tree',parent,env=env);git('add','--',*files,env=env)
 assert set(git('diff','--cached','--name-only',parent,env=env).splitlines())<=set(files)
 tree=git('write-tree',env=env);commit=git('-c','user.name=Codex','-c','user.email=codex@users.noreply.github.com','commit-tree',tree,'-p',parent,input=b'Create project7068 South Water Tower revision1 review drawings and3D model; holdOBJ/MTL for approval\n')
 git('push','origin',commit+':refs/heads/'+branch);assert git('ls-remote','origin','refs/heads/'+branch).split()[0]==commit
 for f in files:assert git('rev-parse',commit+':'+f)==git('hash-object',f)
print(json.dumps({'commit':commit,'branch':branch,'verified_files':len(files),'OBJ_MTL':'Held for engineer approval'}))
