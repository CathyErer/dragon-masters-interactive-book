"""Create the source-required DM1 production workspace only."""
import argparse, csv, json, shutil, uuid
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--destination',type=Path,required=True)
a=p.parse_args()
if a.destination.exists():raise SystemExit('Destination exists; choose a new directory.')
source=Path(__file__).resolve().parents[1]/'assets/starter'
a.destination.mkdir(parents=True)
engine=a.destination/'engine-reference';engine.mkdir()
for name in ['index.html','style.css','app.js','track-flight.js']:shutil.copy2(source/name,engine/name)
blank={'schemaVersion':1,'id':'dm1-'+uuid.uuid4().hex[:12],'title':{'en':'Rise of the Earth Dragon','zh':'Dragon Masters 第一本'},'description':{'en':'DM1 source and scenes are awaiting verification.','zh':'DM1原书与场景资料待核对。'},'music':{},'scenes':[]}
(engine/'story.json').write_text(json.dumps(blank,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(engine/'story.js').write_text('window.BOOK = '+json.dumps(blank,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
(a.destination/'qa').mkdir()
for name,content in {
'SOURCE.md':'# Source and input gaps\n\nTitle: '+'Rise of the Earth Dragon'+'\n\nEdition, readable source, page mapping, permitted use and visual references: 待补\n',
'character-bible.md':'# Character bible\n\nRecord verified identity, source locator, reference IDs, scale and approved art. 待补\n',
'scene-state-table.json':'[]\n','music-cues.json':'[]\n','art-provenance.json':'[]\n','prompts.jsonl':'',
'qa/report.json':json.dumps({'runtimeSha256':{},'checks':[]},indent=2)+'\n'
}.items():(a.destination/name).write_text(content,encoding='utf-8')
with (a.destination/'chapter-evidence.csv').open('w',newline='',encoding='utf-8') as f:
 csv.writer(f).writerow(['chapter_id','event_id','locator','fact','kind','status'])
data={'version':1,'profile':'dm1','title':'Rise of the Earth Dragon','status':'planning','source':{'edition':'','coverage':'missing','permittedUse':''},'bookDirectory':'book','qaReport':'qa/report.json','chapters':[]}
data['chapters']=[{'id':f'ch{i:02}','sourceStatus':'missing','requiredEvents':[],'sceneIds':[],'quizSceneId':None,'retellSceneId':None} for i in range(1,17)]
(a.destination/'production.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Created PLANNING workspace. Read the source, fill records, then build book/: '+str(a.destination))
