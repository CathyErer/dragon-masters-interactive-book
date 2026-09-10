'use strict';
const bookData=window.BOOK, $=id=>document.getElementById(id);
const key='interactive-book:'+bookData.id, musicKey=key+':mute';
const reduce=matchMedia('(prefers-reduced-motion: reduce)');
const fresh=()=>({version:1,index:0,language:'en',steps:{},orders:{}});
let state=fresh(),opened=false,epoch=0,abort=new AbortController(),gestureCancel=()=>{},picked=false;
try{const saved=JSON.parse(localStorage.getItem(key));if(saved?.version===1&&Number.isInteger(saved.index)&&saved.index>=0&&saved.index<bookData.scenes.length){state={...fresh(),...saved,language:saved.language==='both'?'both':'en',steps:saved.steps||{},orders:saved.orders||{}};}}catch{}
function save(){try{localStorage.setItem(key,JSON.stringify(state));}catch{$('status').textContent='Storage unavailable: progress lasts only in this tab.';}}
function esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function text(t){return esc(t?.en||'')+(state.language==='both'&&t?.zh?'<span class="cn">'+esc(t.zh)+'</span>':'');}
function label(en,zh){return state.language==='both'?en+' · '+zh:en;}
function listen(el,event,fn){el.addEventListener(event,fn,{signal:abort.signal});}
function button(en,zh,fn,parent=$('panel')){const b=document.createElement('button');b.textContent=label(en,zh);listen(b,'click',fn);parent.append(b);return b;}
function at(el,p){el.style.left=p[0]+'%';el.style.top=p[1]+'%';}
function point(e){const r=$('stage').getBoundingClientRect();return [(e.clientX-r.left)*100/r.width,(e.clientY-r.top)*100/r.height];}
function distance(a,b){return Math.hypot(a[0]-b[0],a[1]-b[1]);}
const images=new Map();
function decode(src){if(!images.has(src)){const img=new Image();images.set(src,new Promise((ok,fail)=>{img.onload=()=>img.decode().then(()=>ok(img),fail);img.onerror=()=>fail(Error('Image unavailable: '+src));img.src=src;}).catch(e=>{images.delete(src);throw e;}));}return images.get(src);}
const score={muted:false,current:null,retiring:new Set(),token:0,mood:null,
 stop(){this.token++;if(this.current){this.current.pause();this.current=null;}for(const a of this.retiring)a.pause();this.retiring.clear();this.mood=null;},
 async set(mood){if(!opened||this.muted||document.hidden){this.stop();return;}if(this.mood===mood&&this.current&&!this.current.paused)return;const src=bookData.music[mood];if(!src)return;const token=++this.token,old=this.current,a=new Audio(src);a.loop=true;a.volume=0;this.current=a;this.mood=mood;if(old)this.retiring.add(old);try{await a.play();}catch{if(token===this.token){$('status').textContent=label('Click Music to enable audio.','点击Music启用声音。');this.stop();}return;}if(token!==this.token){a.pause();return;}const start=performance.now(),oldVolume=old?.volume||0;const fade=now=>{if(token!==this.token){if(old){old.pause();this.retiring.delete(old);}return;}const t=Math.max(0,Math.min(1,(now-start)/1300));a.volume=.16*t;if(old)old.volume=oldVolume*(1-t);if(t<1)requestAnimationFrame(fade);else if(old){old.pause();this.retiring.delete(old);}};requestAnimationFrame(fade);}
};
try{score.muted=localStorage.getItem(musicKey)==='true';}catch{}
function musicUI(){$('music').textContent=score.muted?label('Music off','音乐关'):label('Music on','音乐开');$('music').setAttribute('aria-pressed',String(!score.muted));}
function mood(){const s=bookData.scenes[state.index],step=state.steps[s.id]||0;return step>0&&s.resultMusic?s.resultMusic:s.music;}
function commit(){const s=bookData.scenes[state.index];gestureCancel();state.steps[s.id]=1;save();render();}
function resetGesture(){gestureCancel();picked=false;}
function prop(src,p,interactive=false){const el=document.createElement(interactive?'button':'div');el.className=interactive?'prop':'placed';const img=new Image();img.src=src;img.alt='';img.draggable=false;el.append(img);at(el,p);$('layers').append(el);return el;}
function circle(p,t){const el=document.createElement('button');el.className='hotspot';el.setAttribute('aria-label',t.en);el.innerHTML='<span>'+text(t)+'</span>';at(el,p);$('layers').append(el);return el;}
function gesture(action){
 if(action.type==='drag'){
  const target=document.createElement('div');target.className='target';at(target,action.to);$('layers').append(target);
  const el=prop(action.sprite,action.from,true);el.setAttribute('aria-label',action.label.en);let dragging=false;
  const cancel=()=>{dragging=false;picked=false;at(el,action.from);el.style.filter='';};gestureCancel=cancel;
  listen(el,'pointerdown',e=>{if(e.button!==0)return;e.preventDefault();dragging=true;el.setPointerCapture(e.pointerId);});
  listen(el,'pointermove',e=>{if(dragging)at(el,point(e));});
  listen(el,'pointerup',e=>{if(!dragging)return;dragging=false;if(distance(point(e),action.to)<=action.radius)commit();else{cancel();$('status').textContent=label('Not there yet. Try the empty socket.','还没放好，再试试空位。');}});
  listen(el,'pointercancel',cancel);listen(el,'lostpointercapture',()=>{if(dragging)cancel();});
  listen(el,'click',e=>{if(e.detail===0){if(picked)commit();else{picked=true;el.style.filter='brightness(1.5)';$('status').textContent=label('Gear picked up. Press Enter again to place.','已拿起，再按Enter放置。');}}});
  button('Pick up / place with keyboard','键盘拿起／放置',()=>{if(picked)commit();else{picked=true;$('status').textContent=label('Picked up. Activate again to place.','已拿起，再次按下放置。');}});return;
 }
 if(action.type==='trace'){
  const ns='http://www.w3.org/2000/svg',svg=document.createElementNS(ns,'svg');svg.classList.add('trace');svg.setAttribute('viewBox','0 0 100 100');svg.setAttribute('preserveAspectRatio','none');const path=document.createElementNS(ns,'path');path.setAttribute('d','M'+action.points.map(p=>p.join(',')).join(' L'));svg.append(path);$('layers').append(svg);let tracing=false,next=0;
  gestureCancel=()=>{tracing=false;next=0;};listen(svg,'pointerdown',e=>{if(e.button===0&&distance(point(e),action.points[0])<7){tracing=true;next=1;svg.setPointerCapture(e.pointerId);}});listen(svg,'pointermove',e=>{if(tracing&&next<action.points.length&&distance(point(e),action.points[next])<7){next++;path.style.stroke='#fff1a0';}});listen(svg,'pointerup',()=>{if(tracing&&next===action.points.length)commit();else resetGesture();});listen(svg,'pointercancel',()=>resetGesture());button('Follow path with keyboard','键盘循迹',commit);return;
 }
 const el=circle(action.at,action.label);let raf=0,start=0,active=false;
 const cancel=()=>{active=false;cancelAnimationFrame(raf);el.classList.remove('pressing');el.style.setProperty('--progress','0deg');};gestureCancel=cancel;
 const tick=now=>{if(!active)return;const progress=Math.min(1,(now-start)/action.duration);el.style.setProperty('--progress',progress*360+'deg');if(progress===1)commit();else raf=requestAnimationFrame(tick);};
 const begin=()=>{if(active)return;active=true;start=performance.now();el.classList.add('pressing');raf=requestAnimationFrame(tick);};
 if(action.type==='observe'){listen(el,'pointerenter',begin);listen(el,'pointerleave',cancel);listen(el,'focus',begin);listen(el,'blur',cancel);button('Inspect with keyboard','键盘观察',commit);}
 else {listen(el,'pointerdown',e=>{if(e.button===0){e.preventDefault();el.setPointerCapture(e.pointerId);begin();}});listen(el,'pointerup',cancel);listen(el,'pointercancel',cancel);listen(el,'lostpointercapture',cancel);listen(el,'pointermove',e=>{if(active&&distance(point(e),action.at)>13)cancel();});listen(el,'keydown',e=>{if(['Enter',' '].includes(e.key)){e.preventDefault();begin();}});listen(el,'keyup',cancel);listen(el,'blur',cancel);button('Turn with keyboard','键盘转动',commit);}
}
function order(s){const ids=s.quiz.options.map(x=>x.id),stored=state.orders[s.id];if(stored?.length===ids.length&&new Set(stored).size===ids.length&&stored.every(x=>ids.includes(x)))return stored;const shuffled=[...ids];for(let i=shuffled.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[shuffled[i],shuffled[j]]=[shuffled[j],shuffled[i]];}state.orders[s.id]=shuffled;save();return shuffled;}
async function render(){
 resetGesture();abort.abort();gestureCancel=()=>{};abort=new AbortController();const token=++epoch,s=bookData.scenes[state.index],step=state.steps[s.id]||0;
 $('bookTitle').innerHTML=text(bookData.title);$('chapterNumber').textContent=label('SCENE','场景')+' '+String(state.index+1).padStart(2,'0');$('chapterTitle').innerHTML=text(s.title);$('progress').textContent=(state.index+1)+' / '+bookData.scenes.length;$('reading').innerHTML=text(s.reading);$('readLabel').textContent=label('Read story','阅读故事');$('language').textContent=state.language==='en'?'EN / 中英':'中英 / EN';musicUI();
 $('chapters').replaceChildren();bookData.scenes.forEach((scene,i)=>{const li=document.createElement('li'),b=document.createElement('button');b.textContent=String(i+1);b.setAttribute('aria-label','Scene '+(i+1));b.setAttribute('aria-current',String(i===state.index));b.disabled=i>0&&(state.steps[bookData.scenes[i-1].id]||0)<3;listen(b,'click',()=>{state.index=i;save();render();});li.append(b);$('chapters').append(li);});
 $('layers').replaceChildren();$('panel').replaceChildren();$('caption').replaceChildren();$('page').classList.add('loading');
 try{const src=step>0&&s.afterImage?s.afterImage:s.image;await decode(src);if(token!==epoch)return;$('scene').src=src;$('scene').alt=step>0&&s.afterAlt?s.afterAlt:s.alt;$('page').classList.remove('loading');}catch{if(token!==epoch)return;$('panel').innerHTML='<p class="error">'+label('Scene image could not load. Check the local art file.','场景图加载失败，请检查素材文件。')+'</p>';button('Retry','重试',render);return;}
 score.set(mood());if(s.decoration)prop(s.decoration.sprite,s.decoration.at);if(step>0&&s.action.type==='drag')prop(s.action.sprite,s.action.to);
 if(step===0){$('caption').innerHTML=text(s.caption);const p=document.createElement('p');p.innerHTML=text(s.instruction);$('panel').append(p);gesture(s.action);}
 else if(step===1){$('caption').innerHTML=text(s.result);const p=document.createElement('p');p.innerHTML=text({en:'Look at what changed. Continue when you are ready.',zh:'观察发生的变化，准备好再继续。'});$('panel').append(p);button('Story check →','理解检查',()=>{state.steps[s.id]=2;save();render();});}
 else if(step===2){const q=document.createElement('div');q.className='quiz';q.innerHTML='<h2>'+text(s.quiz.question)+'</h2><div class="options"></div><p class="hint" role="status"></p>';$('panel').append(q);let wrong=0;for(const id of order(s)){const o=s.quiz.options.find(x=>x.id===id),b=document.createElement('button');b.dataset.option=id;b.innerHTML=text(o.text);listen(b,'click',()=>{if(id===s.quiz.answer){state.steps[s.id]=3;save();render();}else{wrong++;q.querySelector('.hint').innerHTML=text(s.quiz.hint);if(wrong===3)button('Review the scene','回看场景',()=>{state.steps[s.id]=1;save();render();},q);}});q.querySelector('.options').append(b);}}
 else {$('caption').innerHTML=text(s.result);const p=document.createElement('p');p.innerHTML=text({en:state.index===bookData.scenes.length-1?'The end. Look → repair → turn → light. Tell the story in your own words.':'Evidence found. The story continues.',zh:state.index===bookData.scenes.length-1?'完。观察→修理→转动→亮灯。用自己的话说说这个故事。':'已找到证据，故事继续。'});$('panel').append(p);button(state.index===bookData.scenes.length-1?'Close the book':'Next scene →',state.index===bookData.scenes.length-1?'合上书':'下一幕',()=>{if(state.index===bookData.scenes.length-1)closeBook();else{state.index++;save();render();}});}
}
function closeBook(){opened=false;epoch++;resetGesture();abort.abort();score.stop();$('book').hidden=true;$('cover').hidden=false;$('open').focus();}
$('open').addEventListener('click',()=>{opened=true;$('cover').hidden=true;$('book').hidden=false;render();});
$('close').addEventListener('click',closeBook);
$('language').addEventListener('click',()=>{state.language=state.language==='en'?'both':'en';save();if(opened)render();});
$('music').addEventListener('click',()=>{score.muted=!score.muted;try{localStorage.setItem(musicKey,String(score.muted));}catch{}musicUI();score.set(mood());});
$('restart').addEventListener('click',()=>{if(confirm('Restart this story? Saved progress for this book will be cleared.')){state=fresh();save();render();}});
window.addEventListener('blur',resetGesture);document.addEventListener('visibilitychange',()=>{resetGesture();if(document.hidden)score.stop();else score.set(mood());});reduce.addEventListener('change',()=>{if(opened)render();});musicUI();
