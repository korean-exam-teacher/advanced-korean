/* 국어의 모든 것 · 지문 그림 자료 공용 엔진
   한 캔버스에 장면(scene)을 바꿔 가며 그림. 3D(끌어서 돌리기)와 2D(그래프·도식) 둘 다 지원. */
(function(){
const R=window.R={};
const $=id=>document.getElementById(id); R.$=$;
const RM=R.RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
const DPR=()=>Math.min(window.devicePixelRatio||1,2);
const add=R.add=(a,b)=>[a[0]+b[0],a[1]+b[1],a[2]+b[2]], mul=R.mul=(a,k)=>[a[0]*k,a[1]*k,a[2]*k];
const hex=R.hex=c=>[parseInt(c.slice(1,3),16),parseInt(c.slice(3,5),16),parseInt(c.slice(5,7),16)];
const mix=R.mix=(a,b,t)=>[a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t,a[2]+(b[2]-a[2])*t];
const css=R.css=c=>`rgb(${c[0]|0},${c[1]|0},${c[2]|0})`;
R.clamp=(x,a,b)=>Math.max(a,Math.min(b,x)); R.ease=x=>x>=1?1:x<=0?0:1-Math.pow(1-x,3);
R.fx=(n,d)=>Number(n).toFixed(d);
let C0=hex('#3D7CC9'), C1=hex('#E8590C');
R.setAcc=f=>document.documentElement.style.setProperty('--acc',css(mix(C0,C1,R.clamp(f,0,1))));
const SANS='"Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif', SERIF='"Noto Serif KR","Noto Serif CJK KR","Batang",serif';
R.SANS=SANS; R.SERIF=SERIF;

/* ---------- 캔버스 ---------- */
const cv=$('cv'), ctx=cv.getContext('2d'); R.ctx=ctx;
const cam=R.cam={yaw:-.45,pitch:.34,zoom:2,tx:0,ty:0,tz:0,dist:16};
let W=0,H=0,tween=null,dirty=true; R.W=()=>W; R.H=()=>H; R.dirty=()=>{dirty=true};
function resize(){const r=cv.getBoundingClientRect(); if(!r.width)return; W=r.width; H=r.height; cv.width=W*DPR(); cv.height=H*DPR(); dirty=true;}
new ResizeObserver(resize).observe(cv);
R.clear=()=>{const d=DPR(); ctx.setTransform(d,0,0,d,0,0); ctx.clearRect(0,0,W,H);};
const P=R.P=p=>{let x=p[0]-cam.tx,y=p[1]-cam.ty,z=p[2]-cam.tz; const cy=Math.cos(cam.yaw),sy=Math.sin(cam.yaw); const x1=cy*x+sy*z, z1=-sy*x+cy*z; const cp=Math.cos(cam.pitch),sp=Math.sin(cam.pitch); const y1=cp*y-sp*z1, z2=sp*y+cp*z1; const dep=cam.dist-z2, f=Math.min(W*.62,H)*cam.zoom*cam.dist/12; return [W/2+f*x1/dep, H/2-f*y1/dep, dep, [x1,y1,z2]];};
R.draw=(F,over)=>{R.clear();
  const L=[-.35,.75,.55], Ln=Math.hypot(...L);
  const fs=F.map(f=>{const q=f.p.map(P), a=q[0][3],b=q[1][3],e=q[2][3]; const u=[b[0]-a[0],b[1]-a[1],b[2]-a[2]], w=[e[0]-a[0],e[1]-a[1],e[2]-a[2]]; const n=[u[1]*w[2]-u[2]*w[1],u[2]*w[0]-u[0]*w[2],u[0]*w[1]-u[1]*w[0]]; const nl=Math.hypot(...n)||1; let dep=0; q.forEach(t=>dep+=t[2]); return {q,dep:dep/q.length+(f.bias||0),c:f.c,a:f.a,flat:f.flat,sh:Math.abs((n[0]*L[0]+n[1]*L[1]+n[2]*L[2])/nl/Ln)};});
  fs.sort((x,y)=>y.dep-x.dep);
  for(const f of fs){const k=f.flat?1:.52+.48*f.sh, col=css(mul(f.c,k)); ctx.beginPath(); f.q.forEach((t,i)=>i?ctx.lineTo(t[0],t[1]):ctx.moveTo(t[0],t[1])); ctx.closePath(); ctx.globalAlpha=f.a==null?1:f.a; ctx.fillStyle=col; ctx.fill(); if(f.a==null){ctx.strokeStyle=col; ctx.lineWidth=.7; ctx.stroke();} ctx.globalAlpha=1;}
  if(over)over();};
R.line=(pts,col,w,dash)=>{ctx.save(); ctx.beginPath(); pts.forEach((p,i)=>{const q=P(p); i?ctx.lineTo(q[0],q[1]):ctx.moveTo(q[0],q[1])}); ctx.strokeStyle=col; ctx.lineWidth=w||1.5; if(dash)ctx.setLineDash(dash); ctx.stroke(); ctx.restore();};
R.dot=(p,col,r)=>{const q=P(p); ctx.fillStyle=col; ctx.beginPath(); ctx.arc(q[0],q[1],r||3.5,0,7); ctx.fill();};
R.label=(p,t,col,dx,dy,size,wt,align)=>{const q=P(p); R.text(q[0]+(dx||0),q[1]+(dy||0),t,{col,size,wt,align});};
R.box=(F,x0,x1,y0,y1,z0,z1,c,a)=>{const Q=[[x0,y0,z0],[x1,y0,z0],[x1,y1,z0],[x0,y1,z0],[x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]];[[0,1,2,3],[4,5,6,7],[0,1,5,4],[3,2,6,7],[0,3,7,4],[1,2,6,5]].forEach(ix=>F.push({p:ix.map(i=>Q[i]),c,a}));};
R.cyl=(F,cx,y0,y1,cz,r,c,n)=>{n=n||24; const t=[],b=[]; for(let i=0;i<n;i++){const a=i/n*Math.PI*2; t.push([cx+r*Math.cos(a),y1,cz+r*Math.sin(a)]); b.push([cx+r*Math.cos(a),y0,cz+r*Math.sin(a)]);} F.push({p:t,c,bias:-.01}); for(let i=0;i<n;i++){const j=(i+1)%n; F.push({p:[b[i],b[j],t[j],t[i]],c});}};
R.sphere=(F,c,r,col,n,a)=>{n=n||14; for(let i=0;i<n;i++){const t0=Math.PI*i/n,t1=Math.PI*(i+1)/n; for(let j=0;j<2*n;j++){const p0=Math.PI*j/n,p1=Math.PI*(j+1)/n; const v=(t,p)=>[c[0]+r*Math.sin(t)*Math.cos(p),c[1]+r*Math.cos(t),c[2]+r*Math.sin(t)*Math.sin(p)]; F.push({p:[v(t0,p0),v(t0,p1),v(t1,p1),v(t1,p0)],c:col,a});}}};
R.arcPt=(B,T,N,k,s)=>{if(Math.abs(k)<1e-7)return [add(B,mul(T,s)),N]; const a=k*s; return [add(add(B,mul(T,Math.sin(a)/k)),mul(N,(1-Math.cos(a))/k)), add(mul(T,-Math.sin(a)),mul(N,Math.cos(a)))];};
R.strip=(F,o)=>{const n=o.n||36, w=o.w/2, h=o.h; const pt=(s,t,z)=>{const [c,nn]=R.arcPt(o.B,o.T,o.N,o.k,s); return add(add(c,mul(nn,t)),mul(o.W,z));};
  for(let i=0;i<n;i++){const s0=o.s0+(o.s1-o.s0)*i/n, s1=o.s0+(o.s1-o.s0)*(i+1)/n;
    for(const [t0,t1,c,out] of [[0,h,o.cP,h],[-h,0,o.cQ,-h]]){F.push({p:[pt(s0,out,-w),pt(s1,out,-w),pt(s1,out,w),pt(s0,out,w)],c}); F.push({p:[pt(s0,t0,-w),pt(s1,t0,-w),pt(s1,t1,-w),pt(s0,t1,-w)],c}); F.push({p:[pt(s0,t0,w),pt(s1,t0,w),pt(s1,t1,w),pt(s0,t1,w)],c});}}
  for(const s of [o.s0,o.s1]) for(const [t0,t1,c] of [[0,h,o.cP],[-h,0,o.cQ]]) F.push({p:[pt(s,t0,-w),pt(s,t1,-w),pt(s,t1,w),pt(s,t0,w)],c});
  return pt;};

/* ---------- 2D 도구 ---------- */
R.text=(x,y,t,o)=>{o=o||{}; ctx.save(); ctx.font=`${o.wt||500} ${o.size||13}px ${o.serif?SERIF:SANS}`; ctx.fillStyle=o.col||'#1D1D1F'; ctx.textAlign=o.align||'center'; ctx.textBaseline=o.base||'middle'; ctx.fillText(t,x,y); ctx.restore();};
R.path=(pts,col,w,dash,fill)=>{ctx.save(); ctx.beginPath(); pts.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1])); if(fill){ctx.closePath(); ctx.fillStyle=fill; ctx.fill();} if(col){ctx.strokeStyle=col; ctx.lineWidth=w||1.5; ctx.lineJoin='round'; ctx.lineCap='round'; if(dash)ctx.setLineDash(dash); ctx.stroke();} ctx.restore();};
R.rect=(x,y,w,h,fill,stroke,r)=>{ctx.save(); ctx.beginPath(); if(r&&ctx.roundRect)ctx.roundRect(x,y,w,h,r); else ctx.rect(x,y,w,h); if(fill){ctx.fillStyle=fill;ctx.fill();} if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=1.2;ctx.stroke();} ctx.restore();};
R.circle=(x,y,r,fill,stroke,w)=>{ctx.save(); ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); if(fill){ctx.fillStyle=fill;ctx.fill();} if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=w||1.2;ctx.stroke();} ctx.restore();};
R.arrow=(x0,y0,x1,y1,col,w,head)=>{head=head||8; const a=Math.atan2(y1-y0,x1-x0); R.path([[x0,y0],[x1,y1]],col,w||1.6); R.path([[x1-head*Math.cos(a-.45),y1-head*Math.sin(a-.45)],[x1,y1],[x1-head*Math.cos(a+.45),y1-head*Math.sin(a+.45)]],col,w||1.6);};
/* 그래프 틀: 화면 안 여백 pad 안에 x0..x1, y0..y1 */
R.frame=(x0,x1,y0,y1,o)=>{o=o||{}; const pad=o.pad||[28,24,38,52]; /* 위 오른 아래 왼 */
  const L=(o.box?o.box[0]:0)+pad[3], T=(o.box?o.box[1]:0)+pad[0], Rr=(o.box?o.box[0]+o.box[2]:W)-pad[1], B=(o.box?o.box[1]+o.box[3]:H)-pad[2];
  const X=x=>L+(Rr-L)*(x-x0)/(x1-x0), Y=y=>B-(B-T)*(y-y0)/(y1-y0);
  if(!o.noAxis){R.path([[L,T],[L,B],[Rr,B]],'#C7C7CC',1);
    if(o.xl)R.text(Rr,B+22,o.xl,{col:'#6E6E73',size:12,wt:400,align:'right'});
    if(o.yl)R.text(L-8,T-14,o.yl,{col:'#6E6E73',size:12,wt:400,align:'left'});
    (o.xt||[]).forEach(([v,t])=>R.text(X(v),B+12,t,{col:'#86868B',size:11,wt:400}));
    (o.yt||[]).forEach(([v,t])=>R.text(L-6,Y(v),t,{col:'#86868B',size:11,wt:400,align:'right'}));}
  return {X,Y,L,T,R:Rr,B};};

/* ---------- 조작 부품 ---------- */
R.rng=(lbl,min,max,val,fmt,on,step)=>{const w=document.createElement('label'); w.className='rng'; w.innerHTML=`<span>${lbl}</span><input type="range" min="${min}" max="${max}" step="${step||1}" value="${val}"><output></output>`; const i=w.querySelector('input'),o=w.querySelector('output'); const u=()=>{o.textContent=fmt(+i.value)}; i.oninput=()=>{on(+i.value);u();dirty=true;}; u(); w.set=v=>{i.value=v;u();}; return w;};
R.seg=(lbl,opts,val,on)=>{const w=document.createElement('span'); w.className='rng'; w.innerHTML=(lbl?`<span>${lbl}</span>`:'')+`<span class="seg" role="group" aria-label="${lbl||'고르기'}">${opts.map(([v,t])=>`<button type="button" data-v="${v}" aria-pressed="${v==val}">${t}</button>`).join('')}</span>`; w.querySelectorAll('button').forEach(b=>b.onclick=()=>{w.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',x===b)); on(b.dataset.v); dirty=true;}); return w;};
R.btn=(t,cls,on)=>{const b=document.createElement('button'); b.type='button'; b.className='btn '+(cls||''); b.textContent=t; b.onclick=()=>{on(b);dirty=true;}; return b;};
R.say=h=>{$('say').innerHTML=h;};

/* ---------- 끌어서 돌리기 ---------- */
let drag=null;
cv.addEventListener('pointerdown',e=>{if(!S[cur]||S[cur].mode==='2d')return; drag=[e.clientX,e.clientY]; cv.setPointerCapture(e.pointerId); tween=null;});
cv.addEventListener('pointermove',e=>{if(!drag)return; cam.yaw+=(e.clientX-drag[0])*.008; cam.pitch=R.clamp(cam.pitch+(e.clientY-drag[1])*.006,-.15,1.35); drag=[e.clientX,e.clientY]; dirty=true;});
['pointerup','pointercancel'].forEach(t=>cv.addEventListener(t,()=>drag=null));
cv.addEventListener('dblclick',()=>{if(S[cur]&&S[cur].cam)goCam(S[cur].cam)});
function goCam(c){const from={...cam}, to=Object.assign({},from,c); if(RM){Object.assign(cam,to);dirty=true;return;} tween={from,to,t0:performance.now(),d:520};}

/* ---------- 장면 고르기 ---------- */
let S={}, cur=null, IMG={};
function show(name){ if(name===cur||!S[name]) return; cur=name; const s=S[name];
  $('sn').textContent=s.sn||''; $('st').textContent=s.st||'';
  const c=$('ctl'); c.innerHTML=''; (s.ctl?s.ctl():[]).forEach(e=>c.appendChild(e));
  const o=$('orig'); o.classList.remove('big'); if(s.img&&IMG[s.img]){$('origImg').src=IMG[s.img].src; $('origImg').alt=IMG[s.img].alt||'시험지 그림'; o.hidden=false;} else o.hidden=true;
  document.querySelector('.view').classList.toggle('flat',s.mode==='2d');
  cv.style.cursor=s.mode==='2d'?'default':''; document.querySelector('.drag').hidden=s.mode==='2d';
  document.querySelectorAll('[data-scene]').forEach(el=>el.classList.toggle('on',el.dataset.scene===name));
  if(s.enter)s.enter(); if(s.cam)goCam(s.cam); dirty=true;}
R.show=show; R.cur=()=>cur;
function pick(){ if(!document.body.classList.contains('fig')) return; const mob=innerWidth<=900, sb=$('stage').getBoundingClientRect(), line=mob?(sb.bottom+(innerHeight-sb.bottom)*.3):innerHeight*.42;
  let n=null; for(const b of blocks){ if(b.getBoundingClientRect().top<line) n=b.dataset.scene; } show(n||blocks[0].dataset.scene);}
let blocks=[];
function setFig(on,scene,anchor){ const y=anchor?anchor.getBoundingClientRect().top:0;
  document.body.classList.toggle('fig',on); $('tog').setAttribute('aria-pressed',on); $('tog').textContent=on?'그림 닫기':'그림 함께 보기';
  if(on){ cur=null; requestAnimationFrame(()=>{resize(); if(anchor){const mob=innerWidth<=900; const target=mob?($('stage').getBoundingClientRect().bottom+12):y; scrollBy(0,anchor.getBoundingClientRect().top-target);} if(scene) show(scene); else pick();}); }
  else if(anchor){ requestAnimationFrame(()=>scrollBy(0,anchor.getBoundingClientRect().top-y)); } }
/* 문제를 다 푼 뒤에만 그림을 열 수 있음 (문제은행 채점 기록 = localStorage 'kbank-records-v1', 같은 사이트) */
function solvedCount(){ let g=window.REF_ITEMS||[]; if(g.length&&!Array.isArray(g[0])) g=[g]; g=g.filter(x=>x.length); let rec={}; try{rec=JSON.parse(localStorage.getItem('kbank-records-v1')||'{}')||{};}catch(e){} if(!g.length) return [0,0];
  /* A·B형처럼 같은 지문이 여러 회차에 있으면 그중 한 회차의 문항을 다 풀면 열림 */
  const r=g.map(keys=>[keys.filter(k=>rec[k]&&rec[k].r).length, keys.length]); r.sort((a,b)=>(b[0]/b[1])-(a[0]/a[1])); return r[0]; }
function gate(){ const [d,n]=solvedCount(), open=!n||d>=n; document.body.classList.toggle('locked',!open);
  const g=$('gate'); if(g){ g.hidden=open; g.innerHTML=open?'':`<b>문제를 먼저 풀어 보세요.</b> 이 지문의 문항 ${n}개를 문제은행에서 모두 풀고 채점하면 그림이 열립니다. <span class="gate-n">지금 ${d}개 / ${n}개</span> <a href="../suneung.html">문제은행에서 풀기</a>`; }
  if(!open && document.body.classList.contains('fig')) document.body.classList.remove('fig');
  return open; }
R.start=function(o){ S=o.scenes; IMG=o.img||{}; if(o.c0)C0=hex(o.c0); if(o.c1)C1=hex(o.c1); R.setAcc(o.acc0||0);
  blocks=[...document.querySelectorAll('[data-scene]')];
  gate(); addEventListener('storage',e=>{ if(e.key==='kbank-records-v1') gate(); }); addEventListener('focus',gate);
  blocks.forEach(b=>{const bt=document.createElement('button'); bt.type='button'; bt.className='figbtn'; bt.textContent='그림으로 보기'; bt.setAttribute('aria-label',(b.querySelector('.no')||{}).textContent+' 그림으로 보기'); bt.onclick=()=>{ if(!gate()){ $('gate').scrollIntoView({block:'center',behavior:R.RM?'auto':'smooth'}); return; } if(document.body.classList.contains('fig')){show(b.dataset.scene);} else setFig(true,b.dataset.scene,b);}; (b.querySelector('.figslot')||b).appendChild(bt);});
  $('tog').onclick=()=>{ if(!gate()){ $('gate').scrollIntoView({block:'center',behavior:R.RM?'auto':'smooth'}); return; } const on=!document.body.classList.contains('fig'); const vis=blocks.find(b=>b.getBoundingClientRect().bottom>80)||blocks[0]; setFig(on,null,vis);};
  $('close').onclick=()=>{const vis=blocks.find(b=>b.getBoundingClientRect().bottom>(innerWidth<=900?$('stage').getBoundingClientRect().bottom:80))||blocks[0]; setFig(false,null,vis);};
  $('orig').onclick=()=>$('orig').classList.toggle('big');
  addEventListener('scroll',pick,{passive:true}); addEventListener('resize',pick);
  if(location.hash==='#fig' && gate()) setFig(true,blocks[0].dataset.scene);
  requestAnimationFrame(frame); if(o.onLoad)o.onLoad();};
function frame(now){
  if(tween){const x=Math.min(1,(now-tween.t0)/tween.d), e=1-Math.pow(1-x,3); for(const k in tween.to) cam[k]=tween.from[k]+(tween.to[k]-tween.from[k])*e; if(x>=1) tween=null; dirty=true;}
  for(const k in S){ if(S[k].tick && S[k].tick(now,k===cur) && k===cur) dirty=true; }
  if(dirty&&W&&cur&&document.body.classList.contains('fig')){dirty=false; S[cur].render();}
  requestAnimationFrame(frame);}
})();
