# The Surveyor — Multi-TOR Refactor

Date: 2026-05-14

## Changes
- Refactored `index.html` from single-TOR to 4-TOR support
- Added TOR selector UI (sticky top, localStorage persistence)
- Added per-TOR aggregate stats
- Added placeholder mode for TORs without live provisioning
- Added `data/` folder with static stops CSVs for fallback

## Preserved
- Bangkok East (ES) behavior — 100% identical
- District grouping logic
- Status calculation (todo/day-only/night-only/needs-photo/done)
- Photo confirmation logic (ยืนยัน + อัพรูป + ครบ + NOT ยังไม่ครบ)
- Form prefill URL pattern
