#!/usr/bin/env python3
"""beat-scribe.py — the deterministic heart of the brewing-beat order.

Pulls the real event batch since the last watermark, decides whether the
current beat commits (>=30min) or keeps brewing, and prints a verdict the
trigger script acts on. This script is DETERMINISTIC — it never writes copy.
The scribe agent writes the copy; this script only decides the action.

Verdicts:
  {"action": "commit"}            — beat brewed long enough, finalize + reset
  {"action": "update", "batch": "..."} — new meaningful events, nudge scribe
  {"action": "noop"}              — nothing new, or beat still young
"""
import json, os, sys, time, urllib.request
from datetime import datetime, timezone

# ---- CONFIG: adapt per city -------------------------------------------
BASE = os.environ.get("GC_SUPERVISOR", "http://127.0.0.1:8372")
CITY = os.environ.get("GC_CITY", "home-city")
COMMIT_WINDOW_MIN = 30          # a beat brews this long before committing
STATE_PATH = "twin/scape/brewing.json"
BEATS_PATH = "twin/scape/beats.json"
# ------------------------------------------------------------------------

def get(path, **params):
    q = "&".join(f"{k}={v}" for k, v in params.items() if v)
    url = f"{BASE}/v0/city/{CITY}{path}" + (f"?{q}" if q else "")
    with urllib.request.urlopen(url, timeout=20) as r:
        return json.load(r)

def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH) as f:
            return json.load(f)
    return {"started_at": datetime.now(timezone.utc).isoformat(),
            "last_pulled_at": None, "events": [], "copy": "", "thread": ""}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)

def is_meaningful(ev):
    """What makes a batch worth a copy update."""
    t = ev.get("type", "")
    if t in ("order.failed", "session.crashed", "session.stranded"):
        return True                      # attention salience
    if t == "mail.sent":
        return True                      # touched the human
    if t.startswith("session.") and ev.get("actor", "").startswith("human"):
        return True                      # human session activity
    return False

def main():
    state = load_state()
    # Incremental pull since the last watermark (time-based; the API's `since`
    # is a duration, `after` is ignored). First run pulls the last 5 minutes.
    since = "5m"
    if state.get("last_pulled_at"):
        try:
            last = datetime.fromisoformat(state["last_pulled_at"].replace("Z", "+00:00"))
            delta = datetime.now(timezone.utc) - last
            since = f"{max(1, int(delta.total_seconds() // 60))}m"
        except Exception:
            since = "5m"
    try:
        d = get("/events", since=since, limit=500)
        events = d.get("items", [])
    except Exception as e:
        print(json.dumps({"action": "noop", "reason": f"pull failed: {e}"}))
        return

    # Advance the watermark regardless, so we never re-pull the same window.
    state["last_pulled_at"] = datetime.now(timezone.utc).isoformat()

    if not events:
        save_state(state)
        print(json.dumps({"action": "noop", "reason": "no new events"}))
        return

    # How long has the current beat been brewing?
    try:
        started = datetime.fromisoformat(state["started_at"].replace("Z", "+00:00"))
        age_min = (datetime.now(timezone.utc) - started).total_seconds() / 60
    except Exception:
        age_min = 0

    if age_min >= COMMIT_WINDOW_MIN:
        # Commit the current beat, start a new one.
        if state.get("copy"):
            beats = []
            if os.path.exists(BEATS_PATH):
                with open(BEATS_PATH) as f:
                    beats = json.load(f)
            beats.append({"committed_at": datetime.now(timezone.utc).isoformat(),
                          "copy": state["copy"], "events": state["events"]})
            with open(BEATS_PATH, "w") as f:
                json.dump(beats, f, indent=2)
        state["started_at"] = datetime.now(timezone.utc).isoformat()
        state["events"] = []
        state["copy"] = ""
        state["thread"] = ""
        save_state(state)
        print(json.dumps({"action": "commit"}))
        return

    # Still brewing. Is the new batch meaningful?
    meaningful = [e for e in events if is_meaningful(e)]
    if meaningful:
        state["events"].extend(events)
        save_state(state)
        batch = ", ".join(f"{e.get('type')}·{e.get('subject','')}" for e in meaningful[:5])
        print(json.dumps({"action": "update", "batch": batch}))
        return

    # Nothing meaningful — just advance the watermark.
    save_state(state)
    print(json.dumps({"action": "noop", "reason": "no meaningful events"}))

if __name__ == "__main__":
    main()
