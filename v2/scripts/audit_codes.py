"""
audit_codes.py — Extract QA/audit data from bkk_shelter_list.xlsx
Outputs three CSV files to v2/data/ and prints a summary.
"""

import csv
import os
from pathlib import Path

import openpyxl

XLSX = "/Users/peakeuarchukiati/Downloads/bkk_shelter_list.xlsx"
OUT_DIR = Path(__file__).resolve().parent.parent / "data"


def read_sheet(wb, name):
    """Return list of dicts from a worksheet (first row = headers)."""
    ws = wb[name]
    rows = list(ws.iter_rows(values_only=True))
    if len(rows) < 2:
        return []
    headers = rows[0]
    return [dict(zip(headers, r)) for r in rows[1:]]


def export_missing_codes(wb):
    """Parse รหัสที่ขาดหาย → audit_missing_codes.csv"""
    records = read_sheet(wb, "รหัสที่ขาดหาย")
    out_rows = []
    for rec in records:
        tor = rec["TOR"]
        max_code = rec["รหัสสูงสุดที่พบ"]
        missing_str = rec["ลำดับที่ขาด"] or ""
        codes = [c.strip() for c in missing_str.split(",") if c.strip()]
        for code in codes:
            out_rows.append({
                "tor": tor,
                "missing_code": code,
                "max_code_found": f"{tor}{max_code:03d}" if isinstance(max_code, (int, float)) else str(max_code),
                "note": f"{rec['จำนวนที่ขาด']} missing in {tor}",
            })
    path = OUT_DIR / "audit_missing_codes.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["tor", "missing_code", "max_code_found", "note"])
        w.writeheader()
        w.writerows(out_rows)
    return out_rows


def export_duplicates(wb):
    """Combine ซ้ำ_ชื่อสถานที่ + ซ้ำ_พิกัด → audit_duplicates.csv"""
    out_rows = []

    # Location duplicates
    for rec in read_sheet(wb, "ซ้ำ_ชื่อสถานที่"):
        detail = f"{rec['เขต']}/{rec['ถนน']}/{rec['ตำแหน่ง']}"
        out_rows.append({
            "type": "location",
            "detail": detail,
            "count": rec["จำนวน"],
            "codes": rec["รหัสที่ซ้ำ"],
        })

    # Coordinate duplicates
    for rec in read_sheet(wb, "ซ้ำ_พิกัด"):
        detail = f"({rec['lat']}, {rec['long']})"
        out_rows.append({
            "type": "coords",
            "detail": detail,
            "count": rec["จำนวน"],
            "codes": rec["รายการ"],
        })

    path = OUT_DIR / "audit_duplicates.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["type", "detail", "count", "codes"])
        w.writeheader()
        w.writerows(out_rows)
    return out_rows


def export_text_issues(wb):
    """Parse ตรวจภาษาไทย → audit_text_issues.csv"""
    records = read_sheet(wb, "ตรวจภาษาไทย")
    out_rows = []
    for rec in records:
        out_rows.append({
            "tor": rec["TOR"],
            "code": rec["รหัส"],
            "column": rec["คอลัมน์"],
            "text": rec["ข้อความ"],
            "issue_char": rec["อักขระที่น่าสงสัย"],
        })
    path = OUT_DIR / "audit_text_issues.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["tor", "code", "column", "text", "issue_char"])
        w.writeheader()
        w.writerows(out_rows)
    return out_rows


def main():
    wb = openpyxl.load_workbook(XLSX, data_only=True)

    missing = export_missing_codes(wb)
    duplicates = export_duplicates(wb)
    text_issues = export_text_issues(wb)

    # --- Summary ---
    print("=" * 50)
    print("AUDIT REPORT SUMMARY")
    print("=" * 50)

    # Missing codes per TOR
    tor_counts = {}
    for row in missing:
        tor_counts[row["tor"]] = tor_counts.get(row["tor"], 0) + 1
    print(f"\nMissing codes: {len(missing)} total")
    for tor in sorted(tor_counts):
        print(f"  {tor}: {tor_counts[tor]}")

    # Duplicates
    loc_dups = [d for d in duplicates if d["type"] == "location"]
    coord_dups = [d for d in duplicates if d["type"] == "coords"]
    print(f"\nDuplicate groups: {len(duplicates)} total")
    print(f"  Location duplicates: {len(loc_dups)}")
    print(f"  Coordinate duplicates: {len(coord_dups)}")

    # Text issues
    print(f"\nText issues: {len(text_issues)} total")
    for row in text_issues:
        print(f"  {row['tor']}/{row['code']}: char '{row['issue_char']}' in {row['column']}")

    print(f"\nOutput written to {OUT_DIR}/")
    print("  - audit_missing_codes.csv")
    print("  - audit_duplicates.csv")
    print("  - audit_text_issues.csv")


if __name__ == "__main__":
    main()
