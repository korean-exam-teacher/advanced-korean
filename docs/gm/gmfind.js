/* 공무원 국어 찾기 — 낱말·제재로 지문과 문항을 다른 시험지까지 찾는다 (국어의 모든 것 v102)
 * 쓰는 곳: /advanced-korean/gongmuwon.html(찾아 풀기), /suneung-korean/teacher.html(기출 골라 과제 만들기)
 * 필요: window.GM_DATA(gm/index.js). 글자(gm/search.js)는 처음 찾을 때 불러온다.
 * 띄어쓰기는 무시하고 찾는다(그림에서 읽은 글자는 띄어쓰기가 틀린 곳이 많아서).
 */
(function () {
  var BASE = "/advanced-korean/gm/";
  var D = window.GM_DATA, EX = {}, IDS = Object.keys(D.items), T = null, NT = {}, loading = null;
  D.exams.forEach(function (e) { EX[e.id] = e; });
  var GRPS = ["국가직", "지방직·서울시", "지역인재", "국회직", "군무원", "법원직", "예시문제"];
  var AREAS = ["어휘·한자", "문법·규범", "화법·작문", "독해", "문학", "논리·추론"];
  function norm(s) { return String(s || "").replace(/\s+/g, "").replace(/[～∼]/g, "~").toLowerCase(); }
  function load() {
    if (T) return Promise.resolve(T);
    if (loading) return loading;
    loading = new Promise(function (res) {
      var s = document.createElement("script"); s.src = BASE + "search.js?v=102";
      s.onload = function () { T = window.GM_TEXT || { p: {}, i: {} }; res(T); };
      s.onerror = function () { T = { p: {}, i: {} }; res(T); };
      document.head.appendChild(s);
    });
    return loading;
  }
  function itemText(id) { var x = T && T.i[id]; var it = D.items[id]; return x ? x[0] : ((it.q || "") + " " + (it.s || "")); }
  function passKey(id) { var x = T && T.i[id]; return x && x[1] || ""; }
  function nrm(key, txt) { return NT[key] || (NT[key] = norm(txt)); }
  function allIn(n, words) { for (var i = 0; i < words.length; i++) if (n.indexOf(words[i]) < 0) return false; return true; }
  /* 원문에서 낱말 자리 찾기(띄어쓰기 무시) → [시작, 끝] */
  function locate(text, w) {
    var map = [], ns = "";
    for (var i = 0; i < text.length; i++) { var c = text[i]; if (/\s/.test(c)) continue; ns += c.toLowerCase(); map.push(i); }
    var k = ns.indexOf(w); if (k < 0) return null;
    return [map[k], map[k + w.length - 1] + 1];
  }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  /* 낱말 둘레 글을 잘라 <mark>로 표시한 HTML */
  function snippet(text, words, len) {
    len = len || 90; text = String(text || "").replace(/[\uE000-\uF8FF]/g, "").replace(/\s+/g, " ");
    var first = null;
    words.forEach(function (w) { var p = locate(text, w); if (p && (!first || p[0] < first[0])) first = p; });
    var a = first ? Math.max(0, first[0] - Math.floor(len / 3)) : 0, b = Math.min(text.length, a + len);
    var part = text.slice(a, b), out = esc(part);
    words.forEach(function (w) {
      var p = locate(part, w); if (!p) return;
      var raw = esc(part.slice(p[0], p[1]));
      out = out.replace(raw, "<mark>" + raw + "</mark>");
    });
    return (a > 0 ? "…" : "") + out + (b < text.length ? "…" : "");
  }
  function sortIds(ids) {
    return ids.sort(function (a, b) {
      var x = D.items[a], y = D.items[b], ex = EX[x.e], ey = EX[y.e];
      return (ey.year - ex.year) || (GRPS.indexOf(ex.grp) - GRPS.indexOf(ey.grp)) || x.e.localeCompare(y.e) || x.n - y.n;
    });
  }
  /* f: {q:"낱말", g:Set(시험), a:Set(영역), y:"연도", e:"회차"} → [{ids:[…], pk:지문키|"", snip:HTML, where:"지문"|"문항"|""}] */
  function search(f) {
    var words = String(f.q || "").trim().split(/\s+/).map(norm).filter(Boolean);
    var ids = IDS.filter(function (id) {
      var it = D.items[id], e = EX[it.e];
      if (f.e && it.e !== f.e) return false;
      if (f.g && f.g.size && !f.g.has(e.grp)) return false;
      if (f.a && f.a.size && !f.a.has(it.a || "영역 미정")) return false;
      if (f.y && String(e.year) !== String(f.y)) return false;
      return true;
    });
    if (!words.length) return sortIds(ids).map(function (id) { return { ids: [id], pk: "", snip: "", where: "" }; });
    var groups = {}, out = [];
    sortIds(ids).forEach(function (id) {
      var it = D.items[id], e = EX[it.e];
      var tI = itemText(id), pk = passKey(id), tP = pk ? T.p[pk] : "";
      var nI = nrm("i" + id, tI + " " + (it.a || "") + " " + e.title), nP = pk ? nrm("p" + pk, tP) : "";
      if (allIn(nI, words)) { out.push({ ids: [id], pk: "", snip: snippet(tI, words), where: "문항" }); return; }
      if (pk && allIn(nP + nI, words)) {
        if (!groups[pk]) { groups[pk] = { ids: [], pk: pk, snip: snippet(tP, words), where: "지문" }; out.push(groups[pk]); }
        groups[pk].ids.push(id);
      }
    });
    return out;
  }
  window.GMFind = {
    load: load, search: search, snippet: snippet, norm: norm, esc: esc, EX: EX, GRPS: GRPS, AREAS: AREAS,
    text: function (id) { return itemText(id); }, pass: function (pk) { return T && T.p[pk] || ""; },
    ready: function () { return !!T; }, base: BASE,
    short: function (e) { return e.title.replace(/\s*국어\s*/, " ").replace(/\s+/g, " ").trim(); },
    /* 과제 문항 모양(account.js가 읽는 꼴) */
    asgItem: function (id) {
      var it = D.items[id], e = EX[it.e], s = window.GMFind.short(e);
      return { k: "adv:gm:" + id, a: "공무원·" + (it.a || "영역 미정"), title: s + " " + it.n + "번", topic: it.q || "", src: "출처: " + e.title + " " + it.n + "번", nc: e.nc, q: [], p: null, txt: null, gm: { e: it.e, n: +it.n }, ans: +it.ans || 0 };
    }
  };
})();
