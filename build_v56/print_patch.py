"""시험지 인쇄를 선생님이 보낸 모의평가 양식(HWP, A3·2단)과 같은 판짜기로 바꾼다.

양식에서 잰 값(A3 297×420mm 기준, A4·B4는 너비 비율로 줄이거나 늘림)
- 여백: 왼쪽·오른쪽 31mm. 머리 줄(굵은 가로선)은 위에서 51.9mm(첫 쪽은 76.8mm).
- 2단: 단 너비 112mm, 가운데 세로줄 하나(0.21mm), 단 사이 10.7mm. 단 아래 끝 376.4mm(평가원 문제지 실측 — 받은 양식은 371.4mm).
- 머리: 홀수 쪽은 오른쪽, 짝수 쪽은 왼쪽에 큰 쪽 번호. 가운데에 "국어 영역".
  첫 쪽: 윗줄 시험 이름, "제 1 교시" 둥근 상자, 큰 "국어 영역", 굵은 가로선.
- 꼬리: 가운데 작은 상자에 대각선으로 "쪽/전체 쪽".
- 본문 11.5pt(A4로는 8.2pt), 줄 간격 160%. 지문은 가는 테두리 상자 안에.
- 문항 번호는 굵게. <보기>는 테두리 상자 위 가운데에 "< 보 기 >".
- 문항 사이를 넉넉히(2.4em) 두고, 쪽을 다 나눈 뒤 단마다 남는 빈칸을 문항 사이와 마지막 문항 아래에 똑같이 나눈다(평가원 원본 실측, 마지막 단 제외).
- 맨 끝 쪽 오른쪽 단 아래에 "* 확인 사항" 상자. 앞에 표지(성명·수험 번호, 유의 사항) 한 쪽.
"""
import sys


def patch(s):
    def rep(old, new, count=1):
        nonlocal s
        n = s.count(old)
        if n != count:
            sys.exit(f'print patch miss ({n} != {count}): {old[:90]!r}')
        s = s.replace(old, new)

    def rep_between(start, end, new):
        nonlocal s
        i = s.index(start); j = s.index(end, i)
        assert s.count(start) == 1, start
        s = s[:i] + new + s[j:]

    # ---- 용지·글자 크기 ----
    rep("const BK_FONT_STEPS = [10.5, 10, 9.5, 9, 8.5];\nconst BK_PAPER = {A4:{w:210, h:297}, B4:{w:257, h:364}};",
        "const BK_FONT_STEPS = [11.5, 11, 10.5, 10, 9.5, 9, 8.5, 8];\n"
        "const BK_PAPER = {A4:{w:210, h:297}, B4:{w:257, h:364}, A3:{w:297, h:420}};\n"
        "/* 자동 맞춤: 양식과 같은 비율의 글자(A3 11.5pt)에서 시작해 조금씩 줄인다 */\n"
        "function bkAutoSteps(paper){ const p = BK_PAPER[paper] || BK_PAPER.A4; const t = 11.5 * p.w / 297;\n"
        "  return [1, .95, .9, .85].map(k=>Math.round(t*k*10)/10); }")

    # ---- 시험지 CSS 전체 ----
    rep_between("const SHEET_CSS = `", "(function injectSheetCss()", r'''const SHEET_CSS = `
.sheet{position:relative;box-sizing:border-box;background:#fff;color:#000;overflow:hidden;
  font-family:"OldHangulSerif",var(--pfam,"Noto Serif KR"),"Noto Serif KR","Noto Serif CJK KR","Batang","AppleMyungjo",serif;font-size:var(--pf,10pt);line-height:1.6;
  letter-spacing:-.04em;word-break:keep-all;overflow-wrap:anywhere;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.sheet *{box-sizing:border-box}
#printArea .sheet{contain:strict}
.sheet .hf{font-family:"HY헤드라인M","HYHeadLine-Medium","OldHangulSans","Noto Sans KR","Noto Sans CJK KR","Malgun Gothic",sans-serif;font-weight:800;font-synthesis:none;letter-spacing:0;line-height:1}
.sheet .pnum{font-family:"Times New Roman",Times,"Noto Serif","Noto Serif KR","Noto Serif CJK KR",serif;font-weight:700;letter-spacing:0;line-height:1}
.sh-hd{position:absolute;border-bottom:var(--rw) solid #000}
.sh-hd .hf{position:absolute;left:0;right:0;bottom:var(--hb);text-align:center}
.sh-hd .pnum{position:absolute;bottom:var(--pb)}
.sh-hd.odd .pnum{right:0} .sh-hd.even .pnum{left:0}
.sh-hd1{position:absolute;border-bottom:var(--rw) solid #000}
.sh-hd1 .t-s{position:absolute;left:0;right:0;text-align:center;font-family:"OldHangulSans","Noto Sans KR","Noto Sans CJK KR","Malgun Gothic",sans-serif;font-weight:500;letter-spacing:-.02em;line-height:1}
.sh-hd1 .pnum{position:absolute;right:0}
.sh-hd1 .gyosi{position:absolute;left:0;display:flex;align-items:center;justify-content:center;border:var(--tw) solid #000;border-radius:999px;
  font-family:"Noto Serif KR","Noto Serif CJK KR",serif;font-weight:700;letter-spacing:0;line-height:1;white-space:nowrap}
.sh-hd1 .gyosi b{font-family:"Times New Roman",Times,serif;margin:0 .18em}
.sh-hd1 .hf{position:absolute;left:0;right:0;text-align:center}
.sh-cols{position:absolute;display:flex}
.sh-col{position:relative;flex:none;height:100%;overflow:hidden}
.sh-rule{flex:none;width:0;border-left:var(--cw) solid #000;margin:0 auto}
.sh-col > :first-child{margin-top:0!important}
.sh-ft{position:absolute;border:var(--tw) solid #000;font-family:"Times New Roman",Times,serif;letter-spacing:0;line-height:1;
  background:linear-gradient(to bottom right,transparent calc(50% - var(--tw)/2),#000 calc(50% - var(--tw)/2),#000 calc(50% + var(--tw)/2),transparent calc(50% + var(--tw)/2))}
.sh-ft .a{position:absolute;left:.18em;top:.08em}
.sh-ft .b{position:absolute;right:.18em;bottom:.06em}
.gh{margin-top:2.2em;text-align:justify}
.gh .rg{margin-right:.25em;letter-spacing:0}
.src{font-family:"OldHangulSans","Noto Sans KR","Noto Sans CJK KR","Malgun Gothic",sans-serif;font-size:.74em;color:#555;font-weight:400;letter-spacing:0}
.gh + .pbox, .gh + .pimg{margin-top:.45em}
.pbox{border:var(--tw) solid #000;padding:.3em .5em .35em}
.pbox + .pbox{margin-top:0}
.pbox > :first-child{margin-top:0!important}
.pp{text-align:justify;text-indent:.6em}
.pp.cont{text-indent:0}
.pp.brk{text-align-last:justify}
.pp.ph{text-indent:0;font-weight:600}
.poem{white-space:pre-wrap;text-indent:0;text-align:left}
.pnote{font-size:.84em;line-height:1.5;text-indent:0;margin-top:.12em;padding-left:.8em}
.pp + .pnote, .poem + .pnote{margin-top:.5em}
.q{margin-top:2.4em}
.pbox + .q, .pimg + .q, .pnote + .q{margin-top:1.9em}
.qs{text-align:justify;padding-left:1.5em;text-indent:-1.5em}
.qs .qn{font-family:"Times New Roman",Times,"Noto Serif KR","Noto Serif CJK KR",serif;font-weight:700;font-size:1.13em;display:inline-block;min-width:1.33em;text-indent:0;letter-spacing:0}
.qb{position:relative;border:var(--tw) solid #000;padding:.35em .55em .4em;margin:.6em 0 .35em}
.qb.lab{margin-top:1.1em;padding-top:.75em}
.qb.cont{border-top-style:dashed;margin-top:0;padding-top:.35em}
.qb.brk{border-bottom-style:dashed;margin-bottom:0}
.qbl{position:absolute;left:50%;top:0;transform:translate(-50%,-52%);background:#fff;padding:0 .45em;white-space:nowrap;letter-spacing:0;line-height:1.2}
.qbt{white-space:pre-wrap;text-align:justify}
.qc{display:grid;gap:0 1.2em;margin-top:.7em;padding-left:.3em}
.qc > div{padding-left:1.25em;text-indent:-1.25em}
.qna{margin-top:.35em;font-size:.88em;color:#444}
.q.part{margin-top:.25em}
.pimg{overflow:hidden;margin:.35em auto 0;break-inside:avoid}
.pimg img{display:block;width:100%;height:auto}
.pimg + .pimg{margin-top:0}
.qs + .pimg{margin-top:.45em}
.chk{position:absolute;left:0;right:0;bottom:0;border:var(--tw) solid #000;padding:.5em .7em;font-family:"OldHangulSans","Noto Sans KR","Noto Sans CJK KR","Malgun Gothic",sans-serif;font-size:.86em;line-height:1.5;letter-spacing:-.02em}
.chk b{display:block;margin-bottom:.2em}
.chk p{margin:0;padding-left:.9em;text-indent:-.9em}
/* 표지 */
.cv{position:absolute;font-family:"OldHangulSans","Noto Sans KR","Noto Sans CJK KR","Malgun Gothic",sans-serif;letter-spacing:-.02em;line-height:1.35}
.cv-gyosi{display:flex;align-items:center;justify-content:center;border:var(--tw) solid #000;border-radius:999px;font-family:"Noto Serif KR","Noto Serif CJK KR",serif;font-weight:700;letter-spacing:0;line-height:1}
.cv-gyosi b{font-family:"Times New Roman",Times,serif;margin:0 .18em}
.cv-title{text-align:center;font-weight:500}
.cv-big{text-align:center}
.cv-id{display:flex;justify-content:space-between}
.cv-id .bx2{display:flex;border:var(--tw) solid #000}
.cv-id .bx2 > span{white-space:nowrap;letter-spacing:-.06em;display:flex;align-items:center;justify-content:center;border-left:var(--tw) solid #000}
.cv-id .bx2 > span:first-child{border-left:0;padding:0 .15em}
.cv-id .bx2 .dash{border-left:var(--tw) dashed #000}
.cv-box{border:var(--tw) solid #000}
.cv-box p{margin:0;padding-left:1.1em;text-indent:-1.1em}
.cv-box .gray{display:block;background:#d9d9d9;border:var(--tw) solid #000}
.cv-row{display:flex;align-items:baseline;gap:.3em}
.cv-row .dots{flex:1;border-bottom:.35mm dotted #000;transform:translateY(-.25em)}
.cv-bar{background:#d9d9d9;border:var(--tw) solid #000;display:flex;align-items:center;justify-content:center;font-weight:700}
.sh-key{position:absolute;font-family:"OldHangulSans","Noto Sans KR","Noto Sans CJK KR","Malgun Gothic",sans-serif;font-size:9.5pt;line-height:1.35;letter-spacing:0}
.sh-key h3{margin:0 0 3mm;font-size:13pt;text-align:center}
.sh-key .kc{display:flex;gap:6mm;align-items:flex-start}
.sh-key table{flex:1;border-collapse:collapse}
.sh-key th,.sh-key td{border:.25mm solid #333;padding:1mm 1.5mm;text-align:center}
.sh-key th{background:#eee;font-weight:700}
.sh-key td.l{text-align:left;font-size:.88em}
.sheet u.ul{text-decoration:underline;text-decoration-thickness:.2mm;text-underline-offset:.22em;text-decoration-skip-ink:none}
.sheet .bx{border:.2mm solid #000;padding:0 .15em;margin:0 .05em;-webkit-box-decoration-break:clone;box-decoration-break:clone}
`;
''')

    # ---- 판 크기 ----
    rep_between("function bkGeom(paper){", "function mm(v)", '''function bkGeom(paper){
  const p = BK_PAPER[paper] || BK_PAPER.A4; const s = p.w/210;   // 양식을 A4로 줄인 값 × 비율
  return {w:p.w, h:p.h, s, mx:21.9*s, colW:79.2*s, rule1:54.3*s, rule:36.7*s, top1:57.1*s, top:39.5*s, bottom:p.h-266.2*s,
    ftY:269.4*s, ftW:12.6*s, ftH:5.6*s, rw:0.3*s, cw:0.21*s, tw:0.085*s+0.06};
}
''')
    rep_between("function sheetHtml(idx, g, title, nItems){", "function bkChoiceCols(", r'''function bkSheetTitle(title){
  const t = (title || '').trim() || '국어 영역 기출 모음';
  return /문제지$/.test(t) ? t : t + ' 문제지';
}
function sheetHtml(idx, g, title, nItems, nPages){
  const first = idx === 0, s = g.s, pt = v=>`${Math.round(v*s*10)/10}pt`;
  const vars = `--rw:${mm(g.rw)};--cw:${mm(g.cw)};--tw:${mm(g.tw)};`;
  const head = first
    ? `<div class="sh-hd1" style="left:${mm(g.mx)};right:${mm(g.mx)};top:0;height:${mm(g.rule1)}">
        <div class="t-s" style="top:${mm(25.2*s)};font-size:${pt(14.9)}">${escapeHtml(bkSheetTitle(title))}</div>
        <div class="pnum" style="top:${mm(24.6*s)};font-size:${pt(23.3)}">1</div>
        <div class="gyosi" style="top:${mm(39.4*s)};width:${mm(22.7*s)};height:${mm(7.8*s)};font-size:${pt(13.5)}">제<b>1</b>교시</div>
        <div class="hf" style="top:${mm(39.2*s)};font-size:${pt(29.6)}">국어 영역</div></div>`
    : `<div class="sh-hd ${idx%2 ? 'even' : 'odd'}" style="left:${mm(g.mx)};right:${mm(g.mx)};top:0;height:${mm(g.rule)};--hb:${mm(1.6*s)};--pb:${mm(1.2*s)}">
        <span class="pnum" style="font-size:${pt(23.3)}">${idx+1}</span><span class="hf" style="font-size:${pt(19.8)}">국어 영역</span></div>`;
  const top = first ? g.top1 : g.top;
  const ruleTop = first ? g.rule1 : g.rule;
  return `<div class="sheet" style="width:${mm(g.w)};height:${mm(g.h)};${vars}">${head}
    <div class="sh-cols" style="left:${mm(g.mx)};right:${mm(g.mx)};top:${mm(top)};bottom:${mm(g.bottom)}">
      <div class="sh-col" style="width:${mm(g.colW)}"></div><div class="sh-rule" style="margin-top:-${mm(top-ruleTop)}"></div><div class="sh-col" style="width:${mm(g.colW)}"></div>
    </div>
    <div class="sh-ft" style="left:${mm(g.w/2-g.ftW/2)};top:${mm(g.ftY)};width:${mm(g.ftW)};height:${mm(g.ftH)};font-size:${pt(8.5)}"><span class="a">${idx+1}</span><span class="b">${nPages||''}</span></div></div>`;
}
/* 표지: 양식 1쪽(A4로 줄인 값에서 잼) */
function bkCoverHtml(g, title, nItems, nPages){
  const s = g.s, pt = v=>`${Math.round(v*s*10)/10}pt`, X = v=>mm(v*s);
  const vars = `--rw:${mm(g.rw)};--cw:${mm(g.cw)};--tw:${mm(g.tw)};`;
  const L = 34.2, W = 141.3;
  const cells = n=>Array.from({length:n}, (_, i)=>`<span class="${i?'dash':''}" style="width:${X(5.6)}"></span>`).join('');
  return `<div class="sheet cover" style="width:${mm(g.w)};height:${mm(g.h)};${vars}">
    <div class="cv cv-gyosi" style="left:${X(28.3)};top:${X(28.2)};width:${X(26.8)};height:${X(9.2)};font-size:${pt(17)}">제<b>1</b>교시</div>
    <div class="cv cv-title" style="left:${X(L)};width:${X(W)};top:${X(43.6)};font-size:${pt(17.6)}">${escapeHtml(bkSheetTitle(title))}</div>
    <div class="cv cv-big hf" style="left:${X(L)};width:${X(W)};top:${X(58.6)};font-size:${pt(34)}">국어 영역</div>
    <div class="cv cv-id" style="left:${X(L)};width:${X(W)};top:${X(85.9)};height:${X(9.2)};font-size:${pt(14.2)}">
      <div class="bx2" style="width:${X(57.3)}"><span style="width:${X(12)}">성명</span><span style="flex:1"></span></div>
      <div class="bx2" style="width:${X(78.4)}"><span style="width:${X(22.6)}">수험 번호</span>${cells(10)}</div></div>
    <div class="cv cv-box" style="left:${X(L)};width:${X(W)};top:${X(107.7)};height:${X(73.3)};padding:${X(6.8)} ${X(5.4)} 0 ${X(6.6)};font-size:${pt(12.7)}">
      <p>○ 문제지의 해당란에 성명과 수험 번호를 정확히 쓰시오.</p>
      <p style="margin-top:${X(3.2)}">○ 답안지의 필적 확인란에 다음의 문구를 정자로 기재하시오.<span class="gray" style="width:${X(77.7)};height:${X(7.1)};margin:${X(2.4)} 0 ${X(3)}"></span></p>
      <p>○ 답안지의 해당란에 성명과 수험 번호를 쓰고, 또 수험 번호와 답을 정확히 표시하시오.</p>
      <p style="margin-top:${X(3.2)}">○ 문항에 따라 배점이 다릅니다. 3점 문항에는 점수가 표시되어 있습니다. 점수 표시가 없는 문항은 모두 2점입니다.</p></div>
    <div class="cv cv-box" style="left:${X(L)};width:${X(W)};top:${X(187.9)};height:${X(48.7)};padding:${X(4.6)} ${X(6.3)} 0 ${X(2.6)};font-size:${pt(12)}">
      <p>※ 문항 수와 쪽수를 확인하고, 답을 정확히 표시하시오.</p>
      <div class="cv-row" style="margin:${X(3.6)} 0 0 ${X(6.2)};font-size:${pt(14.2)}">○ 문항<span class="dots"></span><span style="font-size:${pt(12.7)}">1~${nItems}번</span></div>
      <div class="cv-row" style="margin:${X(3.4)} 0 0 ${X(6.2)};font-size:${pt(14.2)}">○ 문제지<span class="dots"></span><span style="font-size:${pt(12.7)}">1~${nPages}쪽</span></div></div>
    <div class="cv cv-bar" style="left:${X(L)};width:${X(W)};top:${X(248.9)};height:${X(10.5)};font-size:${pt(14.2)}">※ 시험이 시작될 때까지 표지를 넘기지 마십시오.</div>
  </div>`;
}
''')

    # ---- 지문 상자 · <보기> 이름표 ----
    rep("""            return `<div class="poem">${escapeHtml(seg.join('\\n'))}</div>`; }});""",
        """            return `<div class="poem">${escapeHtml(seg.join('\\n'))}</div>`; }, box:gr.gk});""")
    rep("""              `<div class="pp${head?' ph':''}${cont?' cont':''}${brk?' brk':''}">${escapeHtml(tok.slice(i,j).join(' '))}</div>`});""",
        """              `<div class="pp${head?' ph':''}${cont?' cont':''}${brk?' brk':''}">${escapeHtml(tok.slice(i,j).join(' '))}</div>`, box:gr.gk});""")
    rep("""        notes.forEach(n=>B.push({t:'unit', html:`<div class="pnote">${escapeHtml(n[2])}</div>`}));""",
        """        notes.forEach(n=>B.push({t:'unit', html:`<div class="pnote">${escapeHtml(n[2])}</div>`, box:gr.gk}));""")
    rep("""        const lab = label ? `<div class="qbl">&lt; ${escapeHtml(label)} &gt;</div>` : '';
        bogiHtml = `<div class="qb">${lab}<div class="qbt">${escapeHtml(body)}</div></div>`;
        const tok = body.split(' ');
        bogiPart = {t:'text', tok, sep:' ', make:(i,j,cont,brk)=>
          `<div class="qb${cont?' cont':''}${brk?' brk':''}">${cont?'':lab}<div class="qbt">${escapeHtml(tok.slice(i,j).join(' '))}</div></div>`};""",
        """        const lt = label.replace(/\\s+/g,'');
        const lab = label ? `<div class="qbl">&lt;${escapeHtml(lt.length <= 2 ? [...lt].join(' ') : label)}&gt;</div>` : '';
        bogiHtml = `<div class="qb${lab?' lab':''}">${lab}<div class="qbt">${escapeHtml(body)}</div></div>`;
        const tok = body.split(' ');
        bogiPart = {t:'text', tok, sep:' ', make:(i,j,cont,brk)=>
          `<div class="qb${lab && !cont?' lab':''}${cont?' cont':''}${brk?' brk':''}">${cont?'':lab}<div class="qbt">${escapeHtml(tok.slice(i,j).join(' '))}</div></div>`};""")

    # ---- 쪽 나누기 ----
    rep_between("function bkLayoutSync(pt){", "function bkAnswerSheets(", r'''function bkLayoutSync(pt){
  const {groups, num, total} = bkGroups();
  const area = document.getElementById('printArea');
  const g = bkGeom(basket.paper);
  area.innerHTML = '';
  area.style.setProperty('--pf', pt+'pt');
  area.style.setProperty('--pfam', bkFaceCss());
  const title = basket.title.trim();
  const sheets = [];
  let cols, cur, forced = 0;
  const newSheet = ()=>{ const sh = bkEl(sheetHtml(sheets.length, g, title, total)); area.appendChild(sh); sheets.push(sh); cols = sh.querySelectorAll('.sh-col'); cur = cols[0]; };
  const nextCol = ()=>{ if(cur === cols[0]) cur = cols[1]; else newSheet(); };
  const used = ()=>{ const l = cur.lastElementChild; if(!l) return 0; return l.getBoundingClientRect().bottom - cur.getBoundingClientRect().top; };
  const cap = ()=>cur.getBoundingClientRect().height - 1;
  const over = ()=>used() > cap();
  const lineH = pt*1.6*96/72;
  /* 지문 조각은 단마다 테두리 상자(.pbox) 하나에 이어 담는다 */
  const put = (node, box)=>{
    if(!box){ cur.appendChild(node); return ()=>cur.removeChild(node); }
    let f = cur.lastElementChild;
    if(!(f && f.classList.contains('pbox') && f.dataset.g === box)){ f = bkEl('<div class="pbox"></div>'); f.dataset.g = box; cur.appendChild(f); }
    f.appendChild(node);
    return ()=>{ f.removeChild(node); if(!f.children.length) f.remove(); };
  };
  const tryPut = (node, box)=>{ const undo = put(node, box); if(!over()) return true; undo(); return false; };
  newSheet();
  function placeText(b){
    let i = 0, cont = false; const n = b.tok.length;
    while(i < n){
      if(tryPut(bkEl(b.make(i, n, cont, false)), b.box)) return;
      let lo = i+1, hi = n-1, best = -1;
      while(lo <= hi){
        const mid = (lo+hi)>>1; const undo = put(bkEl(b.make(i, mid, cont, true)), b.box);
        const ok = !over(); undo();
        if(ok){ best = mid; lo = mid+1; } else hi = mid-1;
      }
      if(best > i){ put(bkEl(b.make(i, best, cont, true)), b.box); i = best; cont = true; nextCol(); }
      else if(!cur.lastElementChild){ put(bkEl(b.make(i, i+1, cont, true)), b.box); i++; cont = true; forced++; nextCol(); }
      else nextCol();
    }
  }
  function place(b){
    if(b.t === 'text'){ placeText(b); return; }
    if(b.t === 'head'){
      const node = bkEl(b.html); cur.appendChild(node);
      if(over() || used() + lineH*3 > cap()){ cur.removeChild(node); if(cur.lastElementChild) nextCol(); cur.appendChild(bkEl(b.html)); }
      return;
    }
    if(tryPut(bkEl(b.html), b.box)) return;
    if(cur.lastElementChild){ nextCol(); if(tryPut(bkEl(b.html), b.box)) return; }
    if(b.parts){ b.parts.forEach(place); return; }
    put(bkEl(b.html), b.box); forced++; nextCol();
  }
  bkBlocks(groups, num, g, pt).forEach(place);
  while(sheets.length > 1 && !sheets[sheets.length-1].querySelector('.sh-col > *')){ sheets.pop().remove(); }
  /* 맨 끝: 오른쪽 단 아래의 "확인 사항" 상자 */
  const lastSh = sheets[sheets.length-1];
  cols = lastSh.querySelectorAll('.sh-col'); cur = cols[1];
  const chk = bkEl(`<div class="chk"><b>* 확인 사항</b><p>◦ 답안지의 해당란에 필요한 내용을 정확히 기입(표기)했는지 확인하시오.</p></div>`);
  const before = used();
  cur.appendChild(chk);
  const room = cur.getBoundingClientRect().height - before - chk.getBoundingClientRect().height;
  if(room < lineH*0.8){                     // 오른쪽 단에 자리가 없으면 새 쪽(오른쪽 단 아래)에 싣는다
    cur.removeChild(chk); newSheet(); cur = cols[1]; cur.appendChild(chk);
  }
  /* 단 채우기: 평가원 문제지처럼 단에 남는 빈칸을 문항 사이와 마지막 문항 아래에 똑같이 나눈다.
     (원본 실측: 짧은 두 문항이면 둘째 문항이 단 가운데쯤에서 시작하고, 문항 아래 빈칸이 서로 같다.)
     다음 단이 이어지는 지문·문항 조각으로 시작하면 마지막 아래 몫은 두지 않고 사이에만 나눈다.
     글이 끝나는 마지막 단은 마지막 문항이 단 아래(확인 사항 상자 위)에 닿도록 사이에만 나눈다(원본도 대개 그렇다). */
  const allCols = sheets.flatMap(sh=>[...sh.querySelectorAll('.sh-col')]);
  const real = c=>[...c.children].filter(x=>!x.classList.contains('chk'));
  const isUnit = x=>!!x && ((x.classList.contains('q') && !x.classList.contains('part')) || x.classList.contains('gh'));
  let lastIdx = -1; allCols.forEach((c, i)=>{ if(real(c).length) lastIdx = i; });
  allCols.forEach((c, i)=>{
    if(i > lastIdx) return;
    const kids = real(c); if(kids.length < 2) return;
    const gaps = kids.slice(1).filter(isUnit);
    if(!gaps.length) return;
    const box = c.getBoundingClientRect();
    const chkEl = c.querySelector('.chk');
    const reserve = chkEl ? chkEl.getBoundingClientRect().height + lineH : 0;
    const room = box.height - (kids[kids.length-1].getBoundingClientRect().bottom - box.top) - 2 - reserve;
    if(room <= 1) return;
    const cur = gaps.map(x=>parseFloat(getComputedStyle(x).marginTop) || 0);
    const sum = cur.reduce((s, v)=>s+v, 0) + room;
    const trail = i < lastIdx && isUnit(real(allCols[i+1])[0]) ? 1 : 0;
    let G = sum / (gaps.length + trail);
    if(G < Math.max(...cur)) G = sum / gaps.length;
    gaps.forEach(x=>{ x.style.marginTop = G.toFixed(1) + 'px'; });
  });
  const pages = sheets.length;
  sheets.forEach(sh=>{ const b = sh.querySelector('.sh-ft .b'); if(b) b.textContent = pages; });
  if(basket.cover) area.insertBefore(bkEl(bkCoverHtml(g, title, total, pages)), area.firstChild);
  if(basket.ansKey) bkAnswerSheets(area, g, groups, num, pages);
  const extra = basket.cover ? 1 : 0;
  return {pages, pt, paper:basket.paper, forced, total, cover:extra, keyPages: area.children.length - pages - extra};
}
''')
    rep("function bkSig(){ return JSON.stringify([bkValidKeys(), basket.paper, basket.font, basket.title.trim(), basket.ansKey, basket.src, bkFaceCss()]); }",
        "function bkSig(){ return JSON.stringify([bkValidKeys(), basket.paper, basket.font, basket.title.trim(), basket.ansKey, basket.src, basket.cover, bkFaceCss()]); }")
    rep("    const steps = basket.font === 'auto' ? BK_FONT_STEPS : [Number(basket.font)];",
        "    const steps = basket.font === 'auto' ? bkAutoSteps(basket.paper) : [Number(basket.font)];")
    # 미리 보기 쪽 이름
    rep("""    const cap = document.createElement('span'); cap.textContent = i < (bkLayout ? bkLayout.pages : sheets.length) ? `${i+1}쪽` : '정답표';""",
        """    const cv = bkLayout ? bkLayout.cover : 0, np = bkLayout ? bkLayout.pages : sheets.length;
    const cap = document.createElement('span'); cap.textContent = i < cv ? '표지' : i < cv + np ? `${i+1-cv}쪽` : '정답표';""")
    # 설정: 표지, A3 용지
    rep("const basket = Object.assign({keys:[], title:'', paper:'A4', font:'auto', ansKey:false, src:true, face:'noto', faceCustom:''}, loadJSON(BK_KEY));",
        "const basket = Object.assign({keys:[], title:'', paper:'A4', font:'auto', ansKey:false, src:true, cover:true, face:'noto', faceCustom:''}, loadJSON(BK_KEY));")
    rep("""<option value="B4">B4 (257×364mm)</option></select></div>""",
        """<option value="B4">B4 (257×364mm)</option><option value="A3">A3 (297×420mm, 양식 원래 크기)</option></select></div>""")
    rep("""        <label class="check"><input type="checkbox" id="bkSrc" ${basket.src?'checked':''}><span>원래 회차·번호 표시</span></label>""",
        """        <label class="check"><input type="checkbox" id="bkCover" ${basket.cover?'checked':''}><span>표지 넣기</span></label>
        <label class="check"><input type="checkbox" id="bkSrc" ${basket.src?'checked':''}><span>원래 회차·번호 표시</span></label>""")
    rep("  else if(id === 'bkSrc'){ basket.src = e.target.checked; }",
        "  else if(id === 'bkSrc'){ basket.src = e.target.checked; }\n  else if(id === 'bkCover'){ basket.cover = e.target.checked; }")
    rep("""(정답표 ${r.keyPages}쪽은 따로)` : ''}`;""",
        """(${r.cover ? '표지 1쪽과 ' : ''}정답표 ${r.keyPages}쪽은 따로)` : (r.cover ? ' (표지 1쪽은 따로)' : '')}`;""")
    rep("  const paper = r.paper === 'B4' ? 'B4' : 'A4';", "  const paper = r.paper in BK_PAPER ? r.paper : 'A4';")
    rep("""${r.paper === 'A4' ? ' B4 용지로 바꾸면 더 많이 들어갑니다.' : ''}`;""",
        """${basket.font === 'auto' ? '' : ' "자동 맞춤"은 용지에 맞춰 양식과 같은 비율의 글자 크기를 고릅니다.'}`;""")
    rep("""— 국어 시험지처럼 2단으로 짜서 ${BK_MAX_PAGES}쪽 안에 넣습니다</small></h3>""",
        """— 모의평가 문제지 양식(표지·2단·지문 상자·&lt;보기&gt;)으로 ${BK_MAX_PAGES}쪽 안에 짭니다</small></h3>""")
    rep("""<option value="auto">자동 맞춤 (${BK_MAX_PAGES}쪽 안)</option>""",
        """<option value="auto">자동 맞춤 (양식 비율, ${BK_MAX_PAGES}쪽 안)</option>""")
    # 이용 안내
    rep("""<p>"시험지로 인쇄하기"는 담은 문제를 국어 시험지처럼 2단으로 짜서 16쪽 안에 넣습니다. 글자 크기 "자동 맞춤"은 10.5pt부터 8.5pt까지 줄여 가며 16쪽 안에 들어가는 가장 큰 글자를 고릅니다.""",
        """<p>"시험지로 인쇄하기"는 담은 문제를 모의평가 문제지 양식(A3 원본을 기준으로 한 여백·2단·가운데 세로줄, 쪽마다 "국어 영역" 머리와 쪽 번호, 가운데 아래 "쪽/전체 쪽" 상자, 테두리 상자 안의 지문, 위 가운데에 이름이 걸린 &lt;보기&gt; 상자, 맨 끝 "확인 사항")으로 짜서 16쪽 안에 넣습니다. 앞에 성명·수험 번호 칸과 유의 사항이 있는 표지를 붙일 수 있고(표지는 16쪽에 세지 않음), 용지는 A4·B4·A3 가운데 고릅니다. 글자 크기 "자동 맞춤"은 양식과 같은 비율의 글자(A3 11.5pt, B4 10pt, A4 8.2pt)에서 시작해 조금씩 줄여 가며 16쪽 안에 들어가는 가장 큰 글자를 고릅니다.""")
    return s
