#!/usr/bin/env bash
# beat-scribe.sh — the 5-minute brewing-beat wake.
# Pulls the event batch since the last watermark, decides whether the current
# beat commits (>=30min) or keeps brewing, and nudges the scribe to write or
# update the beat's copy. No-op when there is nothing new.
set -euo pipefail
cd "$(dirname "$0")/.."

VERDICT=$(python3 commands/beat-scribe.py 2>/dev/null || echo '{"action":"error"}')

if echo "$VERDICT" | grep -q '"action": "commit"'; then
  gc session nudge scribe "COMMIT: the beat has brewed 30 minutes. Finalize its copy in the handoff voice (first-person 'We', meaning over mechanics), then close it as a committed timeline item. A new beat is now brewing." --delivery wait-idle 2>/dev/null \
    || gc session wake scribe 2>/dev/null || true
  echo "beat-scribe: committed + new beat brewing"
elif echo "$VERDICT" | grep -q '"action": "update"'; then
  BATCH=$(echo "$VERDICT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('batch',''))")
  gc session nudge scribe "UPDATE: new events landed in the brewing beat. Read the batch ($BATCH). If it extends the current thread, revise the beat's sentence to summarise both. If it is a new thread, note it as a second sentence. Keep the handoff voice." --delivery wait-idle 2>/dev/null \
    || gc session wake scribe 2>/dev/null || true
  echo "beat-scribe: update requested"
else
  echo "beat-scribe: no-op"
fi
