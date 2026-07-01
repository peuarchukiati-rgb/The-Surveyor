#!/usr/bin/env python3
"""
Build v2/map/data.js from the single source of truth v2/data/all_stops.csv
so the field-navigation map stays in sync with the monitoring dashboard.

Emits มนต์'s map schema (keys: g, code, dist, road, place, type, lat, lng).
- g    <- tor   (group key, drives marker color + layer)
- code <- code  WITH the space stripped: "ES 001" -> "ES001"
- dist <- district
- road <- road
- place<- location
- type <- type
- lat  <- lat   (float)
- lng  <- long  (float)

UTF-8 + ensure_ascii=False so Thai renders correctly (not mojibake).
"""

import csv
import json
from pathlib import Path

DATA_CSV = Path(__file__).parent.parent / "data" / "all_stops.csv"
OUTPUT = Path(__file__).parent.parent / "map" / "data.js"


def main():
    pts = []
    skipped = 0
    with open(DATA_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lat = row.get("lat", "").strip()
            lng = row.get("long", "").strip()
            if not lat or not lng:
                skipped += 1
                continue
            pts.append({
                "g": row.get("tor", "").strip(),
                "code": row.get("code", "").strip().replace(" ", ""),  # "ES 001" -> "ES001"
                "dist": row.get("district", "").strip(),
                "road": row.get("road", "").strip(),
                "place": row.get("location", "").strip(),
                "type": row.get("type", "").strip(),
                "lat": float(lat),
                "lng": float(lng),
            })

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("var DATA = ")
        json.dump(pts, f, ensure_ascii=False)
        f.write(";")

    # Stats
    groups = {}
    for p in pts:
        groups[p["g"]] = groups.get(p["g"], 0) + 1
    print(f"Wrote {len(pts)} stops to {OUTPUT}  (skipped {skipped} with no lat/lng)")
    for g, n in sorted(groups.items()):
        print(f"  {g}: {n}")


if __name__ == "__main__":
    main()
