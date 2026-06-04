#!/usr/bin/env python3
"""
Traffy Fondue → TOR Stop Geo-Matcher

Matches Traffy complaint lat/long to nearest TOR bus stop.
Usage:
    python3 geo_matcher.py                          # interactive mode
    python3 geo_matcher.py --lat 13.81 --long 100.56
    python3 geo_matcher.py --traffy traffy_cases.csv --output matched.csv
"""

import csv
import math
import os
import sys
import argparse
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
RADIUS_THRESHOLD_M = 200  # max distance to consider a match


def haversine_m(lat1, lon1, lat2, lon2):
    """Distance in meters between two lat/long points."""
    R = 6_371_000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def load_all_stops():
    """Load all TOR stop CSVs into a single list."""
    stops = []
    for csv_file in sorted(DATA_DIR.glob("stops_*.csv")):
        tor_id = csv_file.stem.replace("stops_", "")  # ES, NS, SS, TNS, MS
        with open(csv_file, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    lat = float(row["lat"])
                    lng = float(row["long"])
                except (ValueError, KeyError):
                    continue
                stops.append({
                    "tor": tor_id,
                    "code": row.get("code", "").strip(),
                    "district": row.get("district", "").strip(),
                    "road": row.get("road", "").strip(),
                    "location": row.get("location", "").strip(),
                    "type": row.get("type", "").strip(),
                    "lat": lat,
                    "long": lng,
                })
    return stops


def find_nearest(lat, lng, stops, threshold_m=RADIUS_THRESHOLD_M):
    """Find nearest stop within threshold. Returns (stop, distance_m) or (None, None)."""
    best_stop = None
    best_dist = float("inf")
    for s in stops:
        d = haversine_m(lat, lng, s["lat"], s["long"])
        if d < best_dist:
            best_dist = d
            best_stop = s
    if best_dist <= threshold_m:
        return best_stop, round(best_dist, 1)
    return None, best_dist


def find_nearby(lat, lng, stops, threshold_m=RADIUS_THRESHOLD_M):
    """Find ALL stops within threshold, sorted by distance."""
    results = []
    for s in stops:
        d = haversine_m(lat, lng, s["lat"], s["long"])
        if d <= threshold_m:
            results.append((s, round(d, 1)))
    return sorted(results, key=lambda x: x[1])


def match_traffy_csv(traffy_path, output_path, stops):
    """Match a Traffy CSV (needs lat, long columns) against TOR stops."""
    matched = 0
    unmatched = 0
    results = []

    with open(traffy_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        traffy_fields = reader.fieldnames or []

        for row in reader:
            try:
                lat = float(row.get("lat") or row.get("latitude") or row.get("case_lat") or 0)
                lng = float(row.get("long") or row.get("longitude") or row.get("lng") or row.get("case_long") or 0)
            except ValueError:
                lat, lng = 0, 0

            if lat == 0 or lng == 0:
                unmatched += 1
                results.append({**row, "match_code": "", "match_tor": "",
                                "match_dist_m": "", "match_status": "no_coords"})
                continue

            stop, dist = find_nearest(lat, lng, stops)
            if stop:
                matched += 1
                results.append({
                    **row,
                    "match_code": stop["code"],
                    "match_tor": stop["tor"],
                    "match_district": stop["district"],
                    "match_dist_m": dist,
                    "match_status": "matched",
                })
            else:
                unmatched += 1
                results.append({
                    **row,
                    "match_code": "",
                    "match_tor": "",
                    "match_district": "",
                    "match_dist_m": round(dist, 1) if dist != float("inf") else "",
                    "match_status": f"no_match_nearest_{round(dist, 1)}m",
                })

    # Write output
    if results:
        out_fields = list(results[0].keys())
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=out_fields)
            writer.writeheader()
            writer.writerows(results)

    return matched, unmatched


def interactive_mode(stops):
    """Interactive single-point lookup."""
    print(f"\nLoaded {len(stops)} stops across all TORs")
    print(f"Threshold: {RADIUS_THRESHOLD_M}m")
    print("Enter 'q' to quit\n")

    while True:
        raw = input("lat,long > ").strip()
        if raw.lower() in ("q", "quit", "exit"):
            break
        try:
            parts = raw.replace(" ", "").split(",")
            lat, lng = float(parts[0]), float(parts[1])
        except (ValueError, IndexError):
            print("  Format: 13.812,100.565")
            continue

        nearby = find_nearby(lat, lng, stops)
        if nearby:
            print(f"  Found {len(nearby)} stop(s) within {RADIUS_THRESHOLD_M}m:")
            for s, d in nearby[:5]:
                print(f"    {s['code']} ({s['tor']}) — {d}m — {s['district']}, {s['location']}")
        else:
            stop, dist = find_nearest(lat, lng, stops, threshold_m=999999)
            if stop:
                print(f"  No match within {RADIUS_THRESHOLD_M}m. Nearest: {stop['code']} at {dist}m")
            else:
                print("  No stops found")
        print()


def main():
    parser = argparse.ArgumentParser(description="Match Traffy complaints to TOR bus stops")
    parser.add_argument("--lat", type=float, help="Single point latitude")
    parser.add_argument("--long", type=float, help="Single point longitude")
    parser.add_argument("--traffy", type=str, help="Traffy cases CSV path")
    parser.add_argument("--output", type=str, default="matched_cases.csv", help="Output CSV path")
    parser.add_argument("--threshold", type=int, default=RADIUS_THRESHOLD_M, help="Match threshold in meters")
    parser.add_argument("--stats", action="store_true", help="Print stop stats and exit")
    args = parser.parse_args()

    stops = load_all_stops()

    threshold = args.threshold

    if args.stats:
        tors = {}
        for s in stops:
            tors.setdefault(s["tor"], 0)
            tors[s["tor"]] += 1
        print(f"Total stops: {len(stops)}")
        for tor, count in sorted(tors.items()):
            print(f"  {tor}: {count}")
        return

    if args.lat and args.long:
        nearby = find_nearby(args.lat, args.long, stops, threshold_m=threshold)
        if nearby:
            for s, d in nearby[:5]:
                print(f"{s['code']} ({s['tor']}) — {d}m — {s['district']}, {s['location']}")
        else:
            stop, dist = find_nearest(args.lat, args.long, stops, threshold_m=999999)
            print(f"No match within {threshold}m. Nearest: {stop['code']} at {dist}m")
        return

    if args.traffy:
        matched, unmatched = match_traffy_csv(args.traffy, args.output, stops)
        print(f"Matched: {matched}, Unmatched: {unmatched}")
        print(f"Output: {args.output}")
        return

    interactive_mode(stops)


if __name__ == "__main__":
    main()
