# 📋 งานให้มนต์: Publish Google Sheets เป็น CSV

**จาก**: พี่พีค
**ถึง**: มนต์
**วันที่**: 9 มิ.ย. 2569
**เวลาที่ใช้**: ~10 นาที (4 forms × 2-3 นาที)

---

## สิ่งที่ต้องทำ

เปิด Google Sheets ของ form response ทั้ง 4 อัน แล้ว publish เป็น CSV URL

---

## ทำซ้ำสำหรับแต่ละ form (4 รอบ)

### Form ที่ต้องทำ

| # | Form | เปิด Edit URL |
|---|------|--------------|
| 1 | P1 Traffy Fix | https://docs.google.com/forms/d/1obh3hP9EcmmXv3-TozRSmS19jHlqrgLxEdofl1xqatQ/edit |
| 2 | P2 Inspection | https://docs.google.com/forms/d/1_wS2-qsw1EqmmfzDYYDz9Ume3r1t3i1im3Xi--_PgSY/edit |
| 3 | P3 Maintenance | https://docs.google.com/forms/d/1DJH08U0WueEnq41RqMYd5Roaoita1ltyzPRoht53nkU/edit |
| 4 | P4 Cleaning | https://docs.google.com/forms/d/1GJvyg7iohIojcVOy_KIaofu0kUEQQA0uJ3QWTLDPxi0/edit |

### ขั้นตอน (ทำทีละ form)

#### Step 1: เปิด Response Sheet
1. เปิด Google Form (กด Edit URL ด้านบน)
2. กดแท็บ **"Responses"** (คำตอบ) ด้านบน
3. กดไอคอน **Google Sheets สีเขียว** (ข้างปุ่ม 3 จุด)
4. จะเปิด Google Sheets ขึ้นมา

#### Step 2: Publish เป็น CSV
1. ใน Google Sheets กด **File → Share → Publish to web**
2. ช่อง "Link" เลือก **Sheet1** (หรือ "Form Responses 1")
3. ช่อง Format เลือก **Comma-separated values (.csv)**
4. กด **Publish**
5. จะได้ URL หน้าตาประมาณ:
   ```
   https://docs.google.com/spreadsheets/d/e/2PACX-.../pub?gid=0&single=true&output=csv
   ```
6. **Copy URL นี้ไว้**

#### Step 3: ทำซ้ำกับ form ถัดไป

---

## ส่งกลับ

**Copy URL ทั้ง 4 ส่งกลับพี่พีค** ตามนี้:

```
P1 Traffy Fix CSV: [วาง URL]
P2 Inspection CSV: [วาง URL]
P3 Maintenance CSV: [วาง URL]
P4 Cleaning CSV: [วาง URL]
```

---

## ⚠️ สิ่งที่ต้องระวัง

- ❌ **อย่าเลือก "Entire Document"** — ให้เลือก Sheet1 หรือ Form Responses 1
- ❌ **อย่าเลือก Web page** — ต้องเลือก CSV
- ✅ ถ้ายังไม่มีใครกรอก form → sheet จะว่างเปล่า ไม่เป็นไร publish ได้เลย
- ✅ เมื่อ publish แล้ว ทุกครั้งที่มีคนกรอก form → CSV จะ update อัตโนมัติ

---

## ถ้ามีปัญหา

| ปัญหา | แก้ไข |
|-------|-------|
| ไม่เห็นไอคอน Sheets สีเขียว | กด 3 จุด → Select response destination |
| Publish to web เป็นสีเทา | ต้อง sign in ด้วย account ที่เป็น owner |
| ไม่มี Sheet1 ให้เลือก | เลือก "Form Responses 1" แทน |

---

**เสร็จแล้วส่ง URL 4 อันกลับมานะมนต์ 🔥**
