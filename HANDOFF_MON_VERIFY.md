# ✅ Handoff — Peak → มนต์ : verify รอบ 2 (แก้ครบ 5 ข้อ + redesign)

**จาก**: พี่พีค · **ถึง**: มนต์ · **วันที่**: 1 ก.ค. 2569

มนต์ แก้ตาม feedback รอบ 1 ครบทั้ง 5 ข้อแล้ว + rebuild หน้าใหม่เป็น drill-down 4 ชั้นตาม PDF. push ขึ้น live แล้ว ช่วย verify รอบ 2 ที

> refresh แบบล้าง cache: มือถือปิดแท็บเปิดใหม่ / คอม Ctrl+Shift+R

**URL:**
```
Dashboard: https://peuarchukiati-rgb.github.io/The-Surveyor/v2/output/dashboard.html
Map:       https://peuarchukiati-rgb.github.io/The-Surveyor/v2/map/
```

---

## ✅ แก้ให้แล้ว (feedback รอบ 1)

| # | มนขอ | สถานะ |
|---|------|-------|
| 1 | ตัด TNS ออกทั้งระบบ | ✅ dashboard + map ไม่มี TNS แล้ว (1620 → **1348**) |
| 2 | TNS154 folder error | ✅ หายเอง (TNS ออกหมด) |
| 3 | สี + ปุ่มเขต แบบ v1 | ✅ P1 แดง / P2 เหลือง / P3 ฟ้า / P4 เขียว + โซนมีสีประจำ |
| 4 | ทุก P ฐาน 1,348 | ✅ P1/P2/P3/P4 = /1348 หมด (นับจาก data จริง: ES606/MS263/NS246/SS233) |
| 5 | flow drill-down 4 ชั้น | ✅ overall → ทีม P → โซน → เขต → ศาลา |

> ⚠️ เลขจะเป็น **MS 263 / SS 233** (ตาม verified list) ไม่ใช่ 259/255 ในภาพ mockup — ตามที่มนสั่งข้อ 4

---

## ☑️ Checklist verify รอบ 2

**ชั้น 1 — หน้าแรก**
- [ ] ปุ่มโซนบนสุดมีแค่ 4 (กลาง/เหนือ/ใต้/ตะวันออก) — **ไม่มีกรุงธน/TNS**
- [ ] stat 5 ใบ: ศาลา 1348 + P1–P4 ทุกตัวหาร /1348
- [ ] ปุ่มทีม P1–P4 สีถูก (แดง/เหลือง/ฟ้า/เขียว) + ตารางย่อ MS/NS/SS/ES ใต้ปุ่ม

**ชั้น 2–4 — drill-down**
- [ ] กดทีม P → เจอ 4 ปุ่มโซน + ยอดเสร็จ/ยังไม่เสร็จ
- [ ] กดโซน → list รายเขต + progression (เช่น คลองเตย x/y)
- [ ] กดเขต → list ศาลา + สถานะ `เสร็จ ✓` / `ยังไม่ทำ`
- [ ] กดศาลา → 3 ปุ่ม 📍 แผนที่ · 📁 อัพรูป · 📄 กรอกข้อมูล
- [ ] ปุ่ม **‹ กลับ** / breadcrumb เดินย้อนชั้นได้

**Live (ยังทำงานเหมือนเดิม)**
- [ ] แก้ P_STATUS 1 แถว (MS001 P4 → done) รอ 1 นาที refresh → ศาลานั้นเปลี่ยนเป็นเสร็จ ✓ (เสร็จแล้วแก้กลับ pending)

**Map**
- [ ] หมุดขึ้น 1,348 ไม่มี TNS, legend ไม่มีชั้น TNS ว่างๆ

---

## 🔴 สถานะไม่อัพเดท (เทส ES001 แล้วเลขไม่ขยับ) — แก้ฝั่งมน

เช็คแล้ว: dashboard ดึงข้อมูลถูก match รหัส 1,348/1,348. **แต่ published CSV ของ P_STATUS ยัง pending ทั้ง 1,348 แถว (non-pending = 0)** → ที่มนแก้ ES001 ยังไม่ทะลุมาถึง CSV ที่ publish. dashboard เลยไม่มีอะไรให้อัพเดท

**สาเหตุ = Publish-to-web ฝั่งมน ไม่ใช่โค้ด.** เช็ค 3 จุดตามลำดับ:

1. **เปิด Auto-republish** (น่าจะตัวนี้) — เปิดไฟล์ P_STATUS → **File → Share → Publish to web** → ต้องติ๊ก **"Automatically republish when changes are made"**. ถ้าไม่ติ๊ก แก้ชีตยังไง CSV ก็ค้างค่าเก่าตลอด
2. **แก้ให้ตรง tab** — ที่ publish คือ tab `gid=1738862538`. ต้องแก้ tab เดียวกันนี้ (ไม่ใช่ไฟล์/แท็บอื่น)
3. **รอ cache ~5 นาที** — pub CSV ของ Google cache ~5 นาที. refresh เร็วกว่านั้นยังเห็นค่าเก่า

**format รหัส**: ในชีตต้องเป็น `ES001` (3 หลัก) ให้ตรงแถวอื่น — `ES01`/`ES1` join ไม่ติด

### ✅ Self-test (ยืนยันว่าจบที่ publish ไม่ใช่ dashboard)
เปิด URL นี้ตรงๆ ในเบราว์เซอร์ → แก้ ES001 P4 = `done` ในชีต → รอ 5 นาที → refresh URL นี้
```
https://docs.google.com/spreadsheets/d/e/2PACX-1vQhYBDAEPsCLz_m5rzh2dIug18LysrxzBgHIqyzfGdVGPJ77449cSbgCS1AdAw0uJ4cybFImGIyqlbT/pub?gid=1738862538&single=true&output=csv
```
- **ยัง pending ใน URL นี้** = ปัญหา publish 100% (แก้ข้อ 1) — dashboard ไม่เกี่ยว
- **เปลี่ยนเป็น done ใน URL นี้แล้ว แต่ dashboard ยังไม่ขึ้น** = ค่อยกลับมาหาพี่ (ตอนนั้นค่อยดูฝั่งเรา)

---

## ✅ อัปเดตรอบ verify-2 (แก้ให้แล้ว)

- **badge "เสร็จ ✓" ผิดปุ่ม** → ย้ายจาก 📁 อัพรูป ไป 📄 กรอกข้อมูล แล้ว (P_STATUS = สัญญาณกรอกฟอร์ม) — refresh เช็คได้
- **auto-sync** ฝั่งมน (Apps Script 5 นาที) — เรื่องสถานะไม่อัพเดทจบสมบูรณ์
- **photo backup** — พี่ทำ script ดึงรูปจาก Master folder เก็บ local weekly (copy, ผู้สำรวจลบไม่กระทบ backup) กัน quota/account risk ที่มนเตือน

## 🔜 รอมนต์ (ค้างฝั่งมน)

- **entry ID (prefill รหัส)**: เปิดฟอร์ม P2/P4 → ⋮ → Get pre-filled link → กรอกช่องรหัสค่าอะไรก็ได้ → Get link → ก็อปเลข `entry.XXXXX` ในURL ส่งพี่ (2 ตัว P2+P4) → พี่เสียบให้ prefill รหัสรายศาลา
- **P1 (Traffy) + P3 (Maintenance)**: form fill link + entry ID + เปิด Editor + folder P1_MAP/P3_MAP + เพิ่มเข้า auto-sync → ส่งรอบเดียว

verify แล้วตีกลับว่าข้อไหนผ่าน/ไม่ผ่านนะครับ 🔥
