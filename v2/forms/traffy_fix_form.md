# Traffy Fix Report Form — แบบฟอร์มรายงานการซ่อม

> สำหรับทีมช่างพี่สาธิต ใช้รายงานผลการซ่อมป้ายรถเมล์จากเคส Traffy Fondue
> จะนำไปสร้างเป็น Google Form — ฟิลด์ที่มี * เป็น required

---

## ฟิลด์ทั้งหมด (Form Fields)

### 1. รหัสป้าย / Stop Code *
- **Type**: Short text
- **Prefill**: Yes — from tracker link
- **Validation**: ต้องขึ้นต้นด้วย ES, MS, NS, SS, TNS (regex: `^(ES|MS|NS|SS|TNS)\d{3}$`)
- **Example**: ES422, MS120, NS003

### 2. Traffy Ticket ID *
- **Type**: Short text
- **Prefill**: Yes — from tracker link
- **Example**: 2025-AMXRAZ, ABREZU

### 3. ประเภทงาน / Work Type *
- **Type**: Dropdown (single select)
- **Options**:
  - ไฟ/แสงสว่าง (Lighting)
  - ที่นั่ง/ม้านั่ง (Seating/Bench)
  - โครงสร้าง/ป้าย (Structure/Sign)
  - หลังคา/กันแดดฝน (Roof/Shelter cover)

### 4. รูป Before / Photo Before *
- **Type**: File upload (image)
- **Note**: ถ่ายก่อนลงมือซ่อม ให้เห็นปัญหาชัดเจน
- **Accepted**: JPG, PNG, HEIC

### 5. รูป After / Photo After *
- **Type**: File upload (image)
- **Note**: ถ่ายหลังซ่อมเสร็จ มุมเดียวกับ Before
- **Accepted**: JPG, PNG, HEIC

### 6. รายละเอียดการซ่อม / Repair Description *
- **Type**: Long text (paragraph)
- **Hint**: อธิบายสิ่งที่ซ่อม เช่น "เปลี่ยนหลอดไฟ LED 2 ดวง", "เชื่อมขาม้านั่งใหม่"

### 7. สถานะ / Repair Status *
- **Type**: Dropdown (single select)
- **Options**:
  - ซ่อมเสร็จ (Completed)
  - ซ่อมบางส่วน (Partially fixed)
  - รอวัสดุ (Waiting for materials)
  - ไม่สามารถซ่อมได้ (Cannot fix — need escalation)

### 8. หมายเหตุ / Notes
- **Type**: Long text (paragraph)
- **Required**: No
- **Hint**: ข้อมูลเพิ่มเติม เช่น ต้องกลับมาซ่อมต่อ, สภาพพื้นที่อันตราย, ฯลฯ

### 9. ชื่อช่าง / Technician Name *
- **Type**: Short text
- **Hint**: ชื่อ-นามสกุล หรือชื่อเล่นที่ทีมใช้

### 10. วันที่ซ่อม / Repair Date *
- **Type**: Date
- **Default**: Today

---

## Google Form Prefill URL Pattern

เมื่อสร้าง Google Form แล้ว ให้ใช้ pattern นี้สร้าง link จาก Traffy Tracker:

```
https://docs.google.com/forms/d/e/{FORM_ID}/viewform?usp=pp_url
  &entry.{FIELD_ID_STOP_CODE}={SHELTER_CODE}
  &entry.{FIELD_ID_TICKET}={TICKET_ID}
  &entry.{FIELD_ID_WORK_TYPE}={WORK_TYPE}
```

**วิธีหา Field ID**:
1. เปิด Google Form ที่สร้างแล้ว
2. กด "Get pre-filled link" (รับลิงก์ที่กรอกไว้ล่วงหน้า)
3. กรอกค่าตัวอย่างในแต่ละช่อง แล้วกด "Get link"
4. จะได้ URL ที่มี `entry.XXXXXXXXX=ค่าตัวอย่าง` — ตัวเลขหลัง entry. คือ Field ID

**ตัวอย่าง URL จริง** (หลังสร้าง form):
```
https://docs.google.com/forms/d/e/1FAIpQL.../viewform?usp=pp_url&entry.123456=ES422&entry.789012=2025-AMXRAZ&entry.345678=ไฟ/แสงสว่าง
```

---

## Flow การใช้งาน

1. ทีมช่างเปิด **Traffy Tracker** บนมือถือ
2. กดเคสที่จะไปซ่อม → เห็น detail + Google Maps link
3. เปลี่ยนสถานะเป็น "In Progress"
4. ถ่ายรูป Before ก่อนลงมือ
5. ซ่อมเสร็จ → ถ่ายรูป After
6. กดลิงก์ "รายงานการซ่อม" → เปิด Google Form (prefill แล้ว)
7. กรอกข้อมูล + แนบรูป → Submit
8. กลับมา Tracker → เปลี่ยนสถานะเป็น "Fixed" หรือ "Reported"

---

## Notes สำหรับการสร้าง Google Form

- ตั้งค่า Form ให้ **Collect email** (เผื่อต้อง follow-up)
- เปิด **File upload** ต้องใช้ Google Workspace account
- ถ้าช่างใช้ personal Gmail ให้เปิด "Allow uploads from external accounts"
- Response sheet ควรชื่อ `Traffy Fix Responses` อยู่ใน Surveyor shared drive
- หลังได้ Form ID จริง ให้ update prefill link ใน `build_traffy_tracker.py`
