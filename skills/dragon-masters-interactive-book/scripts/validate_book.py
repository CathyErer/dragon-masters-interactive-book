"""Validate portable scene data, local dependencies and the emitted browser data."""
import argparse,json,re
from pathlib import Path
def validate(root):
    errors=[];assets=set()
    def need(condition,message):
        if not condition: errors.append(message)
    def pair(value,label):need(isinstance(value,dict) and all(isinstance(value.get(k),str) and value[k].strip() for k in ['en','zh']),label+' requires en/zh')
    def asset(ref):
        need(isinstance(ref,str),'asset must be a string')
        if not isinstance(ref,str):return
        p=Path(ref);need(not p.is_absolute() and '..' not in p.parts and not re.match(r'\w+:',ref),'unsafe asset path')
        need((root/p).is_file(),'missing asset '+ref);assets.add(ref)
    def point(p):need(isinstance(p,list) and len(p)==2 and all(isinstance(x,(float,int)) and 0<=x<=100 for x in p),'coordinates must be [0..100,0..100]')
    try:
        data=json.loads((root/'story.json').read_text(encoding='utf-8'));js=(root/'story.js').read_text(encoding='utf-8');emitted=json.loads(js.removeprefix('window.BOOK = ').rstrip().removesuffix(';'))
        need(data==emitted,'story.js stale; run sync_story.py');need(data['schemaVersion']==1,'unknown schema');need(isinstance(data.get('id'),str) and bool(data['id']),'missing book id');pair(data['title'],'title');need(bool(data['scenes']),'no scenes')
        ids=[]
        for s in data['scenes']:
            ids.append(s['id']);asset(s['image']);need(bool(s['alt']),'missing alt');need(bool(s['source']),'missing source locator')
            for k in ['title','reading','caption','instruction','result']:pair(s[k],k)
            if s.get('afterImage'):asset(s['afterImage']);need(bool(s.get('afterAlt')),'missing result alt')
            need(s['music'] in data['music'],'unknown mood')
            if s.get('resultMusic'):need(s['resultMusic'] in data['music'],'unknown result mood')
            a=s['action'];need(a['type'] in ['observe','drag','hold','trace','advance','track'],'unsupported action');pair(a['label'],'action label')
            if a['type']=='drag':point(a['from']);point(a['to']);asset(a['sprite']);need(0<a['radius']<30,'invalid drag radius');need(0<a.get('width',8)<=50 and 0<a.get('aspectRatio',1)<=10,'invalid drag geometry')
            elif a['type']=='track':asset(a['sprite']);need(isinstance(a.get('path'),str) and a['path'].startswith('M') and len(a['path'])>5,'track needs SVG path');need(0<a.get('width',18)<=50,'invalid track width')
            elif a['type']=='trace':need(len(a['points'])>=2,'trace needs points');[point(p) for p in a['points']]
            elif a['type']!='advance':point(a['at']);need(200<=a['duration']<=15000,'invalid hold duration')
            if s.get('decoration'):asset(s['decoration']['sprite']);point(s['decoration']['at']);need(0<s['decoration'].get('width',8)<=50 and 0<s['decoration'].get('aspectRatio',1)<=10,'invalid decoration geometry')
            if s.get('retell'):
                t=s['retell'];pair(t['prompt'],'retell prompt');itemids=[i['id'] for i in t['items']];need(len(itemids)>=2 and len(set(itemids))==len(itemids),'invalid retell items');need(len(t['order'])==len(itemids) and set(t['order'])==set(itemids),'invalid retell order');[pair(i['text'],'retell item') for i in t['items']]
            if not s.get('quiz'):continue
            q=s['quiz'];pair(q['question'],'question');pair(q['hint'],'hint');opts=[o['id'] for o in q['options']];need(len(opts)>=2 and len(opts)==len(set(opts)),'duplicate/few options');need(q['answer'] in opts,'answer missing');[pair(o['text'],'option') for o in q['options']]
        need(len(ids)==len(set(ids)),'duplicate scene IDs')
        for ref in data['music'].values():asset(ref)
        for file in ['index.html','app.js','style.css','track-flight.js']:need((root/file).is_file(),'missing runtime '+file)
    except (OSError,ValueError,KeyError,TypeError,AttributeError,IndexError) as e:errors.append(type(e).__name__+': '+str(e))
    return {'ok':not errors,'errors':errors,'assets':len(assets)}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('directory',type=Path);a=p.parse_args();r=validate(a.directory);print(json.dumps(r,ensure_ascii=False));raise SystemExit(0 if r['ok'] else 1)
