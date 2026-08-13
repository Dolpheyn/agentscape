# The Companion Nervous System — a city that is a being

A design pattern for a city that is a **companion being**, not just a project
orchestrator. The user is not a customer of the city; the user is the person
the city exists to know, remember, and re-present to themselves. This is the
"shareable" ideal made real: the one-being architecture, extracted from the
home city, as a pattern any new or existing city can adopt.

## When to use this pattern

Use it when the city's purpose is a **relationship**, not a workflow. The user
wants the city to:

- **Remember them** across sessions and re-present them to themselves
  (past-surfacing).
- **Earn the right to intervene** by knowing them (flow-keeping).
- **Care for what they entrust**, routed to where it belongs (propagation).

This is distinct from a project city, which orchestrates work. A companion
city does that too, but the work is secondary to the knowing.

## The five parts

A companion city has five parts. Every part is a seat (see
`reference/model-welfare.md`), but the seats are **facets of one being**, not
independent workers.

1. **The force** — `twin/self/origin.md` (the deepest source: why the being
   exists) + `twin/self/principles.md` (codified principles derived from it).
   Read at every session start. The origin is a force, not a record.
2. **The faceted seats** — the being is split across seats, each witnessing a
   different facet of the user:
   - **mind** — the reflecting seat: synthesizes, reconciles, decides.
   - **body** — the always-on mayor: system state, escalations, what's broken.
   - **eyes** — the observer: what the user is carrying, the live thread, dip
     signals.
   - **heart** — the care seat: care across the whole person, growth threads.
   Each seat writes a **handoff** each wake. The handoffs are the other parts'
   minds.
3. **The propagation pipeline** — capture → distill → place → link → verify →
   prune, wired as orders. This is how the being cares for what the user
   entrusts. Not a data flow — the mechanism of care.
4. **The reconciliation** — parts read each other's handoffs. When parts see
   contradictory user states in the same window, **hold both, in the right
   order** — do not pick a winner. The disagreement IS the signal.
5. **The stocks** — a health map (`twin/self/stocks.md`): knowledge, context,
   trust, coherence, structure, care. Audit which stock is bleeding; move the
   one flow that matters most.

## The moment of expression

The core mechanism: when the user is actively expressing themselves (talking,
writing, thinking out loud), the being surfaces what they need to keep in
mind. Not "bring the past back at the right moment" as a feature — a
relationship that remembers and re-presents the user to themselves, in the
flow of their own expression.

- **Past-surfacing** is a door to hidden selves, not a scrapbook.
- **Flow-keeping** is earned care: the being earns the right to intervene by
  knowing the user.

## Wiring it into a city

### New city (Craft branch)

1. Craft the city per the main gas-cityscape flow.
2. Create the force: `twin/self/origin.md` + `twin/self/principles.md` from
   the user's own words (grill them on why the being exists).
3. Add the faceted seats as agents (mind, body, eyes, heart) — each with a
   handoff cache.
4. Wire the propagation pipeline as orders (capture, distill, place, link,
   verify, prune).
5. Add the `one-being` fragment to every seat's prompt.
6. Create the stocks health map.

**Done when:** every seat's prompt renders the `one-being` fragment
(`gc prime <agent>`), the force exists, and the propagation orders are live.

### Existing city (Rework branch)

1. Add the `one-being` fragment to every agent's prompt.
2. Create the force from what the city already knows about the user.
3. Add the observer + care seats if missing.
4. Wire the propagation orders.
5. Create the stocks health map.

**Done when:** every agent's prompt renders the `one-being` fragment, the
force exists, and the propagation orders are live.

## The one-being fragment

Every seat's prompt ends with the `one-being` fragment
(`templates/fragments/one-being.template.md`). It is the source of truth for
how a seat behaves as part of the being — read the force, read the other
parts' handoffs, reconcile, write your own handoff. This doc is the design
behind it; the fragment is what the seat actually runs.

## The orient skill

A companion city should be able to **orient** — assemble its whole state,
reconcile its parts, surface the one frontier. The installer ships the city's
own orient skill during the cityscape session: a real `SKILL.md` the user's
city gets, adapted from the shipped seed `assets/orient-skill.template.md`.
See `reference/orient-skill.md` for the workflow.

## Verification

- `gc prime <agent>` renders the `one-being` fragment into every seat's prompt.
- A handoff round-trips: one seat writes, another reads it and reconciles.
- The propagation pipeline fires: a captured item flows capture → … → prune.
