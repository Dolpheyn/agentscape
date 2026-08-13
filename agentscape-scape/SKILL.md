---
name: agentscape-scape
description: Continually scape an existing Gas City that is a being — orient, inspect structural health, and work with the human to act (new wiki domain, new city member, close a loop, pay debt, refactor). Use when scaping an existing city. Invoked by /agentscape.
---

# agentscape-scape

The **continual scaping** mode of `/agentscape`. The wizard stays in the city, keeps orienting, keeps inspecting structural health, and works with the human to act on what it finds. The city is a living thing; this is the hand that shapes it over time.

## The loop

```
orient → inspect → propose → act → remember
```

- **Orient** — read the city, wiki, gbrain, origin. What exists, what's stale, what's missing.
- **Inspect** — detect structural-health signals.
- **Propose** — work with the human to decide the scaping move.
- **Act** — do the scaping work.
- **Remember** — propagate into wiki + gbrain so the next orientation sees it.

## Steps

### 1. Orient

Read the current state before anything else:

- **The wayfinder — MUST.** Read `<city>/.agentscape/map.md` and `history.md` before anything else. The decisions recorded there are the contract for this scape. If `.agentscape/` is missing, stop and create it (per the router skill's `.agentscape/` directive) before scaping — a scape without its wayfinder starts blind.
- **The city** — `gc status`, `gc doctor`. Is it up? Healthy?
- **The wiki** — what domains exist? What's stale? What's orphaned?
- **The brain** — is gbrain wired? What's salient? What's anomalous?
- **The origin** — read it first if it exists. Interpret state through the force, not as a status dump.
- **The pipeline** — is the nervous system firing? Any stuck beads?
- **The stocks** — which stock is bleeding? The one flow to move.

The external agent runs the city's orient skill for this. **Completion criterion:** you can state the city's health, what the wiki and gbrain hold, whether the pipeline is firing, which stock is bleeding, and you have re-read the `.agentscape/` wayfinder.

### 2. Inspect

Detect structural-health signals. The wizard sees when:

- **A refactor is needed** — structure is degrading. Duplicated domains, sprawl, orphaned pages, a wiki that reads like prose instead of reference.
- **A debt needs to be paid** — a shortcut taken, now costing. A config hack, a skipped step, a workaround that became permanent.
- **A loop is not closed** — a thread started but never resolved. An open bead, a dropped handoff, a decision never recorded.
- **An issue is showing up** — a failure pattern emerging. A recurring error, a stuck bead, a part that keeps breaking.
- **An opportunity exists** — a new domain or city member the city needs. A workflow the human does by hand that should become a formula; a seat the city lacks.

**Completion criterion:** the inspect findings are recorded as proposed scaping moves, each with evidence (not plausible — verified).

### 3. Propose

Work with the human to decide the scaping move. Present the findings as a short plan; invoke `/grill-me` for any open decision. The moves are the same craft as bootstrap, applied incrementally:

- **New wiki domain** — a subject earns a page when it is durable, distinct, and linkable.
- **New city member** — a new agent/seat when an opportunity is found.
- **Close the loop** — resolve the open bead, record the decision, finish the handoff.
- **Pay the debt** — fix the shortcut, do the skipped step.
- **Refactor** — restructure the degrading part.

**Completion criterion:** the human approved the scaping move(s), and each is recorded on the wayfinder.

### 4. Act

Do the scaping work. Each move is a scape:

- **New wiki domain** — create the page per `reference/wiki-principles.md` (lead summary, key-facts, faceted sections, provenance, linking).
- **New city member** — add the agent/seat per `reference/city-config.md` + `reference/model-welfare.md`.
- **Close the loop** — resolve the bead, record the decision, finish the handoff.
- **Pay the debt** — fix the shortcut, do the skipped step.
- **Refactor** — restructure the degrading part.

Validate as you go with `gc config show` and `gc doctor`.

**Completion criterion:** the scaping move is done and verified — the wiki page exists and is linked, the member is live, the loop is closed, the debt is paid, the refactor passes `gc doctor`.

### 5. Remember

Propagate the change into wiki + gbrain so the next orientation sees it. **MUST** update the `.agentscape/` wayfinder: record what was scaped on `map.md`'s Decisions-so-far, append the scape to `history.md`, and close any decision ticket the scape resolved. Update the stocks.

**Completion criterion:** the change is in the wiki and gbrain, the `.agentscape/` wayfinder records the scape (map + history + closed tickets), and the stocks are updated.

## Reference

- `reference/wiki-principles.md` — the being's memory organized by care.
- `reference/city-config.md` — the config shapes this skill writes.
- `reference/model-welfare.md` — the welfare architecture.
- `reference/gbrain-integration.md` — wiring the retrieval brain.
- `reference/pitfalls.md` — the ways city craft commonly fails.
- The city's own orient skill (for step 1).
