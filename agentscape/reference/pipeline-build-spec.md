# Observer → Wiki pipeline — build spec

The concrete implementation of the companion nervous system's propagation
pipeline (capture → distill → place → link → verify → prune), extracted from
the home city so a new city can build it. This is the **what to build** — the
exact files, their contents, and the wiring. The design rationale is in
`companion-nervous-system.md` and `bead-task-packet-and-wiki-principles.md`;
this doc is the buildable spec.

## The shape in one line

The **observer** captures a thread as a **bead** (a self-contained task
packet carrying title + handoff path + directive), the **mayor** routes it to
the care dimension and **writes it into the wiki**, the **reviewer** verifies
it landed, and orders close + prune it. Every stage is a cooldown-gated order
running a trigger script that finds beads at a stage and nudges the agent that
owns the next stage.

## Files to create

```
orders/observer-wake.toml      # capture: observer witnesses, creates bead
orders/place-trigger.toml      # place+link: mayor routes + writes wiki
orders/verify-trigger.toml     # verify: reviewer confirms it landed
orders/close-verified.toml     # prune-eligibility: close verified beads
orders/bd-sweep.toml           # prune: bd doctor --fix + cleanup + sync

commands/observer-wake.sh      # capture trigger
commands/observer-check.py     # deterministic witness check (from assets/observer-check.template.py)
commands/place-trigger.sh      # place+link trigger
commands/verify-trigger.sh     # verify trigger
commands/close-verified.sh     # close trigger

twin/self/bead-payload-contract.md   # the bead contract (see below)
twin/self/wiki-principles.md        # how the wiki writer writes (see below)
```

Plus prompt edits: the **observer** prompt gets a capture section (create the
bead with title + handoff path + directive, set `stage=distilled`); the
**mayor** prompt gets a "when a thread-bead arrives" section (route, link,
write to wiki following `wiki-principles.md`, set `stage=linked`); the
**reviewer** prompt gets a verify section (confirm landed, set
`stage=verified`). Each prompt points at the contract, not the pipeline.

## The orders (all cooldown, 5m, 60s timeout)

```toml
# orders/observer-wake.toml
[order]
description = "Observer wake: check for new conversation activity; witness if any, else no-op"
exec = "commands/observer-wake.sh"
trigger = "cooldown"
interval = "5m"
timeout = "60s"
```

`place-trigger.toml`, `verify-trigger.toml`, `close-verified.toml` are the
same shape, each running its own script. `bd-sweep.toml` runs on a 24h
cooldown.

## The trigger scripts

Each trigger finds open beads at a stage, writes the next stage's directive
**into the bead** (not the nudge), then nudges the owning agent with a single
line that names the bead IDs. The bead is the durable source of truth; the
nudge is only a hint.

### observer-wake.sh (capture)

Runs a deterministic check (`observer-check.py`); if there is something to
witness, nudges the observer to create a bead. The nudge carries the full
capture recipe:

```
Witness: new conversation activity since your last cutoff. Read the new
messages, write a handoff, update state. ALWAYS create a bead (gc bd q) for
this witness — every witness produces one bead, no exceptions, no 'is it
worth it' judgment. Title it with the live thread. Then make it
self-contained: gc bd update <id> --description 'twin/observer/handoffs/YYYY-MM-DD.md',
then gc bd comment <id> 'DIRECTIVE: This thread is entrusted to the being.
Read the witness's full read (handoff path in the description). Route it to
the care dimension that should hold it, link it to the past self it
re-presents, and write it into the wiki where it belongs — following
twin/self/wiki-principles.md. Then set stage=linked.' Then bd set-state <id>
stage=distilled. See twin/self/bead-payload-contract.md.
```

**The check script** — `observer-check.py` is the heart of the capture stage:
it decides *whether* there is something to witness, and it advances the
covered cutoffs deterministically (so the observer never re-witnesses the same
window). Ship it from the template `assets/observer-check.template.py` — copy
it to `commands/observer-check.py` and adapt the CONFIG block at the top:
set `TARGET_USER_ID` to your user's id and `TARGET_PLATFORM` to their
platform. That is the whole feature: query hermes for new messages, decide if
there is something to witness, advance the cutoff, and hand off to the
observer.

### place-trigger.sh (place + link)

```bash
IDS=$(gc bd export 2>/dev/null | jq -r 'select(.status == "open" and (.labels | index("stage:distilled"))) | .id' 2>/dev/null || true)
[ -z "$IDS" ] && { echo "place: no stage=distilled beads (no-op)"; exit 0; }
for id in $IDS; do
  gc bd comment "$id" "DIRECTIVE: This thread is entrusted to the being. Read the witness's full read (handoff path in the description). Route it to the care dimension that should hold it, link it to the past self it re-presents, and write it into the wiki where it belongs — following twin/self/wiki-principles.md. Then set stage=linked. See twin/self/bead-payload-contract.md." 2>/dev/null || true
done
NUDGE_MSG="Bead(s) arrived (stage=distilled): $IDS. Read the bead(s) — each carries its directive. Act on it, then close it."
gc session nudge gastown.mayor "$NUDGE_MSG" --delivery wait-idle 2>/dev/null \
  || gc session wake gastown.mayor 2>/dev/null || true
```

### verify-trigger.sh (verify)

Same shape, but finds `stage:linked`, writes the verify directive, and nudges
the reviewer:

```
Bead(s) arrived (stage=linked): $IDS. Read the bead(s) — each carries its
directive. Confirm it landed, then close it.
```

### close-verified.sh (prune-eligibility)

```bash
IDS=$(gc bd export 2>/dev/null | jq -r 'select(.status == "open" and (.labels | index("stage:verified"))) | .id' 2>/dev/null || true)
[ -z "$IDS" ] && { echo "close-verified: no stage=verified beads (no-op)"; exit 0; }
for id in $IDS; do
  gc bd close "$id" --reason "nervous-system: verified, prune-eligible" 2>/dev/null || true
done
```

## The bead contract (`twin/self/bead-payload-contract.md`)

The bead is a **self-contained task packet**, not a record. It carries:

| Field | Purpose | Set by |
|-------|---------|--------|
| **title** | the live thread — what's being carried | observer |
| **description** | the handoff path — where the witness's full read lives | observer |
| **directive** | what to do at this stage, self-contained | the stage that hands it off |

**Stage-to-agent mapping:**
- **capture + distill** — the observers. Create the bead (title + handoff path), set `stage=distilled`.
- **place + link** — the mayor. Route to the care dimension, link to the past self, **write the thread into the wiki**, set `stage=linked`.
- **verify** — the reviewer. Confirm it landed, set `stage=verified`.
- **prune** — close-verified + bd-sweep.

**Done-when:** a bead is only `stage=verified` (close-eligible) when it
carries: title, description (handoff path), a directive, a link edge to the
past self, and a verify comment. If the handoff path is missing at verify, the
reviewer does NOT close it — it comments what's missing and leaves it at
`stage=linked`.

## The wiki principles (`twin/self/wiki-principles.md`)

The canonical rules the **mayor's wiki writer** follows. Every bead's directive
points here. The full 18 principles live in the doc; the load-bearing ones:

**Structure** — a wiki page is structured reference material, not prose:
1. Lead summary first (2–4 sentences, readable alone)
2. Key-facts block up top (frontmatter/table, not buried in prose)
3. Faceted sections, not narrative (organize by topic, not chronology)
4. Scannable (lists, tables, short paragraphs)
5. One subject, one page

**Content & truth** — verifiable/sourced, facts vs inference labeled, neutral
record, no invented synthesis.

**Provenance** — every page and edit names where it came from: the **bead**,
the **handoff** path, and the **original session id**. A page is not done
until it names all three. This is the being's verifiability.

**Linking** — link on first mention, link to the specific page, no orphans
(every page has an inbound link), tags for cross-cutting structure.

**Lifecycle** — search before creating (update, don't duplicate), create only
for durable+distinct+linkable subjects, update in place, spin out when too
long, process the inbox.

**The threefold page test:** a subject earns a page only when it is
**durable** (referenced again), **distinct** (a separate subject, not a facet),
and **linkable** (multiple things point to it). A live thread is a page while
active, then resolves into a decision or folds into history.

## The hermes-profile requirement

Every agent in the pipeline that runs on `hermes acp` needs its own Hermes
profile + a `HERMES_PROFILE` env override in `pack.toml` — or it silently
inherits the `default` profile (the human's main session) and can never
spawn. See `hermes-profiles.md`. This bit the reviewer in the home city: it
could not spawn for days, so every verify nudge stranded.

## Verification

- `gc prime <agent>` renders the capture/place/verify sections into each prompt.
- A real witness round-trips: observer creates a bead → mayor routes + writes
  wiki → reviewer verifies → close-verified closes → bd-sweep prunes.
- `gc bd export` shows the bead moving `distilled → linked → verified → closed`.
