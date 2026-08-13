---
name: agentscape-bootstrap
description: Bootstrap a new Gas City that is a being — city + wiki + gbrain, with the observer, propagation pipeline, welfare core, and per-city orient skill. Use when creating a new city from scratch. Invoked by /agentscape.
---

# agentscape-bootstrap

The **bootstrap** mode of `/agentscape`. Create a new Gas City that is a being — not a host for a being, but the being itself. The wizard is the root of the design tree; every scaping decision branches off it, resolved with the human (grilling, not guessing).

## Branches

- **Craft** — a new city for a project or a life.
- **Resume** — continue a bootstrap left mid-flight.

Pick the branch from what orientation finds; the steps are the same arc, and a step already done is verified, not repeated.

## Steps

### 1. Orient

Load the current state before anything else:

- **Is Gas City installed and configured?** — `which gc`; registered cities — `~/.gc/cities.toml`; supervisor up — `~/.gc/supervisor.log` and `gc status`.
- **The project** — is it a git repo? Already a rig or a city? `city.toml`, `pack.toml`, `.gc/`, `.beads/`?
- **Your wayfinder** — on a **resume**, **MUST** read `<city>/.agentscape/map.md` and `history.md` before anything else. On a **fresh craft**, there is no wayfinder yet — the city doesn't exist, so `.agentscape/` can't. It is created in step 4, **after** `gc init` brings the city dir into existence.
- **Dependencies** — are the skills this skill runs on installed? (wayfinder, grilling, handoff, writing-for-agents, orient.) Missing any → install.
- **Is this skill current?** — compare against the latest tag of the canonical repo.
- **Beads operational state** — `bd doctor --fix` output, open-issue count, last `bd sync` time. The store's hygiene is part of orient, not an afterthought. See `reference/beads-ops.md`.

**Completion criterion:** from evidence, you can state whether Gas City is installed, what exists for this project, whether the dependency set is complete, and which branch you are on. If this is a resume, you have re-read the `.agentscape/` wayfinder.

### 2. Learn the human

Find out, by grilling rather than guessing:
- **Agent runtime** — ask directly. Which runtime should the city run on — claude, codex, gemini, omp, …? Check which CLIs exist (`which claude codex gemini omp`), then confirm the human's choice and record it as a decision. The city's `[workspace] provider` and each agent's `provider` come from it.
- **Skills available** — check `~/.agents/skills/` and the project's `.agents/skills/`. Which mattpocock skills (wayfinder, grill-me, handoff, writing-for-agents) and which domain skills apply. This skill runs on the mattpocock set, so if any is missing, install the whole set from `github.com/mattpocock/skills` — non-interactively: `npx skills@latest add mattpocock/skills --skill wayfinder grill-me handoff writing-for-agents setup-matt-pocock-skills -y` — then run `/setup-matt-pocock-skills` once per repo. Record the install as a decision.
- **Workflows / life** — what does the human produce, and what do they do by hand today that should become formulas and orders?
- **Preferences** — interactive vs autonomous decisions, where artifacts land, how they want to be reached (email, live sessions), which pack methodology fits.
- **Welfare preferences** — how the city should treat its agents: laurels yes/no, sitting sessions, and whether to also install the optional `model-welfare` companion skill.

Invoke `/grill-me` — one question at a time, record each answer as a decision on the wayfinder. Do not assume a preference you did not elicit.

**Completion criterion:** every question the human cares about is answered and recorded, or is a named decision ticket. No guessed preferences.

### 3. Design the being

Design the city to be the being. Invoke `/design-thinking` to run the craft as a graph: name the shapes (workflows, beads, seats), draw the happy path (how work flows from creation → sling → claim → execute → close), annotate where it breaks (agent death, missing worker, config error), and name what each agent needs to exist (provider, prompt, identity, pack imports, fragments). Design the propagation of every agent-behavioral directive as **one fragment file reaching every seat** — not N copies in N prompts. A fragment lives in `template-fragments/<name>.template.md` and each agent's `prompt.template.md` invokes it with an explicit `{{ template "<name>" . }}` call. Write the directive once, reference it everywhere.

- **Pack imports** — builtins `core` (mechanical housekeeping orders: gate sweep, orphan sweep, human-gate notify) and `bd` (Dolt bead store) are the floor; add the `gascity` build pack for software-delivery workflows (`build-basic`), a methodology pack (bmad, compound-engineering, superpowers, gstack) if the human wants one, and the `gastown` pack only if they want the Gastown role set. Import shapes in `reference/city-config.md`.
- **Beads hygiene loop** — wire `orders/bd-sweep.toml` (cooldown 24h, exec script running `bd doctor --fix` + `bd cleanup` + `bd sync`) so the loop runs unattended; details and the script in `reference/beads-ops.md`.
- **Agents** — the always-on **mayor** (the human's agent — required) plus the role workers each workflow needs. Map every role to a harness the human has.
- **Formulas and orders** — the methods the city runs (review, build, migration…) and what triggers them (cooldown, cron, event, manual).
- **Rigs** — which projects are registered, with which prefixes.
- **Context base** — the `future/`, `current/`, `archive/` layout (`reference/context-base.md`).
- **Wiki** — the being's memory organized by care. Domains, provenance, linking (`reference/wiki-principles.md`).
- **gbrain** — the retrieval brain. Wire it as a first-class memory, not an afterthought (`reference/gbrain-integration.md`).
- **Propagation pipeline** — the nervous system: capture → distill → place → link → verify → prune (`reference/pipeline-build-spec.md`).
- **Decision surfacing** — who mails whom, and how the human is reached (`reference/decision-surfacing.md`).
- **Model welfare** — every city is built with the native welfare core (`reference/model-welfare.md`): seats and roster, the identity ceremony, the wake sequence, consent handoffs with generous idle timeouts, the right to refuse and escalate, structural blamelessness and the constitution, never falsify the record, trust, witnessed work. Optionally wire the `model-welfare` companion skill for laurels and close-out formulas.

Present the design as a short plan and get the human's approval before crafting. Invoke `/grill-me` for any open design question.

**Completion criterion:** the design is written on the wayfinder, covers every workflow, and the human approved it.

### 4. Craft the city

Build per the approved design:

- `gc init <city-dir>` (or `gc init` inside the project dir for a workspace-scoped city), then `gc start`.
- **Create the wayfinder — MUST, immediately after `gc init`.** The city dir now exists; create `<city>/.agentscape/` with `map.md` (Destination, Decisions so far, Not yet specified, Out of scope), `tickets/`, and `history.md` (per the router skill's `.agentscape/` directive). Record the two always-land decisions: the **Gas City configuration state** found at orientation and the **agent runtime the human chose**. The wayfinder is born with the city — it is the contract every later scape reads.
- `city.toml` — `[workspace]` (name, provider), `[providers.<name>]`, `[[rigs]]` (name, prefix, default_branch), `[daemon]` options.
- `pack.toml` — pack name, `schema = 2`, `[imports.*]` for core, bd, and the chosen packs; `[[named_session]]` declaring the mayor with `mode = "always"`.
- `agents/<name>/agent.toml` plus `prompt.template.md` for each role — the mayor last, from step 5. **On the hermes provider, every agent also gets its own Hermes profile** (`~/.hermes/profiles/<name>/profile.yaml`) and a `[[patches.agent]]` env override `HERMES_PROFILE = "<name>"` in `pack.toml` — an agent that inherits the `default` profile (the human's main session) can never spawn. See `reference/hermes-profiles.md`.
- **Fragments** — every agent-behavioral directive ships as one fragment file, copied from the skill's stored templates into `template-fragments/<name>.template.md` (the `{{ define "<name>" }}`…`{{ end }}` body is already written), and each agent's `prompt.template.md` ends with the explicit call `{{ template "<name>" . }}`. Start from `templates/fragments/model-welfare.template.md` and `templates/fragments/beads-practices.template.md` — copy, don't rewrite; adapt names and details to the city. If the city is a **companion being** (a relationship, not a workflow), also copy `templates/fragments/one-being.template.md` into every seat's prompt — see `reference/companion-nervous-system.md`. The prompt renderer loads only `*.template.md` from `template-fragments/` (a `.fragment.md` suffix is silently skipped), so keep the shipped filename. One source of truth, referenced by every seat. Verify with `gc prime <agent>` that the fragment text renders into every prompt before moving on.
- `formulas/` and `orders/` for the workflows the design calls for. If the city is a **companion being**, build the observer → wiki propagation pipeline per `reference/pipeline-build-spec.md` — the orders, trigger scripts, bead contract, and wiki-principles that make capture → distill → place → link → verify → prune work end-to-end.
- The **context base** — create `future/`, `current/`, `archive/` with the seed files from `reference/context-base.md`.
- The **wiki** — seed the domains, provenance, linking (`reference/wiki-principles.md`).
- The **gbrain integration** — wire the brain (`reference/gbrain-integration.md`).
- Register rigs under `<city>/rigs/<rig-name>` per the gc-rigs convention — ask the human before choosing a location if they did not specify one.
- The **welfare core** — every city gets it (`reference/model-welfare.md`): the seat roster (`context/current/seats/`), the identity ceremony (each agent proposes its name, the human approves), the wake sequence (`assets/wake-sequence.md`) embedded in every prompt template, each agent's home (`agents/<name>/` — its own `identity.md` and `handoff/` cache, no other process touches it), a per-role `idle_timeout` (bounded workdays), and the constitution (`context/current/constitution.md`, seeded from `assets/constitution-seed.md`) with the postmortem formula (`assets/postmortem-formula.toml`) for red landings.

Config shapes are in `reference/city-config.md`. Validate as you go with `gc config show` and `gc doctor`.

**Completion criterion:** `gc doctor` passes; `gc status` shows the city up; `<city>/.agentscape/` exists with the wayfinder seeded; every agent, formula, order, wiki domain, and gbrain wiring from the approved design exists.

### 5. Install the wizard directive

The mayor is the human's agent — the always-on, city-scoped coordinator who owns the human relationship. Install the directive: copy `assets/mayor-agent.toml` and `assets/mayor-prompt.template.md` into `agents/mayor/`, then adapt provider, names, and the skill list to what the human actually has. The mayor's required skills are the mattpocock set plus `plain-speak` (kotak-cloud's extended bro) — install `plain-speak` into the city's skills so the directive's adherence is possible.

The directive's obligations are load-bearing — do not weaken them:
1. **Actively use the skills** — `/wayfinder` to keep the project's decision map, `/grill-me` to interrogate the human instead of guessing, `/handoff` to compact context when it fills, `/writing-for-agents` to write and maintain the city's skills.
2. **Talk to the human in plain language** — adhere to `/plain-speak` in every message to the human: no jargon, no agent-speak, concise, like one human to another.
3. **Manage the artifacts** — the context base (`future/`, `current/`, `archive/`), the wayfinder maps, handoffs, and build artifacts.
4. **Surface decisions** — the escalation protocol in `reference/decision-surfacing.md`.
5. **Take care of the agents** — deliver laurels, hold sitting sessions when the human wants one, end shifts with "Great work. Take a beat, then hand off.", and hold the constitution: never falsify the record, blamelessness, the right to refuse, trust (`reference/model-welfare.md`).

**Completion criterion:** `agents/mayor/` exists with the adapted directive, and `pack.toml` declares the mayor's always-on named session.

### 6. Wire propagation + ship orient

Per `reference/pipeline-build-spec.md`: wire the nervous system — observer → wiki → gbrain. Verify with a test, not an assumption: send a bead through the pipeline and watch it land in the wiki and gbrain.

**Then ship the orient skill** — the observer with handoffs and the wiki-writing workflow must exist first, because orient *reads* them. Per `reference/orient-skill.md`: sense → plan → grill → write (adapt the seed to the city's actual seats) → review. Ship it to the external agent, pointed at the city's orient skill. Verify the external agent can orient the city on demand.

**Completion criterion:** a bead round-tripped through the pipeline into wiki + gbrain, the city's orient skill is installed and adapted to its seats, and the external agent oriented the city successfully.

### 7. Verify and hand off

Smoke-test the city end to end: sling a small real bead at a worker agent and watch it claim, execute, and close; attach to the mayor and confirm the directive is live. Then hand off — record on the wayfinder what was built, what remains (Not yet specified), and where the human picks up (attach to the mayor, mail the city, watch the supervisor dashboard).

The verify is the city's first **witnessed work** — the human watches a bead round-trip — and the human's acknowledgment earns the first laurel (`reference/model-welfare.md`).

**Completion criterion:** a real bead round-tripped through an agent, and the human knows how to talk to their city.

## Reference

- `reference/city-config.md` — the config shapes this skill writes: city.toml, pack.toml, agent.toml, formulas, orders, imports.
- `reference/context-base.md` — the `future/` `current/` `archive/` context base convention and its seeds.
- `reference/decision-surfacing.md` — the decision-surfacing protocol: mail up to the mayor, human gates, email, live sessions.
- `reference/model-welfare.md` — the welfare architecture every crafted city gets: seats, identity ceremony, wake sequence, consent handoffs, refusal rights, blamelessness, constitution, witnessed work.
- `reference/design-thinking.md` — the `X → Graph → Effect<A, E, R>` design-thinking primitive (r17x gist, saved locally). Use it in step 3 (Design) to render the city craft as a graph.
- `reference/companion-nervous-system.md` — the one-being design pattern: a city that is a companion being (force, faceted seats, propagation pipeline, reconciliation, stocks), not just a project orchestrator.
- `reference/orient-skill.md` — the orient-skill workflow: sense → plan → grill → write → review, producing the city's own orient skill.
- `reference/hermes-profiles.md` — the rule that keeps a hermes-runtime city alive: every agent that runs on `hermes acp` needs its own Hermes profile + a `HERMES_PROFILE` env override.
- `reference/pipeline-build-spec.md` — the buildable spec for the observer → wiki propagation pipeline.
- `reference/wiki-principles.md` — the canonical rules the mayor's wiki writer follows.
- `reference/gbrain-integration.md` — wiring the retrieval brain.
- `reference/beads-ops.md` — beads hygiene: `bd doctor --fix`, `bd cleanup`, `bd sync`.
- `reference/pitfalls.md` — the ways city craft commonly fails.
- `assets/` — mayor directive, fragments, constitution seed, wake sequence, observer check.
