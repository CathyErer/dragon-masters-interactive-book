"""Exercise actual project creation, dependency gates and stale QA rejection."""
import copy,csv,json,os,subprocess,sys,tempfile
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'skills/dragon-masters-interactive-book/scripts'
sys.path.insert(0,str(SCRIPTS))
from validate_book import validate
from validate_production import validate_production,runtime_hashes
checks=[]
def check(name,ok):
 checks.append({'name':name,'pass':bool(ok)})
 if not ok:raise AssertionError(name)
def write(p,data):p.write_text(json.dumps(data),encoding='utf-8')
def sync(book,data):write(book/'story.json',data);(book/'story.js').write_text('window.BOOK = '+json.dumps(data)+';')
with tempfile.TemporaryDirectory(prefix='book contracts ') as d:
 base=Path(d);project=base/'production';demo=base/'demo';demo2=base/'demo two'
 for p,profile in [(project,'dm1'),(demo,'demo'),(demo2,'demo')]:subprocess.run([sys.executable,str(SCRIPTS/'new_project.py'),'--destination',str(p),'--profile',profile],check=True,stdout=subprocess.DEVNULL)
 check('production never presents demo as book',not (project/'index.html').exists() and not (project/'book').exists())
 check('16 missing chapters stay visible',len(json.loads((project/'production.json').read_text())['chapters'])==16)
 check('incomplete production rejected',not validate_production(project)['ok'])
 check('duplicate destination protected',subprocess.run([sys.executable,str(SCRIPTS/'new_project.py'),'--destination',str(demo)],capture_output=True).returncode!=0)
 check('new demos have independent storage',json.loads((demo/'story.json').read_text())['id']!=json.loads((demo2/'story.json').read_text())['id'])
 check('fresh demo validates',validate(demo)['ok'])
 data=json.loads((demo/'story.json').read_text());bad=copy.deepcopy(data);bad['scenes'][0]['image']='art/missing.svg';sync(demo,bad);check('missing image rejected',not validate(demo)['ok']);sync(demo,data)
 bad=copy.deepcopy(data);bad['scenes'][0]['quiz']=None;bad['scenes'][0]['action']={'type':'advance','label':{'en':'Enter','zh':'进入'}};sync(demo,bad);check('non-quiz advance supported',validate(demo)['ok'])
 bad['scenes'][0]['action']={'type':'track','label':{'en':'Fly','zh':'飞'},'sprite':'art/gear.svg','path':'M100 500 L900 500'};sync(demo,bad);check('integrated track supported',validate(demo)['ok'])
 bad['scenes'][0]['action']['sprite']='missing.svg';sync(demo,bad);check('missing track sprite rejected',not validate(demo)['ok'])
 # Synthetic record fixture only: these pass strings test the gate and claim no actual review.
 import shutil
 book=project/'book';shutil.copytree(demo2,book);data=json.loads((book/'story.json').read_text());data['id']='synthetic-record-fixture';data['scenes']=data['scenes'][:1];s=data['scenes'][0];s['chapterId']='ch01';s['eventIds']=['look'];sync(book,data)
 m={'profile':'original','status':'complete','source':{'coverage':'complete','edition':'synthetic-fixture','permittedUse':'MIT fixture'},'bookDirectory':'book','qaReport':'qa/report.json','chapters':[{'id':'ch01','sourceStatus':'verified','requiredEvents':['look'],'sceneIds':[s['id']],'quizSceneId':s['id'],'retellSceneId':None}]};write(project/'production.json',m)
 (project/'chapter-evidence.csv').write_text('chapter_id,event_id,locator,fact,kind,status\nch01,look,fixture paragraph 1,The learner observes a socket.,source,verified\n')
 write(project/'scene-state-table.json',[{'id':s['id'],'chapterId':'ch01','eventIds':['look'],'entry':{'seen':False},'action':'look','result':'socket observed','exit':{'seen':True},'next':None}])
 write(project/'music-cues.json',[{'sceneId':s['id'],'before':s['music'],'after':s.get('resultMusic',s['music']),'reason':'fixture observation'}])
 (project/'prompts.jsonl').write_text(json.dumps({'id':'fixture','prompt':'synthetic metadata fixture','tool':'local test','review':'accepted'})+'\n')
 paths=set(data['music'].values())|{s['image']}
 if s.get('afterImage'):paths.add(s['afterImage'])
 write(project/'art-provenance.json',[{'path':p,'promptId':'fixture','origin':'bundled original demo test fixture','rights':'MIT','review':'accepted'} for p in sorted(paths)])
 names=['source-evidence','normal-route','reduced-motion-route','language-reload','input-cancellation','asset-failure-retry','quiz-no-leak','visual-review','music-listening']
 write(project/'qa/report.json',{'runtimeSha256':runtime_hashes(book),'checks':[{'name':n,'status':'pass','evidence':'SYNTHETIC VALIDATOR FIXTURE ONLY'} for n in names]})
 check('coherent synthetic records accepted',validate_production(project)['ok'])
 (book/'app.js').write_text((book/'app.js').read_text()+'\n// changed after QA\n');check('stale runtime QA rejected',any('hashes stale' in e for e in validate_production(project)['errors']))
 m['chapters'][0]['requiredEvents'].append('unrendered');write(project/'production.json',m);check('missing event and source evidence rejected',any('event not rendered' in e for e in validate_production(project)['errors']))
 m['profile']='dm1';write(project/'production.json',m);check('short demo cannot count as full DM1',any('ch01..ch16' in e for e in validate_production(project)['errors']))
print(json.dumps({'checks':checks,'scope':'Tool contracts and synthetic gate tests, not full-book content acceptance'},indent=2))
