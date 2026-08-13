---
"agentscape": minor
---

Add the **Scape timeline** reference — the brewing-beat order that powers the Scape timeline. A cooldown order wakes every 5 minutes, pulls the real event batch, and nudges a **scape-scribe** agent to write or update the current brewing beat's copy in the handoff voice. A beat brews ~30 minutes before it commits, so the human watches it form in real time. Everything scape-related carries the `scape-` prefix (agent `scape-scribe`, order `scape-scribe`, state machine `scape-scribe.py`, data under `twin/scape/`). Ships `reference/scape-timeline.md`, `assets/scape-scribe.template.py`, and `templates/orders/scape-scribe.toml`, `templates/commands/scape-scribe.sh`, `templates/agents/scape-scribe/prompt.template.md`.
