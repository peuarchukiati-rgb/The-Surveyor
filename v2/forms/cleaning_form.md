# Cleaning Form — แบบฟอร์มทำความสะอาด (P4)

> ทีมทำความสะอาด — 2 คัน (คนขับ + ช่าง + 3 แรงงาน per คัน)
> ทำได้เลยทุกป้าย 1,400+ หลัง ไม่ต้องรอทีมอื่น
> Google Form — ฟิลด์ที่มี * เป็น required

---

## ฟิลด์ทั้งหมด (Form Fields)

### 1. รหัสศาลา / Stop Code *
- **Type**: Short text
- **Prefill**: Yes — from map/navigator link
- **Validation**: regex `^(ES|MS|NS|SS)\d{3}$`
- **Editable**: Yes — แก้ไขได้ถ้ารหัสไม่ตรง

### 2. สถานะ / Cleaning Status *
- **Type**: Radio button (single select)
- **Options**:
  - ◉ แก้ไขเรียบร้อย
  - ◉ แก้ไขไม่ได้ → **โปรดระบุเหตุผล** (conditional long text)

### 3. รูปถ่าย — Upload to Drive Folder
- **วิธี**: อัปโหลดเข้า Drive folder ของศาลา (ref `folder_url` จาก all_stops.csv)
- **ต้องมี 2 รูป**:
  1. **Before** — ถ่ายก่อนทำความสะอาด
  2. **After** — ถ่ายหลังทำเสร็จ มุมเดียวกับ Before

### 4. Timestamp
- **Type**: Auto (Google Form response timestamp)
- ไม่ต้องกรอก

---

## Google Form Prefill URL Pattern

```
https://docs.google.com/forms/d/e/{FORM_ID}/viewform?usp=pp_url
  &entry.{STOP_CODE_ID}={SHELTER_CODE}
```

---

## Flow การใช้งาน

1. ทีมเปิด **Map/Navigator** บนมือถือ
2. Navigate ตาม TOR lat/long: `https://www.google.com/maps/dir/?api=1&destination={lat},{long}`
3. Locate ป้าย + ยืนยันรหัสศาลา
4. ถ่ายรูป **Before** → อัปโหลดเข้า Drive folder
5. ทำความสะอาด (15-20 นาที/หลัง)
6. ถ่ายรูป **After** → อัปโหลดเข้า Drive folder เดียวกัน
7. เปิด Google Form (prefill รหัสศาลา) → เลือกสถานะ → Submit
8. ไปป้ายถัดไป

---

## Notes

- Response sheet: `Cleaning Responses` ใน Surveyor shared drive
- Schedule: 4 รอบ/ปี — ต้อง track ว่ารอบไหนทำแล้วบ้าง
- ทำขนานกับทุกทีมได้เลย ไม่ต้องรอ Inspection/Traffy
- ถ้าพี่สาธิต (P1) ทำความสะอาดป้ายไหนไปแล้ว → ทีมนี้ skip ได้
