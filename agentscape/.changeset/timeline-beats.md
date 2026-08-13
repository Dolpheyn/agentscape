---
"agentscape": minor
---

Add the **timeline beats** reference — the brewing-beat order that powers the Scape timeline. A cooldown order wakes every 5 minutes, pulls the real event batch, and nudges a **scribe** agent to write or update the current brewing beat's copy in the handoff voice. A beat brews ~30 minutes before it commits, so the human watches it form in real time. Ships `reference/timeline-beats.md`, `assets/beat-scribe.template.py`, and `templates/orders/beat-scribe.toml`, `templates/commands/beat-scribe.sh`, `templates/agents/scribe/prompt.template.md`.
