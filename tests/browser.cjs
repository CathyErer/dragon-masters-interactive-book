// Requires Playwright; set PLAYWRIGHT_MODULE and CHROME_PATH when not on PATH.
const fs=require('node:fs'),path=require('node:path'),{pathToFileURL}=require('node:url');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(process.argv[2]||path.join(__dirname,'../skills/dragon-masters-interactive-book/assets/starter'));
(async()=>{const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH||undefined,args:['--allow-file-access-from-files']});const checks=[],errors=[];
const check=(name,ok)=>{checks.push({name,pass:!!ok});if(!ok)throw Error(name);};
const screenshot=async(page,name)=>{if(process.env.SCREENSHOT_DIR){fs.mkdirSync(process.env.SCREENSHOT_DIR,{recursive:true});await page.screenshot({path:path.join(process.env.SCREENSHOT_DIR,name+'.png')});}};
try{for(const reduced of [false,true]){const page=await browser.newPage({viewport:reduced?{width:1440,height:900}:{width:1280,height:800},reducedMotion:reduced?'reduce':'no-preference'});page.on('pageerror',e=>errors.push(e.message));
await page.goto(pathToFileURL(path.join(root,'index.html')).href);await page.locator('#open').click();await page.waitForFunction(()=>!document.querySelector('.loading'));
if(!reduced)await screenshot(page,'start');
const center=async s=>{const r=await page.locator(s).boundingBox();return {x:r.x+r.width/2,y:r.y+r.height/2};};
const data=JSON.parse(fs.readFileSync(path.join(root,'story.json'),'utf8'));
for(let i=0;i<3;i++){
 const s=data.scenes[i];await page.waitForTimeout(100);
 if(i===0){await page.locator('.hotspot').hover();await page.waitForTimeout(1000);}
 if(i===1){const a=await center('.prop'),b=await center('.target');await page.mouse.move(a.x,a.y);await page.mouse.down();await page.mouse.move(b.x,b.y,{steps:20});check('drag requires release',await page.evaluate(()=>state.steps[bookData.scenes[state.index].id]===undefined));await page.mouse.up();}
 if(i===2){const p=await center('.hotspot');for(let n=0;n<2;n++){await page.mouse.move(p.x,p.y);await page.mouse.down();await page.waitForTimeout(150);await page.evaluate(()=>window.dispatchEvent(new Event('blur')));await page.mouse.up();await page.waitForTimeout(1500);check('repeat blur cancels hold',await page.evaluate(()=>!state.steps[bookData.scenes[state.index].id]));}await page.mouse.move(p.x,p.y);await page.mouse.down();await page.waitForTimeout(1650);await page.mouse.up();}
 await page.waitForTimeout(150);check('result precedes quiz '+i,await page.evaluate(()=>state.steps[bookData.scenes[state.index].id]===1));
 if(i===2&&!reduced)await screenshot(page,'light-result');
 await page.getByRole('button',{name:'Story check →',exact:true}).click();check('quiz hides caption '+i,(await page.locator('#caption').textContent())==='');await page.locator(`[data-option="${s.quiz.answer}"]`).click();await page.waitForTimeout(100);
 if(i<2)await page.getByRole('button',{name:'Next scene →',exact:true}).click();
}
check('all scenes complete',await page.evaluate(()=>Object.values(state.steps).every(s=>s===3)));
await page.locator('#language').click();await page.reload();await page.locator('#open').click();await page.waitForTimeout(200);check('reload keeps progress and language',await page.evaluate(()=>state.index===2&&state.language==='both'&&Object.values(state.steps).every(s=>s===3)));
await page.addScriptTag({url:pathToFileURL(path.join(root,'track-flight.js')).href});
await page.evaluate(()=>{const c=document.createElement('div');c.id='track-test';c.style.cssText='position:fixed;left:20px;top:150px;width:900px;height:500px;background:#203941;z-index:1000';document.body.append(c);window.flightDone=false;window.flight=mountTrackFlight({container:c,sprite:'art/gear.svg',path:'M800 200 C800 160 760 160 710 160 C610 160 600 300 710 300 C810 300 830 170 740 170 C690 170 680 220 700 250',onComplete:()=>window.flightDone=true});});await page.waitForTimeout(80);
const pts=await page.evaluate(()=>{const p=flight.route,m=p.getScreenCTM(),l=p.getTotalLength();return Array.from({length:201},(_,i)=>{const q=p.getPointAtLength(l*i/200),r=new DOMPoint(q.x,q.y).matrixTransform(m);return {x:r.x,y:r.y};});});
const p=await center('#track-test button');await page.mouse.move(p.x,p.y);await page.mouse.down();for(let i=0;i<=192;i+=12)await page.mouse.move(pts[i].x,pts[i].y);await page.mouse.move(pts[200].x,pts[200].y);await page.waitForTimeout(40);check('portable fast track reaches end',await page.evaluate(()=>Number(flight.element.dataset.progress)>.98&&!flightDone));await page.mouse.up();check('portable track commits on release',await page.evaluate(()=>flightDone));await page.evaluate(()=>flight.destroy());check('component cleanup',await page.locator('#track-test button').count()===0);await page.close();
}}catch(e){errors.push(String(e));}finally{await browser.close();}const report=JSON.stringify({checks,errors,scope:'Isolated original demo + component regression; not full-book reproduction or classroom acceptance'},null,2);if(process.env.OUTPUT_REPORT){fs.mkdirSync(path.dirname(process.env.OUTPUT_REPORT),{recursive:true});fs.writeFileSync(process.env.OUTPUT_REPORT,report+'\n');}console.log(report);if(errors.length)process.exitCode=1;})();
