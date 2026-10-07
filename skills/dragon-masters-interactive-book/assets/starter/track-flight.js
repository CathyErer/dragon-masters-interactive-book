/* Standalone fixed-track sprite movement. No book text, private IDs or assets. */
'use strict';
window.mountTrackFlight=function({container,sprite,path,width=20,label='Follow the path',onComplete=()=>{},signal,completed=false}){
 const ns='http://www.w3.org/2000/svg',svg=document.createElementNS(ns,'svg');
 svg.setAttribute('viewBox','0 0 1000 1000');svg.setAttribute('preserveAspectRatio','none');svg.setAttribute('aria-hidden','true');svg.style.cssText='position:absolute;inset:0;width:100%;height:100%;pointer-events:none';
 const route=document.createElementNS(ns,'path');route.setAttribute('d',path);route.setAttribute('fill','none');route.setAttribute('stroke','#f5dda1');route.setAttribute('stroke-width','2');route.setAttribute('vector-effect','non-scaling-stroke');route.setAttribute('stroke-dasharray','4 6');svg.append(route);container.append(svg);
 const el=document.createElement('button');el.type='button';el.setAttribute('aria-label',label+'; arrows follow, Enter finishes, Escape cancels');el.style.cssText=`position:absolute;left:0;top:0;width:${width}%;padding:0;border:0;background:none;touch-action:none;will-change:transform;transition:none;cursor:grab`;
 const img=new Image();img.src=sprite;img.alt='';img.draggable=false;img.style.cssText='display:block;width:100%;pointer-events:none';el.append(img);container.append(el);
 if(completed){el.disabled=true;svg.style.opacity='0';}
 const controller=new AbortController(),listen=(target,event,fn)=>target.addEventListener(event,fn,{signal:controller.signal});
 const count=400,len=route.getTotalLength(),pts=Array.from({length:count+1},(_,i)=>route.getPointAtLength(len*i/count));
 let progress=completed?count:0,start=null,id=null,offset=null,frame=0,done=completed,rect=container.getBoundingClientRect();
 const position=()=>{const i=Math.min(count-1,Math.floor(progress)),t=progress-i;return {x:pts[i].x+(pts[i+1].x-pts[i].x)*t,y:pts[i].y+(pts[i+1].y-pts[i].y)*t};};
 const draw=()=>{frame=0;const p=position();el.style.transform=`translate3d(${p.x*rect.width/1000}px,${p.y*rect.height/1000}px,0) translate(-50%,-50%)`;el.dataset.progress=String(progress/count);};
 const paint=()=>{if(!frame)frame=requestAnimationFrame(draw);};
 const move=(x,y)=>{const r=rect,p=position(),gap=Math.hypot((p.x-x)*r.width/1000,(p.y-y)*r.height/1000),windowSize=Math.min(80,Math.max(18,Math.ceil(gap*count/(len*Math.min(r.width,r.height)/1000)*1.5)+6));let best=progress,distance=Infinity;
  for(let i=Math.max(0,Math.floor(progress-windowSize));i<Math.min(count,Math.ceil(progress+windowSize));i++){const a=pts[i],b=pts[i+1],dx=(b.x-a.x)*r.width/1000,dy=(b.y-a.y)*r.height/1000,ux=(x-a.x)*r.width/1000,uy=(y-a.y)*r.height/1000,t=Math.max(0,Math.min(1,(ux*dx+uy*dy)/(dx*dx+dy*dy||1))),d=Math.hypot(ux-dx*t,uy-dy*t);if(d<distance){best=i+t;distance=d;}}
  if(distance<=32){progress=best;paint();}
 };
 const stop=(commit=false)=>{if(start===null)return;if(!commit)progress=start;start=null;const captured=id;id=null;offset=null;if(frame)cancelAnimationFrame(frame);draw();if(captured!==null&&el.hasPointerCapture(captured))el.releasePointerCapture(captured);if(commit&&progress>=count-3&&!done){done=true;el.disabled=true;svg.style.opacity='0';onComplete();}};
 listen(el,'pointerdown',e=>{if(e.button!==0||done||id!==null)return;e.preventDefault();el.focus();rect=container.getBoundingClientRect();const p=position();start=progress;id=e.pointerId;offset={x:(e.clientX-rect.x)/rect.width*1000-p.x,y:(e.clientY-rect.y)/rect.height*1000-p.y};el.setPointerCapture(id);});
 listen(el,'pointermove',e=>{if(e.pointerId===id&&offset)move((e.clientX-rect.x)/rect.width*1000-offset.x,(e.clientY-rect.y)/rect.height*1000-offset.y);});
 listen(el,'pointerup',e=>{if(e.pointerId===id)stop(true);});
 for(const event of ['pointercancel','lostpointercapture','blur'])listen(el,event,()=>stop());
 listen(window,'blur',()=>stop());listen(document,'visibilitychange',()=>{if(document.hidden)stop();});
 listen(window,'scroll',()=>{rect=container.getBoundingClientRect();});
 listen(el,'keydown',e=>{if(id!==null||done)return;const delta={ArrowRight:10,ArrowUp:10,ArrowLeft:-10,ArrowDown:-10}[e.key];if(delta){e.preventDefault();if(start===null)start=progress;progress=Math.max(0,Math.min(count,progress+delta));paint();}else if(['Enter',' '].includes(e.key)){e.preventDefault();stop(true);}else if(e.key==='Escape'){e.preventDefault();stop();}});
 const resize=new ResizeObserver(()=>{stop();rect=container.getBoundingClientRect();paint();});resize.observe(container);draw();
 const destroy=()=>{stop();if(frame)cancelAnimationFrame(frame);resize.disconnect();controller.abort();svg.remove();el.remove();};
 if(signal){if(signal.aborted)destroy();else signal.addEventListener('abort',destroy,{once:true});}
 return {element:el,route,cancel:()=>stop(),destroy};
};
