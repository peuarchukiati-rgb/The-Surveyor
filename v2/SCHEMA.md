# Surveyor 2.0 — Multi-Team Data Schema

## Teams

| Team | Priority | Trigger | People | Output |
|------|----------|---------|--------|--------|
| Traffy (พี่สาธิต) | P1 ASAP | Traffy Fondue ticket | 3-4 ช่าง, night work | fix report + 3 photos + case closure |
| Inspection (Rider) | P2 | TOR stop list | 5 Riders (trained w/ พี่สอง) | BOQ assessment per stop |
| Maintenance | P3 | Inspection + Traffy data | ช่าง + แรงงาน, night | fix + before/after + completion |
| Cleaning | P4 | Schedule 4x/year | 2 คัน (driver+mech+3 each) | before/after photos + done flag |

> P1 วิ่งอิสระ (urgent, ตาม complaint) — อาจทับงาน P2-P4 ได้ ถ้าทำแล้วแจ้งทีมอื่นให้ skip
> P4 วิ่งขนานได้เลย ไม่ต้องรอใคร

## Stop Master (all_stops.csv)

| Field | Type | Example |
|-------|------|---------|
| tor | string | ES, SS, NS, MS |
| code | string | ES001, NS245 |
| district | string | จตุจักร |
| road | string | ลาดพร้าว |
| location | string | หน้าโรงแรมลาดพร้าว |
| type | string | Type A, B, B2, JC, S |
| lat | float | 13.811233 |
| long | float | 100.564611 |
| folder_url | string | Google Drive URL |

> verified data from มนต์: `bkk_shelter_list_verified.xlsx` (4 TOR: ES/MS/NS/SS = 1,348 หลัง)

## Traffy Case (traffy_cases.csv — input from มนต์)

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
- 5 tickets @ ES001 = 1 case
- Report to กทม. per case, not per ticket

## P1: Traffy Fix Report

| Field | Type | Notes |
|-------|------|-------|
| code | string | Stop code (prefill from tracker) |
| ticket_id | string | Traffy ticket (prefill) |
| damage_type | string[] | Checkbox: หลอดไฟ, Solar เสีย, หลังคา, เก้าอี้, ระบบไฟ, ทำสี, ทำความสะอาด, **ไม่เสีย** |
| photos | Drive folder | Before + Ongoing + After (3 รูป, same folder) |
| status | enum | แก้ไขเรียบร้อย / ไม่สามารถแก้ไขได้ (+ เหตุผล) |
| timestamp | auto | Google Form response timestamp |

## P2: Inspection Report (BOQ)

| Field | Type | Notes |
|-------|------|-------|
| code | string | Stop code (prefill) |
| หลอดไฟ | checkbox + dropdown | จำนวน 1-10 |
| ระบบไฟ | checkbox | — |
| เก้าอี้ | checkbox + dropdown | จำนวน 1-20 |
| พลังงา | checkbox + dropdown | จำนวน 1-10 |
| ทำสี/ปรับปรุง | checkbox | — |
| ทำความสะอาด | checkbox | — |
| อื่นๆ | checkbox + text | free text |
| ไม่เสีย | checkbox | — |
| Solar เสีย | checkbox | — |
| photos | Drive folder | รูปสภาพจริง |
| timestamp | auto | Google Form response timestamp |

> Night mode only. Rider trained กับพี่สองเรื่องไฟฟ้า. ต้องมีกุญแจตู้ไฟ.

## P3: Maintenance Report (TBD — รอ data structure)

| Field | Type | Notes |
|-------|------|-------|
| code | string | Stop code |
| source | enum | inspection / traffy |
| source_id | string | Inspection ID or Traffy ticket |
| damage_type | string[] | เหมือน P1 form |
| photos | Drive folder | Before + Ongoing + After (เหมือน P1) |
| status | enum | แก้ไขเรียบร้อย / ไม่สามารถแก้ไขได้ |
| timestamp | auto | |

> Form เหมือน Traffy (P1) — ใช้ data จาก P1 + P2 รวมกัน

## P4: Cleaning Report

| Field | Type | Notes |
|-------|------|-------|
| code | string | Stop code (prefill) |
| photos | Drive folder | Before + After (2 รูป) |
| status | enum | แก้ไขเรียบร้อย / แก้ไขไม่ได้ (+ เหตุผล) |
| timestamp | auto | Google Form response timestamp |

## Photo Approach

ทุกทีมใช้ **Google Drive folder** (ไม่ใช่ form upload):
- แต่ละศาลามี folder อยู่แล้ว (`folder_url` ใน all_stops.csv)
- ช่าง/Rider อัปโหลดรูปเข้า folder โดยตรง
- Form แค่บันทึกข้อมูล ไม่รับ file upload
