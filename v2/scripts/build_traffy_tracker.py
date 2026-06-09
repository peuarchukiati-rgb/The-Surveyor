#!/usr/bin/env python3
"""
build_traffy_tracker.py
Reads traffy_rematched.csv + traffy_dedup.csv → generates v2/traffy_tracker.html
with embedded data as JS arrays. Static single-page dashboard.
"""

import csv
import json
import os
import html

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data")
OUT_DIR = os.path.join(SCRIPT_DIR, "..")

REMATCHED_CSV = os.path.join(DATA_DIR, "traffy_rematched.csv")
DEDUP_CSV = os.path.join(DATA_DIR, "traffy_dedup.csv")
OUT_HTML = os.path.join(OUT_DIR, "traffy_tracker.html")

# Google Form IDs (created 8 Jun 2026)
P1_FORM_ID = "1FAIpQLSfpfTkED3m-66HalnmnKZSSxpjvY3c97Y4wmSJp4Dv4a9vJ1A"


def read_csv(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    return rows


def main():
    rematched = read_csv(REMATCHED_CSV)
    dedup = read_csv(DEDUP_CSV)

    # JSON-encode data for embedding
    rematched_json = json.dumps(rematched, ensure_ascii=False, indent=None)
    dedup_json = json.dumps(dedup, ensure_ascii=False, indent=None)

    html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<meta name="theme-color" content="#1a1a1a">
<title>Traffy Tracker — The Surveyor v2</title>
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}
body {{
  margin: 0; font-family: 'Sarabun', -apple-system, sans-serif;
  background: #121212; color: #e0e0e0; -webkit-font-smoothing: antialiased;
  font-size: 15px; line-height: 1.5;
}}

/* Top bar */
.top-bar {{
  position: sticky; top: 0; z-index: 20;
  background: #1a1a1a; border-bottom: 1px solid #333;
  padding: 12px 16px;
  display: flex; align-items: center; justify-content: space-between;
}}
.top-bar h1 {{ margin: 0; font-size: 17px; font-weight: 700; color: #d4a843; }}
.top-bar .sub {{ font-size: 12px; color: #888; }}

/* Tab bar */
.tab-bar {{
  display: flex; gap: 0; background: #1a1a1a; border-bottom: 1px solid #333;
  position: sticky; top: 52px; z-index: 19;
}}
.tab {{
  flex: 1; text-align: center; padding: 10px 8px; font-size: 13px; font-weight: 600;
  color: #888; cursor: pointer; border-bottom: 3px solid transparent;
  transition: all .15s;
}}
.tab.active {{ color: #d4a843; border-bottom-color: #d4a843; }}
.tab:hover {{ color: #ccc; }}

/* Summary bar */
.summary {{
  display: grid; grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
  gap: 8px; padding: 12px 16px; background: #1a1a1a;
}}
.sum-card {{
  background: #222; border-radius: 10px; padding: 10px 12px; text-align: center;
  border: 1px solid #333;
}}
.sum-card .n {{ font-size: 22px; font-weight: 700; color: #d4a843; display: block; }}
.sum-card .l {{ font-size: 11px; color: #888; }}

/* Filters */
.filters {{
  padding: 8px 16px; display: flex; gap: 8px; flex-wrap: wrap;
  background: #161616; border-bottom: 1px solid #2a2a2a;
}}
.filters select, .filters input {{
  background: #222; color: #e0e0e0; border: 1px solid #444; border-radius: 8px;
  padding: 7px 10px; font-size: 13px; font-family: inherit;
}}
.filters input {{ flex: 1; min-width: 120px; }}
.filters select {{ min-width: 100px; }}

/* Case list */
.case-list {{ padding: 8px 12px 100px; }}
.case-card {{
  background: #1e1e1e; border-radius: 10px; margin: 6px 0; padding: 12px 14px;
  border: 1px solid #2a2a2a; cursor: pointer; transition: border-color .15s;
}}
.case-card:active, .case-card:hover {{ border-color: #d4a843; }}
.case-row {{ display: flex; align-items: center; gap: 10px; }}
.case-id {{ font-weight: 700; font-size: 14px; color: #d4a843; min-width: 0; }}
.case-shelter {{ font-size: 13px; color: #aaa; }}
.case-desc {{ font-size: 13px; color: #888; margin-top: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
.case-meta {{ display: flex; gap: 6px; flex-wrap: wrap; margin-top: 6px; align-items: center; }}

/* Pills */
.pill {{
  display: inline-block; padding: 2px 10px; border-radius: 12px;
  font-size: 11px; font-weight: 600; white-space: nowrap;
}}
.pill-matched {{ background: #1b5e20; color: #a5d6a7; }}
.pill-no_match {{ background: #b71c1c; color: #ef9a9a; }}
.pill-open {{ background: #555; color: #ccc; }}
.pill-assigned {{ background: #1565c0; color: #90caf9; }}
.pill-in_progress {{ background: #f9a825; color: #333; }}
.pill-fixed {{ background: #2e7d32; color: #a5d6a7; }}
.pill-reported {{ background: #6a1b9a; color: #ce93d8; }}
.pill-work {{ background: #333; color: #d4a843; border: 1px solid #555; }}
.pill-dist {{ background: #263238; color: #80cbc4; font-size: 10px; }}

/* Detail expand */
.case-detail {{
  display: none; margin-top: 10px; padding-top: 10px;
  border-top: 1px solid #333; font-size: 13px;
}}
.case-card.expanded .case-detail {{ display: block; }}
.detail-row {{ margin: 4px 0; }}
.detail-label {{ color: #888; min-width: 80px; display: inline-block; }}
.detail-value {{ color: #e0e0e0; }}
.detail-value a {{ color: #64b5f6; text-decoration: none; }}
.detail-value a:hover {{ text-decoration: underline; }}

/* Status dropdown in detail */
.status-select {{
  background: #333; color: #e0e0e0; border: 1px solid #555; border-radius: 6px;
  padding: 4px 8px; font-size: 12px; font-family: inherit; cursor: pointer;
}}

/* Dedup view */
.dedup-card {{
  background: #1e1e1e; border-radius: 10px; margin: 6px 0; padding: 12px 14px;
  border: 1px solid #2a2a2a;
}}
.dedup-header {{ display: flex; justify-content: space-between; align-items: center; }}
.dedup-code {{ font-weight: 700; color: #d4a843; font-size: 15px; }}
.dedup-count {{ font-size: 12px; color: #888; }}
.dedup-tickets {{ margin-top: 6px; font-size: 12px; color: #aaa; }}
.dedup-types {{ margin-top: 4px; }}

/* Empty */
.empty {{ text-align: center; padding: 40px 20px; color: #666; font-size: 14px; }}

/* Mobile */
@media (max-width: 480px) {{
  .summary {{ grid-template-columns: repeat(2, 1fr); }}
  .filters {{ flex-direction: column; }}
  .filters select, .filters input {{ width: 100%; }}
}}
</style>
</head>
<body>

<div class="top-bar">
  <div>
    <h1>Traffy Tracker</h1>
    <div class="sub">The Surveyor v2 — ติดตามเคส Traffy Fondue</div>
  </div>
</div>

<div class="tab-bar">
  <div class="tab active" data-tab="cases" onclick="switchTab('cases')">เคสทั้งหมด</div>
  <div class="tab" data-tab="dedup" onclick="switchTab('dedup')">ตามศาลา (Dedup)</div>
</div>

<div id="summaryBar" class="summary"></div>

<div id="filtersBar" class="filters">
  <input id="searchInput" type="search" placeholder="ค้น ticket, shelter code, ถนน..." autocomplete="off">
  <select id="filterStatus">
    <option value="">สถานะ match</option>
    <option value="matched">Matched</option>
    <option value="no_match">No Match</option>
  </select>
  <select id="filterWork">
    <option value="">ประเภทงาน</option>
  </select>
  <select id="filterDistrict">
    <option value="">เขต</option>
  </select>
</div>

<div id="caseList" class="case-list"></div>
<div id="dedupList" class="case-list" style="display:none"></div>

<script>
// ═══════════════════════════════════════════════════
// EMBEDDED DATA (generated by build_traffy_tracker.py)
// ═══════════════════════════════════════════════════
const CASES = {rematched_json};
const DEDUP = {dedup_json};

// ═══════════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════════
let currentTab = 'cases';
let caseStatuses = JSON.parse(localStorage.getItem('traffy_statuses') || '{{}}');

function saveStatuses() {{
  localStorage.setItem('traffy_statuses', JSON.stringify(caseStatuses));
}}

// ═══════════════════════════════════════════════════
// TABS
// ═══════════════════════════════════════════════════
function switchTab(tab) {{
  currentTab = tab;
  document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
  document.getElementById('caseList').style.display = tab === 'cases' ? '' : 'none';
  document.getElementById('dedupList').style.display = tab === 'dedup' ? '' : 'none';
  document.getElementById('filtersBar').style.display = tab === 'cases' ? '' : 'none';
  if (tab === 'dedup') renderDedup();
}}

// ═══════════════════════════════════════════════════
// SUMMARY
// ═══════════════════════════════════════════════════
function renderSummary() {{
  const total = CASES.length;
  const matched = CASES.filter(c => c.match_status === 'matched').length;
  const unmatched = total - matched;

  const workTypes = {{}};
  CASES.forEach(c => {{
    const w = c.work_type || 'ไม่ระบุ';
    workTypes[w] = (workTypes[w] || 0) + 1;
  }});

  let html = `
    <div class="sum-card"><span class="n">${{total}}</span><span class="l">เคสทั้งหมด</span></div>
    <div class="sum-card"><span class="n">${{matched}}</span><span class="l">จับคู่แล้ว</span></div>
    <div class="sum-card"><span class="n">${{unmatched}}</span><span class="l">ไม่พบศาลา</span></div>
  `;
  Object.entries(workTypes).sort((a,b) => b[1]-a[1]).forEach(([k,v]) => {{
    html += `<div class="sum-card"><span class="n">${{v}}</span><span class="l">${{esc(k)}}</span></div>`;
  }});
  document.getElementById('summaryBar').innerHTML = html;
}}

// ═══════════════════════════════════════════════════
// FILTERS
// ═══════════════════════════════════════════════════
function populateFilters() {{
  const works = new Set();
  const districts = new Set();
  CASES.forEach(c => {{
    if (c.work_type) works.add(c.work_type);
    if (c.district_shelter) districts.add(c.district_shelter);
    if (c.district_case) districts.add(c.district_case);
  }});

  const wSel = document.getElementById('filterWork');
  [...works].sort().forEach(w => {{
    const o = document.createElement('option');
    o.value = w; o.textContent = w;
    wSel.appendChild(o);
  }});

  const dSel = document.getElementById('filterDistrict');
  [...districts].sort().forEach(d => {{
    const o = document.createElement('option');
    o.value = d; o.textContent = d;
    dSel.appendChild(o);
  }});
}}

function getFilteredCases() {{
  const q = document.getElementById('searchInput').value.toLowerCase();
  const ms = document.getElementById('filterStatus').value;
  const wt = document.getElementById('filterWork').value;
  const dist = document.getElementById('filterDistrict').value;

  return CASES.filter(c => {{
    if (ms && c.match_status !== ms) return false;
    if (wt && c.work_type !== wt) return false;
    if (dist && c.district_shelter !== dist && c.district_case !== dist) return false;
    if (q) {{
      const hay = [c.ticket_id, c.shelter_code, c.road, c.shelter_location, c.description, c.case_address, c.district_shelter].join(' ').toLowerCase();
      if (!hay.includes(q)) return false;
    }}
    return true;
  }});
}}

// ═══════════════════════════════════════════════════
// RENDER CASES
// ═══════════════════════════════════════════════════
function esc(s) {{
  if (!s) return '';
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}}

function truncate(s, n) {{
  if (!s) return '';
  return s.length > n ? s.substring(0, n) + '...' : s;
}}

function statusPill(status) {{
  const labels = {{ open:'เปิด', assigned:'มอบหมาย', in_progress:'กำลังซ่อม', fixed:'เสร็จ', reported:'รายงานแล้ว' }};
  return `<span class="pill pill-${{status}}">${{labels[status] || status}}</span>`;
}}

function matchPill(ms) {{
  return ms === 'matched'
    ? '<span class="pill pill-matched">matched</span>'
    : '<span class="pill pill-no_match">no match</span>';
}}

function renderCases() {{
  const cases = getFilteredCases();
  const container = document.getElementById('caseList');

  if (!cases.length) {{
    container.innerHTML = '<div class="empty">ไม่พบเคสที่ตรงเงื่อนไข</div>';
    return;
  }}

  container.innerHTML = cases.map(c => {{
    const st = caseStatuses[c.ticket_id] || 'open';
    const dist = c.distance_m ? c.distance_m + 'm' : '';
    const mapsUrl = (c.case_lat && c.case_long) ? `https://www.google.com/maps?q=${{c.case_lat}},${{c.case_long}}` : '';
    const shelterMapsUrl = (c.shelter_lat && c.shelter_long) ? `https://www.google.com/maps?q=${{c.shelter_lat}},${{c.shelter_long}}` : '';

    return `<div class="case-card" data-id="${{esc(c.ticket_id)}}" onclick="toggleCase(this)">
      <div class="case-row">
        <span class="case-id">${{esc(c.ticket_id)}}</span>
        <span class="case-shelter">${{esc(c.shelter_code || '—')}}</span>
      </div>
      <div class="case-desc">${{esc(truncate(c.description, 80))}}</div>
      <div class="case-meta">
        ${{matchPill(c.match_status)}}
        ${{statusPill(st)}}
        ${{c.work_type ? `<span class="pill pill-work">${{esc(c.work_type)}}</span>` : ''}}
        ${{dist ? `<span class="pill pill-dist">${{dist}}</span>` : ''}}
      </div>
      <div class="case-detail">
        <div class="detail-row"><span class="detail-label">รายละเอียด</span><span class="detail-value">${{esc(c.description)}}</span></div>
        <div class="detail-row"><span class="detail-label">ที่อยู่เคส</span><span class="detail-value">${{esc(c.case_address)}}</span></div>
        <div class="detail-row"><span class="detail-label">ศาลา</span><span class="detail-value">${{esc(c.shelter_code)}} — ${{esc(c.shelter_location)}} (${{esc(c.shelter_type)}})</span></div>
        <div class="detail-row"><span class="detail-label">ถนน</span><span class="detail-value">${{esc(c.road)}}</span></div>
        <div class="detail-row"><span class="detail-label">เขต</span><span class="detail-value">${{esc(c.district_shelter || c.district_case)}}</span></div>
        <div class="detail-row"><span class="detail-label">ระยะห่าง</span><span class="detail-value">${{dist || '—'}}</span></div>
        ${{mapsUrl ? `<div class="detail-row"><span class="detail-label">แผนที่เคส</span><span class="detail-value"><a href="${{mapsUrl}}" target="_blank">เปิด Google Maps (เคส)</a></span></div>` : ''}}
        ${{shelterMapsUrl ? `<div class="detail-row"><span class="detail-label">แผนที่ศาลา</span><span class="detail-value"><a href="${{shelterMapsUrl}}" target="_blank">เปิด Google Maps (ศาลา)</a></span></div>` : ''}}
        <div class="detail-row"><span class="detail-label">📋 รายงานซ่อม</span><span class="detail-value"><a href="https://docs.google.com/forms/d/e/{P1_FORM_ID}/viewform?usp=pp_url&entry.62705490=${{encodeURIComponent(c.shelter_code || '')}}&entry.711616789=${{encodeURIComponent(c.ticket_id || '')}}" target="_blank" style="color:#4fc3f7;font-weight:600">กรอกฟอร์ม P1</a></span></div>
        <div class="detail-row" style="margin-top:8px">
          <span class="detail-label">สถานะงาน</span>
          <select class="status-select" onchange="setStatus('${{esc(c.ticket_id)}}', this.value); event.stopPropagation();" onclick="event.stopPropagation();">
            <option value="open" ${{st==='open'?'selected':''}}>Open</option>
            <option value="assigned" ${{st==='assigned'?'selected':''}}>Assigned</option>
            <option value="in_progress" ${{st==='in_progress'?'selected':''}}>In Progress</option>
            <option value="fixed" ${{st==='fixed'?'selected':''}}>Fixed</option>
            <option value="reported" ${{st==='reported'?'selected':''}}>Reported</option>
          </select>
        </div>
      </div>
    </div>`;
  }}).join('');
}}

function toggleCase(el) {{
  el.classList.toggle('expanded');
}}

function setStatus(ticketId, status) {{
  caseStatuses[ticketId] = status;
  saveStatuses();
  renderCases();
}}

// ═══════════════════════════════════════════════════
// RENDER DEDUP
// ═══════════════════════════════════════════════════
function renderDedup() {{
  const container = document.getElementById('dedupList');
  container.innerHTML = DEDUP.map(d => {{
    const tickets = (d.ticket_ids || '').split(',').map(t => t.trim()).filter(Boolean);
    return `<div class="dedup-card">
      <div class="dedup-header">
        <span class="dedup-code">${{esc(d.shelter_code)}}</span>
        <span class="dedup-count">${{d.ticket_count || tickets.length}} ticket(s)</span>
      </div>
      <div class="dedup-types">${{(d.work_types||'').split(',').map(w => `<span class="pill pill-work">${{esc(w.trim())}}</span>`).join(' ')}}</div>
      <div class="dedup-tickets">Tickets: ${{tickets.map(t => `<strong>${{esc(t)}}</strong>`).join(', ')}}</div>
    </div>`;
  }}).join('');
}}

// ═══════════════════════════════════════════════════
// INIT
// ═══════════════════════════════════════════════════
renderSummary();
populateFilters();
renderCases();

document.getElementById('searchInput').addEventListener('input', renderCases);
document.getElementById('filterStatus').addEventListener('change', renderCases);
document.getElementById('filterWork').addEventListener('change', renderCases);
document.getElementById('filterDistrict').addEventListener('change', renderCases);
</script>
</body>
</html>"""

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Generated: {OUT_HTML}")
    print(f"  Cases embedded: {len(rematched)}")
    print(f"  Dedup groups embedded: {len(dedup)}")


if __name__ == "__main__":
    main()
