#!/usr/bin/env python3
"""
gen_dummy_data.py
Generate dummy form response CSVs for Dashboard 2.0 testing.
Run once, then build_dashboard.py to see the dashboard.
Delete dummy_responses_*.csv when real data arrives.
"""

import csv
import os
import random
from datetime import datetime, timedelta

random.seed(42)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data")

DAMAGE_TYPES = [
    "หลอดไฟ (หลอดเสีย)",
    "Solar เสีย",
    "หลังคา",
    "เก้าอี้",
    "ระบบไฟ (อุปกรณ์เสีย)",
    "ทำสี/ปรับปรุง/ขัดสนิม",
    "ทำความสะอาด",
]

TEAMS = ["ทีม A", "ทีม B"]

FAIL_REASONS = [
    "ต้องใช้รถเครน",
    "อุปกรณ์ไม่พอ รอเบิกเพิ่ม",
    "พื้นที่เข้าถึงลำบาก",
    "รอวัสดุจาก supplier",
    "สภาพอากาศไม่เอื้ออำนวย",
]


def rand_ts(start_month, end_month, year=2026):
    start = datetime(year, start_month, 1)
    end = datetime(year, end_month, 28)
    delta = (end - start).days
    d = start + timedelta(days=random.randint(0, max(delta, 1)))
    h, m = random.randint(8, 20), random.randint(0, 59)
    return d.replace(hour=h, minute=m).strftime("%Y-%m-%d %H:%M:%S")


def load_stops():
    rows = []
    with open(os.path.join(DATA_DIR, "all_stops.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


def load_traffy():
    rows = []
    path = os.path.join(DATA_DIR, "traffy_rematched.csv")
    if not os.path.exists(path):
        return rows
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


def write_csv(filename, fieldnames, rows):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Wrote {len(rows)} rows → {filename}")


def gen_p1(traffy_cases):
    """P1 Traffy Fix: ~50% of matched cases."""
    matched = [c for c in traffy_cases if c.get("match_status") == "matched"]
    sample = random.sample(matched, min(len(matched), int(len(matched) * 0.5)))

    rows = []
    for c in sample:
        code = c.get("shelter_code", "").strip()
        if not code:
            continue
        n_damage = random.randint(1, 3)
        damage = ";".join(random.sample(DAMAGE_TYPES, min(n_damage, len(DAMAGE_TYPES))))
        status = "แก้ไขเรียบร้อย" if random.random() < 0.9 else "ไม่สามารถแก้ไขได้"
        reason = random.choice(FAIL_REASONS) if "ไม่สามารถ" in status else ""
        rows.append({
            "timestamp": rand_ts(5, 6),
            "code": code,
            "ticket_id": c.get("ticket_id", ""),
            "damage_type": damage,
            "status": status,
            "reason": reason,
        })
    write_csv("dummy_responses_p1.csv",
              ["timestamp", "code", "ticket_id", "damage_type", "status", "reason"], rows)
    return {r["code"] for r in rows}


def gen_p2(stops):
    """P2 Inspection: ~10% of all stops."""
    sample = random.sample(stops, int(len(stops) * 0.10))

    items_pool = [
        ("หลอดไฟ", 1, 10), ("เก้าอี้", 1, 20), ("พลังงา", 1, 10),
    ]
    flag_pool = ["ระบบไฟ", "Solar เสีย", "ทำสี/ปรับปรุง", "ทำความสะอาด"]

    rows = []
    for s in sample:
        code = s["code"].strip()
        if random.random() < 0.3:
            items = "ไม่เสีย"
        else:
            parts = []
            for name, lo, hi in random.sample(items_pool, random.randint(1, 3)):
                parts.append(f"{name}:{random.randint(lo, hi)}")
            for flag in random.sample(flag_pool, random.randint(0, 2)):
                parts.append(flag)
            items = ";".join(parts)
        rows.append({
            "timestamp": rand_ts(4, 6),
            "code": code,
            "damage_items": items,
            "notes": "",
        })
    write_csv("dummy_responses_p2.csv",
              ["timestamp", "code", "damage_items", "notes"], rows)
    return rows


def gen_p3(p2_rows):
    """P3 Maintenance: ~25% of P2 damaged stops."""
    damaged = [r for r in p2_rows if r["damage_items"] != "ไม่เสีย"]
    sample = random.sample(damaged, min(len(damaged), int(len(damaged) * 0.25)))

    rows = []
    for r in sample:
        status = "แก้ไขเรียบร้อย" if random.random() < 0.85 else "ไม่สามารถแก้ไขได้"
        reason = random.choice(FAIL_REASONS) if "ไม่สามารถ" in status else ""
        rows.append({
            "timestamp": rand_ts(5, 6),
            "code": r["code"],
            "team": random.choice(TEAMS),
            "damage_type": r["damage_items"],
            "status": status,
            "reason": reason,
        })
    write_csv("dummy_responses_p3.csv",
              ["timestamp", "code", "team", "damage_type", "status", "reason"], rows)
    return {r["code"] for r in rows}


def gen_p4(stops):
    """P4 Cleaning: ~30% R1, ~15% R2, ~5% R3, ~1% R4."""
    rates = [(1, 0.30, 1, 2), (2, 0.15, 3, 4), (3, 0.05, 5, 5), (4, 0.01, 6, 6)]

    rows = []
    for rnd, rate, m1, m2 in rates:
        sample = random.sample(stops, int(len(stops) * rate))
        for s in sample:
            code = s["code"].strip()
            status = "แก้ไขเรียบร้อย" if random.random() < 0.95 else "แก้ไขไม่ได้"
            reason = random.choice(FAIL_REASONS) if "ไม่ได้" in status else ""
            rows.append({
                "timestamp": rand_ts(m1, m2),
                "code": code,
                "round": rnd,
                "team": random.choice(TEAMS),
                "status": status,
                "reason": reason,
            })
    write_csv("dummy_responses_p4.csv",
              ["timestamp", "code", "round", "team", "status", "reason"], rows)


def main():
    print("Generating dummy data...")
    stops = load_stops()
    traffy = load_traffy()
    print(f"  Loaded {len(stops)} stops, {len(traffy)} traffy cases")

    gen_p1(traffy)
    p2_rows = gen_p2(stops)
    gen_p3(p2_rows)
    gen_p4(stops)
    print("Done! Run build_dashboard.py next.")


if __name__ == "__main__":
    main()
