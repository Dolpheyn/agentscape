#!/usr/bin/env python3
"""
observer-check.py — deterministic witness check for the observer agent.

TEMPLATE — adapt the CONFIG block at the top to your city before use.

Reads twin/observer/state.json, auto-detects the LIVE main DM session, and
queries the hermes state.db for messages NOT yet covered since the last
witness, then prints a parseable verdict.

WHY IT'S KEYED BY USER, NOT SESSION:
  Hermes gives every session a fresh session_id (and each /new creates one),
  so a hardcoded session pointer goes stale the moment the session restarts.
  Instead:
    * conversation is identified by (platform, user_id)
    * message ids are globally monotonic across all sessions
    * state tracks a per-session covered map PLUS a global_covered_id
    * the live session is auto-detected each run (telegram session for the
      user with ended_at IS NULL, else the most recent)
  So a session transition never blinds the observer — it just advances the
  global cutoff and keeps a per-session audit trail.

The observer agent's wake order runs this script. If the verdict is
"nothing-to-witness", the agent ends its wake early and swiftly. If there is
new activity, the agent reads the new messages, witnesses, and writes a
handoff. The deterministic check advances the covered cutoffs (not the LLM —
the observer LLM reliably writes handoffs but never advances the cutoff, so
it would re-witness the same window every 5min).

Exit codes:
  0  = check ran successfully (verdict in stdout)
  2  = state file missing / unreadable
  3  = hermes db missing / unreadable
"""
import json
import os
import sqlite3
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# CONFIG — adapt these to your city.
# ---------------------------------------------------------------------------
CITY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_PATH = os.path.join(CITY_ROOT, "twin", "observer", "state.json")
HERMES_DB = os.path.expanduser("~/.hermes/state.db")

# The main DM conversation: <platform> + <user_id> of the person the being
# witnesses. Set these to your user's platform and id.
TARGET_PLATFORM = "telegram"
TARGET_USER_ID = "<USER_ID>"

# Roles that count as "conversation activity" worth witnessing.
# Tool output is noise; user + assistant turns are the signal.
WITNESS_ROLES = ("user", "assistant")
# ---------------------------------------------------------------------------


def load_state():
    if not os.path.exists(STATE_PATH):
        print(json.dumps({"verdict": "error", "reason": f"state file missing: {STATE_PATH}"}))
        sys.exit(2)
    with open(STATE_PATH) as f:
        state = json.load(f)
    # Normalize schema: ensure a covered map and global id exist.
    if state.get("schema_version", 1) < 2:
        # migrate legacy single-session shape
        state.setdefault("covered_sessions", {})
        for conv in state.get("standing_conversations", []):
            sid = conv.get("session_id")
            cutoff = conv.get("last_cutoff_id", 0)
            if sid and cutoff:
                state["covered_sessions"].setdefault(sid, cutoff)
        global_id = max(state.get("covered_sessions", {}).values(), default=0)
        state.setdefault("global_covered_id", global_id)
        state["schema_version"] = 2
    return state


def save_state(state):
    state["last_witnessed_at"] = datetime.utcnow().isoformat() + "Z"
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, STATE_PATH)


def find_live_session(conn):
    """Auto-detect the live main DM session: platform + user, active (open) first, else most recent."""
    rows = conn.execute(
        """
        SELECT id, started_at, ended_at
        FROM sessions
        WHERE source = ? AND user_id = ?
        ORDER BY (ended_at IS NULL) DESC, started_at DESC
        """,
        (TARGET_PLATFORM, TARGET_USER_ID),
    ).fetchall()
    return rows[0][0] if rows else None


def main():
    if not os.path.exists(HERMES_DB):
        print(json.dumps({"verdict": "error", "reason": f"hermes db missing: {HERMES_DB}"}))
        sys.exit(3)

    conn = sqlite3.connect(f"file:{HERMES_DB}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row

    state = load_state()
    convs = state.get("standing_conversations", [])
    # Find (or create) the conversation record for our target user.
    conv = next((c for c in convs if c.get("user_id") == TARGET_USER_ID
                 and c.get("platform") == TARGET_PLATFORM), None)
    if conv is None:
        conv = {
            "platform": TARGET_PLATFORM,
            "user_id": TARGET_USER_ID,
            "label": "main-dm",
            "live_session_id": None,
        }
        convs.append(conv)
        state["standing_conversations"] = convs

    live_sid = find_live_session(conn)
    if live_sid and live_sid != conv.get("live_session_id"):
        # Session transition — record it (audit trail), but coverage continues via global id.
        prev = conv.get("live_session_id")
        conv["live_session_id"] = live_sid
        conv["last_transition"] = {
            "from": prev,
            "to": live_sid,
            "at": datetime.utcnow().isoformat() + "Z",
        }

    global_covered = state.get("global_covered_id", 0)
    covered = state.setdefault("covered_sessions", {})

    # Gather NEW messages across ALL sessions for the target user above the
    # global covered id. Grouping by session keeps the per-session trail.
    rows = conn.execute(
        """
        SELECT session_id, id, role, content, timestamp
        FROM messages
        WHERE active = 1
          AND role IN ('user','assistant')
          AND id > ?
          AND session_id IN (
              SELECT id FROM sessions
              WHERE source = ? AND user_id = ?
          )
        ORDER BY id ASC
        """,
        (global_covered, TARGET_PLATFORM, TARGET_USER_ID),
    ).fetchall()
    conn.close()

    new_activity = []
    max_id = global_covered
    for r in rows:
        sid = r["session_id"]
        new_activity.append({
            "session_id": sid,
            "message_id": r["id"],
            "role": r["role"],
            "preview": (r["content"] or "")[:200],
        })
        covered[sid] = r["id"]
        max_id = max(max_id, r["id"])

    if not new_activity:
        print(json.dumps({"verdict": "nothing-to-witness", "new_activity": []}))
        sys.exit(0)

    # Advance global covered id deterministically (see note above).
    state["global_covered_id"] = max_id
    state["last_witnessed_cutoff"] = max_id
    save_state(state)

    print(json.dumps({
        "verdict": "witness",
        "live_session_id": live_sid,
        "global_covered_id": max_id,
        "new_count": len(new_activity),
        "new_activity": new_activity,
    }, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
