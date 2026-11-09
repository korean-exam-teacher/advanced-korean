"""화면 다시 꾸미기(v56): 한양대 입학처 첫 화면처럼 간결하고 깔끔하게.

- 첫 화면: 화면 가득 배경 영상(책장 넘기기·손글씨·창가 독서·도서관 서가, Pexels 무료 영상)을
  어둡게 깔고 흰 글씨로 문구와 검색창. 영상은 한 편이 끝나면 다음 편으로 부드럽게 바뀐다.
  아래쪽에 '01 / 04' 넘김 단추와 멈춤 단추. 움직임 줄이기 설정이면 영상 대신 정지 사진.
- 머리 메뉴: 첫 화면 위에서는 투명(흰 글씨), 내려가면 흰 바탕으로 바뀐다.
- 첫 화면 아래: 자주 쓰는 네 곳(회차별 기출, 2028 개편 예시문항, 오답 노트, 담은 문제)으로 가는 카드.
- 본문: 흰 바탕, Pretendard 글꼴, 둥근 모서리 카드, 넉넉한 여백. 기능·데이터는 그대로.
"""
import sys

FONT_LINK = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">\n'

LIGHT_OLD = """  --bg:#FFFFFF;
  --bg-sub:#F3F5F8;
  --bg-input:#FFFFFF;
  --paper:#FCFCFA;               /* 지문 원문 상자 */
  --line:#DDE2E9;
  --line-strong:#B7C0CC;
  --text:#1B2230;
  --text-sub:#566173;
  --text-faint:#8A93A2;
  --brand:#1F4E96;               /* 남색 계열 기본색 */
  --brand-strong:#163B73;
  --brand-soft:#E9F0FA;
  --hero:#1F4E96;
  --hero-text:#FFFFFF;
  --hero-sub:#C9D7EE;
  --point:#D9480F;               /* 검색 건수 강조 */
  --good:#1D7A47;
  --warn:#A3620A;
  --warn-bg:#FFF5E3;
  --a-reading:#1F5FAE; --a-reading-bg:#E7F0FB;
  --a-lit:#A33A62;     --a-lit-bg:#FBEAF1;
  --a-speech:#8F6400;  --a-speech-bg:#FBF2DC;
  --a-lang:#1E7A5C;    --a-lang-bg:#E3F4EE;
  --foot-bg:#2B3039;
  --foot-text:#AEB5C1;
  --foot-strong:#FFFFFF;
  --foot-line:#40464F;
  --font-sans:"OldHangulSans","Noto Sans KR",-apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;"""
LIGHT_NEW = """  --bg:#FFFFFF;
  --bg-sub:#F4F5F7;
  --bg-input:#FFFFFF;
  --paper:#FAFAF9;               /* 지문 원문 상자 */
  --line:#E5E7EB;
  --line-strong:#CBD0D8;
  --text:#111418;
  --text-sub:#4A5160;
  --text-faint:#8A919E;
  --brand:#1D3A6B;               /* 깊은 남색 */
  --brand-strong:#13284D;
  --brand-soft:#EEF2F8;
  --hero:#0D121B;
  --hero-text:#FFFFFF;
  --hero-sub:#D5DAE2;
  --point:#C8442F;               /* 검색 건수 강조 */
  --good:#1D7A4C;
  --warn:#A2660A;
  --warn-bg:#FFF6E5;
  --a-reading:#2C5DAA; --a-reading-bg:#EBF1FA;
  --a-lit:#AE3F5C;     --a-lit-bg:#FBEEF2;
  --a-speech:#95680A;  --a-speech-bg:#FBF3E0;
  --a-lang:#1D7A5E;    --a-lang-bg:#E6F4EF;
  --foot-bg:#0E1116;
  --foot-text:#9AA1AD;
  --foot-strong:#F3F4F6;
  --foot-line:#242830;
  --radius:14px;
  --shadow:0 1px 2px rgba(16,24,40,.04),0 4px 16px rgba(16,24,40,.06);
  --font-sans:"OldHangulSans","Pretendard Variable","Pretendard","Noto Sans KR","Noto Sans CJK KR",-apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;"""
DARK_OLD = """--bg:#13171E; --bg-sub:#1B2029; --bg-input:#1F2530; --paper:#171C24;
    --line:#2B323D; --line-strong:#434C5A;
    --text:#E4E8EE; --text-sub:#A9B2C0; --text-faint:#7C8696;
    --brand:#6FA0E6; --brand-strong:#9BBEF0; --brand-soft:#1E2B40;
    --hero:#15294A; --hero-text:#FFFFFF; --hero-sub:#A9BCDB;
    --point:#FF8A4C; --good:#5CC48C; --warn:#E3A44A; --warn-bg:#33281A;
    --a-reading:#8DB6EC; --a-reading-bg:#1D2A3D;
    --a-lit:#E59BB9;     --a-lit-bg:#3A2330;
    --a-speech:#E0BB63;  --a-speech-bg:#352B17;
    --a-lang:#79CDB0;    --a-lang-bg:#1A3029;
    --foot-bg:#0D1015; --foot-text:#959DAA; --foot-strong:#F1F3F6; --foot-line:#262B33;"""
DARK_NEW = """--bg:#0E1015; --bg-sub:#161920; --bg-input:#1B1F27; --paper:#13161C;
    --line:#262A33; --line-strong:#3A404B;
    --text:#ECEEF2; --text-sub:#AEB5C2; --text-faint:#7B8392;
    --brand:#93B2E8; --brand-strong:#B9CDF2; --brand-soft:#1A2335;
    --hero:#07090D; --hero-text:#FFFFFF; --hero-sub:#D5DAE2;
    --point:#FF8D72; --good:#63C694; --warn:#E6AE52; --warn-bg:#33291A;
    --a-reading:#93B6EC; --a-reading-bg:#1B2638;
    --a-lit:#EBA0B6;     --a-lit-bg:#38222B;
    --a-speech:#E2BF6A;  --a-speech-bg:#33291A;
    --a-lang:#7FD0B3;    --a-lang-bg:#18302A;
    --foot-bg:#07090C; --foot-text:#8D94A1; --foot-strong:#F1F3F6; --foot-line:#1E222A;
    --shadow:0 1px 2px rgba(0,0,0,.3),0 6px 20px rgba(0,0,0,.25);"""

HERO = """<section class="search-band hero" id="hero">
  <div class="hero-media" aria-hidden="true">
    <video class="hv on" muted playsinline preload="auto" poster="media/hero1.jpg" data-src="media/hero1.mp4"></video>
    <video class="hv" muted playsinline preload="none" poster="media/hero2.jpg" data-src="media/hero2.mp4"></video>
    <video class="hv" muted playsinline preload="none" poster="media/hero3.jpg" data-src="media/hero3.mp4"></video>
    <video class="hv" muted playsinline preload="none" poster="media/hero4.jpg" data-src="media/hero4.mp4"></video>
    <div class="hero-shade"></div>
  </div>
  <div class="inner hero-inner">
    <p class="hero-eyebrow">평가원 수능·모의평가<i></i>국어 기출 문제은행</p>
    <p class="hero-copy">뿌리 깊은 나무는<br>바람에 흔들리지 않는다.</p>
    <h1 id="bandTitle">수능 국어 기출문제 검색</h1>
    <p class="sub" id="bandSub">평가원 모의평가·수능 국어 문항을 소재, 발문, 지문 속 낱말로 찾아볼 수 있습니다.</p>
    <form class="search-form" id="searchForm" role="search">
      <input id="searchInput" type="search" autocomplete="off" placeholder="소재·발문·지문·작품명·작가로 검색하세요 (예: 열팽창, 음운 변동, 김기림)" aria-label="검색어">
      <button type="submit">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg>
        검색
      </button>
    </form>
    <div class="suggest" id="suggest"></div>
    <div class="stat-line" id="statLine"></div>
  </div>
  <div class="hero-ctl inner">
    <div class="hero-pager"><b id="heroNow">01</b><span>/</span><span>04</span>
      <button type="button" id="heroPrev" aria-label="이전 장면"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="m15 18-6-6 6-6"/></svg></button>
      <button type="button" id="heroPause" aria-label="배경 영상 멈춤" aria-pressed="false"><svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg></button>
      <button type="button" id="heroNext" aria-label="다음 장면"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg></button>
    </div>
    <a class="hero-down" href="#quick" aria-label="아래로"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 4v16M5 13l7 7 7-7"/></svg></a>
  </div>
</section>

<section class="quick inner" id="quick" aria-label="바로 가기">
  <button type="button" class="qk" data-go="exams"><span class="qk-k">회차별 기출</span><b>시험지 순서대로 풀기</b><span class="qk-d">2009~2027학년도 68개 회차</span><i aria-hidden="true">→</i></button>
  <button type="button" class="qk" data-go="2028"><span class="qk-k">2028 개편</span><b>예시문항 살펴보기</b><span class="qk-d">새 수능 체제 45문항</span><i aria-hidden="true">→</i></button>
  <button type="button" class="qk" data-go="nb"><span class="qk-k">오답 노트</span><b>틀린 문제 다시 보기</b><span class="qk-d">약한 유형을 모아 줍니다</span><i aria-hidden="true">→</i></button>
  <button type="button" class="qk" data-go="bk"><span class="qk-k">문제 담기</span><b>나만의 시험지 만들기</b><span class="qk-d">모의평가 양식으로 인쇄</span><i aria-hidden="true">→</i></button>
</section>
"""

HERO_JS = r"""<script>
/* ---------- 첫 화면 배경 영상 · 머리 메뉴 ---------- */
(function(){
  const hero = document.getElementById('hero'); if(!hero) return;
  const vids = [...hero.querySelectorAll('.hv')];
  const now = document.getElementById('heroNow'), pauseBtn = document.getElementById('heroPause');
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches || (navigator.connection && navigator.connection.saveData);
  let i = 0, paused = !!still, timer = null;
  const load = v=>{ if(!v.src && v.dataset.src){ v.src = v.dataset.src; v.preload = 'auto'; } };
  function show(n){
    const prev = vids[i]; i = (n + vids.length) % vids.length; const v = vids[i];
    vids.forEach(x=>x.classList.toggle('on', x === v));
    now.textContent = String(i+1).padStart(2,'0');
    if(prev !== v) setTimeout(()=>{ try{ prev.pause(); }catch(e){} }, 1200);
    if(!paused){ load(v); try{ v.currentTime = 0; }catch(e){} const p = v.play(); if(p && p.catch) p.catch(()=>{}); load(vids[(i+1)%vids.length]); }
    clearTimeout(timer); timer = setTimeout(()=>{ if(!paused) show(i+1); }, 9000);
  }
  vids.forEach((v, k)=>v.addEventListener('ended', ()=>{ if(k === i && !paused) show(i+1); }));
  document.getElementById('heroPrev').addEventListener('click', ()=>show(i-1));
  document.getElementById('heroNext').addEventListener('click', ()=>show(i+1));
  function setPaused(p){
    paused = p; pauseBtn.setAttribute('aria-pressed', String(p)); pauseBtn.setAttribute('aria-label', p ? '배경 영상 재생' : '배경 영상 멈춤');
    pauseBtn.classList.toggle('play', p);
    if(p){ vids.forEach(v=>{ try{ v.pause(); }catch(e){} }); clearTimeout(timer); } else show(i);
  }
  pauseBtn.addEventListener('click', ()=>setPaused(!paused));
  if(still) setPaused(true); else show(0);
  /* 머리 메뉴 높이만큼 첫 화면을 끌어올림 */
  const gnb = document.querySelector('.gnb');
  const setH = ()=>document.documentElement.style.setProperty('--gnbH', Math.round(gnb.getBoundingClientRect().height) + 'px');
  setH(); if('ResizeObserver' in window) new ResizeObserver(setH).observe(gnb); else addEventListener('resize', setH);
  /* 화면 밖이면 영상 쉬기 */
  if('IntersectionObserver' in window){
    new IntersectionObserver(es=>es.forEach(e=>{
      document.body.classList.toggle('past-hero', !e.isIntersecting);
      if(paused) return; const v = vids[i];
      if(e.isIntersecting){ const p = v.play(); if(p && p.catch) p.catch(()=>{}); } else { try{ v.pause(); }catch(err){} }
    }), {rootMargin:'-140px 0px 0px 0px'}).observe(hero);
  }
  document.addEventListener('visibilitychange', ()=>{ if(document.hidden) vids.forEach(v=>{ try{ v.pause(); }catch(e){} }); else if(!paused && !document.body.classList.contains('past-hero')){ const p = vids[i].play(); if(p && p.catch) p.catch(()=>{}); } });
  /* 바로 가기 카드 */
  document.getElementById('quick').addEventListener('click', e=>{
    const b = e.target.closest('.qk'); if(!b) return;
    const go = b.dataset.go;
    if(go === 'exams'){ const m = document.querySelector('.gnb-link[data-mode="legacy"]'); if(m && !m.classList.contains('active')) m.click(); setTimeout(()=>document.getElementById('exams').scrollIntoView({behavior:'smooth'}), 50); }
    else if(go === '2028') document.querySelector('.gnb-link[data-mode="2028"]').click();
    else if(go === 'nb') document.getElementById('nbLink').click();
    else if(go === 'bk') document.getElementById('bkLink').click();
  });
})();
</script>
"""

CSS = r"""<style>
/* ===== v56 화면: 간결하고 깔끔하게 ===== */
body{font-size:15.5px;letter-spacing:-.01em;line-height:1.6}
.inner{max-width:1240px;padding-inline:28px}
::selection{background:#CFDcF3}

/* 머리 메뉴: 첫 화면 위에서는 투명 */
.gnb{background:transparent;border-bottom:1px solid rgba(255,255,255,.14);margin-bottom:calc(-1 * var(--gnbH,73px));color:#fff;transition:background .25s,border-color .25s,box-shadow .25s,color .25s}
.gnb .logo-old{color:#fff;font-size:21px}
.gnb .logo-gloss{color:rgba(255,255,255,.72);font-size:12.5px;letter-spacing:.04em}
.logo-mark{display:none}
.gnb-link{color:rgba(255,255,255,.92);font-weight:600;font-size:15px;padding:0 13px}
.gnb-link.sub{color:rgba(255,255,255,.7);font-weight:500}
.gnb-link:hover,.gnb-link.active{color:#fff}
.gnb-link.active::after{left:13px;right:13px;height:2px;bottom:16px;background:#fff;border-radius:2px}
body.past-hero .gnb,.gnb:focus-within:not(:hover){}
body.past-hero .gnb{background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:saturate(1.4) blur(12px);-webkit-backdrop-filter:saturate(1.4) blur(12px);border-bottom-color:var(--line);box-shadow:0 1px 0 var(--line)}
body.past-hero .gnb .logo-old{color:var(--text)}
body.past-hero .gnb .logo-gloss{color:var(--text-faint)}
body.past-hero .gnb-link{color:var(--text)}
body.past-hero .gnb-link.sub{color:var(--text-sub)}
body.past-hero .gnb-link:hover,body.past-hero .gnb-link.active{color:var(--brand)}
body.past-hero .gnb-link.active::after{background:var(--brand)}
.gnb-count{background:var(--point)}

/* 첫 화면 */
.hero{position:relative;isolation:isolate;overflow:hidden;background:var(--hero);color:#fff;min-height:clamp(560px,86vh,820px);display:flex;flex-direction:column}
.hero-media{position:absolute;inset:0;z-index:-1}
.hv{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transform:scale(1.04);transition:opacity 1.2s ease,transform 9s linear}
.hv.on{opacity:1;transform:scale(1)}
.hero-shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,11,17,.62) 0%,rgba(8,11,17,.38) 38%,rgba(8,11,17,.55) 70%,rgba(8,11,17,.82) 100%)}
.search-band .inner.hero-inner{flex:1;display:flex;flex-direction:column;justify-content:center;padding-top:calc(var(--gnbH,73px) + 48px);padding-bottom:40px;width:100%}
.hero-eyebrow{margin:0 0 18px;display:flex;align-items:center;gap:12px;font-size:14px;letter-spacing:.14em;color:rgba(255,255,255,.82)}
.hero-eyebrow .okm{font-size:16px;letter-spacing:.04em;color:#fff}
.hero-eyebrow i{display:inline-block;width:28px;height:1px;background:rgba(255,255,255,.5)}
.hero-copy{word-break:keep-all;margin:0 0 26px;font-size:clamp(34px,5.2vw,62px);font-weight:700;line-height:1.18;letter-spacing:-.035em;color:#fff;text-wrap:balance}
.search-band h1{margin:0 0 6px;font-size:17px;font-weight:700;letter-spacing:-.01em;color:#fff}
.search-band .sub{margin:0 0 18px;font-size:14.5px;color:rgba(255,255,255,.78)}
.search-form{max-width:760px;height:60px;border-radius:999px;background:rgba(255,255,255,.96);box-shadow:0 10px 30px rgba(0,0,0,.25);padding:6px}
.search-form input{padding:0 22px;font-size:16.5px;color:#111418}
.search-form input::placeholder{color:#8A919E}
.search-form:focus-within{box-shadow:0 0 0 4px rgba(255,255,255,.28),0 10px 30px rgba(0,0,0,.25)}
html:root .search-form button{width:auto;padding:0 26px;border-radius:999px;background:#13284D;color:#fff;font-weight:700;font-size:15.5px}
html:root .search-form button:hover{background:#1D3A6B}
.suggest{margin-top:18px;gap:8px}
.suggest-label{color:rgba(255,255,255,.7);margin-right:4px;font-size:13px}
.suggest button{border:1px solid rgba(255,255,255,.32);border-radius:999px;padding:5px 14px;color:#fff;font-size:13px;background:rgba(255,255,255,.08);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);transition:background .2s}
.suggest button:first-of-type{padding-left:14px;border-left:1px solid rgba(255,255,255,.32)}
.suggest button:hover{background:rgba(255,255,255,.2);text-decoration:none}
.stat-line{margin-top:22px;font-size:13px;color:rgba(255,255,255,.72)}
.stat-line b{color:#fff}
.search-band .hero-ctl{display:flex;align-items:center;justify-content:space-between;padding-block:0 86px;width:100%}
.hero-pager{display:flex;align-items:center;gap:8px;font-size:13px;color:rgba(255,255,255,.7);font-variant-numeric:tabular-nums}
.hero-pager b{color:#fff;font-size:15px}
.hero-pager button{display:grid;place-items:center;width:32px;height:32px;border-radius:50%;border:1px solid rgba(255,255,255,.3);background:rgba(255,255,255,.06);color:#fff}
.hero-pager button:hover{background:rgba(255,255,255,.18)}
.hero-pager button:first-of-type{margin-left:8px}
#heroPause.play svg{display:none}
#heroPause.play::before{content:"";border-left:10px solid #fff;border-top:6px solid transparent;border-bottom:6px solid transparent;margin-left:3px}
.hero-down{color:#fff;opacity:.8;display:grid;place-items:center;width:40px;height:40px;animation:heroDown 2.4s ease-in-out infinite}
@keyframes heroDown{0%,100%{transform:translateY(0)}50%{transform:translateY(6px)}}

/* 바로 가기 카드 */
.quick{position:relative;z-index:2;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-top:-58px}
.qk{position:relative;text-align:left;display:flex;flex-direction:column;gap:3px;padding:20px 22px 20px;border:1px solid var(--line);border-radius:var(--radius);background:var(--bg);box-shadow:var(--shadow);color:var(--text);transition:transform .2s,box-shadow .2s,border-color .2s}
.qk:hover{transform:translateY(-3px);border-color:var(--line-strong);box-shadow:0 2px 4px rgba(16,24,40,.05),0 14px 30px rgba(16,24,40,.1)}
.qk-k{font-size:12.5px;font-weight:700;color:var(--brand);letter-spacing:.02em}
.qk b{font-size:17px;font-weight:700;letter-spacing:-.02em}
.qk-d{font-size:13px;color:var(--text-faint)}
.qk i{position:absolute;right:20px;top:20px;font-style:normal;color:var(--text-faint);transition:transform .2s,color .2s}
.qk:hover i{transform:translateX(3px);color:var(--brand)}

/* 공지 */
.notice{margin-top:28px;border-radius:12px;border-color:var(--line);background:var(--bg-sub)}
.notice-tag{border-radius:999px;padding:2px 10px}

/* 본문 */
.layout{padding-block:44px 80px}
@media (min-width:901px){.layout{grid-template-columns:270px minmax(0,1fr);gap:40px}}
@media (min-width:701px){.gnb .inner{min-height:72px;gap:40px}.result-row{padding:16px 10px}}
.side{gap:14px}
.side-box{border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;background:var(--bg)}
.side-title{background:transparent;border-bottom:1px solid var(--line);padding:14px 16px;font-size:14.5px}
.side-list{padding:8px 16px 12px}
.side-fields{padding:14px 16px 16px}
.field select,.tools select,.bk-fields input[type="text"]{border-radius:10px;border-color:var(--line-strong)}
.reset{border-radius:12px;height:44px}
.content{gap:56px}
.sec-head{margin-bottom:16px}
.sec-head h2{font-size:24px;font-weight:800;letter-spacing:-.035em}
.exam-title h2{font-size:26px;letter-spacing:-.035em}

/* 회차표 */
.table-wrap{border:1px solid var(--line);border-radius:var(--radius);background:var(--bg)}
.year-table{border-top:0}
.year-table th{background:var(--bg-sub);border-bottom:1px solid var(--line);font-weight:600;padding:12px 10px}
.year-table th:first-child{padding-left:20px}
.year-table td{padding:10px}
.year-table td:first-child{padding-left:20px}
.year-table tr:last-child td{border-bottom:0}
.ylink{border-radius:999px;border-color:var(--line);padding:6px 14px;font-weight:600}
.ylink:hover{border-color:var(--brand);background:var(--brand-soft)}
.ylink.active{background:var(--brand);border-color:var(--brand)}
.table-wrap .more-years,.more-years{border:0;border-top:1px solid var(--line);border-radius:0;margin:0}

/* 검색 결과 */
.count{font-size:17px}
.result-headrow{border-top:0;border-radius:12px;background:var(--bg-sub);border-bottom:0}
.result-list > li{border-bottom:1px solid var(--line)}
.result-row{border-radius:12px;transition:background .15s}
.r-topic{font-size:16px;letter-spacing:-.02em}
.area{border-radius:999px;padding:3px 9px}
.tag{border-radius:999px}
.detail{border-radius:0 0 12px 12px;border-top:1px solid var(--line)}
.bogi,.passage,.explain,.notes,.pfig-wrap{border-radius:12px}
.btn-line,.btn-plain,.btn-fill{border-radius:10px;padding:8px 15px}
.ch{border-radius:10px}
.qbtn{border-radius:10px}
.pager button{border-radius:10px;min-width:38px;height:38px}
.pg{border-radius:var(--radius);overflow:hidden;border-color:var(--line)}
.pg-head{background:var(--bg-sub)}
.exam-title{border-bottom:1px solid var(--line)}
.nb-summary,.bk-groups{border-top:0}
.nb-summary{border:1px solid var(--line);border-radius:var(--radius)}
.bk-panel,.bk-grade{border-radius:var(--radius)}
.bk-g-head{border-radius:10px}
.tools button.sz,.bk-g-ctl button,.bk-it button.x{border-radius:8px}
.bk-toast{border-radius:999px;padding:12px 20px}
.nb-empty{border-radius:var(--radius)}

/* 꼬리말 */
footer .inner{padding-block:56px 48px}
.foot-name{font-size:17px}
.foot-verse{font-size:15px;margin-top:10px}

@media (max-width:900px){
  .quick{grid-template-columns:repeat(2,minmax(0,1fr));margin-top:-40px}
  .filter-panel{border-radius:var(--radius);overflow:hidden}
}
@media (max-width:700px){
  .inner{padding-inline:18px}
  .gnb .inner{padding-top:12px}
  .gnb-link{height:46px}
  .gnb-link.active::after{bottom:8px}
  .hero{min-height:620px}
  .search-band .inner.hero-inner{padding-top:calc(var(--gnbH,120px) + 28px)}
  .search-band .hero-ctl{padding-bottom:58px}
  .hero-copy{font-size:32px}
  .search-form{height:54px}
  html:root .search-form button{padding:0 16px}
  .search-form input{padding:0 14px;font-size:15.5px}
  .quick{gap:10px;margin-top:-30px}
  .qk{padding:16px}
  .qk b{font-size:15.5px}
  .qk-d{display:none}
  .layout{padding-block:30px 60px}
}
@media (prefers-reduced-motion: reduce){.hv{transition:none;transform:none}.hero-down{animation:none}}
@media print{.hero-media{display:none}}
</style>
"""

GUIDE = """      <details>
        <summary>첫 화면 배경 영상</summary>
        <p>첫 화면의 배경 영상(책장 넘기기, 손글씨, 창가에서 책 읽기, 도서관 서가)은 Pexels(pexels.com)에서 누구나 무료로 쓸 수 있도록 공개한 영상을 짧게 잘라 화질을 줄인 것입니다. 책장 넘기는 영상은 책 속 글씨가 읽히지 않도록 흐리게 처리했습니다. 아래쪽 멈춤 단추로 영상을 멈출 수 있고, 기기에서 '동작 줄이기'를 켜 두었거나 데이터 절약 모드이면 영상 대신 정지 사진만 보입니다.</p>
      </details>
"""


def patch(s):
    def rep(old, new, count=1):
        nonlocal s
        n = s.count(old)
        if n != count:
            sys.exit(f'ui patch miss ({n} != {count}): {old[:90]!r}')
        s = s.replace(old, new)

    rep('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&family=Noto+Serif+KR:wght@400;600&display=swap">\n<style>\n/* Layout:',
        FONT_LINK + '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&family=Noto+Serif+KR:wght@400;600;700&display=swap">\n<style>\n/* Layout:')
    rep(LIGHT_OLD, LIGHT_NEW)
    rep(DARK_OLD, DARK_NEW)
    rep(DARK_OLD.replace('\n    ', '\n  '), DARK_NEW.replace('\n    ', '\n  '))
    rep('      <span class="logo-mark">국</span>\n', '')
    a = s.index('<section class="search-band">'); b = s.index('</section>', a) + len('</section>\n')
    assert s.count('<section class="search-band">') == 1
    s = s[:a] + HERO + s[b:]
    rep('<div id="page-top"></div>', CSS + '<div id="page-top"></div>')
    rep("""      <details>
        <summary>오류 신고 · 의견 보내기</summary>""", GUIDE + """      <details>
        <summary>오류 신고 · 의견 보내기</summary>""")
    rep('<div id="printArea" aria-hidden="true"></div>\n', '<div id="printArea" aria-hidden="true"></div>\n' + HERO_JS)
    return s
