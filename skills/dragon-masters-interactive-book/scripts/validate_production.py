"""Check full-book coverage and current QA evidence, never assert source truth."""
import argparse,csv,hashlib,json
from pathlib import Path
from validate_book import validate

def runtime_hashes(book):
 return {p.relative_to(book).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(book.rglob('*')) if p.is_file()}

def validate_production(root, *, require_dm1=True):
 errors=[]
 def need(ok,msg):
  if not ok:errors.append(msg)
 def read(name):return json.loads((root/name).read_text(encoding='utf-8'))
 def local(base,ref):
  p=(base/ref).resolve()
  if p!=base.resolve() and base.resolve() not in p.parents:raise ValueError('Path escapes project: '+str(ref))
  return p
 try:
  m=read('production.json');need(not require_dm1 or m['profile']=='dm1','this production Skill only accepts DM1');need(m['status']=='complete','production is not complete')
  need(m['source']['coverage']=='complete' and bool(m['source']['edition']) and bool(m['source']['permittedUse']),'source coverage/edition/permission missing')
  for name in ['SOURCE.md','character-bible.md']:need(bool((root/name).read_text().strip()),'missing '+name)
  book=local(root,m['bookDirectory']);runtime=validate(book);errors.extend(runtime['errors'])
  data=json.loads((book/'story.json').read_text());need(not data['id'].startswith(('demo-','fog-')),'demo id is not production')
  scenes=data['scenes'];ids=[s['id'] for s in scenes];byid={s['id']:s for s in scenes}
  plan=read('scene-state-table.json');need([s['id'] for s in plan]==ids,'scene table order differs from runtime')
  for i,s in enumerate(plan):
   actual=byid.get(s['id'],{})
   need(s['chapterId']==actual.get('chapterId') and s['eventIds']==actual.get('eventIds'),'scene event/chapter mapping mismatch '+s['id'])
   need(bool(s['action']) and bool(s['result']) and isinstance(s['entry'],dict) and bool(s['entry']) and isinstance(s['exit'],dict) and bool(s['exit']),'incomplete state plan '+s['id'])
   need(s['next']==(plan[i+1]['id'] if i+1<len(plan) else None),'bad next scene '+s['id'])
   if i+1<len(plan):need(s['exit']==plan[i+1]['entry'],'unexplained state discontinuity '+s['id'])
  with (root/'chapter-evidence.csv').open(newline='',encoding='utf-8') as f:evidence=list(csv.DictReader(f))
  verified={(e['chapter_id'],e['event_id']) for e in evidence if e['status']=='verified' and e['locator'].strip() and e['fact'].strip() and e['kind']=='source'}
  chapters=m['chapters'];chapter_ids=[c['id'] for c in chapters]
  need(len(chapter_ids)>0 and len(chapter_ids)==len(set(chapter_ids)),'missing/duplicate chapters')
  if m['profile']=='dm1':need(chapter_ids==[f'ch{i:02}' for i in range(1,17)],'DM1 requires ordered ch01..ch16')
  collected=[]
  for c in chapters:
   cid=c['id'];need(c['sourceStatus']=='verified','unverified chapter '+cid);need(bool(c['requiredEvents']) and len(c['requiredEvents'])==len(set(c['requiredEvents'])),'missing/duplicate required events '+cid)
   seq=c['sceneIds'];collected+=seq;need(bool(seq),'empty chapter '+cid)
   covered=set()
   for sid in seq:
    s=byid.get(sid,{});need(s.get('chapterId')==cid,'chapter mismatch '+sid);covered.update(s.get('eventIds',[]))
   for event in c['requiredEvents']:
    need((cid,event) in verified,'no source evidence '+cid+'/'+event);need(event in covered,'event not rendered '+cid+'/'+event)
   for event in covered:need(event in c['requiredEvents'],'runtime event not planned '+cid+'/'+event)
   quizzes=[sid for sid in seq if byid.get(sid,{}).get('quiz')]
   need(quizzes==[c['quizSceneId']],'expected one chapter quiz '+cid)
   if m['profile']=='dm1' and quizzes:need(len(byid[quizzes[0]]['quiz']['options'])==3,'DM1 quiz requires three choices '+cid)
   retells=[sid for sid in seq if byid.get(sid,{}).get('retell')]
   expected=c.get('retellSceneId')
   need(retells==([expected] if expected else []),'retell mapping mismatch '+cid)
   if m['profile']=='dm1':need(bool(expected)==(cid in ['ch04','ch08','ch12','ch16']),'DM1 optional retell missing/extra '+cid)
  need(collected==ids,'chapter scene list must cover runtime once, in order')
  prompts=[json.loads(line) for line in (root/'prompts.jsonl').read_text().splitlines() if line.strip()];prompt_ids={p['id'] for p in prompts}
  need(len(prompt_ids)==len(prompts) and len(prompts)>0,'missing/duplicate prompts')
  for p in prompts:need(bool(p['prompt']) and bool(p['tool']) and p['review']=='accepted','unfinished prompt '+p['id'])
  provenance=read('art-provenance.json');paths={p['path'] for p in provenance};used=set(data['music'].values())
  for s in scenes:
   used.add(s['image'])
   if s.get('afterImage'):used.add(s['afterImage'])
   if s['action'].get('sprite'):used.add(s['action']['sprite'])
   if s.get('decoration'):used.add(s['decoration']['sprite'])
  need(used<=paths,'runtime assets missing provenance: '+', '.join(sorted(used-paths)))
  for p in provenance:
   need(local(book,p['path']).is_file(),'provenance asset missing '+p['path']);need(p['promptId'] in prompt_ids and bool(p['origin']) and bool(p['rights']) and p['review']=='accepted','unreviewed asset '+p['path'])
  cues=read('music-cues.json');need([c['sceneId'] for c in cues]==ids,'music cue coverage/order mismatch')
  for c in cues:
   s=byid[c['sceneId']];need(c['before']==s['music'] and c['after']==s.get('resultMusic',s['music']) and bool(c['reason']),'music event mismatch '+s['id'])
  qa=json.loads(local(root,m['qaReport']).read_text());need(qa['runtimeSha256']==runtime_hashes(book),'QA runtime hashes stale or incomplete')
  checks={c['name']:c for c in qa['checks']}
  for name in ['source-evidence','normal-route','reduced-motion-route','language-reload','input-cancellation','asset-failure-retry','quiz-no-leak','visual-review','music-listening']:
   c=checks.get(name,{});need(c.get('status')=='pass' and bool(c.get('evidence')),'required QA not passed: '+name)
 except (OSError,ValueError,KeyError,TypeError,AttributeError,IndexError) as e:errors.append(type(e).__name__+': '+str(e))
 return {'ok':not errors,'errors':errors,'scope':'Structural coverage and recorded evidence only; source facts, art and listening need actual review.'}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('project',type=Path);p.add_argument('--hash-runtime',action='store_true');a=p.parse_args()
 if a.hash_runtime:print(json.dumps(runtime_hashes(a.project),indent=2))
 else:
  report=validate_production(a.project);print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(0 if report['ok'] else 1)
