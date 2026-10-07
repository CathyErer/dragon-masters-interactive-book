"""Create an explicit demo or a source-required production workspace."""
import argparse, csv, json, shutil, uuid
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--destination',type=Path,required=True)
p.add_argument('--profile',choices=['dm1','original','demo'],default='dm1')
p.add_argument('--title',default='Rise of the Earth Dragon')
a=p.parse_args()
if a.destination.exists():raise SystemExit('Destination exists; choose a new directory.')
source=Path(__file__).resolve().parents[1]/'assets/starter'
if a.profile=='demo':
 shutil.copytree(source,a.destination)
 data=json.loads((a.destination/'story.json').read_text())
 data['id']='demo-'+uuid.uuid4().hex[:12]
 for name,content in [('story.json',json.dumps(data,ensure_ascii=False,indent=2)+'\n'),('story.js','window.BOOK = '+json.dumps(data,ensure_ascii=False,indent=2)+';\n')]:
  (a.destination/name).write_text(content,encoding='utf-8')
 print('Created ORIGINAL DEMO; not the requested source book: '+str(a.destination))
else:
 a.destination.mkdir(parents=True)
 shutil.copytree(source,a.destination/'engine-reference')
 (a.destination/'qa').mkdir()
 for name,content in {
 'SOURCE.md':'# Source and input gaps\n\nTitle: '+a.title+'\n\nEdition, readable source, page mapping, permitted use and visual references: 待补\n',
 'character-bible.md':'# Character bible\n\nRecord verified identity, source locator, reference IDs, scale and approved art. 待补\n',
 'scene-state-table.json':'[]\n','music-cues.json':'[]\n','art-provenance.json':'[]\n','prompts.jsonl':'',
 'qa/report.json':json.dumps({'runtimeSha256':{},'checks':[]},indent=2)+'\n'
 }.items():(a.destination/name).write_text(content,encoding='utf-8')
 with (a.destination/'chapter-evidence.csv').open('w',newline='',encoding='utf-8') as f:
  csv.writer(f).writerow(['chapter_id','event_id','locator','fact','kind','status'])
 data={'version':1,'profile':a.profile,'title':a.title,'status':'planning','source':{'edition':'','coverage':'missing','permittedUse':''},'bookDirectory':'book','qaReport':'qa/report.json','chapters':[]}
 if a.profile=='dm1':
  data['chapters']=[{'id':f'ch{i:02}','sourceStatus':'missing','requiredEvents':[],'sceneIds':[],'quizSceneId':None,'retellSceneId':None} for i in range(1,17)]
 (a.destination/'production.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Created PLANNING workspace. Read the source, fill records, then build book/: '+str(a.destination))
