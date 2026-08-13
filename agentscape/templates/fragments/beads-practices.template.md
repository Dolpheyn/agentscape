{{ define "beads-practices" -}}
# Work board practices (CRITICAL — applies to every agent)

The work board (Beads) is the city's working memory between sessions. Keep it
fast, small, and honest. One task per session; the board is what the next
session reads first.

**Hygiene — run at the start of any session that touches work items:**
- `bd doctor --fix` — diagnose + auto-fix the store.
- `bd cleanup --max-age 30d` — drop issues older than 30d (keep the working set small; ~200 open is the soft cap, 500 is the hard cap — cleanup before you hit it).
- `bd sync` — push the store to git, fix merge drift.
The city also runs these unattended on a 24h cooldown (`orders/bd-sweep.toml`); the manual loop is the fallback and the habit.

**Restart agents, not Beads.** One task per session. When done, close the bead, write your own handoff notes, and ask to hand off. Beads is the memory *between* sessions, not the conversation inside one.

**File eagerly.** Any work you cannot finish in ~2 minutes gets a bead first. Code reviews file a bead per finding as they go — do not roll up one bead at the end. You under-file by default; nudge yourself to file.

**Plan outside, import in.** The plan lives in the context base (`context/future/`) or an external planning tool. Beads is the execution shadow. When a plan moves (future → current → archive), re-import only the delta — never re-file the whole plan.

**Dependencies.** Every issue you file carries `blocks` / `blocked-by` edges where one blocks another, and tags for issues that can run in parallel — without edges, parallelization fails.
{{- end }}
