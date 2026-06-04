# Surveyor 2.0 — Multi-Team Data Schema

## Teams

| Team | Priority | Trigger | Output |
|------|----------|---------|--------|
| Cleaning | P2 | Schedule (4x/year) | before/after photos + done flag |
| Traffy | P1 ASAP | Traffy Fondue ticket | fix report + case closure |
| Inspection | P2 | TOR stop list | BOQ assessment per stop |
| Fixing | P4 | Inspection results | before/after + completion |

## Stop Master (all_stops.csv)

| Field | Type | Example |
|-------|------|---------|
| tor | string | ES, TNS, SS, NS, MS |
| code | string | ES 001, NS 245 |
| district | string | จตุจักร |
| road | string | ลาดพร้าว |
| location | string | หน้าโรงแรมลาดพร้าว |
| type | string | Type A, B, B2, JC, S |
| lat | float | 13.811233 |
| long | float | 100.564611 |
| folder_url | string | Google Drive URL |

## Traffy Case (traffy_cases.csv — input from มนต์)

Expected columns (flexible matching):
| Field | Type | Notes |
|-------|------|-------|
| ticket_id | string | Traffy case ID |
| lat/latitude | float | Complaint location |
| long/longitude/lng | float | Complaint location |
| description | string | Complaint text |
| status | string | open/in_progress/resolved |
| reported_date | date | When citizen reported |

After geo-matching → adds: match_code, match_tor, match_district, match_dist_m, match_status

## Case Ticket Dedup

Multiple Traffy tickets can map to 1 physical stop:
- Group by match_code
- 5 tickets @ ES 001 = 1 case
- Report to กทม. per case, not per ticket

## Cleaning Report

| Field | Type | Notes |
|-------|------|-------|
| code | string | Stop code |
| round | int | 1-4 (which quarter) |
| date | date | Cleaning date |
| team | string | Team A or B |
| before_photo | url | Drive photo link |
| after_photo | url | Drive photo link |
| status | enum | done / skipped / inaccessible |
| notes | string | Optional |

## Inspection Report (BOQ)

| Field | Type | Notes |
|-------|------|-------|
| code | string | Stop code |
| date | date | Inspection date |
| inspector | string | Name |
| lights_total | int | Total light fixtures |
| lights_broken | int | Need replacement |
| seats_total | int | Total seats |
| seats_broken | int | Need replacement |
| structure_status | enum | good / damaged / critical |
| roof_status | enum | good / damaged / missing |
| signage_status | enum | good / damaged / missing |
| photo_url | url | Drive link |
| notes | string | Free text |
| rider_data_match | bool | Does Phase 1 data match reality? |

## Fixing Report

| Field | Type | Notes |
|-------|------|-------|
| code | string | Stop code |
| source | enum | inspection / traffy |
| source_id | string | Inspection ID or Traffy ticket |
| date | date | Fix date |
| team | string | Team name |
| before_photo | url | |
| after_photo | url | |
| items_fixed | string | What was fixed |
| status | enum | fixed / partial / deferred |
| notes | string | |
