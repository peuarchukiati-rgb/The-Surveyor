# The Surveyor — spec.md

## Project
สำรวจ + บำรุงรักษาศาลาที่พักผู้โดยสารรถประจำทาง กทม. (5 TOR: ES/TNS/SS/NS/MS)
ได้งาน e-bidding 19 พ.ค. 2569 — เข้า operational phase (Surveyor 2.0)

## Architecture

### Phase 1 (Survey — DONE)
- `index.html` — Multi-TOR dashboard (5 tabs, localStorage, Google Sheets as DB)
- `data/stops_*.csv` — Static shelter lists per TOR
- Google Forms → Google Sheets (Master Sheet per TOR) → CSV export → Dashboard
- Live: https://peuarchukiati-rgb.github.io/The-Surveyor/

### Phase 2 (Surveyor 2.0 — IN PROGRESS)
- `v2/data/all_stops.csv` — Consolidated 1,620 stops (all 5 TORs)
- `v2/data/traffy_cases.csv` — 40 Traffy Fondue cases imported
- `v2/data/traffy_rematched.csv` — Re-matched against updated stop data (17/40 auto-matched)
- `v2/data/traffy_dedup.csv` — 33 unique shelters (dedup: 5 tickets can = 1 case)
- `v2/data/audit_*.csv` — Data quality audit (missing codes, duplicates, text issues)
- `v2/scripts/geo_matcher.py` — Traffy lat/long → TOR stop matcher (haversine, configurable threshold)
- `v2/scripts/build_all_stops.py` — Consolidate per-TOR CSVs into all_stops.csv
- `v2/scripts/import_traffy.py` — xlsx → traffy_cases.csv + dedup
- `v2/scripts/update_master.py` — bkk_shelter_list.xlsx → updated per-TOR CSVs
- `v2/scripts/audit_codes.py` — Extract QA data from bkk_shelter_list
- `v2/SCHEMA.md` — Multi-team data schema (Cleaning/Traffy/Inspection/Fixing)

## TOR Registry

| TOR | Name | Stops | Owner | Status |
|-----|------|-------|-------|--------|
| ES | กรุงเทพตะวันออก | 606 | SO! | survey ~99% done |
| TNS | กรุงธนเหนือ-ใต้ | 272 | Look Ads | survey in progress |
| SS | กรุงเทพใต้ | 233 | Look Ads | survey in progress |
| NS | กรุงเทพเหนือ | 246 | Look Ads | survey in progress |
| MS | กรุงเทพกลาง | 263 | Look Ads | survey started |

Total: 1,620 stops

## Surveyor 2.0 — 4 Field Teams

| Team | Priority | Trigger | People | Output |
|------|----------|---------|--------|--------|
| Cleaning x2 | P2 | Schedule 4x/year | 2 trucks, driver+mech+3 cleaners each | before/after photos per shelter |
| Traffy Fondue (พี่สาธิต) | P1 ASAP | Citizen complaint tickets | 3-4 mechanics, night work | fix + close Traffy ticket |
| Inspection | P2 | TOR stop list | 5-10 mechanics | BOQ assessment (lights/seats/structure) |
| Fixing | P4 | Inspection results | mechanic + worker, night | before/after, target 90% |

All teams → forms → photos → Surveyor 2.0 dashboard → report กทม.

## Traffy Pipeline Status

- 40 cases imported (มนต์ curated from Traffy Fondue)
- Re-matched with geo_matcher: 17 auto-matched (≤200m), 23 need field verification
- Dedup: 33 unique shelters (MS120=4 tickets, NS083/MS203/SS029/SS001=2 each)
- Work types: ไฟ/แสงสว่าง, ที่นั่ง/ม้านั่ง, โครงสร้าง/ป้าย, หลังคา/กันแดดฝน

## Data Quality Audit

- 54 missing code gaps (ES: 26, MS: 20, NS: 5, SS: 3) — sequence gaps, not data loss
- 24 duplicate entries (12 location name, 12 coordinate)
- 3 text encoding issues (SS130, ES389, MS108)

## What's Done (as of 2026-06-04)

- [x] Phase 1 dashboard live (5 TORs, GitHub Pages)
- [x] Won e-bidding (19 พ.ค. 2569)
- [x] Surveyor 2.0 data foundation (v2/ folder, branch `surveyor-2.0`)
- [x] All stops consolidated: 1,620 across 5 TORs with lat/long
- [x] Geo-matcher built + tested (haversine, batch CSV, interactive)
- [x] Traffy cases imported + re-matched (17/40 auto, 6 new finds vs มนต์'s original)
- [x] Data audit complete (missing codes, duplicates, text issues)
- [x] Multi-team schema defined (SCHEMA.md)
- [x] Field verification list generated (v2/output/field_verification_list.html)
  - gen_field_list.py: reads traffy_rematched.csv, outputs printable A4 HTML
  - Section A: 17 auto-matched (go fix), Section B: 23 field verify (sorted by district)
  - Google Maps links, checkbox column, Sarabun font, print-optimized CSS
- [x] Traffy Tracker dashboard (v2/traffy_tracker.html)
  - build_traffy_tracker.py: reads CSVs → generates static HTML with embedded data
  - Summary bar, case list with expand detail, dedup view, filters (match/work_type/district)
  - Status tracking per case via localStorage (open/assigned/in_progress/fixed/reported)
  - Google Maps links for case + shelter locations, dark theme, Sarabun font, mobile-first
- [x] Traffy fix form spec (v2/forms/traffy_fix_form.md)
  - 10 fields: stop code, ticket ID, work type, before/after photos, description, status, notes, technician, date
  - Google Form prefill URL pattern documented
  - End-to-end flow: tracker → maps → fix → form → report
- [x] Dedup report for กทม. (v2/output/traffy_dedup_report.html + .csv)
  - 55 tickets → 33 unique shelters, formal print-ready report
  - Multi-ticket table, work type breakdown, executive summary
  - CSV handoff for data integration

## What's Next

### Step 1: Traffy Pipeline (P1 — unblocks พี่สาธิต)
- [x] Case ticket status tracking (open → assigned → fixed → reported)
- [x] Traffy fix form spec (ช่างถ่ายรูป + report) — ready to create Google Form
- [x] 23 unmatched cases → field verification list for พี่สาธิต
- [x] Case dedup reporting for กทม. (55 tickets → 33 shelters, formal HTML + CSV)

### Step 2: Inspection Form (P2 — รอ BOQ fields จากมนต์)
- [ ] Simplified BOQ form (≤2 pages: lights/seats/structure/roof/signage)
- [ ] Printout generator — Phase 1 data for mechanics to carry
- [ ] ~10% lat/long re-verification flow

### Step 3: Cleaning Form + Schedule (P2)
- [ ] Cleaning form (before/after photo, done flag)
- [ ] Schedule tracker (4 rounds/year, progress per round)

### Step 4: Fixing Flow (P4 — depends on Step 2)
- [ ] Fixing form (receive from Inspection, before/after)
- [ ] Completion tracking (target 90%)

### Step 5: Dashboard 2.0
- [ ] Unified multi-team view
- [ ] Daily performance tracking per team
- [ ] Report generator for กทม.

### Blocked on มนต์
- BOQ field list for Inspection form
- Updated lat/long data (~10% changed)
- Cleaning team schedule/route preference

## Key Decisions
- Drive folders must be public
- MS forms use `/d/{ID}` path (no published key)
- Code format: "ES 001" (with space) in all CSVs
- Geo-match threshold: 200m default, >200m = field verify
- 5 Traffy tickets at same stop = 1 case for reporting
- All teams use same form→photo→report pattern, different form fields
