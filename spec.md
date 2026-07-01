# The Surveyor — spec.md

## Project
สำรวจ + บำรุงรักษาศาลาที่พักผู้โดยสารรถประจำทาง กทม. (4 TOR: ES/SS/NS/MS)
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
- `v2/SCHEMA.md` — Multi-team data schema (P1-P4)
- `v2/forms/traffy_fix_form.md` — P1 Traffy fix form spec
- `v2/forms/inspection_form.md` — P2 Inspection BOQ form spec
- `v2/forms/cleaning_form.md` — P4 Cleaning form spec

## TOR Registry

| TOR | Name | Stops | Owner | Status |
|-----|------|-------|-------|--------|
| ES | กรุงเทพตะวันออก | 606 | SO! | survey ~99% done |
| SS | กรุงเทพใต้ | 233 | Look Ads | survey in progress |
| NS | กรุงเทพเหนือ | 246 | Look Ads | survey in progress |
| MS | กรุงเทพกลาง | 263 | Look Ads | survey started |

Total: 1,348 stops (verified by มนต์)

> TNS (กรุงธนเหนือ-ใต้, 272 หลัง) — ไม่อยู่ใน verified list จากมนต์

## Surveyor 2.0 — 4 Field Teams

| Team | Priority | Trigger | People | Output |
|------|----------|---------|--------|--------|
| Traffy (พี่สาธิต) | P1 ASAP | Traffy Fondue ticket | 3-4 ช่าง, night | fix report + 3 photos + case closure |
| Inspection (Rider) | P2 | TOR stop list | 5 Riders + พี่สอง train | BOQ assessment (checkbox+count) |
| Maintenance | P3 | Inspection + Traffy data | ช่าง + แรงงาน, night | fix + before/after + completion |
| Cleaning x2 | P4 | Schedule 4x/year | 2 คัน (driver+mech+3) | before/after photos per shelter |

All teams → Drive folder photos → Google Form → Sheets → Dashboard → report กทม.

> P1 วิ่งอิสระ ทำก่อนทุกทีม — ทำเสร็จแจ้งทีมอื่นให้ skip
> P4 วิ่งขนานได้เลย ไม่ต้องรอใคร

## Traffy Pipeline Status

- 40 cases imported (มนต์ curated from Traffy Fondue)
- Re-matched with geo_matcher: 17 auto-matched (≤200m), 23 need field verification
- Dedup: 33 unique shelters (MS120=4 tickets, NS083/MS203/SS029/SS001=2 each)
- Work types: ไฟ/แสงสว่าง, ที่นั่ง/ม้านั่ง, โครงสร้าง/ป้าย, หลังคา/กันแดดฝน

## Data Quality Audit

- 54 missing code gaps (ES: 26, MS: 20, NS: 5, SS: 3) — sequence gaps, not data loss
- 24 duplicate entries (12 location name, 12 coordinate)
- 3 text encoding issues (SS130, ES389, MS108)

## What's Done (as of 2026-06-08)

- [x] Phase 1 dashboard live (5 TORs, GitHub Pages)
- [x] Won e-bidding (19 พ.ค. 2569)
- [x] Surveyor 2.0 data foundation (v2/ folder, branch `surveyor-2.0`)
- [x] All stops consolidated: 1,620 across 5 TORs with lat/long
- [x] Geo-matcher built + tested (haversine, batch CSV, interactive)
- [x] Traffy cases imported + re-matched (17/40 auto, 6 new finds vs มนต์'s original)
- [x] Data audit complete (missing codes, duplicates, text issues)
- [x] Multi-team schema defined (SCHEMA.md)
- [x] Field verification list generated (v2/output/field_verification_list.html)
- [x] Traffy Tracker dashboard (v2/traffy_tracker.html)
- [x] Dedup report for กทม. (v2/output/traffy_dedup_report.html + .csv)
- [x] P1 Traffy Fix form spec — updated per 8 มิ.ย. meeting
  - Checkboxes (multi-select) อาการเสีย + "ไม่เสีย" option
  - 3 photos: Before/Ongoing/After → Drive folder (ไม่ใช่ form upload)
  - Status: แก้ไขเรียบร้อย / ไม่สามารถแก้ไขได้
  - Prefill from Traffy data, timestamp auto
- [x] P2 Inspection form spec — from whiteboard 8 มิ.ย.
  - Checkbox + count: หลอดไฟ(1-10), เก้าอี้(1-20), พลังงา(1-10), ระบบไฟ, Solar, etc.
  - Night mode only, Rider x5 trained กับพี่สอง
- [x] P4 Cleaning form spec — simplest form
  - รหัสศาลา + status + 2 photos (Before/After)
  - ทำได้เลยทุกป้าย ไม่ต้องรอทีมอื่น

## What's Next

### Step 1: Traffy Pipeline (P1) ✅ DONE
- [x] Case ticket status tracking
- [x] Traffy fix form spec (updated 8 มิ.ย.)
- [x] 23 unmatched cases → field verification list
- [x] Case dedup reporting for กทม.

### Step 2: Create Google Forms จริง ✅ DONE (9 มิ.ย.)
มนต์สร้างผ่าน Apps Script + ปรับแก้เพิ่มเอง

| Form | Edit URL | Fill URL |
|------|----------|----------|
| P1 Traffy Fix | [edit](https://docs.google.com/forms/d/1obh3hP9EcmmXv3-TozRSmS19jHlqrgLxEdofl1xqatQ/edit) | [fill](https://docs.google.com/forms/d/e/1FAIpQLSfpfTkED3m-66HalnmnKZSSxpjvY3c97Y4wmSJp4Dv4a9vJ1A/viewform) |
| P2 Inspection | [edit](https://docs.google.com/forms/d/1_wS2-qsw1EqmmfzDYYDz9Ume3r1t3i1im3Xi--_PgSY/edit) | [fill](https://docs.google.com/forms/d/e/1FAIpQLSeaDJtyyu7Ba4ZT7P34P8Qkrtau3ddVr5F1JP2eCplp7NdS1g/viewform) |
| P3 Maintenance | [edit](https://docs.google.com/forms/d/1DJH08U0WueEnq41RqMYd5Roaoita1ltyzPRoht53nkU/edit) | [fill](https://docs.google.com/forms/d/e/1FAIpQLSd1i8sw2-ZXvjGO3OeEmHgTA_bTD8YSpd0UlnN1aunqXY2Beg/viewform) |
| P4 Cleaning | [edit](https://docs.google.com/forms/d/1GJvyg7iohIojcVOy_KIaofu0kUEQQA0uJ3QWTLDPxi0/edit) | [fill](https://docs.google.com/forms/d/e/1FAIpQLSeLmkl5WLc57j8nwGW4iV84seIDDA-q-UCCYvknm8kVrpAAEQ/viewform) |

มนต์ปรับเพิ่มจาก script:
- P1: ปรับคำอธิบาย options ให้ชัดขึ้น
- P2: เพิ่มจาก 10 → 18 fields (ไล่ logic ไฟฟ้าจริง, แยก component, ประเภทม้านั่ง) — รอ confirm กับวิศวะไฟฟ้า
- P4: เพิ่ม field ชื่อ-ทีมผู้ปฏิบัติงาน

Prefill entry IDs (P1): stop_code=62705490, ticket_id=711616789, damage_type=1825707891

### Step 3: Import verified data จากมนต์ ✅ DONE (9 มิ.ย.)
- [x] Import `bkk_shelter_list_verified.xlsx` → data ตรงกับที่มีอยู่แล้ว (ไม่มี diff)
- [x] Tracker rebuilt with P1 form prefill links

### Step 4: P3 Maintenance Form ✅ DONE (9 มิ.ย.)
- [x] มนต์สร้าง form เอง (= P1 + ชื่อ-ทีมผู้ปฏิบัติงาน)
- [x] Fields: รหัสป้าย, ชื่อ-ทีม, อาการเสีย (checkboxes), สถานะ, เหตุผล

### Step 5: Dashboard 2.0 (IN PROGRESS)
- [x] Unified multi-team view — `v2/output/dashboard.html` (dummy data, live on GitHub Pages)
- [x] Restyle → light theme เหมือน v1 (#f5f7fa, การ์ดขาว, accent #1a73e8) — 23 มิ.ย.
- [x] ปุ่ม 3 ปุ่มต่อ P (📍 Map / 📁 Upload / 📋 Form) ใน section ของแต่ละ P — 23 มิ.ย.
  - Map ใช้ lat/long จาก DATA, refactor template ซ้ำเป็น `cardHTML()`/`pSection()`
  - Script: `v2/scripts/restyle_dashboard.py` (regex แก้ style+formUrl+render, ไม่แตะ DATA)
- [ ] ต่อ Google Sheets live CSV (รอมนต์ publish 4 sheets → ส่ง CSV URLs กลับ)
- [ ] Daily performance tracking per team
- [ ] Report generator for กทม.
- [ ] ลบ dummy data เมื่อมี data จริง

### Step 6: P2+P4 Response Sheets (23 มิ.ย. — handoff `HANDOFF_PEAK` + `HANDOFF_PEAK2`)
- [ ] Peak กดสร้าง Response Sheet เอง P2+P4 — **BLOCKED**: เปิด form edit URL ขึ้น "Request edit access" → Peak ไม่มีสิทธิ์ Editor บนฟอร์มมนต์
  - ฟอร์มสร้างใต้ account มนต์ (Apps Script) → ทุก artifact ผูก ownership มนต์
  - แก้: มนต์ add `p.euarchukiati@gmail.com` เป็น Editor ทั้ง 4 ฟอร์ม → Peak สร้าง sheet เอง (sheet = Peak owns)
  - โอน ownership ฟอร์มข้าม account ไม่ได้ (คนละ Workspace org / gmail ส่วนตัว) → ใช้ Editor พอ
- มนต์ยืนยัน P2+P4 forms แก้ข้อมูลเสร็จ → ทีมงานใช้พุธ 24 มิ.ย.

### Step 7: Master Drive Folder (HANDOFF_PEAK2 — ใหม่)
- [ ] Peak สร้าง `The Surveyor v2 - Photos/` + 4 subfolder (ES/NS/SS/MS) ใน Drive ตัวเอง → share Editor ให้มนต์
  - ไม่ติด ownership (Peak สร้างเอง) → ทำได้ทันที
  - มนต์จะเข้าไป gen ฟอร์ม audit + อัลบั้มรูป ภายใต้ ownership Peak

### Step 8: Map integration (23 มิ.ย. — DONE build-ahead)
มนต์ส่งแอปแผนที่ Leaflet (`mapoverview_version2.0.rar`) — field navigation + route(OSRM) + share/QR + zoning
- [x] รวมเข้า repo `v2/map/` (design1_classic.html + data.js + share/status/traffy.js)
- [x] `v2/scripts/build_map_data.py` — regenerate `v2/map/data.js` จาก all_stops.csv (1,620 จุด, single source)
  - schema มนต์: `g,code(no-space),dist,road,place,type,lat,lng`
- [x] ปุ่ม "📋 เปิดฟอร์ม" (P2) ใน popup ทุกหมุด
- [x] cross-link Map ↔ Dashboard 2 ทาง
- [x] `loadStatus(csvUrl)` stub (OFF) — ⚠️ sub-agent เขียนสมมติ column `code`+`status` (single) แต่มนต์ทำ P_STATUS แบบ **แยกราย P** → ต้องปรับ map ให้อ่าน column P<n> ตาม filter ที่เลือก ตอน CSV จริงมา
- [x] live-data layer ใน dashboard — อัปเดตตรง schema P_STATUS แล้ว + tested (node unit test ผ่าน)

### P_STATUS — single source of truth (มนต์ยืนยัน 23 มิ.ย.)
ชีตเดียว: `code, zone, P1, P2, P3, P4` — แต่ละช่อง `pending / progress / done` (dropdown)
- dashboard: `CONFIG.statusCsv` + `mergeStatus()` map P1-P4 → DATA, เพิ่ม pill `progress` (สีฟ้า 🔧)
- `codeOf()` จับ code column ได้ทั้ง `รหัสศาลา / Stop Code` (form sheets) และ `code` (P_STATUS) — ค่า ES001
- header form unify เป็น `รหัสศาลา / Stop Code` ทุกฟอร์มแล้ว
- flip live = แปะ `statusCsv` URL + `LIVE: true` (per-form `csv` p1-p4 เป็น optional raw)

### Waiting on มนต์ (รวม)
- P1 + P3 forms + เปิด Editor ให้ Peak (ส่งก่อนพุธ 24)
- publish `P_STATUS` เป็น CSV URL → flip dashboard LIVE + ปรับ map loadStatus
- mapping `P<n>_<code>` → Drive folder URL (เริ่ม P4 ES) → ปุ่ม Upload
- มนต์ขอ **รอ push** map+live-layer (เช็คอีกรอบก่อนเคาะ)

### Peak — DONE (23 มิ.ย.)
- [x] Response Sheet P2+P4 สร้าง+publish CSV แล้ว
  - P2 raw: `.../2PACX-1vT5fskXBCJnoIY7GDSSFaaDhTwIIs1aZP4PZfjvW8DLvwKjK47FdXC12ToJOVvOetsI6sgBnZYyuBeF/pub?gid=1943423996&output=csv` (70 col BOQ, header code = `รหัสศาลา / Stop Code`, มี response ES422)
  - P4 raw: `.../2PACX-1vS0JfYidiVTOZL5XjWsamjYkXDBdAekcDVbkBIpiOpoLlrAULrQe2pEIw7s92UGHCzaSkgTh6rH5n3O/pub?gid=271580481&output=csv` (มี col `สถานะ / Cleaning Status`, ยังว่าง)
  - raw sheets = ปลายทางฟอร์ม; dashboard อ่านสถานะจาก P_STATUS ไม่ใช่ raw
- [x] Master Folder `The Surveyor v2 - Photos` (id `1TezoCbHGOCFi1Kor53QA6Gb8tzN6Opai`) + 4 โซน ES/NS/SS/MS
  - permission: **anyone with link = Editor** (Peak เลือก — frictionless field upload, รูปกู้ได้ผ่าน Drive trash). blast radius = ทั้งต้นไม้; ยังไม่ add มนต์ named (เข้าได้ผ่าน link)
- codeOf() เทสต์กับ header จริงแล้ว — จับ `รหัสศาลา / Stop Code` ได้ ✓

### Waiting
- มนต์: publish 4 Google Sheets เป็น CSV URLs (handoff ส่งแล้ว `HANDOFF_MON_SHEETS.md`)
- มนต์: P1 + P3 forms ยังแก้ข้อมูลอยู่ (P3 อิงโครงสร้าง P1, code พร้อมใน `create_forms.gs`)
- มนต์: ส่ง mapping `P<n>_<code>` → Drive folder URL (เริ่มโซน ES) → เอามาใส่ปุ่ม Upload (ตอนนี้ใช้ s.folder ศาลาเดิมไปก่อน)
- P2 Inspection form: รอ confirm กับวิศวะไฟฟ้า
- Cleaning team schedule/route preference
- กุญแจตู้ไฟ: รอเซ็นสัญญากับ กทม.

## Session Log

### 1 ก.ค. 2569 — go LIVE + redesign (Peak + claude)
- **Live subscription ON**: `dashboard.html` LIVE:true, เสียบ CSV มนต์ (P_STATUS + P2_MAP + P4_MAP). match รหัส 1,348/1,348. push แล้ว — "นิ่งสนิท" ก่อนหน้าเพราะยังไม่ commit (Pages serve dummy เก่า)
- **มนต์ verify รอบ 1** (`FEEDBACK_PEAK.md`) → แก้ครบ 5 ข้อ:
  - ตัด TNS 272 ออกทั้งระบบ (dashboard init splice + map data.js + design1_classic) → 1,348
  - ทุก P counter ฐาน /1348 (renderSummary), เลขนับจาก data จริง (MS263/SS233)
  - redesign เป็น **drill-down 4 ชั้น**: overall→ทีม P→โซน→เขต→ศาลา + back/breadcrumb
  - สี v1: P1 แดง/P2 เหลือง/P3 ฟ้า/P4 เขียว + zone palette
- data layer (DATA/CONFIG/mergeStatus/loadLive) ไม่แตะ. commits: `b11e0a2` (TNS+base), `79cf0ff` (redesign)
- handoff verify รอบ 2 → `HANDOFF_MON_VERIFY.md`
- **ค้าง**: P1+P3 form entry ID + folder CSV (ปุ่มอัพรูป P1/P3 เทา, prefill P2-P4 รอ entry). dead CSS เก่ายังค้างในไฟล์ (harmless)

## Meeting Notes

### 8 มิ.ย. 2569 (มนต์ + พี่บอย + Peak)
- Whiteboard spec ครบ 4 ทีม (P1-P4) — photos saved: p1.jpg, p2p3.jpg, p4.jpg
- P1 Traffy: checkbox อาการเสีย + "ไม่เสีย" + 3 photos (Before/Ongoing/After) + Drive folder
- P2 Inspection: checkbox+count BOQ, Night only, Rider x5, กุญแจตู้ไฟรอสัญญา
- P3 Maintenance: form เหมือน P1, ใช้ data P1+P2 combined
- P4 Cleaning: form ง่ายสุด (code + status + 2 photos)
- Key decisions: P1 วิ่งอิสระ, P4 ขนานได้, photos ใช้ Drive folder ไม่ใช่ form upload
- มนต์ส่ง `bkk_shelter_list_verified.xlsx` (4 TOR, 1,348 หลัง, lat/long verified)

## Key Decisions
- Drive folders must be public
- Photos → Drive folder (ไม่ใช่ Google Form file upload)
- Code format: "ES001" (no space) in forms, "ES 001" (with space) in old CSVs
- Geo-match threshold: 200m default, >200m = field verify
- 5 Traffy tickets at same stop = 1 case for reporting
- All teams use same form→photo→report pattern, different form fields
- Timestamp auto — ไม่ต้องกรอกวันที่
- ไม่เก็บชื่อช่างในฟอร์ม
