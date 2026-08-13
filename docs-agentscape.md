# agentscape

Model-invoked **wizard** skill: make your agent your wizard for a Gas City that is a being — city + wiki + gbrain. It bootstraps a new city and keeps scaping an existing one.

[SKILL.md](../../skills/engineering/agentscape/SKILL.md)

## What it does

- **Router** — orients, then routes to one of two sub-skills:
  - `/agentscape-bootstrap` — create a new city (7-step arc: orient, learn the human, design the being, craft, install the wizard directive, wire propagation + ship orient, verify and hand off).
  - `/agentscape-scape` — continually scape an existing city (`orient → inspect → propose → act → remember`).
- **The `.agentscape/` wayfinder** — the skill's working memory, kept inside the city directory. Read at session start, updated at session end. A bootstrap's wayfinder is born with the city (after `gc init`); a scape reads it first.
- **External-agent invocation** — used via an external agent (e.g. Dixon), which ships the city's **orient skill** to that agent. The orient skill is unique per city, adapted to its seats, pipeline, and stocks.
- **gbrain as a first-class memory** — the retrieval brain, wired alongside the wiki (memory organized by care).

## The two modes

| Mode | Sub-skill | When |
|---|---|---|
| **Bootstrap** | `/agentscape-bootstrap` | Create a new city. |
| **Continual scaping** | `/agentscape-scape` | Keep scaping an existing city. |

## Dependencies

- [mattpocock/skills](https://github.com/mattpocock/skills) — wayfinder, grill-me, handoff, writing-for-agents; installed with `npx skills@latest add mattpocock/skills`.
- Gas City itself (`gc`) — the runtime the skill configures.
- gbrain — the retrieval brain (optional but recommended for a being).

## Versioned

Ships from this repo; every change goes through a `.changeset/`; releases are tagged. Refresh an installed copy with `npx skills update`.
