"""
gen_field_list.py
Generate printable HTML field verification list from traffy_rematched.csv
for field team to verify unmatched Traffy cases on-site.
"""

import csv
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
V2_DIR = os.path.dirname(SCRIPT_DIR)
INPUT_CSV = os.path.join(V2_DIR, "data", "traffy_rematched.csv")
OUTPUT_HTML = os.path.join(V2_DIR, "output", "field_verification_list.html")


def truncate(text, length=80):
    text = text.strip().replace("\n", " ")
    return text[:length] + "..." if len(text) > length else text


def maps_link(lat, lon):
    if lat and lon:
        return f"https://www.google.com/maps?q={lat},{lon}"
    return "#"


def read_csv():
    rows = []
    with open(INPUT_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def generate_html(rows):
    matched = [r for r in rows if r["match_status"] == "matched"]
    no_match = [r for r in rows if "no_match" in r["match_status"]]

    # Sort no_match by district_case for route efficiency
    no_match.sort(key=lambda r: r.get("district_case", ""))

    today = datetime.now().strftime("%d/%m/%Y")
    total = len(rows)
    n_matched = len(matched)
    n_nomatch = len(no_match)

    html = f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Field Verification List - Traffy Cases</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: 'Sarabun', sans-serif; font-size: 11px; color: #222; padding: 12mm; }}

  @media print {{
    body {{ padding: 0; }}
    .no-print {{ display: none; }}
    table {{ page-break-inside: auto; }}
    tr {{ page-break-inside: avoid; page-break-after: auto; }}
    .section {{ page-break-before: always; }}
    .section:first-of-type {{ page-break-before: avoid; }}
  }}

  .header {{ text-align: center; margin-bottom: 16px; border-bottom: 2px solid #1a237e; padding-bottom: 8px; }}
  .header h1 {{ font-size: 18px; font-weight: 700; color: #1a237e; }}
  .header .subtitle {{ font-size: 13px; color: #555; margin-top: 4px; }}
  .header .stats {{ font-size: 12px; margin-top: 6px; }}
  .header .stats span {{ background: #e8eaf6; padding: 2px 8px; border-radius: 3px; margin: 0 4px; }}

  .section h2 {{ font-size: 14px; font-weight: 700; color: #fff; background: #1a237e; padding: 6px 10px; margin: 14px 0 6px 0; }}
  .section h2.verify {{ background: #c62828; }}
  .section .note {{ font-size: 10px; color: #666; margin-bottom: 6px; padding-left: 4px; }}

  table {{ width: 100%; border-collapse: collapse; margin-bottom: 12px; }}
  th {{ background: #e8eaf6; font-weight: 600; text-align: left; padding: 4px 5px; border: 1px solid #bbb; font-size: 10px; }}
  td {{ padding: 3px 5px; border: 1px solid #ccc; vertical-align: top; font-size: 10.5px; line-height: 1.3; }}
  tr:nth-child(even) {{ background: #fafafa; }}
  tr:hover {{ background: #fff9c4; }}

  .check {{ width: 30px; text-align: center; font-size: 14px; }}
  .mono {{ font-family: monospace; font-size: 10px; }}
  a {{ color: #1565c0; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .dist {{ white-space: nowrap; }}
  .desc {{ max-width: 220px; word-break: break-word; }}
  .badge {{ display: inline-block; background: #e0e0e0; padding: 1px 4px; border-radius: 2px; font-size: 9px; }}
  .badge-district {{ background: #e3f2fd; color: #1565c0; }}
</style>
</head>
<body>

<div class="header">
  <h1>Traffy x Surveyor - Field Verification List</h1>
  <div class="subtitle">รายการตรวจสอบภาคสนาม สำหรับทีมพี่สาธิต</div>
  <div class="stats">
    วันที่พิมพ์: {today} &nbsp;|&nbsp;
    <span>ทั้งหมด {total} เคส</span>
    <span>Auto-matched: {n_matched}</span>
    <span>ต้องตรวจสอบ: {n_nomatch}</span>
  </div>
</div>

<!-- SECTION A: Auto-matched -->
<div class="section">
  <h2>Section A: Auto-matched ({n_matched} cases) - ยืนยันแล้ว ไปซ่อมได้เลย</h2>
  <div class="note">เคสเหล่านี้จับคู่ป้ายได้อัตโนมัติ ทีมไปดำเนินการซ่อมบำรุงตามรายการ</div>
  <table>
    <thead>
      <tr>
        <th class="check">ตรวจแล้ว</th>
        <th>#</th>
        <th>Ticket ID</th>
        <th>รหัสป้าย</th>
        <th>ระยะห่าง (m)</th>
        <th>ประเภทงาน</th>
        <th>รายละเอียด</th>
        <th>แผนที่</th>
      </tr>
    </thead>
    <tbody>
"""

    for i, r in enumerate(matched, 1):
        link = maps_link(r.get("case_lat", ""), r.get("case_long", ""))
        desc = truncate(r.get("description", ""))
        html += f"""      <tr>
        <td class="check">{chr(9744)}</td>
        <td>{i}</td>
        <td class="mono">{r['ticket_id']}</td>
        <td><b>{r.get('match_code', r.get('shelter_code', ''))}</b></td>
        <td class="dist">{r.get('match_dist_m', r.get('distance_m', ''))}</td>
        <td>{r.get('work_type', '')}</td>
        <td class="desc">{desc}</td>
        <td><a href="{link}" target="_blank">Maps</a></td>
      </tr>
"""

    html += """    </tbody>
  </table>
</div>

<!-- SECTION B: Field Verify -->
<div class="section">
"""
    html += f"""  <h2 class="verify">Section B: Field Verify ({n_nomatch} cases) - ต้องตรวจสอบภาคสนาม</h2>
  <div class="note">เคสเหล่านี้จับคู่ป้ายอัตโนมัติไม่ได้ ต้องไปยืนยันหน้างาน | เรียงตามเขตเพื่อวางเส้นทาง</div>
  <table>
    <thead>
      <tr>
        <th class="check">ตรวจแล้ว</th>
        <th>#</th>
        <th>Ticket ID</th>
        <th>รหัสป้าย (มนต์)</th>
        <th>ป้ายใกล้สุด</th>
        <th>ระยะ (m)</th>
        <th>เขต</th>
        <th>ประเภทงาน</th>
        <th>รายละเอียด</th>
        <th>ที่อยู่</th>
        <th>แผนที่</th>
      </tr>
    </thead>
    <tbody>
"""

    for i, r in enumerate(no_match, 1):
        link = maps_link(r.get("case_lat", ""), r.get("case_long", ""))
        desc = truncate(r.get("description", ""))
        addr = truncate(r.get("case_address", ""), 60)
        nearest = r.get("match_code", "") or r.get("shelter_code", "")
        shelter_code = r.get("shelter_code", "")
        dist = r.get("match_dist_m", "") or r.get("distance_m", "")
        district = r.get("district_case", "")

        html += f"""      <tr>
        <td class="check">{chr(9744)}</td>
        <td>{i}</td>
        <td class="mono">{r['ticket_id']}</td>
        <td>{shelter_code}</td>
        <td>{nearest}</td>
        <td class="dist">{dist}</td>
        <td><span class="badge badge-district">{district}</span></td>
        <td>{r.get('work_type', '')}</td>
        <td class="desc">{desc}</td>
        <td>{addr}</td>
        <td><a href="{link}" target="_blank">Maps</a></td>
      </tr>
"""

    html += """    </tbody>
  </table>
</div>

<div class="no-print" style="text-align:center; margin-top:20px; color:#999; font-size:11px;">
  Generated by gen_field_list.py | Print with Ctrl+P / Cmd+P
</div>

</body>
</html>"""

    return html, n_matched, n_nomatch


def main():
    os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)
    rows = read_csv()
    html, n_matched, n_nomatch = generate_html(rows)

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Generated: {OUTPUT_HTML}")
    print(f"Total cases: {len(rows)}")
    print(f"  Section A (Auto-matched): {n_matched}")
    print(f"  Section B (Field Verify): {n_nomatch}")


if __name__ == "__main__":
    main()
