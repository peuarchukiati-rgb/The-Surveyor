# The Surveyor — spec.md

## Project
สำรวจ + บำรุงรักษาศาลาที่พักผู้โดยสารรถประจำทาง กทม. (5 TOR: ES/TNS/SS/NS/MS)

## Architecture
- `index.html` — Multi-TOR dashboard (5 tabs, localStorage persistence, Google Sheets as DB)
- `data/stops_*.csv` — Static shelter lists per TOR
- `published_urls.json` — Google Forms prefill URLs per TOR
- Google Forms → Google Sheets (Master Sheet per TOR) → CSV export → Dashboard

## TOR Registry

| TOR | Name | Stops | Owner | Sheet ID |
|-----|------|-------|-------|----------|
| ES | กรุงเทพตะวันออก | 606 | SO! | (legacy pub URLs) |
| TNS | กรุงธนเหนือ-ใต้ | 272 | Look Ads | 1JiUp6HxBkO5P75txGmiFbtxb0SB3wkc57UHpnL1JfdA |
| SS | กรุงเทพใต้ | 233 | Look Ads | 1YJaVIX9gJDXkRcoVrGwZGQfs3nlxKSmmrIJv6kTTlRk |
| NS | กรุงเทพเหนือ | 246 | Look Ads | 1QuiJkP9kvYvRGzSoOzXd4EJOeQEChZ4fzJCITcj9_RU |
| MS | กรุงเทพกลาง | 259 | Look Ads | 1m3BtEkaFOaqqXgFTgQbKx-XiOlt6qgigJVLLZb5QGN4 (stops) / 1RNppV8F5we57NtOj5qtVOVVHzZzX2uMNpa6sByPHnGE (responses) |

## Form → Sheet Pipeline

### TNS/SS/NS (fixed 2026-05-16)
- Forms linked to Master Sheets via Google Forms UI
- Response tab gids: TNS Day=116756779/Night=331680235, SS Day=1603041302/Night=386227147, NS Day=388228796/Night=225515044

### MS (fixed 2026-05-20)
- Form URLs ใช้ `/d/{ID}` ไม่ใช่ `/d/e/{ID}` (MS ไม่มี published key แบบ 1FAIpQL)
- folder_url ถูก overwrite หายตอน provision → restored ด้วย `restore_ms_folders.py` (scan Drive → re-populate Sheet)
- 236/259 stops matched, 23 stops (MS 260-282) ยังไม่มี folder

### Known limitations
- TNS/SS/NS/MS ใช้ `/export?format=csv` (ต้อง sheet เป็น public)
- ES ใช้ `/pub?...output=csv` (Published to Web, stable กว่า)
- Drive folder ต้องเป็น public ไม่งั้น Master Sheet + Dashboard พัง

## Current State (2026-05-20)

### Dashboard — DONE
- 5-TOR support (ES/TNS/SS/NS/MS)
- Per-TOR aggregate stats, district grouping
- Status: todo/day-only/night-only/needs-photo/done
- Form → Sheet pipeline ใช้งานได้ทุก TOR

### Field Survey — IN PROGRESS
- ES: ~99% done
- TNS: กำลังกรอก
- SS: กำลังกรอก
- NS: กำลังกรอก
- MS: เริ่มแล้ว (4 responses as of 2026-05-20)

### Summit Prep — ยื่นแล้ว 19 พ.ค. 2569

| File | Status |
|------|--------|
| `Prep for Summit/slide_proposal_v3.html` | **v3 FINAL** — 14 slides |
| `Prep for Summit/boq_template.html` | DONE — 8 หมวดงาน, 1,361 ศาลา |
| `Prep for Summit/survey_sample.html` | DONE — 15 ES ศาลา, รูปจริง |

### Tools Created
- `restore_ms_folders.py` — Scan Drive subfolders → re-populate folder_url in Sheet
- `fetch_photos.gs` — Apps Script ดึง photo IDs จาก Drive
- `patch_photos.py` — Replace HTML placeholders ด้วยรูปจริง

### What's Next
1. **MS 23 folders ขาด** — มนต์สร้าง folders เพิ่มสำหรับ MS 260-282
2. **Publish to Web** — upgrade จาก `/export` เป็น `/pub?` URLs (nice-to-have)

### Key Decisions
- Drive folder ต้องเป็น public เสมอ
- MS forms ใช้ `/d/{ID}` path (ไม่มี published key)
- Bidding docs เป็น "น้ำจิ้ม" โชว์ความพร้อม
