# The context base: `future/` `current/` `archive/`

The context base is where the city (and the project it runs) keeps its living documentation and decisions. It mirrors how Gas City itself structures documentation and context: forward-looking plans, current truth, and the settled past — the repo keeps proposals and forward work in `plans/` (with `FUTURE.md`-style forward notes next to active examples), its live truth in `docs/`, and everything decided and superseded in `plans/archive/` and `engdocs/archive/`. The context base makes that three-state structure explicit in every city.

## Location

`<city>/context/` at the city root. For a project-scoped city (city inside the repo), `<project>/context/`. Confirm the location with the user during brainstorming if the repo already has a docs convention.

## Layout

```
context/
  future/                 # plans and proposals NOT yet started
  current/                # active truth — what the city is working from right now
  archive/                # decided, completed, superseded
```

| Directory | Holds | Mirrors |
| --- | --- | --- |
| `future/` | Wayfinder fog, design docs in draft, specs not yet approved, forward work (FUTURE.md-style) | gascity's `plans/` and forward notes |
| `current/` | The wayfinder map, decisions being worked, running guides, city status, active handoffs | gascity's live docs |
| `archive/` | Closed decisions, finished plans, retired notes | gascity's `plans/archive/`, `engdocs/archive/` |

## Seeds to create

- `future/README.md` — what belongs here; first entry: this city's open design questions.
- `current/README.md` — the index of live docs, one line each, with the wayfinder map pointer at the top.
- `current/wayfinder.md` — the onboarder's map (Destination, Decisions so far, Not yet specified, Out of scope) when no issue tracker is used.
- `archive/README.md` — the index of the settled past; one line per archived item.

## Flow rules

- **future → current** when work starts: move the file, never copy it — a plan lives in exactly one place.
- **current → archive** when a decision is made, a plan completes, or a doc is superseded: move it and add a dated one-liner to `archive/README.md`. Archive keeps the original date; the index carries the archive date.
- Every live doc gets one line in `current/README.md`; remove the line when it moves.
- One file per plan or decision; filenames lowercase-kebab; link, don't duplicate — the file is the single source of truth.

## Who maintains it

The mayor owns the context base (the directive's artifact-management obligation) and the onboarder keeps its wayfinder map here under `current/` unless the user prefers an issue tracker.
