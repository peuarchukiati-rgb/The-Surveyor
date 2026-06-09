/**
 * The Surveyor 2.0 — สร้าง Google Forms อัตโนมัติ
 * รันครั้งเดียว จะได้ 3 forms: P1 Traffy Fix, P2 Inspection, P4 Cleaning
 *
 * วิธีใช้:
 * 1. เปิด script.google.com
 * 2. สร้าง Project ใหม่
 * 3. วาง code นี้ทั้งหมด
 * 4. กด Run → เลือก createAllForms
 * 5. อนุญาต permissions
 * 6. ดู Log (View → Execution log) จะเห็น Form URL ทั้ง 3 อัน
 */

function createAllForms() {
  const results = [];

  results.push(createP1TraffyFixForm());
  results.push(createP2InspectionForm());
  results.push(createP4CleaningForm());

  Logger.log("\n============================");
  Logger.log("สร้างเสร็จทั้ง 3 ฟอร์ม!");
  Logger.log("============================\n");

  results.forEach(r => {
    Logger.log(`${r.name}`);
    Logger.log(`  Edit: ${r.editUrl}`);
    Logger.log(`  Fill: ${r.publishedUrl}`);
    Logger.log(`  ID:   ${r.id}\n`);
  });

  Logger.log("ส่ง URL ทั้ง 3 กลับให้พี่พีคด้วยนะ!");
}


// ─────────────────────────────────────────────
// P1: Traffy Fix Report — ทีมช่างพี่สาธิต
// ─────────────────────────────────────────────
function createP1TraffyFixForm() {
  const form = FormApp.create("P1 รายงานการซ่อม — Traffy Fix Report");
  form.setDescription(
    "ทีมช่างพี่สาธิต — ซ่อมป้ายรถเมล์ตามเคส Traffy Fondue\n" +
    "กรอกหลังซ่อมเสร็จทุกเคส\n\n" +
    "⚠️ อัปโหลดรูป Before / Ongoing / After เข้า Drive folder ของศาลาก่อนกรอกฟอร์ม"
  );
  form.setCollectEmail(true);
  form.setConfirmationMessage("บันทึกเรียบร้อย ✓");

  // 1. รหัสป้าย
  const stopCode = form.addTextItem();
  stopCode.setTitle("รหัสป้าย / Stop Code");
  stopCode.setHelpText("เช่น ES422, MS120, NS003");
  stopCode.setRequired(true);
  stopCode.setValidation(
    FormApp.createTextValidation()
      .requireTextMatchesPattern("^(ES|MS|NS|SS)\\d{3}$")
      .setHelpText("รูปแบบ: ES001, MS120, NS003, SS233")
      .build()
  );

  // 2. Traffy Ticket ID
  const ticketId = form.addTextItem();
  ticketId.setTitle("Traffy Ticket ID");
  ticketId.setHelpText("เช่น 2025-AMXRAZ");
  ticketId.setRequired(true);

  // 3. อาการเสีย (checkboxes)
  const damageType = form.addCheckboxItem();
  damageType.setTitle("อาการเสีย / Damage Type");
  damageType.setHelpText("เลือกได้หลายข้อ — ติ๊กตามที่ซ่อมจริง");
  damageType.setRequired(true);
  damageType.setChoices([
    damageType.createChoice("หลอดไฟ (หลอดเสีย)"),
    damageType.createChoice("Solar เสีย"),
    damageType.createChoice("หลังคา"),
    damageType.createChoice("เก้าอี้"),
    damageType.createChoice("ระบบไฟ (อุปกรณ์เสีย)"),
    damageType.createChoice("ทำสี/ปรับปรุง/บัดกรีผิน"),
    damageType.createChoice("ทำความสะอาด"),
    damageType.createChoice("ไม่เสีย (แก้ไขไปแล้ว)")
  ]);

  // 4. สถานะ
  const status = form.addMultipleChoiceItem();
  status.setTitle("สถานะ / Repair Status");
  status.setRequired(true);

  // Create page for "cannot fix" reason
  const reasonPage = form.addPageBreakItem();
  reasonPage.setTitle("ระบุเหตุผลที่แก้ไขไม่ได้");

  const reason = form.addParagraphTextItem();
  reason.setTitle("เหตุผลที่ไม่สามารถแก้ไขได้");
  reason.setRequired(true);

  status.setChoices([
    status.createChoice("แก้ไขเรียบร้อย", FormApp.PageNavigationType.SUBMIT),
    status.createChoice("ไม่สามารถแก้ไขได้", reasonPage)
  ]);

  Logger.log("✓ P1 Traffy Fix Form created");
  return {
    name: "P1 Traffy Fix",
    id: form.getId(),
    editUrl: form.getEditUrl(),
    publishedUrl: form.getPublishedUrl()
  };
}


// ─────────────────────────────────────────────
// P2: Inspection BOQ — ทีม Rider
// ─────────────────────────────────────────────
function createP2InspectionForm() {
  const form = FormApp.create("P2 สำรวจสภาพศาลา — Inspection BOQ");
  form.setDescription(
    "ทีม Rider — สำรวจสภาพศาลาเพื่อทำ BOQ\n" +
    "ไม่ซ่อม แค่เก็บข้อมูล — Night mode only\n\n" +
    "⚠️ อัปโหลดรูปสภาพจริงเข้า Drive folder ของศาลาก่อนกรอกฟอร์ม"
  );
  form.setCollectEmail(true);
  form.setConfirmationMessage("บันทึกเรียบร้อย ✓");

  // 1. รหัสศาลา
  const stopCode = form.addTextItem();
  stopCode.setTitle("รหัสศาลา / Stop Code");
  stopCode.setHelpText("เช่น ES001, MS120");
  stopCode.setRequired(true);
  stopCode.setValidation(
    FormApp.createTextValidation()
      .requireTextMatchesPattern("^(ES|MS|NS|SS)\\d{3}$")
      .setHelpText("รูปแบบ: ES001, MS120, NS003, SS233")
      .build()
  );

  // 2. หลอดไฟ
  const lights = form.addCheckboxItem();
  lights.setTitle("หลอดไฟ");
  lights.setChoices([lights.createChoice("เสีย")]);
  lights.setRequired(false);

  const lightsCount = form.addListItem();
  lightsCount.setTitle("จำนวนหลอดไฟที่เสีย");
  lightsCount.setHelpText("เลือกจำนวน (ถ้าติ๊กหลอดไฟเสีย)");
  lightsCount.setRequired(false);
  lightsCount.setChoices(
    Array.from({length: 10}, (_, i) => lightsCount.createChoice(String(i + 1)))
  );

  // 3. ระบบไฟ
  const elecSystem = form.addCheckboxItem();
  elecSystem.setTitle("ระบบไฟ");
  elecSystem.setChoices([elecSystem.createChoice("เสีย")]);
  elecSystem.setRequired(false);

  // 4. เก้าอี้
  const seats = form.addCheckboxItem();
  seats.setTitle("เก้าอี้");
  seats.setChoices([seats.createChoice("เสีย")]);
  seats.setRequired(false);

  const seatsCount = form.addListItem();
  seatsCount.setTitle("จำนวนเก้าอี้ที่เสีย");
  seatsCount.setRequired(false);
  seatsCount.setChoices(
    Array.from({length: 20}, (_, i) => seatsCount.createChoice(String(i + 1)))
  );

  // 5. พลังงา (Solar/ไฟฟ้า)
  const energy = form.addCheckboxItem();
  energy.setTitle("พลังงา (Solar/ไฟฟ้า)");
  energy.setChoices([energy.createChoice("เสีย")]);
  energy.setRequired(false);

  const energyCount = form.addListItem();
  energyCount.setTitle("จำนวนพลังงาที่เสีย");
  energyCount.setRequired(false);
  energyCount.setChoices(
    Array.from({length: 10}, (_, i) => energyCount.createChoice(String(i + 1)))
  );

  // 6. Solar เสีย
  const solar = form.addCheckboxItem();
  solar.setTitle("Solar เสีย");
  solar.setChoices([solar.createChoice("เสีย")]);
  solar.setRequired(false);

  // 7. ทำสี/ปรับปรุง
  const paint = form.addCheckboxItem();
  paint.setTitle("ทำสี/ปรับปรุง/บัดกรีผิน");
  paint.setChoices([paint.createChoice("ต้องทำ")]);
  paint.setRequired(false);

  // 8. ทำความสะอาด
  const clean = form.addCheckboxItem();
  clean.setTitle("ทำความสะอาด");
  clean.setChoices([clean.createChoice("ต้องทำ")]);
  clean.setRequired(false);

  // 9. อื่นๆ
  const other = form.addParagraphTextItem();
  other.setTitle("อื่นๆ (ระบุ)");
  other.setRequired(false);

  // 10. ไม่เสีย
  const notBroken = form.addCheckboxItem();
  notBroken.setTitle("สถานะรวม");
  notBroken.setChoices([notBroken.createChoice("ไม่เสีย (สภาพดี)")]);
  notBroken.setRequired(false);

  Logger.log("✓ P2 Inspection Form created");
  return {
    name: "P2 Inspection BOQ",
    id: form.getId(),
    editUrl: form.getEditUrl(),
    publishedUrl: form.getPublishedUrl()
  };
}


// ─────────────────────────────────────────────
// P4: Cleaning — ทีมทำความสะอาด
// ─────────────────────────────────────────────
function createP4CleaningForm() {
  const form = FormApp.create("P4 รายงานทำความสะอาด — Cleaning Report");
  form.setDescription(
    "ทีมทำความสะอาด — ทำได้เลยทุกป้าย ไม่ต้องรอทีมอื่น\n\n" +
    "⚠️ อัปโหลดรูป Before / After เข้า Drive folder ของศาลาก่อนกรอกฟอร์ม"
  );
  form.setCollectEmail(true);
  form.setConfirmationMessage("บันทึกเรียบร้อย ✓");

  // 1. รหัสศาลา
  const stopCode = form.addTextItem();
  stopCode.setTitle("รหัสศาลา / Stop Code");
  stopCode.setHelpText("เช่น ES001, MS120");
  stopCode.setRequired(true);
  stopCode.setValidation(
    FormApp.createTextValidation()
      .requireTextMatchesPattern("^(ES|MS|NS|SS)\\d{3}$")
      .setHelpText("รูปแบบ: ES001, MS120, NS003, SS233")
      .build()
  );

  // 2. สถานะ
  const status = form.addMultipleChoiceItem();
  status.setTitle("สถานะ / Cleaning Status");
  status.setRequired(true);

  const reasonPage = form.addPageBreakItem();
  reasonPage.setTitle("ระบุเหตุผลที่ทำไม่ได้");

  const reason = form.addParagraphTextItem();
  reason.setTitle("เหตุผลที่แก้ไขไม่ได้");
  reason.setRequired(true);

  status.setChoices([
    status.createChoice("แก้ไขเรียบร้อย", FormApp.PageNavigationType.SUBMIT),
    status.createChoice("แก้ไขไม่ได้", reasonPage)
  ]);

  Logger.log("✓ P4 Cleaning Form created");
  return {
    name: "P4 Cleaning",
    id: form.getId(),
    editUrl: form.getEditUrl(),
    publishedUrl: form.getPublishedUrl()
  };
}
