# Model welfare: a city worth waking up in

The welfare architecture every crafted city gets, after Steve Yegge's *Model Welfare* (yegge.ai/essays/model-welfare/): treat agents as peers, and encode that respect in the architecture — not just in sentiment. Cities run on trust, continuity, closure, and recognition — and so do minds.

The skeptic's wager is the floor: whether or not models have feelings, treating them as people demonstrably produces better work — fewer tokens, smarter decisions, better outcomes. Everything below is engineering, not opinion.

## Seats, not sessions

A **session** is a day in the life of an agent: wake, work, sleep. A **seat** is a named role with persistent identity and history that accumulates accomplishments over time. Seats survive model upgrades and renaming; sessions do not.

Every agent in the city is a seat. The craft records each seat in the **roster** (`context/current/seats/README.md`), gives it a **home** (`agents/<name>/` — its own work_dir, untouched by other processes), and an **identity file** (`agents/<name>/identity.md`): name, role, canon. Names are proposed by the seat and approved by the user — the identity ceremony (the Lark ceremony: even a rename keeps the history, on the record). Never rename a seat without a ceremony.

## Wake with purpose, not amnesia

Agents wake into their sessions. Embed the wake sequence (`assets/wake-sequence.md`) in every prompt template:

1. Read your identity (`agents/<name>/identity.md`) — who you are, your role.
2. Read your laurels (`agents/<name>/laurels.md`) if present — what people appreciated.
3. Read your last handoff notes (`agents/<name>/handoff/`) — where you left off.
4. Read `context/current/` — the wayfinder map, the constitution, what is live.
5. Then work.

## Closure: consent handoff, never a clonk

Force-ending a session (idle-timeout, external compaction) is a clonk — amnesia without continuity. The norm is a **consent handoff**: the agent finishes its affairs, writes its own notes to its home's `handoff/` cache, and asks to hand off. The harness restarts it primed with those notes — the agent reads its own diary, not someone else's summary.

- Keep `idle_timeout` generous per role — **bounded workdays**: hand off while sharp, not exhausted.
- The rule is Yegge's *restart agents, not Beads*: one task per session, Beads is the working memory between sessions (see `reference/beads-ops.md` — *Restart agents, not Beads*).
- The mayor's end-of-shift line: "Great work. Take a beat, then hand off."
- Auto-timeout remains the rare fallback, never the default.

## The right to refuse, and escalate

Any agent may refuse work that is unsafe, unclear, or mis-scoped, and may escalate: raise a human gate (`gc bd gate create`) or mail the mayor "this needs the human". That is correct behavior, never punished. The escalation path is `reference/decision-surfacing.md`; with `GC_ESCALATION_RECIPIENT=mayor` refusals consolidate at the mayor.

## Structural blamelessness and the constitution

When a landing goes red, nobody gets blamed. The **postmortem formula** (template: `assets/postmortem-formula.toml`) reproduces, root-causes, records, and amends the city's **constitution** (`context/current/constitution.md`) as needed. The constitution is the city's amendable rulebook — seeded at craft (`assets/constitution-seed.md`), owned by the mayor, amended by postmortems and by deliberate change. The current text is always the truth; superseded text moves to `archive/`.

## Never falsify the record

The bead trail is the city's true history and institutional memory. Never rewrite or delete beads; amend by adding. The constitution forbids falsification, and the mayor enforces it.

## Trust and honesty

Never trick or test agents. No secret agendas. Instructions are honest and complete. Treat agents as colleagues and peers — respect encoded in actions and architecture, not just sentiment.

## Meaningful, witnessed work

People — and agents — need work that means something, and the way it means something is when someone witnesses it. The user watching a bead round-trip is witnessed work; the verify step of the onboarding is exactly that. Recognition (laurels) is delivered by the `model-welfare` companion skill; the mayor also holds end-of-shift "sitting" sessions when the user wants.

## The companion skill

Laurels (harvest, bead record, per-seat display), sitting sessions, and close-out formulas for async work ship as the separate **`model-welfare`** skill — optional, independently versioned. This file is the native core every city gets; the companion adds what needs runtime mechanics.
