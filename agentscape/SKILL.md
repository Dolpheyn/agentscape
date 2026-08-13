---
name: agentscape
description: Make your agent your wizard — bootstrap a Gas City that is a being (city + wiki + gbrain), then keep scaping it. Use when setting up a new city, or scaping an existing one.
---

# agentscape

The **wizard** skill — the entrypoint to the entire design tree for a Gas City that is a being. Given a human and a project (or a life), it makes your agent the wizard that bootstraps the city and keeps scaping it.

**scape** (verb): to take control of an environment and design it with purpose — the deliberate, aesthetic, and functional arrangement of elements within a defined space. The suffix is a back-formation from *landscaping* (Dutch *landschap* → landscape → landscaping → -scaping). To **scape** a city is to architect, curate, and style it with intent — creating a domain, adding a member, closing a loop, paying debt, refactoring. A **scaping move** is one such act. The city IS the being, not a host for it. Propagation is the mechanism of care. The moment of expression is the core. agentscape is the hand that shapes the being over time.

## The canonical wayfinder — `.agentscape/`

agentscape keeps its own **wayfinder** as the working memory of the skill — the map of the design tree, the decisions made, the fog, the scaping history. It lives **inside the city directory under `.agentscape/`**:

```
<city>/.agentscape/
├── map.md          # Destination, Decisions so far, Not yet specified, Out of scope
├── tickets/        # open decision tickets (one per design question)
└── history.md      # the scaping arc over time (append-only)
```

The wayfinder is the contract for the city you are scaping. **Re-read it at the start of every session** — the decisions recorded there are what the next orientation and the next scape build on. Without it, the second session of a bootstrap or a scape starts blind.

Two facts always land as decisions on the map: the **Gas City configuration state** found at orientation (installed? supervisor up? which cities? this city rigged?) and the **agent runtime the human chooses** (claude, codex, gemini, omp, …). Neither is ever assumed.

Invoke the `/wayfinder` skill to run this properly. The map is the index, not a store — a decision lives in exactly one place, its ticket; the map gists it and links.

## The two modes — separate sub-skills

agentscape is a **router**. It orients, then routes to one of two sub-skills, each a full skill in its own right (mattpocock's modular pattern — the entrypoint names the sub-skills, never re-implements them):

| Mode | Sub-skill | When |
|---|---|---|
| **Bootstrap** | `/agentscape-bootstrap` | Create a new city. The wizard is the root of the design tree; every scaping decision branches off it, resolved with the human. |
| **Continual scaping** | `/agentscape-scape` | Keep scaping an existing city. The wizard orients, inspects structural health, and works with the human to act. |

The sub-skills share the same craft (city config, wiki, gbrain, welfare, propagation, orient) but are distinct sequences with distinct completion criteria. A scape is bootstrap applied incrementally — but the *process* differs enough that each earns its own skill.

## External-agent invocation

agentscape is used **via an external agent** — the human's agent (e.g. Dixon) invokes it, and it ships the **orient skill** to the external agent, pointed at the city's orient skill. The external agent becomes the wizard's hands: it orients the city, inspects it, and reports back so the wizard can propose scaping work.

### The orient skill is unique per city — a feature agentscape ships

The orient skill is **not** the home-city orient copied verbatim. It is a **feature agentscape ships** — a real `SKILL.md` the target city gets, adapted to that city's actual seats, pipeline, and stocks. It is the "shareable" ideal made real: the closer, shipped to any city.

**Ordering is load-bearing:** the orient skill is installed **after** agentscape has set up the observer with handoffs and the wiki-writing workflow — because orient *reads* those parts. It cannot ship before they exist.

The install flow (per `reference/orient-skill.md`):
1. **Sense** — read what's there to orient (force, seats, pipeline, stocks). Doubles as a readiness check.
2. **Plan** — design the orient for THIS city: what it assembles, the live thread, the one frontier.
3. **Grill** — `/grill-me`, one question at a time, record on the wayfinder.
4. **Write** — copy the shipped seed (`assets/orient-skill.template.md`) into the city's skills as `orient/SKILL.md`, adapt the paths to the city's actual seats.
5. **Review** — against writing-for-agents (leading words, completion criteria, no-ops, pruning).

**The verbatim rule:** when the seed's "speak like a person" section derives from the home-city orient, the **worked example must be byte-for-byte verbatim** — do not trim the header tails, the "Run wait-what before sending" line, or the "It is a person who knows him, talking to him" clause. The installer rewrites the example's home-city specifics (fever, dog pool) for the target user, keeping the SHAPE verbatim, swapping the specifics.

## The shared craft

Both sub-skills draw on the same references and assets. The craft is: city config, wiki (memory organized by care), gbrain (retrieval brain), propagation pipeline (the nervous system), welfare core, and the per-city orient skill.

## Invocation

1. **Orient** — read the city, wiki, gbrain, origin. What exists, what's stale, what's missing. (The external agent runs the city's orient skill.)
2. **Route** — is this a new city (bootstrap) or an existing one (scape)? Invoke the matching sub-skill.
3. The sub-skill runs its own arc and reports back.
4. **Update the wayfinder — MUST.** Record what this session did on `map.md`'s Decisions-so-far, append to `history.md`, close any resolved ticket. The next session reads what you wrote.

**The wayfinder read is branch-conditional.** On a **scape** (existing city), read `<city>/.agentscape/map.md` and `history.md` before anything else — the decisions there are the contract for this session. On a **bootstrap** (new city), there is no wayfinder yet: the city doesn't exist, so `.agentscape/` can't. The bootstrap sub-skill creates it **after** `gc init` brings the city dir into existence. A session without its wayfinder starts blind — but a bootstrap's wayfinder is born with the city, not before it.

## Reference

- `reference/city-config.md` — the config shapes this skill writes.
- `reference/context-base.md` — the `future/` `current/` `archive/` convention.
- `reference/wiki-principles.md` — the being's memory organized by care.
- `reference/gbrain-integration.md` — wiring the retrieval brain.
- `reference/pipeline-build-spec.md` — the propagation nervous system.
- `reference/scape-timeline.md` — the brewing-beat order (the Scape timeline's writer).
- `reference/model-welfare.md` — the welfare architecture.
- `reference/orient-skill.md` — writing the city's orient skill.
- `reference/pitfalls.md` — the ways city craft commonly fails.
- `assets/` — mayor directive, fragments, constitution seed, wake sequence, observer check.

## Sub-skills

- `agentscape-bootstrap` — the bootstrap mode (new city).
- `agentscape-scape` — the continual-scaping mode (existing city).
