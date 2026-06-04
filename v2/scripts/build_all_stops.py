#!/usr/bin/env python3
"""
Consolidate all TOR CSV files into one all_stops.csv
Used as the master reference for all Surveyor 2.0 operations.
"""

import csv
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT = DATA_DIR / "all_stops.csv"

FIELDS = ["tor", "code", "district", "road", "location", "type", "lat", "long", "folder_url"]


def main():
    all_rows = []
    for csv_file in sorted(DATA_DIR.glob("stops_*.csv")):
        if csv_file.name == "all_stops.csv":
            continue
        tor_id = csv_file.stem.replace("stops_", "")
        with open(csv_file, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                all_rows.append({
                    "tor": tor_id,
                    "code": row.get("code", "").strip(),
                    "district": row.get("district", "").strip(),
                    "road": row.get("road", "").strip(),
                    "location": row.get("location", "").strip(),
                    "type": row.get("type", "").strip(),
                    "lat": row.get("lat", "").strip(),
                    "long": row.get("long", "").strip(),
                    "folder_url": row.get("folder_url", "").strip(),
                })

    with open(OUTPUT, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(all_rows)

    # Stats
    tors = {}
    for r in all_rows:
        tors[r["tor"]] = tors.get(r["tor"], 0) + 1
    print(f"Wrote {len(all_rows)} stops to {OUTPUT}")
    for tor, count in sorted(tors.items()):
        print(f"  {tor}: {count}")


if __name__ == "__main__":
    main()
