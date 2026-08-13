---

# Beads operations: hygiene, sizing, and import

Beads is the city's working memory between agent sessions. Operational rules keep it fast and mergeable — Steve Yegge's six best practices, condensed for a Gas City context.

## Hygiene loop (per working session)

Run once at the start of any session that touches Beads:

```bash
bd doctor --fix            # diagnose + auto-fix; handles migrations, metadata, git hooks
bd cleanup --max-age 30d   # delete issues older than 30d (city default; tighten to 2d for solo)
bd sync                    # push the store to git; fixes merge drift
```

Wire the loop as a cooldown order in `orders/bd-sweep.toml`:

```toml
[order]
description = "Beads hygiene: doctor, cleanup, sync"
exec = "scripts/bd-sweep.sh"
trigger = "cooldown"
interval = "24h"
timeout = "60s"
```

with `scripts/bd-sweep.sh`:

```bash
#!/usr/bin/env bash
# Beads hygiene loop — runs unattended on the cooldown order above.
set -euo pipefail
cd "$(dirname "$0")/.."
bd doctor --fix
bd cleanup --max-age 30d
bd sync
```

The exec script runs the loop unattended; the manual `bd doctor --fix` + `bd cleanup` + `bd sync` sequence is the fallback habit. There is no `city.health.bd-sweep` formula in the gascity pack catalog, and exec orders reject a `pool` key — the script form above is the verified default.

## Sizing — keep the working set small

Open issues should not exceed **200** (soft cap — start cleanup earlier); **500** is a hard cap. Agents sometimes grep `issues.jsonl` directly via jQuery-style filters; that breaks above ~25k tokens of working set, which is roughly 500 issues. `bd cleanup --max-age 30d` is the cheap lever; `bd cleanup --max-age 7d` is the aggressive one. Deleted issues remain in git history — never lost.

## Upgrade cadence + daily hygiene

Beads ships bug fixes fast. Run `bd upgrade` weekly. Beads handles its own migrations on upgrade; manual cleanup (`bd doctor --fix`) is rarely needed outside of merge conflicts. Conflicts on `.beads/issues.jsonl` happen — ask the agent to resolve them rather than hand-merging; the agent has the context.

## Plan outside, import in

The plan lives in the context base (`context/future/` — see `reference/context-base.md`) or in an external planning tool. The onboarder or a planning agent translates the approved plan into Beads:

1. **Epics first, issues under them** — one epic per major piece, issues under it for each concrete task.
2. **Explicit dependencies** — every issue has `blocks` / `blocked-by` edges where one blocks another. Without edges, parallelization fails.
3. **Parallelization notes** — for any two issues that can run in parallel, tag them so the sling layer can fan out.
4. **Review pass** — once filing is done, run a polish cycle: tighten titles, sharpen descriptions, validate dependencies, kill duplicates. Iterate up to **5×** on the plan, then up to **5×** on the Beads, before grinding.

The plan stays the source of truth; Beads is the execution shadow. When the plan moves (future → current → archive), re-import only the delta.

## Restart agents, not Beads

One task per session. When the task is done, the agent closes the bead, writes its handoff notes, and asks to hand off (see `reference/model-welfare.md` — *consent handoff*). The harness restarts it primed with those notes; Beads is what the new session reads first. This is Yegge's principle restated: Beads is the working memory between sessions, not the conversation inside one.

## File eagerly

For any work the agent cannot finish in **~2 minutes**, file a bead first. Code reviews file beads as they go; an inline bead per finding is the expected pattern, not a single roll-up at the end. Nudge the model to file rather than waiting for it to — it under-files by default.
