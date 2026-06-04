#!/usr/bin/env python3
"""
gen_dedup_report.py — Generate กทม. dedup report for Traffy Fondue cases.
Outputs:
  v2/output/traffy_dedup_report.html  (formal Thai report)
  v2/output/traffy_dedup_report.csv   (data handoff)
"""

import csv
import os
from datetime import datetime
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
OUT = os.path.join(BASE, "output")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

def load_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

rematched = load_csv(os.path.join(DATA, "traffy_rematched.csv"))
dedup = load_csv(os.path.join(DATA, "traffy_dedup.csv"))
cases = load_csv(os.path.join(DATA, "traffy_cases.csv"))

# ---------------------------------------------------------------------------
# Compute stats
# ---------------------------------------------------------------------------

total_tickets = len(rematched)  # 40 rows = 40 case-rows (some rows have multi-ticket_id)

# Count actual individual ticket IDs across all rows
all_ticket_ids = []
for r in rematched:
    for tid in r["ticket_id"].split(","):
        tid = tid.strip().strip('"')
        if tid:
            all_ticket_ids.append(tid)
total_individual_tickets = len(all_ticket_ids)

unique_shelters = len(dedup)  # 33

# matched = distance <= 200m in rematched
matched_rows = [r for r in rematched if r["match_status"] == "matched"]
unmatched_rows = [r for r in rematched if r["match_status"] != "matched"]
matched_count = len(matched_rows)
unmatched_count = len(unmatched_rows)

# work_type breakdown from rematched
wt_counter = Counter()
wt_matched = Counter()
wt_unmatched = Counter()
for r in rematched:
    wt = r["work_type"].strip()
    wt_counter[wt] += 1
    if r["match_status"] == "matched":
        wt_matched[wt] += 1
    else:
        wt_unmatched[wt] += 1

# Multi-ticket shelters from dedup
multi_ticket = [d for d in dedup if int(d["ticket_count"]) > 1]
multi_ticket.sort(key=lambda d: int(d["ticket_count"]), reverse=True)

# For Table 2, build from rematched sorted: matched first, then unmatched, within each by distance
sorted_cases = sorted(rematched, key=lambda r: (0 if r["match_status"] == "matched" else 1, float(r["distance_m"])))

# For multi-ticket table, enrich with district from rematched
shelter_district = {}
shelter_location = {}
for r in rematched:
    sc = r["shelter_code"]
    if sc not in shelter_district:
        shelter_district[sc] = r.get("district_shelter", r.get("district_case", ""))
        shelter_location[sc] = r.get("shelter_location", "")

today = datetime.now().strftime("%d/%m/%Y")
today_file = datetime.now().strftime("%Y-%m-%d")

# ---------------------------------------------------------------------------
# Generate CSV
# ---------------------------------------------------------------------------

csv_path = os.path.join(OUT, "traffy_dedup_report.csv")
with open(csv_path, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["shelter_code", "ticket_count", "ticket_ids", "work_types", "district", "match_status", "distance_m"])
    for d in dedup:
        sc = d["shelter_code"]
        # Determine match_status and distance from rematched (use first matching row)
        ms = ""
        dist = ""
        for r in rematched:
            if r["shelter_code"] == sc:
                ms = r["match_status"]
                dist = r["distance_m"]
                break
        district = shelter_district.get(sc, "")
        w.writerow([sc, d["ticket_count"], d["ticket_ids"], d["work_types"], district, ms, dist])

print(f"CSV written: {csv_path}")

# ---------------------------------------------------------------------------
# Generate HTML
# ---------------------------------------------------------------------------

def esc(s):
    """Escape HTML special chars."""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def status_thai(s):
    if s == "matched":
        return "จับคู่สำเร็จ"
    else:
        return "รอตรวจสอบ"

def status_class(s):
    return "matched" if s == "matched" else "unmatched"

# Sum total individual tickets from multi-ticket shelters
multi_total_tickets = sum(int(d["ticket_count"]) for d in multi_ticket)

html = f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>รายงานสรุปการจับคู่เคสร้องเรียน — ศาลาที่พักผู้โดยสาร</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600;700&display=swap');

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
    font-family: 'Sarabun', sans-serif;
    font-size: 14px;
    color: #1a1a2e;
    background: #fff;
    line-height: 1.6;
}}

@media print {{
    body {{ font-size: 11px; }}
    .page-break {{ page-break-before: always; }}
    .no-print {{ display: none; }}
}}

@page {{
    size: A4;
    margin: 20mm 15mm;
}}

.container {{
    max-width: 210mm;
    margin: 0 auto;
    padding: 20px 30px;
}}

/* Header */
.report-header {{
    border-bottom: 3px solid #16213e;
    padding-bottom: 16px;
    margin-bottom: 24px;
}}

.logo-area {{
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 12px;
}}

.logo-placeholder {{
    width: 60px;
    height: 60px;
    border: 2px solid #16213e;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    color: #666;
    text-align: center;
}}

.header-text h1 {{
    font-size: 20px;
    font-weight: 700;
    color: #16213e;
    letter-spacing: 0.5px;
}}

.header-text .subtitle {{
    font-size: 13px;
    color: #4a5568;
    margin-top: 2px;
}}

.report-date {{
    font-size: 12px;
    color: #718096;
    text-align: right;
    margin-top: -20px;
}}

/* Executive Summary */
.exec-summary {{
    background: linear-gradient(135deg, #f0f4ff 0%, #e8eef9 100%);
    border: 1px solid #c3d4e9;
    border-left: 5px solid #16213e;
    border-radius: 6px;
    padding: 20px 24px;
    margin-bottom: 28px;
}}

.exec-summary h2 {{
    font-size: 16px;
    color: #16213e;
    margin-bottom: 14px;
    font-weight: 700;
}}

.stat-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px 24px;
}}

.stat-item {{
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    border-bottom: 1px dotted #c3d4e9;
}}

.stat-label {{
    color: #4a5568;
    font-weight: 400;
}}

.stat-value {{
    font-weight: 700;
    color: #16213e;
    font-size: 15px;
}}

.stat-highlight {{
    background: #16213e;
    color: #fff;
    padding: 10px 16px;
    border-radius: 6px;
    margin-top: 14px;
    text-align: center;
    font-size: 14px;
    grid-column: 1 / -1;
}}

.stat-highlight strong {{
    font-size: 18px;
}}

/* Section headings */
.section-title {{
    font-size: 16px;
    font-weight: 700;
    color: #16213e;
    border-bottom: 2px solid #16213e;
    padding-bottom: 6px;
    margin: 28px 0 14px 0;
}}

.section-desc {{
    color: #4a5568;
    margin-bottom: 12px;
    font-size: 13px;
}}

/* Tables */
table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
    font-size: 12px;
}}

th {{
    background: #16213e;
    color: #fff;
    padding: 8px 10px;
    text-align: left;
    font-weight: 600;
    font-size: 11px;
    white-space: nowrap;
}}

td {{
    padding: 6px 10px;
    border-bottom: 1px solid #e2e8f0;
    vertical-align: top;
}}

tr:nth-child(even) {{
    background: #f8fafc;
}}

tr:hover {{
    background: #eef2ff;
}}

.badge {{
    display: inline-block;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 10px;
    font-weight: 600;
}}

.badge-matched {{
    background: #d4edda;
    color: #155724;
}}

.badge-unmatched {{
    background: #fff3cd;
    color: #856404;
}}

.ticket-count {{
    background: #16213e;
    color: #fff;
    display: inline-block;
    width: 28px;
    height: 28px;
    line-height: 28px;
    text-align: center;
    border-radius: 50%;
    font-weight: 700;
    font-size: 13px;
}}

.multi-highlight {{
    background: #fff8e1;
}}

.ticket-id {{
    font-family: monospace;
    font-size: 11px;
    color: #2d3748;
}}

.dist-val {{
    font-weight: 600;
}}

.dist-close {{ color: #155724; }}
.dist-mid {{ color: #856404; }}
.dist-far {{ color: #721c24; }}

.wt-bar {{
    height: 8px;
    background: #16213e;
    border-radius: 4px;
    display: inline-block;
    vertical-align: middle;
    margin-right: 6px;
}}

.wt-bar-unmatched {{
    background: #a0aec0;
}}

/* Footer */
.report-footer {{
    margin-top: 40px;
    padding-top: 16px;
    border-top: 2px solid #16213e;
    font-size: 11px;
    color: #718096;
    display: flex;
    justify-content: space-between;
}}

.desc-cell {{
    max-width: 200px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}}
</style>
</head>
<body>
<div class="container">

<!-- HEADER -->
<div class="report-header">
    <div class="logo-area">
        <div class="logo-placeholder">โลโก้<br>หน่วยงาน</div>
        <div class="header-text">
            <h1>รายงานสรุปการจับคู่เคสร้องเรียน</h1>
            <div class="subtitle">ศาลาที่พักผู้โดยสาร — ระบบ Traffy Fondue</div>
        </div>
    </div>
    <div class="report-date">วันที่จัดทำ: {today}</div>
</div>

<!-- EXECUTIVE SUMMARY -->
<div class="exec-summary">
    <h2>สรุปภาพรวม (Executive Summary)</h2>
    <div class="stat-grid">
        <div class="stat-item">
            <span class="stat-label">จำนวน ticket Traffy ทั้งหมด</span>
            <span class="stat-value">{total_individual_tickets} ticket</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">จำนวนแถวข้อมูล (case-rows)</span>
            <span class="stat-value">{total_tickets} แถว</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">จำนวนศาลาที่ระบุได้ (unique shelters)</span>
            <span class="stat-value">{unique_shelters} จุด</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">จำนวนเคสที่จับคู่สำเร็จ (≤200m)</span>
            <span class="stat-value">{matched_count} เคส</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">จำนวนเคสรอตรวจสอบ (&gt;200m)</span>
            <span class="stat-value">{unmatched_count} เคส</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">อัตราส่วน ticket : shelter</span>
            <span class="stat-value">{total_individual_tickets} : {unique_shelters}</span>
        </div>
        <div class="stat-highlight">
            <strong>{total_individual_tickets}</strong> ticket จากประชาชน → จับกลุ่มได้เป็น <strong>{unique_shelters}</strong> ศาลาที่ต้องดำเนินการ
            &nbsp;|&nbsp; แก้ไข 1 จุด = เคลียร์ได้หลาย ticket พร้อมกัน
        </div>
    </div>
</div>

<!-- WORK TYPE BREAKDOWN in summary -->
<div class="exec-summary" style="border-left-color: #2b5ea7;">
    <h2>ประเภทงานที่ร้องเรียน</h2>
    <table>
        <tr>
            <th>ประเภทงาน (work_type)</th>
            <th style="text-align:center">จำนวนเคส</th>
            <th style="text-align:center">สัดส่วน</th>
        </tr>
"""

for wt, count in sorted(wt_counter.items(), key=lambda x: -x[1]):
    pct = count / total_tickets * 100
    bar_w = int(pct * 2)
    html += f"""        <tr>
            <td>{esc(wt)}</td>
            <td style="text-align:center">{count}</td>
            <td><div class="wt-bar" style="width:{bar_w}px"></div> {pct:.0f}%</td>
        </tr>
"""

html += """    </table>
</div>

<!-- TABLE 1: MULTI-TICKET SHELTERS -->
"""

html += f"""<h2 class="section-title">ตารางที่ 1: ศาลาที่มีหลาย ticket (Multi-ticket Shelters)</h2>
<p class="section-desc">ศาลาที่มีประชาชนร้องเรียนมากกว่า 1 ticket — แก้ไข 1 จุด เคลียร์ได้หลายเคสพร้อมกัน
({len(multi_ticket)} ศาลา รวม {multi_total_tickets} ticket)</p>
<table>
    <tr>
        <th>รหัสศาลา</th>
        <th style="text-align:center">จำนวน ticket</th>
        <th>Ticket IDs</th>
        <th>ประเภทงาน</th>
        <th>เขต</th>
        <th>ตำแหน่ง</th>
    </tr>
"""

for d in multi_ticket:
    sc = d["shelter_code"]
    tc = int(d["ticket_count"])
    html += f"""    <tr class="multi-highlight">
        <td><strong>{esc(sc)}</strong></td>
        <td style="text-align:center"><span class="ticket-count">{tc}</span></td>
        <td class="ticket-id">{esc(d['ticket_ids'])}</td>
        <td>{esc(d['work_types'])}</td>
        <td>{esc(shelter_district.get(sc, ''))}</td>
        <td>{esc(shelter_location.get(sc, ''))}</td>
    </tr>
"""

html += """</table>

<div class="page-break"></div>

<!-- TABLE 2: ALL CASES BY STATUS -->
"""

html += """<h2 class="section-title">ตารางที่ 2: รายละเอียดเคสทั้งหมด จำแนกตามสถานะ</h2>
<p class="section-desc">เรียงจากเคสที่จับคู่สำเร็จ (matched ≤200m) ก่อน ตามด้วยเคสรอตรวจสอบ</p>
<table>
    <tr>
        <th>#</th>
        <th>Ticket ID</th>
        <th>สถานะ</th>
        <th>รหัสศาลา</th>
        <th style="text-align:right">ระยะห่าง (m)</th>
        <th>ประเภทงาน</th>
        <th>เขต</th>
        <th>รายละเอียด</th>
    </tr>
"""

for i, r in enumerate(sorted_cases, 1):
    dist = float(r["distance_m"])
    if dist <= 100:
        dist_cls = "dist-close"
    elif dist <= 500:
        dist_cls = "dist-mid"
    else:
        dist_cls = "dist-far"

    badge_cls = "badge-matched" if r["match_status"] == "matched" else "badge-unmatched"
    status = status_thai(r["match_status"])
    desc = r.get("description", "")
    if len(desc) > 60:
        desc = desc[:60] + "..."

    html += f"""    <tr>
        <td>{i}</td>
        <td class="ticket-id">{esc(r['ticket_id'])}</td>
        <td><span class="badge {badge_cls}">{status}</span></td>
        <td><strong>{esc(r['shelter_code'])}</strong></td>
        <td style="text-align:right"><span class="dist-val {dist_cls}">{dist:,.1f}</span></td>
        <td>{esc(r['work_type'])}</td>
        <td>{esc(r.get('district_shelter', r.get('district_case', '')))}</td>
        <td class="desc-cell">{esc(desc)}</td>
    </tr>
"""

html += """</table>

<div class="page-break"></div>

<!-- TABLE 3: WORK TYPE SUMMARY -->
"""

html += """<h2 class="section-title">ตารางที่ 3: สรุปตามประเภทงาน (Work Type Summary)</h2>
<p class="section-desc">จำนวนเคสแยกตามประเภทงานและสถานะการจับคู่</p>
<table>
    <tr>
        <th>ประเภทงาน</th>
        <th style="text-align:center">รวมทั้งหมด</th>
        <th style="text-align:center">จับคู่สำเร็จ</th>
        <th style="text-align:center">รอตรวจสอบ</th>
        <th>สัดส่วนจับคู่</th>
    </tr>
"""

for wt, count in sorted(wt_counter.items(), key=lambda x: -x[1]):
    m = wt_matched.get(wt, 0)
    u = wt_unmatched.get(wt, 0)
    pct = m / count * 100 if count > 0 else 0
    bar_m = int(pct * 1.5)
    bar_u = int((100 - pct) * 1.5)
    html += f"""    <tr>
        <td>{esc(wt)}</td>
        <td style="text-align:center"><strong>{count}</strong></td>
        <td style="text-align:center">{m}</td>
        <td style="text-align:center">{u}</td>
        <td>
            <div class="wt-bar" style="width:{bar_m}px"></div><div class="wt-bar wt-bar-unmatched" style="width:{bar_u}px"></div>
            &nbsp;{pct:.0f}%
        </td>
    </tr>
"""

html += f"""</table>

<!-- FOOTER -->
<div class="report-footer">
    <span>จัดทำโดยระบบ The Surveyor v2 — Traffy Dedup Pipeline</span>
    <span>วันที่ {today}</span>
</div>

</div>
</body>
</html>
"""

html_path = os.path.join(OUT, "traffy_dedup_report.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"HTML written: {html_path}")

# ---------------------------------------------------------------------------
# Print summary
# ---------------------------------------------------------------------------

print("\n" + "=" * 60)
print("DEDUP REPORT SUMMARY")
print("=" * 60)
print(f"Total individual tickets:    {total_individual_tickets}")
print(f"Total case-rows:             {total_tickets}")
print(f"Unique shelters:             {unique_shelters}")
print(f"Matched (≤200m):             {matched_count}")
print(f"Unmatched (>200m):           {unmatched_count}")
print(f"Multi-ticket shelters:       {len(multi_ticket)}")
print(f"  → total tickets in multi:  {multi_total_tickets}")
print(f"\nWork type breakdown:")
for wt, count in sorted(wt_counter.items(), key=lambda x: -x[1]):
    m = wt_matched.get(wt, 0)
    u = wt_unmatched.get(wt, 0)
    print(f"  {wt:25s}  total={count:2d}  matched={m:2d}  unmatched={u:2d}")
print("=" * 60)
