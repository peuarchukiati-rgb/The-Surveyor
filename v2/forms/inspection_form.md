# Inspection Form — แบบฟอร์มสำรวจ BOQ (P2)

> ทีม Rider x5 คน (คัดจาก 9) — สำรวจสภาพศาลาเพื่อทำ BOQ ให้ทีมซ่อม
> ไม่ซ่อม แค่เก็บข้อมูล — Night mode only
> Google Form — ฟิลด์ที่มี * เป็น required

---

## ฟิลด์ทั้งหมด (Form Fields)

### 1. รหัสศาลา / Stop Code *
- **Type**: Short text
- **Prefill**: Yes — from map/navigator link
- **Validation**: regex `^(ES|MS|NS|SS)\d{3}$`
- **Editable**: Yes — แก้ไขได้ถ้ารหัสไม่ตรง

### 2. อาการเสีย + จำนวน / Damage Assessment *
- **Type**: Checkbox + Dropdown (จำนวน) per item

| Checkbox | จำนวน (Dropdown) | Range |
|----------|-----------------|-------|
| ☐ หลอดไฟ | จำนวนหลอด | 1–10 |
| ☐ ระบบไฟ | — | (checkbox only) |
| ☐ เก้าอี้ | จำนวน | 1–20 |
| ☐ พลังงา (Solar/ไฟฟ้า) | จำนวน | 1–10 |
| ☐ ทำสี/ปรับปรุง/บัดกรีผิน | — | (checkbox only) |
| ☐ ทำความสะอาด | — | (checkbox only) |
| ☐ อื่นๆ | — | free text ระบุ |
| ☐ ไม่เสีย | — | — |
| ☐ Solar เสีย | — | (checkbox only) |

> **Google Form implementation**: ใช้ checkbox grid หรือแยกเป็น section per item
> Dropdown จำนวนจะเป็น conditional field — แสดงเฉพาะเมื่อติ๊ก checkbox นั้น

### 3. รูปถ่าย — Upload to Drive Folder
- **วิธี**: อัปโหลดรูปตามที่ถ่ายได้เข้า Drive folder ของศาลา (ref `folder_url`)
- ถ่ายให้เห็นสภาพจริง เน้นจุดเสียหาย

### 4. Timestamp
- **Type**: Auto (Google Form response timestamp)
- ไม่ต้องกรอก

---

## Google Form Prefill URL Pattern

```
https://docs.google.com/forms/d/e/{FORM_ID}/viewform?usp=pp_url
  &entry.{STOP_CODE_ID}={SHELTER_CODE}
```

> Prefill เฉพาะ stop code — อาการเสียให้ Rider กรอกจากที่เห็นหน้างาน

---

## Flow การใช้งาน

1. Rider เปิด **Map/Navigator** บนมือถือ
2. Navigate ตาม TOR lat/long ไปหาศาลา
3. Locate ป้าย + ยืนยันรหัสศาลา
4. ถ่ายรูปสภาพจริง → อัปโหลดเข้า Drive folder
5. เปิด Google Form (prefill รหัสศาลา)
6. ติ๊ก checkbox อาการเสีย + ระบุจำนวนแต่ละรายการ
7. Submit → ไปป้ายถัดไป

---

## Prerequisites

- **อบรมกับพี่สอง**: Rider ต้องเทรนเรื่องระบบไฟฟ้าก่อนลงงาน
  - แยกได้ว่า: หลอดขาด vs ระบบไฟล่ม vs Solar panel เสีย
  - ถ้าไม่แน่ใจ → ติ๊ก "ระบบไฟ" แล้วถ่ายรูปตู้ไฟ
- **กุญแจตู้ไฟ**: ต้องเซ็นสัญญากับ กทม. ก่อนถึงจะได้กุญแจ
- **ทำ Inspection ปชส.บนกระดาน**: ติดประกาศที่ป้ายว่ากำลังสำรวจ

## Notes

- Response sheet: `Inspection Responses` ใน Surveyor shared drive
- Night mode only — ไม่มี Day survey
- Rider 5 คนที่คัดแล้ว ค่อนข้างมั่นใจ (จาก 9 ตัด 4)
- Output นี้จะเป็น input ให้ P3 (Maintenance) + P4 (Fixing) ใช้เบิกของซ่อม
