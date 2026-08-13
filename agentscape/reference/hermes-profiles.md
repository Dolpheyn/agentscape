# Every hermes-acp agent needs its own Hermes profile

The rule that keeps a hermes-runtime city alive: **every agent that runs on
`hermes acp` must have its own Hermes profile and a `HERMES_PROFILE` env
override.** Never let a city agent inherit the `default` profile.

## Why

The `default` Hermes profile is the human's main session (Dixon, the always-on
companion). A second session **cannot start in the default profile**. When a
city agent inherits it, the session create aborts before `creation_complete`,
the reconciler rolls the create back, and the agent never spawns. Every nudge
to it sits unclaimed forever — the work it was supposed to do strands.

This is not a design problem. It is a config omission: the agent was declared
without a profile, so it silently fell through to `default`.

## The symptom

An `on_demand` agent that never comes up despite nudges:

- `gc session list` shows **no session** for the agent, even after
  `gc session wake <name>`.
- `.gc/events.jsonl` shows a `bead.closed` for the session with
  `close_reason: "session create failed: aborted before creation_complete"`.
- The reconciler trace (`.gc/runtime/session-reconciler-trace/segments/YYYY/MM/DD/*.jsonl`)
  shows `reconciler.session.rollback_pending_create` →
  `reason_code: "pending_create_rollback"` → `outcome_code: "rollback"`.
- The ACP process, if it appears at all, has `HERMES_PROFILE=default` in its
  environment (`tr '\0' '\n' < /proc/<pid>/environ | grep HERMES_PROFILE`).

## The fix

Two parts, both required.

**1. Create the profile.** `~/.hermes/profiles/<name>/profile.yaml` — a
minimal profile with the toolsets the agent needs. Match the working agents'
shape (observer, mayor, faris-observer all have one):

```yaml
name: <name>
description: Gas City home-city <name> profile — <one line on the seat>.
default_model: anthropic/claude-sonnet-4-5
fallback_models:
  - openai/gpt-4o
toolsets:
  - terminal
  - file
  - skills
  - session_search
denied_tools:
  - sudo
  - computer-use
  - send_message
default_toolsets:
  - terminal
  - file
  - skills
  - session_search
yolo: false
safe_mode: true
```

**2. Wire the env override.** In `pack.toml`, add a `[[patches.agent]]` block
that sets `HERMES_PROFILE` for the agent. This is the same mechanism the
mayor, observer, and faris-observer use:

```toml
[[patches.agent]]
dir = ""
name = "<name>"
prompt_template = "//agents/<name>/prompt.template.md"
[patches.agent.env]
HERMES_PROFILE = "<name>"
```

Then `gc reload` so the controller picks up the new env.

## Verification

```bash
gc config show | grep -A3 'name = "<name>"'   # shows [agent.env] HERMES_PROFILE = "<name>"
gc session wake <name>                          # session comes up
gc session list | grep <name>                   # state = active
# ACP proc env carries the profile:
tr '\0' '\n' < /proc/<pid>/environ | grep HERMES_PROFILE   # HERMES_PROFILE=<name>
```

## The general rule

When you craft a city on the hermes provider, **every agent gets a profile** —
not just the mayor. The mayor's profile gating is documented in
`mayor-telegram-transport.md`; this is the same rule applied to every seat.
A city agent without a profile is a city agent that will never wake.
