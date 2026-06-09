#!/usr/bin/env python3
"""
build_dashboard.py
Reads all_stops.csv + traffy_rematched.csv + 4 dummy response CSVs
→ generates v2/output/dashboard.html with embedded JSON data.
Self-contained single-page dashboard for all 4 field teams.
"""

import csv
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data")
OUT_DIR = os.path.join(SCRIPT_DIR, "..", "output")

ALL_STOPS_CSV = os.path.join(DATA_DIR, "all_stops.csv")
TRAFFY_CSV = os.path.join(DATA_DIR, "traffy_rematched.csv")
P1_CSV = os.path.join(DATA_DIR, "dummy_responses_p1.csv")
P2_CSV = os.path.join(DATA_DIR, "dummy_responses_p2.csv")
P3_CSV = os.path.join(DATA_DIR, "dummy_responses_p3.csv")
P4_CSV = os.path.join(DATA_DIR, "dummy_responses_p4.csv")
OUT_HTML = os.path.join(OUT_DIR, "dashboard.html")


def read_csv(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    return rows


def norm(code):
    """Normalize shelter code: strip spaces."""
    return (code or "").replace(" ", "").strip()


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # 1. Read all data
    stops = read_csv(ALL_STOPS_CSV)
    traffy = read_csv(TRAFFY_CSV)
    p1_rows = read_csv(P1_CSV)
    p2_rows = read_csv(P2_CSV)
    p3_rows = read_csv(P3_CSV)
    p4_rows = read_csv(P4_CSV)

    # 2. Build lookup indexes (normalized code → list of rows)
    traffy_codes = set()
    for t in traffy:
        c = norm(t.get("shelter_code") or t.get("code", ""))
        if c:
            traffy_codes.add(c)

    p1_by_code = {}
    for r in p1_rows:
        c = norm(r.get("code", ""))
        if c:
            p1_by_code.setdefault(c, []).append(r)

    p2_by_code = {}
    for r in p2_rows:
        c = norm(r.get("code", ""))
        if c:
            p2_by_code.setdefault(c, []).append(r)

    p3_by_code = {}
    for r in p3_rows:
        c = norm(r.get("code", ""))
        if c:
            p3_by_code.setdefault(c, []).append(r)

    p4_by_code = {}
    for r in p4_rows:
        c = norm(r.get("code", ""))
        if c:
            p4_by_code.setdefault(c, []).append(r)

    # 3. Merge into flat JSON array
    shelters = []
    for s in stops:
        code_raw = s.get("code", "")
        cn = norm(code_raw)

        # P1: traffy-based
        has_traffy = cn in traffy_codes
        p1_responses = p1_by_code.get(cn, [])
        if not has_traffy:
            p1_status = "na"
        elif p1_responses:
            p1_status = "done"
        else:
            p1_status = "pending"
        p1_ts = p1_responses[0].get("timestamp", "")[:10] if p1_responses else None
        p1_dmg = p1_responses[0].get("damage_type", "") if p1_responses else None

        # P2: inspection
        p2_responses = p2_by_code.get(cn, [])
        if p2_responses:
            p2_status = "done"
        else:
            p2_status = "pending"
        p2_ts = p2_responses[0].get("timestamp", "")[:10] if p2_responses else None
        p2_items = p2_responses[0].get("damage_items", "") if p2_responses else None

        # P3: maintenance — depends on P2
        p3_responses = p3_by_code.get(cn, [])
        if p2_status != "done":
            p3_status = "waiting"
        elif p2_items and p2_items.strip():
            # P2 found damage
            if p3_responses:
                p3_status = "done"
            else:
                p3_status = "pending"
        else:
            p3_status = "na"
        p3_ts = p3_responses[0].get("timestamp", "")[:10] if p3_responses else None

        # P4: cleaning rounds (0-4)
        p4_responses = p4_by_code.get(cn, [])
        rounds_done = len(set(r.get("round", "") for r in p4_responses))
        if rounds_done >= 4:
            p4_status = "done"
        elif rounds_done >= 1:
            p4_status = "partial"
        else:
            p4_status = "pending"
        p4_ts = p4_responses[-1].get("timestamp", "")[:10] if p4_responses else None

        lat = s.get("lat", "")
        lng = s.get("long", "")
        try:
            lat = round(float(lat), 6) if lat else None
        except ValueError:
            lat = None
        try:
            lng = round(float(lng), 6) if lng else None
        except ValueError:
            lng = None

        shelters.append({
            "tor": s.get("tor", ""),
            "code": code_raw,
            "district": s.get("district", ""),
            "road": s.get("road", ""),
            "location": s.get("location", ""),
            "type": s.get("type", ""),
            "lat": lat,
            "long": lng,
            "folder": s.get("folder_url", ""),
            "p1": p1_status,
            "p1_ts": p1_ts or None,
            "p1_dmg": p1_dmg or None,
            "p2": p2_status,
            "p2_ts": p2_ts or None,
            "p2_items": p2_items or None,
            "p3": p3_status,
            "p3_ts": p3_ts or None,
            "p4": p4_status,
            "p4r": rounds_done,
            "p4_ts": p4_ts or None,
        })

    # 4. Stats
    total = len(shelters)
    traffy_total = sum(1 for s in shelters if s["p1"] != "na")
    p1_done = sum(1 for s in shelters if s["p1"] == "done")
    p2_done = sum(1 for s in shelters if s["p2"] == "done")
    p3_eligible = sum(1 for s in shelters if s["p3"] not in ("na", "waiting"))
    p3_done = sum(1 for s in shelters if s["p3"] == "done")
    p4_done = sum(1 for s in shelters if s["p4"] == "done")

    print(f"Total shelters: {total}")
    print(f"Traffy cases: {traffy_total}")
    print(f"P1 done: {p1_done}/{traffy_total}")
    print(f"P2 done: {p2_done}/{total}")
    print(f"P3 done: {p3_done}/{p3_eligible} (eligible)")
    print(f"P4 done: {p4_done}/{total}")

    # 5. Build HTML
    data_json = json.dumps(shelters, ensure_ascii=False, separators=(",", ":"))

    html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<meta name="theme-color" content="#0f1117">
<title>The Surveyor v2 — Dashboard</title>
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}
body {{
  margin: 0; font-family: 'Sarabun', -apple-system, sans-serif;
  background: #0f1117; color: #e4e6ef; -webkit-font-smoothing: antialiased;
  font-size: 15px; line-height: 1.5;
}}

/* Header */
.header {{
  position: sticky; top: 0; z-index: 20;
  background: #1a1d27; border-bottom: 1px solid #2e3345;
  padding: 12px 16px;
  display: flex; align-items: center; justify-content: space-between;
}}
.header h1 {{ margin: 0; font-size: 17px; font-weight: 700; color: #d4a843; }}
.header .sub {{ font-size: 12px; color: #8b8fa3; }}
.badge-dummy {{
  display: inline-block; background: #b71c1c; color: #ffcdd2;
  padding: 2px 10px; border-radius: 12px; font-size: 11px; font-weight: 700;
}}

/* Summary */
.summary {{
  display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: 8px; padding: 12px 16px; background: #1a1d27;
}}
.sum-card {{
  background: #0f1117; border-radius: 10px; padding: 10px 12px; text-align: center;
  border: 1px solid #2e3345;
}}
.sum-card .n {{ font-size: 22px; font-weight: 700; color: #d4a843; display: block; }}
.sum-card .l {{ font-size: 11px; color: #8b8fa3; }}
.sum-card .d {{ font-size: 11px; color: #555; }}

/* Filters */
.filters {{
  position: sticky; top: 52px; z-index: 19;
  padding: 8px 16px; display: flex; gap: 8px; flex-wrap: wrap;
  background: #1a1d27; border-bottom: 1px solid #2e3345;
}}
.filters select, .filters input {{
  background: #0f1117; color: #e4e6ef; border: 1px solid #2e3345; border-radius: 8px;
  padding: 7px 10px; font-size: 13px; font-family: inherit;
}}
.filters input {{ flex: 1; min-width: 140px; }}
.filters select {{ min-width: 90px; }}

/* Shelter list */
.shelter-list {{ padding: 8px 12px 100px; }}
.shelter-card {{
  background: #1a1d27; border-radius: 10px; margin: 6px 0; padding: 12px 14px;
  border: 1px solid #2e3345; cursor: pointer; transition: border-color .15s;
}}
.shelter-card:hover, .shelter-card:active {{ border-color: #d4a843; }}
.card-top {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}
.card-code {{ font-weight: 700; font-size: 14px; color: #d4a843; }}
.card-dist {{ font-size: 13px; color: #8b8fa3; }}
.card-road {{ font-size: 13px; color: #8b8fa3; }}
.card-loc {{ font-size: 13px; color: #555; margin-top: 2px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
.card-pills {{ display: flex; gap: 6px; flex-wrap: wrap; margin-top: 6px; align-items: center; }}

/* Pills */
.pill {{
  display: inline-block; padding: 2px 10px; border-radius: 12px;
  font-size: 11px; font-weight: 600; white-space: nowrap;
}}
.p-done {{ background: #2e7d32; color: #a5d6a7; }}
.p-pending {{ background: #f9a825; color: #333; }}
.p-na {{ background: #555; color: #888; }}
.p-waiting {{ background: #37474f; color: #90a4ae; }}
.p-partial {{ background: #00695c; color: #80cbc4; }}
.pill-label {{ font-size: 10px; color: #8b8fa3; margin-right: -4px; }}

/* Detail expand */
.card-detail {{
  display: none; margin-top: 10px; padding-top: 10px;
  border-top: 1px solid #2e3345; font-size: 13px;
}}
.shelter-card.expanded .card-detail {{ display: block; }}
.dt-row {{ margin: 4px 0; }}
.dt-label {{ color: #8b8fa3; min-width: 100px; display: inline-block; }}
.dt-value {{ color: #e4e6ef; }}
.dt-value a {{ color: #64b5f6; text-decoration: none; }}
.dt-value a:hover {{ text-decoration: underline; }}
.dt-section {{
  margin-top: 8px; padding: 8px 10px; background: #0f1117;
  border-radius: 8px; border: 1px solid #2e3345;
}}
.dt-section-title {{ font-weight: 700; color: #d4a843; font-size: 12px; margin-bottom: 4px; }}
.dt-links {{
  display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px;
}}
.dt-links a {{
  display: inline-block; padding: 4px 12px; border-radius: 8px;
  font-size: 12px; font-weight: 600; text-decoration: none;
  border: 1px solid #2e3345; color: #e4e6ef; transition: border-color .15s;
}}
.dt-links a:hover {{ border-color: #d4a843; color: #d4a843; }}

/* Count */
.count-bar {{
  padding: 4px 16px; font-size: 12px; color: #555;
}}

/* Empty */
.empty {{ text-align: center; padding: 40px 20px; color: #555; font-size: 14px; }}

/* Mobile */
@media (max-width: 480px) {{
  .summary {{ grid-template-columns: repeat(2, 1fr); }}
  .filters {{ flex-direction: column; }}
  .filters select, .filters input {{ width: 100%; }}
}}
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>The Surveyor v2 — Dashboard รวม 4 ทีม</h1>
    <div class="sub">ศาลาที่พักผู้โดยสาร กรุงเทพมหานคร</div>
  </div>
  <span class="badge-dummy">DUMMY DATA</span>
</div>

<div id="summaryBar" class="summary"></div>

<div class="filters">
  <select id="fTor"><option value="">TOR ทั้งหมด</option></select>
  <select id="fDistrict"><option value="">เขต ทั้งหมด</option></select>
  <input id="fSearch" type="search" placeholder="ค้น code, เขต, ถนน, สถานที่..." autocomplete="off">
  <select id="fP1"><option value="">P1 ทั้งหมด</option></select>
  <select id="fP2"><option value="">P2 ทั้งหมด</option></select>
  <select id="fP3"><option value="">P3 ทั้งหมด</option></select>
  <select id="fP4"><option value="">P4 ทั้งหมด</option></select>
</div>

<div id="countBar" class="count-bar"></div>
<div id="shelterList" class="shelter-list"></div>

<script>
// ===== DATA =====
const DATA = {data_json};

// ===== FORM URLS =====
const FORMS = {{
  p1: {{ url: "https://docs.google.com/forms/d/e/1FAIpQLSfpfTkED3m-66HalnmnKZSSxpjvY3c97Y4wmSJp4Dv4a9vJ1A/viewform", entry: "62705490" }},
  p2: {{ url: "https://docs.google.com/forms/d/e/1FAIpQLSeaDJtyyu7Ba4ZT7P34P8Qkrtau3ddVr5F1JP2eCplp7NdS1g/viewform", entry: "XXXXXX" }},
  p3: {{ url: "https://docs.google.com/forms/d/e/1FAIpQLSd1i8sw2-ZXvjGO3OeEmHgTA_bTD8YSpd0UlnN1aunqXY2Beg/viewform", entry: "XXXXXX" }},
  p4: {{ url: "https://docs.google.com/forms/d/e/1FAIpQLSeLmkl5WLc57j8nwGW4iV84seIDDA-q-UCCYvknm8kVrpAAEQ/viewform", entry: "XXXXXX" }},
}};

// ===== UTILS =====
function esc(s) {{
  if (!s) return '';
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}}

function statusPill(phase, val, rounds) {{
  const lbl = phase.toUpperCase();
  if (val === 'done') return '<span class="pill-label">' + lbl + '</span><span class="pill p-done">\u2705</span>';
  if (val === 'pending') return '<span class="pill-label">' + lbl + '</span><span class="pill p-pending">\u23f3</span>';
  if (val === 'na') return '<span class="pill-label">' + lbl + '</span><span class="pill p-na">\u2014</span>';
  if (val === 'waiting') return '<span class="pill-label">' + lbl + '</span><span class="pill p-waiting">\u23f8</span>';
  if (val === 'partial') return '<span class="pill-label">' + lbl + '</span><span class="pill p-partial">R' + rounds + '/4</span>';
  return '';
}}

function formUrl(phase, code) {{
  const f = FORMS[phase];
  if (!f) return '#';
  return f.url + '?usp=pp_url&entry.' + f.entry + '=' + encodeURIComponent(code);
}}

function mapsUrl(lat, lng) {{
  if (!lat || !lng) return '';
  return 'https://www.google.com/maps?q=' + lat + ',' + lng;
}}

// ===== SUMMARY =====
function renderSummary() {{
  const total = DATA.length;
  const traffyTotal = DATA.filter(s => s.p1 !== 'na').length;
  const p1Done = DATA.filter(s => s.p1 === 'done').length;
  const p2Done = DATA.filter(s => s.p2 === 'done').length;
  const p3Eligible = DATA.filter(s => s.p3 !== 'na' && s.p3 !== 'waiting').length;
  const p3Done = DATA.filter(s => s.p3 === 'done').length;
  const p4Done = DATA.filter(s => s.p4 === 'done').length;

  document.getElementById('summaryBar').innerHTML = `
    <div class="sum-card"><span class="n">${{total}}</span><span class="l">ศาลาทั้งหมด</span></div>
    <div class="sum-card"><span class="n">${{p1Done}}/${{traffyTotal}}</span><span class="l">P1 Traffy</span><span class="d">เฉพาะเคส Traffy</span></div>
    <div class="sum-card"><span class="n">${{p2Done}}/${{total}}</span><span class="l">P2 ตรวจสภาพ</span></div>
    <div class="sum-card"><span class="n">${{p3Done}}/${{p3Eligible}}</span><span class="l">P3 ซ่อมบำรุง</span><span class="d">เฉพาะที่พบความเสียหาย</span></div>
    <div class="sum-card"><span class="n">${{p4Done}}/${{total}}</span><span class="l">P4 ทำความสะอาด R1</span></div>
  `;
}}

// ===== FILTERS =====
function populateFilters() {{
  const tors = new Set();
  const districts = new Set();
  const statuses = ['done', 'pending', 'na', 'waiting', 'partial'];
  const statusLabels = {{ done: 'done \u2705', pending: 'pending \u23f3', na: 'na \u2014', waiting: 'waiting \u23f8', partial: 'partial' }};

  DATA.forEach(s => {{
    if (s.tor) tors.add(s.tor);
    if (s.district) districts.add(s.district);
  }});

  const torSel = document.getElementById('fTor');
  [...tors].sort().forEach(t => {{
    const o = document.createElement('option');
    o.value = t; o.textContent = t;
    torSel.appendChild(o);
  }});

  const distSel = document.getElementById('fDistrict');
  [...districts].sort().forEach(d => {{
    const o = document.createElement('option');
    o.value = d; o.textContent = d;
    distSel.appendChild(o);
  }});

  ['fP1','fP2','fP3','fP4'].forEach(id => {{
    const sel = document.getElementById(id);
    statuses.forEach(st => {{
      const o = document.createElement('option');
      o.value = st; o.textContent = statusLabels[st];
      sel.appendChild(o);
    }});
  }});
}}

function getFiltered() {{
  const q = document.getElementById('fSearch').value.toLowerCase();
  const tor = document.getElementById('fTor').value;
  const dist = document.getElementById('fDistrict').value;
  const fp1 = document.getElementById('fP1').value;
  const fp2 = document.getElementById('fP2').value;
  const fp3 = document.getElementById('fP3').value;
  const fp4 = document.getElementById('fP4').value;

  return DATA.filter(s => {{
    if (tor && s.tor !== tor) return false;
    if (dist && s.district !== dist) return false;
    if (fp1 && s.p1 !== fp1) return false;
    if (fp2 && s.p2 !== fp2) return false;
    if (fp3 && s.p3 !== fp3) return false;
    if (fp4 && s.p4 !== fp4) return false;
    if (q) {{
      const hay = [s.code, s.district, s.road, s.location].join(' ').toLowerCase();
      if (!hay.includes(q)) return false;
    }}
    return true;
  }});
}}

// ===== RENDER =====
function toggleCard(el) {{
  el.classList.toggle('expanded');
}}

function renderShelters() {{
  const filtered = getFiltered();
  const container = document.getElementById('shelterList');
  document.getElementById('countBar').textContent = 'แสดง ' + filtered.length + ' / ' + DATA.length + ' ศาลา';

  if (!filtered.length) {{
    container.innerHTML = '<div class="empty">ไม่พบศาลาที่ตรงเงื่อนไข</div>';
    return;
  }}

  // Render in batches for performance
  const BATCH = 200;
  const show = filtered.slice(0, BATCH);

  container.innerHTML = show.map(s => {{
    const maps = mapsUrl(s.lat, s.long);
    return `<div class="shelter-card" onclick="toggleCard(this)">
      <div class="card-top">
        <span class="card-code">${{esc(s.code)}}</span>
        <span class="card-dist">${{esc(s.district)}}</span>
        <span class="card-road">${{esc(s.road)}}</span>
      </div>
      <div class="card-loc">${{esc(s.location)}}</div>
      <div class="card-pills">
        ${{statusPill('p1', s.p1, 0)}}
        ${{statusPill('p2', s.p2, 0)}}
        ${{statusPill('p3', s.p3, 0)}}
        ${{statusPill('p4', s.p4, s.p4r)}}
      </div>
      <div class="card-detail">
        <div class="dt-row"><span class="dt-label">สถานที่</span><span class="dt-value">${{esc(s.location)}}</span></div>
        <div class="dt-row"><span class="dt-label">ประเภท</span><span class="dt-value">${{esc(s.type)}}</span></div>

        <div class="dt-section">
          <div class="dt-section-title">P1 Traffy</div>
          <div class="dt-row"><span class="dt-label">สถานะ</span><span class="dt-value">${{s.p1}}</span></div>
          ${{s.p1_ts ? '<div class="dt-row"><span class="dt-label">วันที่</span><span class="dt-value">' + esc(s.p1_ts) + '</span></div>' : ''}}
          ${{s.p1_dmg ? '<div class="dt-row"><span class="dt-label">ความเสียหาย</span><span class="dt-value">' + esc(s.p1_dmg) + '</span></div>' : ''}}
        </div>

        <div class="dt-section">
          <div class="dt-section-title">P2 ตรวจสภาพ</div>
          <div class="dt-row"><span class="dt-label">สถานะ</span><span class="dt-value">${{s.p2}}</span></div>
          ${{s.p2_ts ? '<div class="dt-row"><span class="dt-label">วันที่</span><span class="dt-value">' + esc(s.p2_ts) + '</span></div>' : ''}}
          ${{s.p2_items ? '<div class="dt-row"><span class="dt-label">รายการ</span><span class="dt-value">' + esc(s.p2_items) + '</span></div>' : ''}}
        </div>

        <div class="dt-section">
          <div class="dt-section-title">P3 ซ่อมบำรุง</div>
          <div class="dt-row"><span class="dt-label">สถานะ</span><span class="dt-value">${{s.p3}}</span></div>
          ${{s.p3_ts ? '<div class="dt-row"><span class="dt-label">วันที่</span><span class="dt-value">' + esc(s.p3_ts) + '</span></div>' : ''}}
        </div>

        <div class="dt-section">
          <div class="dt-section-title">P4 ทำความสะอาด</div>
          <div class="dt-row"><span class="dt-label">สถานะ</span><span class="dt-value">${{s.p4}} (${{s.p4r}}/4 รอบ)</span></div>
          ${{s.p4_ts ? '<div class="dt-row"><span class="dt-label">ล่าสุด</span><span class="dt-value">' + esc(s.p4_ts) + '</span></div>' : ''}}
        </div>

        <div class="dt-links">
          <a href="${{formUrl('p1', s.code)}}" target="_blank">&#x1F4CB; P1 Form</a>
          <a href="${{formUrl('p2', s.code)}}" target="_blank">&#x1F4CB; P2 Form</a>
          <a href="${{formUrl('p3', s.code)}}" target="_blank">&#x1F4CB; P3 Form</a>
          <a href="${{formUrl('p4', s.code)}}" target="_blank">&#x1F4CB; P4 Form</a>
          ${{maps ? '<a href="' + maps + '" target="_blank">&#x1F4CD; Google Maps</a>' : ''}}
          ${{s.folder ? '<a href="' + esc(s.folder) + '" target="_blank">&#x1F4C1; Drive Folder</a>' : ''}}
        </div>
      </div>
    </div>`;
  }}).join('');

  // Lazy-load remaining
  if (filtered.length > BATCH) {{
    const more = document.createElement('div');
    more.className = 'empty';
    more.id = 'loadMore';
    more.textContent = 'showing ' + BATCH + ' / ' + filtered.length + ' — scroll for more';
    container.appendChild(more);

    let loaded = BATCH;
    const observer = new IntersectionObserver((entries) => {{
      if (entries[0].isIntersecting && loaded < filtered.length) {{
        const next = filtered.slice(loaded, loaded + BATCH);
        const frag = document.createDocumentFragment();
        const tmp = document.createElement('div');
        tmp.innerHTML = next.map(s => {{
          const maps = mapsUrl(s.lat, s.long);
          return `<div class="shelter-card" onclick="toggleCard(this)">
            <div class="card-top">
              <span class="card-code">${{esc(s.code)}}</span>
              <span class="card-dist">${{esc(s.district)}}</span>
              <span class="card-road">${{esc(s.road)}}</span>
            </div>
            <div class="card-loc">${{esc(s.location)}}</div>
            <div class="card-pills">
              ${{statusPill('p1', s.p1, 0)}}
              ${{statusPill('p2', s.p2, 0)}}
              ${{statusPill('p3', s.p3, 0)}}
              ${{statusPill('p4', s.p4, s.p4r)}}
            </div>
            <div class="card-detail">
              <div class="dt-row"><span class="dt-label">location</span><span class="dt-value">${{esc(s.location)}}</span></div>
              <div class="dt-row"><span class="dt-label">type</span><span class="dt-value">${{esc(s.type)}}</span></div>
              <div class="dt-section">
                <div class="dt-section-title">P1 Traffy</div>
                <div class="dt-row"><span class="dt-label">status</span><span class="dt-value">${{s.p1}}</span></div>
                ${{s.p1_ts ? '<div class="dt-row"><span class="dt-label">date</span><span class="dt-value">' + esc(s.p1_ts) + '</span></div>' : ''}}
                ${{s.p1_dmg ? '<div class="dt-row"><span class="dt-label">damage</span><span class="dt-value">' + esc(s.p1_dmg) + '</span></div>' : ''}}
              </div>
              <div class="dt-section">
                <div class="dt-section-title">P2 Inspection</div>
                <div class="dt-row"><span class="dt-label">status</span><span class="dt-value">${{s.p2}}</span></div>
                ${{s.p2_ts ? '<div class="dt-row"><span class="dt-label">date</span><span class="dt-value">' + esc(s.p2_ts) + '</span></div>' : ''}}
                ${{s.p2_items ? '<div class="dt-row"><span class="dt-label">items</span><span class="dt-value">' + esc(s.p2_items) + '</span></div>' : ''}}
              </div>
              <div class="dt-section">
                <div class="dt-section-title">P3 Maintenance</div>
                <div class="dt-row"><span class="dt-label">status</span><span class="dt-value">${{s.p3}}</span></div>
                ${{s.p3_ts ? '<div class="dt-row"><span class="dt-label">date</span><span class="dt-value">' + esc(s.p3_ts) + '</span></div>' : ''}}
              </div>
              <div class="dt-section">
                <div class="dt-section-title">P4 Cleaning</div>
                <div class="dt-row"><span class="dt-label">status</span><span class="dt-value">${{s.p4}} (${{s.p4r}}/4 rounds)</span></div>
                ${{s.p4_ts ? '<div class="dt-row"><span class="dt-label">latest</span><span class="dt-value">' + esc(s.p4_ts) + '</span></div>' : ''}}
              </div>
              <div class="dt-links">
                <a href="${{formUrl('p1', s.code)}}" target="_blank">&#x1F4CB; P1 Form</a>
                <a href="${{formUrl('p2', s.code)}}" target="_blank">&#x1F4CB; P2 Form</a>
                <a href="${{formUrl('p3', s.code)}}" target="_blank">&#x1F4CB; P3 Form</a>
                <a href="${{formUrl('p4', s.code)}}" target="_blank">&#x1F4CB; P4 Form</a>
                ${{maps ? '<a href="' + maps + '" target="_blank">&#x1F4CD; Google Maps</a>' : ''}}
                ${{s.folder ? '<a href="' + esc(s.folder) + '" target="_blank">&#x1F4C1; Drive Folder</a>' : ''}}
              </div>
            </div>
          </div>`;
        }}).join('');
        while (tmp.firstChild) frag.appendChild(tmp.firstChild);
        container.insertBefore(frag, more);
        loaded += next.length;
        if (loaded >= filtered.length) {{
          observer.disconnect();
          more.remove();
        }} else {{
          more.textContent = 'แสดง ' + loaded + ' จาก ' + filtered.length + ' — เลื่อนลงเพื่อโหลดเพิ่ม';
        }}
      }}
    }});
    observer.observe(more);
  }}
}}

// ===== INIT =====
renderSummary();
populateFilters();
renderShelters();

// Debounced search
let searchTimer;
document.getElementById('fSearch').addEventListener('input', () => {{
  clearTimeout(searchTimer);
  searchTimer = setTimeout(renderShelters, 200);
}});
document.getElementById('fTor').addEventListener('change', renderShelters);
document.getElementById('fDistrict').addEventListener('change', renderShelters);
document.getElementById('fP1').addEventListener('change', renderShelters);
document.getElementById('fP2').addEventListener('change', renderShelters);
document.getElementById('fP3').addEventListener('change', renderShelters);
document.getElementById('fP4').addEventListener('change', renderShelters);
</script>
</body>
</html>"""

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\nGenerated: {OUT_HTML}")
    print(f"  HTML size: {len(html_content):,} bytes")


if __name__ == "__main__":
    main()
