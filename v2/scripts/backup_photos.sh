#!/usr/bin/env bash
#
# backup_photos.sh — pull a local safety copy of every field photo from the
# Master Drive folder "The Surveyor v2 - Photos".
#
# WHY: field-survey photos are owned by whoever uploaded them, not by the
# folder owner (Peak/มนต์). If a surveyor deletes a photo or their Google
# account, the file vanishes from our Drive too. This keeps an independent,
# append-only local copy so the project never loses evidence.
#
# We use `rclone copy` (NOT `sync`): files removed on Drive are KEPT locally.
# That is the whole point — deletions upstream must not propagate to backup.
#
# ── ONE-TIME SETUP ────────────────────────────────────────────────────────
#   1. brew install rclone
#   2. rclone config
#        n) new remote
#        name> surveyor
#        storage> drive            (Google Drive)
#        client_id / secret> (blank, press enter — uses rclone default)
#        scope> 1                  (full access) or 2 (read-only) — 2 is safer
#        root_folder_id> (blank)
#        service_account_file> (blank)
#        Edit advanced config> n
#        Use auto config> y        → browser opens, log in as the Drive owner
#                                     account that can see the Master folder
#        Configure as team drive> n
#        y) confirm  →  q) quit
#   3. Test: rclone lsd "surveyor:" --drive-root-folder-id="$MASTER_FOLDER_ID"
#
# ── RUN ───────────────────────────────────────────────────────────────────
#   ./backup_photos.sh                 # full incremental backup
#   DEST=/Volumes/ext/backup ./backup_photos.sh   # override destination
#
# ── SCHEDULE (weekly, launchd on macOS) ───────────────────────────────────
#   see backup_photos.plist.sample next to this script.
#
set -euo pipefail

# ── config (override via env) ─────────────────────────────────────────────
REMOTE="${REMOTE:-surveyor}"
# Master folder "The Surveyor v2 - Photos" (owned by Peak, anyone-link access).
MASTER_FOLDER_ID="${MASTER_FOLDER_ID:-1TezoCbHGOCFi1Kor53QA6Gb8tzN6Opai}"
DEST="${DEST:-$HOME/Desktop/the-surveyor/photo-backup}"
LOG_DIR="${LOG_DIR:-$HOME/Desktop/the-surveyor/photo-backup/_logs}"

TS="$(date +%Y-%m-%d_%H%M%S)"
LOG_FILE="$LOG_DIR/backup_$TS.log"

# ── preflight ─────────────────────────────────────────────────────────────
if ! command -v rclone >/dev/null 2>&1; then
  echo "✗ rclone not installed. Run: brew install rclone   (then see SETUP in this file)" >&2
  exit 1
fi
if ! rclone listremotes 2>/dev/null | grep -qx "${REMOTE}:"; then
  echo "✗ rclone remote '${REMOTE}:' not configured. Run: rclone config  (see SETUP in this file)" >&2
  exit 1
fi

mkdir -p "$DEST" "$LOG_DIR"

echo "▶ Surveyor photo backup — $TS"
echo "  remote : ${REMOTE}: (root folder $MASTER_FOLDER_ID)"
echo "  dest   : $DEST"
echo "  log    : $LOG_FILE"
echo "  mode   : copy (upstream deletions are preserved locally)"

# ── run ───────────────────────────────────────────────────────────────────
# --drive-root-folder-id : scope the remote to the Master photos folder
# copy (not sync)        : never delete local files
# --drive-acknowledge-abuse : allow files Google flags (large albums)
# --fast-list            : fewer API calls on big trees
# --transfers/-checkers  : keep it gentle on the API quota
rclone copy "${REMOTE}:" "$DEST" \
  --drive-root-folder-id="$MASTER_FOLDER_ID" \
  --fast-list \
  --transfers=4 --checkers=8 \
  --drive-acknowledge-abuse \
  --log-file="$LOG_FILE" --log-level INFO \
  --stats=30s --stats-one-line \
  -P

# ── summary ───────────────────────────────────────────────────────────────
NEW=$(grep -c "Copied (new)" "$LOG_FILE" 2>/dev/null || echo 0)
TOTAL_FILES=$(find "$DEST" -type f -not -path "*/_logs/*" | wc -l | tr -d ' ')
TOTAL_SIZE=$(du -sh "$DEST" 2>/dev/null | cut -f1)
echo "✓ Done. new files this run: $NEW · total backed up: $TOTAL_FILES files ($TOTAL_SIZE)"
echo "  log: $LOG_FILE"
