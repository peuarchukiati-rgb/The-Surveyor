"""
import_traffy.py — Convert Traffy case-matching Excel into clean CSVs.

Input:  ~/Downloads/จับคู่เคส-ศาลา.xlsx
Output: v2/data/traffy_cases.csv, v2/data/traffy_dedup.csv
"""

import csv
import os
from collections import defaultdict
from pathlib import Path

import openpyxl

# Paths
XLSX_PATH = os.path.expanduser("~/Downloads/จับคู่เคส-ศาลา.xlsx")
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CASES_CSV = DATA_DIR / "traffy_cases.csv"
DEDUP_CSV = DATA_DIR / "traffy_dedup.csv"

# Column mapping: Thai header → English field name
COLUMN_MAP = {
    "รหัสเคส (ticket)": "ticket_id",
    "สถานะจับคู่": "match_status",
    "รหัสศาลา": "shelter_code",
    "ประเภทศาลา": "shelter_type",
    "เขต(ศาลา)": "district_shelter",
    "ถนน": "road",
    "ตำแหน่งศาลา": "shelter_location",
    "ระยะห่าง (ม.)": "distance_m",
    "ศาลาใกล้สุด#2": "nearest_2nd",
    "ระยะ#2 (ม.)": "distance_2nd_m",
    "ประเภทงาน": "work_type",
    "จำนวนแจ้ง": "report_count",
    "ลักษณะปัญหา": "description",
    "เขต(เคส)": "district_case",
    "ที่อยู่เคส": "case_address",
    "พิกัดเคส": "_coord_case",
    "พิกัดศาลา": "_coord_shelter",
}

OUTPUT_FIELDS = [
    "ticket_id", "match_status", "shelter_code", "shelter_type",
    "district_shelter", "road", "shelter_location", "distance_m",
    "nearest_2nd", "distance_2nd_m", "work_type", "report_count",
    "description", "district_case", "case_address",
    "case_lat", "case_long", "shelter_lat", "shelter_long",
]

DEDUP_FIELDS = [
    "shelter_code", "ticket_count", "ticket_ids", "work_types", "case_count",
]


def split_coord(val):
    """Split '13.76286,100.51431' into (lat, long). Returns ('','') if empty."""
    if not val:
        return ("", "")
    parts = str(val).split(",")
    if len(parts) == 2:
        return (parts[0].strip(), parts[1].strip())
    return ("", "")


def main():
    wb = openpyxl.load_workbook(XLSX_PATH, read_only=True, data_only=True)
    ws = wb["จับคู่เคส-ศาลา"]

    rows = list(ws.iter_rows(values_only=True))
    wb.close()

    headers = [str(h).strip() if h else "" for h in rows[0]]
    data_rows = rows[1:]

    # Build header index
    col_idx = {}
    for i, h in enumerate(headers):
        if h in COLUMN_MAP:
            col_idx[COLUMN_MAP[h]] = i
        elif h == "พิกัดเคส":
            col_idx["_coord_case"] = i
        elif h == "พิกัดศาลา":
            col_idx["_coord_shelter"] = i

    # Process rows
    cases = []
    for row in data_rows:
        if row[0] is None:
            continue  # skip empty rows

        record = {}
        for field, idx in col_idx.items():
            val = row[idx]
            record[field] = val if val is not None else ""

        # Split coordinates
        case_lat, case_long = split_coord(record.pop("_coord_case", ""))
        shelter_lat, shelter_long = split_coord(record.pop("_coord_shelter", ""))
        record["case_lat"] = case_lat
        record["case_long"] = case_long
        record["shelter_lat"] = shelter_lat
        record["shelter_long"] = shelter_long

        cases.append(record)

    # Write traffy_cases.csv
    with open(CASES_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        for c in cases:
            writer.writerow({k: c.get(k, "") for k in OUTPUT_FIELDS})

    # Build dedup by shelter_code
    shelter_map = defaultdict(lambda: {"tickets": [], "work_types": set()})
    for c in cases:
        code = c.get("shelter_code", "")
        if not code:
            continue
        shelter_map[code]["tickets"].append(str(c["ticket_id"]))
        wt = c.get("work_type", "")
        if wt:
            shelter_map[code]["work_types"].add(wt)

    dedup_rows = []
    for code in sorted(shelter_map.keys()):
        info = shelter_map[code]
        dedup_rows.append({
            "shelter_code": code,
            "ticket_count": len(info["tickets"]),
            "ticket_ids": ",".join(info["tickets"]),
            "work_types": ",".join(sorted(info["work_types"])),
            "case_count": 1,
        })

    with open(DEDUP_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=DEDUP_FIELDS)
        writer.writeheader()
        writer.writerows(dedup_rows)

    # Summary
    total = len(cases)
    matched = sum(1 for c in cases if c["match_status"] == "ตรงกับศาลา")
    review = sum(1 for c in cases if c["match_status"] == "ใกล้เคียง-ตรวจสอบ")
    unmatched = sum(1 for c in cases if c["match_status"] == "ไม่พบศาลา MS")

    multi = [(code, len(info["tickets"])) for code, info in shelter_map.items() if len(info["tickets"]) > 1]
    multi.sort(key=lambda x: -x[1])

    print(f"=== Traffy Import Summary ===")
    print(f"Total cases:   {total}")
    print(f"  Matched:     {matched}")
    print(f"  Review:      {review}")
    print(f"  Unmatched:   {unmatched}")
    print(f"Unique shelters: {len(shelter_map)}")
    print(f"Multi-ticket shelters: {len(multi)}")
    for code, count in multi:
        tickets = ",".join(shelter_map[code]["tickets"])
        print(f"  {code}: {count} tickets ({tickets})")
    print(f"\nOutput:")
    print(f"  {CASES_CSV}")
    print(f"  {DEDUP_CSV}")


if __name__ == "__main__":
    main()
