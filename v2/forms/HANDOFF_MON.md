# 📋 งานให้มนต์: สร้าง Google Forms

**จาก**: พี่พีค
**ถึง**: มนต์
**วันที่**: 8 มิ.ย. 2569
**เวลาที่ใช้**: ~5 นาที

---

## สิ่งที่ต้องทำ

สร้าง Google Forms 3 ฟอร์ม ด้วย script (ไม่ต้องสร้างเอง)

---

## ขั้นตอน

### 1. เปิด Google Apps Script
ไปที่ **script.google.com** → กด **New Project**

### 2. ลบ code เก่าทิ้ง
ลบ `function myFunction() {}` ที่อยู่ในหน้าออกให้หมด

### 3. วาง code
เปิดไฟล์ `create_forms.gs` (อยู่ใน folder เดียวกับไฟล์นี้)
**Copy ทั้งหมด** → **Paste** ลงไปแทน

### 4. รัน
- กดปุ่ม **▶ Run** ด้านบน
- ตรงช่อง function ให้เลือก **createAllForms**
- กด Run
- ถ้าขึ้น **Authorization required** → กด Review Permissions → เลือก Google Account → Allow

### 5. ดูผลลัพธ์
- กด **View → Execution log** (หรือ Ctrl+Enter)
- จะเห็น URL ของ 3 ฟอร์ม:
  - P1 รายงานการซ่อม (Traffy Fix)
  - P2 สำรวจสภาพศาลา (Inspection BOQ)
  - P4 รายงานทำความสะอาด (Cleaning)

### 6. ส่งกลับ
**Copy URL ทั้ง 3 ส่งกลับพี่พีค** ทั้ง Edit URL และ Fill URL

---

## ⚠️ สิ่งที่ไม่ต้องทำ

- ❌ ไม่ต้องแก้ code อะไร
- ❌ ไม่ต้องสร้าง form เอง
- ❌ ไม่ต้องตั้งค่าอะไรเพิ่ม

---

## ถ้ามีปัญหา

| ปัญหา | แก้ไข |
|-------|-------|
| ขึ้น "Authorization required" | กด Allow ให้หมด |
| ขึ้น error สีแดง | Screenshot ส่งพี่พีค |
| ไม่เห็น Execution log | กด View → Execution log |

---

**เสร็จแล้วส่ง URL กลับมานะมนต์ 🔥**
