#!/usr/bin/env python3
"""Restyle dashboard.html: light v1-like theme + per-P 3-button layout.
Edits only the <style> block, formUrl(), and the RENDER section.
Leaves the giant inline DATA array (line 152) untouched.
"""
import re
import pathlib

HTML = pathlib.Path(__file__).resolve().parent.parent / "output" / "dashboard.html"

NEW_CSS = """* { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
body {
  margin: 0; font-family: 'Sarabun', -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
  background: #f5f7fa; color: #1a1a1a; -webkit-font-smoothing: antialiased;
  font-size: 15px; line-height: 1.5;
}

/* Header */
.header {
  position: sticky; top: 0; z-index: 20;
  background: #fff; border-bottom: 1px solid #e1e5eb;
  padding: 12px 16px;
  display: flex; align-items: center; justify-content: space-between; gap: 10px;
}
.header h1 { margin: 0; font-size: 17px; font-weight: 700; color: #1a1a1a; }
.header .sub { font-size: 12px; color: #5f6368; }
.badge-dummy {
  display: inline-block; background: #fce8e6; color: #c5221f;
  padding: 2px 10px; border-radius: 12px; font-size: 11px; font-weight: 700;
}

/* Summary */
.summary {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: 8px; padding: 12px 16px; background: #fff; border-bottom: 1px solid #e1e5eb;
}
.sum-card {
  background: #f5f7fa; border-radius: 10px; padding: 10px 12px; text-align: center;
  border: 1px solid #e8eaed;
}
.sum-card .n { font-size: 22px; font-weight: 700; color: #1a73e8; display: block; }
.sum-card .l { font-size: 11px; color: #5f6368; }
.sum-card .d { font-size: 10px; color: #9aa0a6; }

/* Filters */
.filters {
  position: sticky; top: 53px; z-index: 19;
  padding: 8px 16px; display: flex; gap: 8px; flex-wrap: wrap;
  background: #fff; border-bottom: 1px solid #e1e5eb;
}
.filters select, .filters input {
  background: #fff; color: #1a1a1a; border: 1px solid #d0d7e0; border-radius: 8px;
  padding: 7px 10px; font-size: 13px; font-family: inherit;
}
.filters input { flex: 1; min-width: 140px; }
.filters input:focus, .filters select:focus { outline: none; border-color: #1a73e8; }
.filters select { min-width: 90px; }

/* Shelter list */
.shelter-list { padding: 8px 12px 100px; }
.shelter-card {
  background: #fff; border-radius: 12px; margin: 6px 0; padding: 12px 14px;
  border: 1px solid #e1e5eb; box-shadow: 0 1px 3px rgba(0,0,0,.04);
  cursor: pointer; transition: border-color .15s;
}
.shelter-card:hover { border-color: #1a73e8; }
.shelter-card.expanded { border-color: #1a73e8; }
.card-top { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.card-code { font-weight: 700; font-size: 14px; color: #1a73e8; }
.card-dist { font-size: 13px; color: #5f6368; }
.card-road { font-size: 13px; color: #5f6368; }
.card-loc { font-size: 13px; color: #80868b; margin-top: 2px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.card-pills { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; align-items: center; }

/* Pills */
.pill {
  display: inline-block; padding: 2px 10px; border-radius: 12px;
  font-size: 11px; font-weight: 600; white-space: nowrap;
}
.p-done { background: #e6f4ea; color: #137333; }
.p-pending { background: #fef7e0; color: #b06000; }
.p-na { background: #f1f3f4; color: #80868b; }
.p-waiting { background: #e8eaed; color: #5f6368; }
.p-partial { background: #e0f2f1; color: #00695c; }
.pill-label { font-size: 10px; color: #9aa0a6; margin-right: -4px; }

/* Detail expand */
.card-detail {
  display: none; margin-top: 10px; padding-top: 10px;
  border-top: 1px solid #f0f0f2; font-size: 13px; cursor: default;
}
.shelter-card.expanded .card-detail { display: block; }
.dt-meta { color: #5f6368; font-size: 12px; margin-bottom: 8px; }

/* P section */
.p-section {
  margin-top: 8px; padding: 10px 12px;
  background: #f8f9fb; border: 1px solid #e8eaed; border-radius: 10px;
}
.p-head { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.p-name { font-weight: 700; font-size: 13px; color: #202124; }
.p-meta { font-size: 12px; color: #5f6368; margin: 4px 0 0; }
.p-btns { display: flex; gap: 8px; margin-top: 8px; }
.pbtn {
  flex: 1; text-align: center; padding: 9px 6px; border-radius: 8px;
  border: 1px solid #d0d7e0; background: #fff; color: #1a1a1a;
  font-size: 13px; font-weight: 600; text-decoration: none; white-space: nowrap;
  transition: border-color .12s, color .12s;
}
.pbtn:hover { border-color: #1a73e8; color: #1a73e8; }
.pbtn:active { background: #f1f3f4; }
.pbtn.off { opacity: .4; pointer-events: none; }

/* Count */
.count-bar { padding: 6px 16px; font-size: 12px; color: #80868b; }

/* Empty */
.empty { text-align: center; padding: 40px 20px; color: #80868b; font-size: 14px; }

/* Mobile */
@media (max-width: 480px) {
  .summary { grid-template-columns: repeat(2, 1fr); }
  .filters { flex-direction: column; }
  .filters select, .filters input { width: 100%; }
}
"""

NEW_FORMURL = """function formUrl(phase, code) {
  const f = FORMS[phase];
  if (!f) return '#';
  if (!f.entry || f.entry === 'XXXXXX') return f.url;
  return f.url + '?usp=pp_url&entry.' + f.entry + '=' + encodeURIComponent(code);
}
"""

NEW_RENDER = """// ===== RENDER =====
const P_LABELS = { p1: 'P1 Traffy', p2: 'P2 \\u0e15\\u0e23\\u0e27\\u0e08\\u0e2a\\u0e20\\u0e32\\u0e1e', p3: 'P3 \\u0e0b\\u0e48\\u0e2d\\u0e21\\u0e1a\\u0e33\\u0e23\\u0e38\\u0e07', p4: 'P4 \\u0e17\\u0e33\\u0e04\\u0e27\\u0e32\\u0e21\\u0e2a\\u0e30\\u0e2d\\u0e32\\u0e14' };

function statusBadge(val, rounds) {
  if (val === 'done') return '<span class="pill p-done">\\u0e40\\u0e2a\\u0e23\\u0e47\\u0e08 \\u2705</span>';
  if (val === 'pending') return '<span class="pill p-pending">\\u0e23\\u0e2d\\u0e17\\u0e33 \\u23f3</span>';
  if (val === 'na') return '<span class="pill p-na">\\u0e44\\u0e21\\u0e48\\u0e40\\u0e01\\u0e35\\u0e48\\u0e22\\u0e27 \\u2014</span>';
  if (val === 'waiting') return '<span class="pill p-waiting">\\u0e23\\u0e2d\\u0e04\\u0e34\\u0e27 \\u23f8</span>';
  if (val === 'partial') return '<span class="pill p-partial">R' + (rounds || 0) + '/4</span>';
  return '';
}

function pSection(s, phase) {
  const val = s[phase];
  const maps = mapsUrl(s.lat, s.long);
  const folder = s.folder;
  const form = formUrl(phase, s.code);
  const ts = s[phase + '_ts'];
  let info = '';
  if (phase === 'p1' && s.p1_dmg) info = esc(s.p1_dmg);
  if (phase === 'p2' && s.p2_items) info = esc(s.p2_items);
  if (phase === 'p4') info = (s.p4r || 0) + '/4 \\u0e23\\u0e2d\\u0e1a';
  const meta = [ts ? esc(ts) : '', info].filter(Boolean).join(' \\u00b7 ');
  return `<div class="p-section">
    <div class="p-head"><span class="p-name">${P_LABELS[phase]}</span>${statusBadge(val, s.p4r)}</div>
    ${meta ? '<div class="p-meta">' + meta + '</div>' : ''}
    <div class="p-btns">
      <a class="pbtn ${maps ? '' : 'off'}" href="${maps || '#'}" target="_blank" rel="noopener">\\ud83d\\udccd Map</a>
      <a class="pbtn ${folder ? '' : 'off'}" href="${folder ? esc(folder) : '#'}" target="_blank" rel="noopener">\\ud83d\\udcc1 Upload</a>
      <a class="pbtn" href="${form}" target="_blank" rel="noopener">\\ud83d\\udccb Form</a>
    </div>
  </div>`;
}

function cardHTML(s) {
  return `<div class="shelter-card" onclick="toggleCard(this)">
    <div class="card-top">
      <span class="card-code">${esc(s.code)}</span>
      <span class="card-dist">${esc(s.district)}</span>
      <span class="card-road">${esc(s.road)}</span>
    </div>
    <div class="card-loc">${esc(s.location)}</div>
    <div class="card-pills">
      ${statusPill('p1', s.p1, 0)}
      ${statusPill('p2', s.p2, 0)}
      ${statusPill('p3', s.p3, 0)}
      ${statusPill('p4', s.p4, s.p4r)}
    </div>
    <div class="card-detail" onclick="event.stopPropagation()">
      <div class="dt-meta">${esc(s.type)}</div>
      ${pSection(s, 'p1')}
      ${pSection(s, 'p2')}
      ${pSection(s, 'p3')}
      ${pSection(s, 'p4')}
    </div>
  </div>`;
}

function toggleCard(el) {
  el.classList.toggle('expanded');
}

function renderShelters() {
  const filtered = getFiltered();
  const container = document.getElementById('shelterList');
  document.getElementById('countBar').textContent = '\\u0e41\\u0e2a\\u0e14\\u0e07 ' + filtered.length + ' / ' + DATA.length + ' \\u0e28\\u0e32\\u0e25\\u0e32';

  if (!filtered.length) {
    container.innerHTML = '<div class="empty">\\u0e44\\u0e21\\u0e48\\u0e1e\\u0e1a\\u0e28\\u0e32\\u0e25\\u0e32\\u0e17\\u0e35\\u0e48\\u0e15\\u0e23\\u0e07\\u0e40\\u0e07\\u0e37\\u0e48\\u0e2d\\u0e19\\u0e44\\u0e02</div>';
    return;
  }

  const BATCH = 200;
  const show = filtered.slice(0, BATCH);
  container.innerHTML = show.map(cardHTML).join('');

  if (filtered.length > BATCH) {
    const more = document.createElement('div');
    more.className = 'empty';
    more.id = 'loadMore';
    more.textContent = '\\u0e41\\u0e2a\\u0e14\\u0e07 ' + BATCH + ' \\u0e08\\u0e32\\u0e01 ' + filtered.length + ' \\u2014 \\u0e40\\u0e25\\u0e37\\u0e48\\u0e2d\\u0e19\\u0e25\\u0e07\\u0e40\\u0e1e\\u0e37\\u0e48\\u0e2d\\u0e42\\u0e2b\\u0e25\\u0e14\\u0e40\\u0e1e\\u0e34\\u0e48\\u0e21';
    container.appendChild(more);

    let loaded = BATCH;
    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting && loaded < filtered.length) {
        const next = filtered.slice(loaded, loaded + BATCH);
        const frag = document.createDocumentFragment();
        const tmp = document.createElement('div');
        tmp.innerHTML = next.map(cardHTML).join('');
        while (tmp.firstChild) frag.appendChild(tmp.firstChild);
        container.insertBefore(frag, more);
        loaded += next.length;
        if (loaded >= filtered.length) {
          observer.disconnect();
          more.remove();
        } else {
          more.textContent = '\\u0e41\\u0e2a\\u0e14\\u0e07 ' + loaded + ' \\u0e08\\u0e32\\u0e01 ' + filtered.length + ' \\u2014 \\u0e40\\u0e25\\u0e37\\u0e48\\u0e2d\\u0e19\\u0e25\\u0e07\\u0e40\\u0e1e\\u0e37\\u0e48\\u0e2d\\u0e42\\u0e2b\\u0e25\\u0e14\\u0e40\\u0e1e\\u0e34\\u0e48\\u0e21';
        }
      }
    });
    observer.observe(more);
  }
}

"""

def main():
    html = HTML.read_text(encoding="utf-8")

    # 1) replace <style> block
    html, n1 = re.subn(r"(?s)(<style>\n).*?(\n</style>)",
                       lambda m: m.group(1) + NEW_CSS + m.group(2), html, count=1)

    # 2) replace formUrl()
    html, n2 = re.subn(r"(?s)function formUrl\(phase, code\) \{.*?\n\}\n",
                       lambda m: NEW_FORMURL, html, count=1)

    # 3) replace RENDER section (up to INIT marker)
    html, n3 = re.subn(r"(?s)// ===== RENDER =====.*?(// ===== INIT =====)",
                       lambda m: NEW_RENDER + m.group(1), html, count=1)

    assert n1 == 1, f"CSS block not replaced (n={n1})"
    assert n2 == 1, f"formUrl not replaced (n={n2})"
    assert n3 == 1, f"RENDER section not replaced (n={n3})"

    HTML.write_text(html, encoding="utf-8")
    print(f"OK: css={n1} formUrl={n2} render={n3}  -> {HTML}")

if __name__ == "__main__":
    main()
