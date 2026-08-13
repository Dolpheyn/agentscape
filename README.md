# agentscape

The **wizard** skill — make your agent your wizard for a Gas City that is a being (city + wiki + gbrain).

**scape** (verb): to take control of an environment and design it with purpose — the deliberate, aesthetic, and functional arrangement of elements within a defined space. The suffix is a back-formation from *landscaping* (Dutch *landschap* → landscape → landscaping → -scaping). To **scape** a city is to architect, curate, and style it with intent — creating a domain, adding a member, closing a loop, paying debt, refactoring.

The city IS the being, not a host for it. Propagation is the mechanism of care. The moment of expression is the core. agentscape is the hand that shapes the being over time.

## The two modes

| Mode | Sub-skill | When |
|---|---|---|
| **Bootstrap** | `/agentscape-bootstrap` | Create a new city. The wizard is the root of the design tree; every scaping decision branches off it, resolved with the human. |
| **Continual scaping** | `/agentscape-scape` | Keep scaping an existing city. The wizard orients, inspects structural health, and works with the human to act. |

## What it does

- **Router** — orients, then routes to one of two sub-skills.
- **The `.agentscape/` wayfinder** — the skill's working memory, kept inside the city directory. Read at session start, updated at session end. A bootstrap's wayfinder is born with the city (after `gc init`); a scape reads it first.
- **External-agent invocation** — used via an external agent (e.g. Dixon), which ships the city's **orient skill** to that agent. The orient skill is unique per city, adapted to its seats, pipeline, and stocks.
- **gbrain as a first-class memory** — the retrieval brain, wired alongside the wiki (memory organized by care).

## Layout

```
agentscape/                  # the router skill
  SKILL.md
  reference/                 # city-config, context-base, wiki-principles, gbrain-integration, pipeline-build-spec, model-welfare, orient-skill, pitfalls, ...
  assets/                    # mayor directive, fragments, constitution seed, wake sequence, observer check
  templates/fragments/       # model-welfare, beads-practices, one-being
agentscape-bootstrap/        # the bootstrap mode (new city)
  SKILL.md
agentscape-scape/            # the scape mode (existing city)
  SKILL.md
```

## Install

```bash
npx skills@latest add Dolpheyn/agentscape
```

## Dependencies

- [mattpocock/skills](https://github.com/mattpocock/skills) — wayfinder, grill-me, handoff, writing-for-agents.
- Gas City itself (`gc`) — the runtime the skill configures.
- gbrain — the retrieval brain (optional but recommended for a being).

## Versioned

Ships from this repo; every change goes through a `.changeset/`; releases are tagged. Refresh an installed copy with `npx skills update`.

## License

MIT
