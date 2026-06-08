# Traffy Fix Report Form — แบบฟอร์มรายงานการซ่อม (P1)

> ทีมช่างพี่สาธิต — ซ่อมป้ายรถเมล์ตามเคส Traffy Fondue
> Google Form — ฟิลด์ที่มี * เป็น required

---

## ฟิลด์ทั้งหมด (Form Fields)

### 1. รหัสป้าย / Stop Code *
- **Type**: Short text
- **Prefill**: Yes — from tracker link
- **Validation**: regex `^(ES|MS|NS|SS)\d{3}$`
- **Editable**: Yes — ช่างแก้ไขได้ถ้ารหัสไม่ตรง
- **Example**: ES422, MS120, NS003

### 2. Traffy Ticket ID *
- **Type**: Short text
- **Prefill**: Yes — from tracker link
- **Example**: 2025-AMXRAZ, ABREZU

### 3. อาการเสีย / Damage Type *
- **Type**: Checkboxes (multiple select)
- **Prefill**: Yes — pre-fill จาก Traffy `work_type` ให้ช่างเห็นก่อนออกงาน
- **Options**:
  - ☐ หลอดไฟ (หลอดเสีย)
  - ☐ Solar เสีย
  - ☐ หลังคา
  - ☐ เก้าอี้
  - ☐ ระบบไฟ (อุปกรณ์เสีย)
  - ☐ ทำสี/ปรับปรุง/บัดกรีผิน
  - ☐ ทำความสะอาด
  - ☐ **ไม่เสีย (แก้ไขไปแล้ว)** — กรณีหน่วยงานอื่นซ่อมไปก่อน

### 4. รูปถ่าย — Upload to Drive Folder
- **วิธี**: ช่างอัปโหลดรูปเข้า Drive folder ของศาลานั้น (ref `folder_url` จาก all_stops.csv)
- **ทุกรูปอยู่โฟลเดอร์เดียวกัน** ไม่แยก sub-folder
- **ต้องมี 3 รูป**:
  1. **Before** — ถ่ายก่อนลงมือ ให้เห็นปัญหาชัด
  2. **Ongoing** — ถ่ายระหว่างทำงาน
  3. **After** — ถ่ายหลังซ่อมเสร็จ มุมเดียวกับ Before
- **Accepted**: JPG, PNG, HEIC

### 5. สถานะ / Repair Status *
- **Type**: Radio button (single select)
- **Options**:
  - ◉ แก้ไขเรียบร้อย
  - ◉ ไม่สามารถแก้ไขได้ → **โปรดระบุเหตุผล** (conditional long text)

### 6. Timestamp
- **Type**: Auto (Google Form response timestamp)
- ไม่ต้องกรอก — ระบบบันทึกเวลาอัตโนมัติ

---

## Google Form Prefill URL Pattern

```
https://docs.google.com/forms/d/e/{FORM_ID}/viewform?usp=pp_url
  &entry.{STOP_CODE_ID}={SHELTER_CODE}
  &entry.{TICKET_ID}={TICKET_ID}
  &entry.{DAMAGE_TYPE_ID}={DAMAGE_1}
  &entry.{DAMAGE_TYPE_ID}={DAMAGE_2}
```

> **Checkbox prefill**: ใน Google Forms ให้ซ้ำ `entry.{ID}` หลายครั้งสำหรับแต่ละ option ที่ต้องการ pre-check
> เช่น `&entry.999=หลอดไฟ (หลอดเสีย)&entry.999=หลังคา`

**วิธีหา Field ID**:
1. เปิด Google Form ที่สร้างแล้ว
2. กด "Get pre-filled link"
3. กรอกค่าตัวอย่าง → กด "Get link"
4. `entry.XXXXXXXXX` = Field ID

---

## Flow การใช้งาน

1. ช่างเปิด **Traffy Tracker** บนมือถือ
2. กดเคสที่จะไปซ่อม → เห็น detail + อาการเสีย + Google Maps link
3. Navigate ไปหน้างานตาม lat/long
4. ถ่ายรูป **Before** → อัปโหลดเข้า Drive folder
5. ลงมือซ่อม → ถ่ายรูป **Ongoing**
6. ซ่อมเสร็จ → ถ่ายรูป **After** → อัปโหลดทั้งหมดเข้า Drive folder เดียวกัน
7. กดลิงก์ "รายงานการซ่อม" → Google Form (prefill รหัส + ticket + อาการเสีย)
8. เลือกสถานะ → Submit
9. กลับ Tracker → เปลี่ยนสถานะเป็น "Fixed" หรือ "Reported"

---

## Notes

- Response sheet: `Traffy Fix Responses` ใน Surveyor shared drive
- หลังได้ Form ID จริง → update prefill link ใน `build_traffy_tracker.py`
- **กำชับพี่สาธิต**: ต้องส่ง 3 รูปครบทุกเคส (Before/Ongoing/After) — Last Shot
- ถ้าเลือก "ไม่เสีย" ยังต้องถ่ายรูป Before เป็นหลักฐาน
