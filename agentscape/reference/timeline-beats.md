# Timeline beats — the brewing-beat order

The concrete implementation of the Scape timeline's **brewing beat**: a timeline
item that accumulates for ~30 minutes before it commits, so the human can watch
a beat form in real time instead of only seeing finished summaries.

This is the **what to build** — the exact files, their contents, and the wiring.
The design rationale is in `companion-nervous-system.md` (propagation is care)
and the Scape wayfinder's `WRAPPED-WRITING.md` (the handoff voice). This doc is
the buildable spec.

## The shape in one line

A **cooldown order** wakes every 5 minutes, pulls the batch of real events since
the last wake, and hands it to a **scribe agent** that writes or updates the
current brewing beat's copy in the handoff voice. When a beat has brewed ~30
minutes, it **commits** (becomes a permanent timeline item) and a new beat
starts brewing.

## Why this shape

- **The human sees the beat form.** A beat is not a finished summary that
  appears at the end of the hour. It is a live item that accumulates: the scribe
  adds a sentence when the batch is meaningful, revises it when the next batch
  extends the same thread, and the human watches it brew.
- **The copy is written by an agent, not a script.** The script is deterministic
  (pull events, decide commit-vs-update, nudge). The *writing* is the scribe's
  job, in the handoff voice — first-person "We", meaning over mechanics, the
  city's own vocabulary.
- **Cooldown, not cron.** The order is `trigger = "cooldown"`, `interval = "5m"`,
  exactly like the observer-wake order. It is idempotent: if a wake is missed or
  overlaps, the `last_seq` watermark prevents double-processing.

## Files to create

```
orders/beat-scribe.toml          # the 5-minute cooldown order
commands/beat-scribe.sh          # the trigger: pull events, decide, nudge
commands/beat-scribe.py          # deterministic state machine (from assets/beat-scribe.template.py)

twin/timeline/brewing.json       # the current brewing beat + last_seq + started_at
twin/timeline/beats.json         # committed beats (append-only)
twin/timeline/README.md          # what the timeline is, how to read it
```

Plus a **scribe agent** (a seat) whose prompt carries the writing rules. The
scribe is the "agent on the side" that produces the timeline items.

## The order

```toml
# orders/beat-scribe.toml
[order]
description = "Beat scribe: pull the event batch, brew or commit the current beat"
exec = "commands/beat-scribe.sh"
trigger = "cooldown"
interval = "5m"
timeout = "60s"
```

## The trigger script (`commands/beat-scribe.sh`)

```bash
#!/usr/bin/env bash
# beat-scribe.sh — the 5-minute brewing-beat wake.
# Pulls the event batch since the last watermark, decides whether the current
# beat commits (>=30min) or keeps brewing, and nudges the scribe to write or
# update the beat's copy. No-op when there is nothing new.
set -euo pipefail
cd "$(dirname "$0")/.."

VERDICT=$(python3 commands/beat-scribe.py 2>/dev/null || echo '{"action":"error"}')

if echo "$VERDICT" | grep -q '"action": "commit"'; then
  # The current beat has brewed long enough — commit it, start a new one.
  gc session nudge scribe "COMMIT: the beat has brewed 30 minutes. Finalize its copy in the handoff voice (first-person 'We', meaning over mechanics), then close it as a committed timeline item. A new beat is now brewing." --delivery wait-idle 2>/dev/null \
    || gc session wake scribe 2>/dev/null || true
  echo "beat-scribe: committed + new beat brewing"
elif echo "$VERDICT" | grep -q '"action": "update"'; then
  # New meaningful events landed in the current beat's window — update its copy.
  BATCH=$(echo "$VERDICT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('batch',''))")
  gc session nudge scribe "UPDATE: new events landed in the brewing beat. Read the batch ($BATCH). If it extends the current thread, revise the beat's sentence to summarise both. If it is a new thread, note it as a second sentence. Keep the handoff voice." --delivery wait-idle 2>/dev/null \
    || gc session wake scribe 2>/dev/null || true
  echo "beat-scribe: update requested"
else
  # Nothing new, or the beat is still young with no meaningful events.
  echo "beat-scribe: no-op"
fi
```

## The state machine (`commands/beat-scribe.py`)

The deterministic heart. It reads `twin/timeline/brewing.json`, pulls events
since `last_seq`, and decides the action. Ship it from
`assets/beat-scribe.template.py` and adapt the CONFIG block (the `/v0` base URL
and the commit window).

**State (`brewing.json`):**

```json
{
  "started_at": "2026-08-13T17:00:00Z",
  "last_seq": 127770,
  "events": [],
  "copy": "",
  "thread": ""
}
```

**The decision:**

1. Pull events with `after=<last_seq>` (incremental — the API supports it).
2. If no new events, and the beat is younger than the commit window → **no-op**.
3. If the beat is older than the commit window (30 min) → **commit** (finalize
   the copy, append to `beats.json`, reset `brewing.json` with a new `started_at`
   and the current `last_seq`).
4. Else, if the new batch has meaningful events (attention signals, human
   session activity, a new thread) → **update** (append the batch to the beat's
   `events`, advance `last_seq`, nudge the scribe).
5. Else → **no-op** (advance `last_seq` only, so we never re-pull the same
   events).

**Meaningful events** (what makes a batch worth a copy update):
- `attention` salience — `order.failed`, `session.crashed`, `session.stranded`.
- Human-session activity — a session with a human actor, or a `mail.sent` to the
  human.
- A new thread — an event whose `subject` differs from the beat's current
  `thread`.

## The scribe agent

The scribe is a seat (like the observer) whose only job is to write timeline
copy. Its prompt carries the writing rules from `WRAPPED-WRITING.md`:

- **First-person plural.** The beat is the being telling its own life. "We",
  never "the being".
- **Meaning over mechanics.** Say what it means, not what it did. No "745
  completed, 744 fired".
- **Name the human's exact words.** Quote Faris verbatim when he is in the batch.
- **Name the being's own concepts.** "craft bar", "Sticking Thing", "provenance
  rule", "moment of expression".
- **One flowing sentence per beat.** Human-shaped, not bulleted.
- **Honest about risk.** The beat does not flatter; it holds the truth.
- **Short sentences.** One idea per sentence. ≤20 words where possible.

The scribe reads the batch (the raw events), not surface counts. It writes the
beat's `copy` into `brewing.json`. On commit, it finalizes and the beat becomes
a permanent timeline item.

## Verification

- `gc prime scribe` renders the writing rules into the scribe's prompt.
- A real batch round-trips: events land → the scribe writes a beat sentence →
  the next batch extends it → 30 min later it commits to `beats.json`.
- `twin/timeline/beats.json` shows committed beats, each with a handoff-voice
  copy and the real events it summarises.
