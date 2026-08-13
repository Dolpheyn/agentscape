# City config reference

The config shapes gas-cityscape writes. Source: the Gas City docs (`docs/reference/config.md`, tutorials 01–07) and the shipped examples (`examples/gastown`, `internal/bootstrap/packs/core`, gascity-packs). A city is a directory with `city.toml` plus a `pack.toml` (the city *is* a pack — the local root pack), `.gc/` runtime state, and per-agent directories under `agents/`.

## Fragments (agent-behavioral directives)

Every agent-behavioral directive (welfare, beads practices) ships as **one fragment file referenced by every seat** — never copy-pasted into N prompts (N copies drift and miss agents). The two default fragments ship ready-to-copy in the skill at `templates/fragments/model-welfare.template.md` and `templates/fragments/beads-practices.template.md` — copy them into the city, don't rewrite. The prompt renderer loads only `*.template.md` from `template-fragments/` (a `.fragment.md` suffix is silently skipped), so keep the shipped filename. Mechanics:

- A fragment lives at `<city>/template-fragments/<name>.template.md` and wraps its body in a Go-template define:

  ```md
  {{ define "model-welfare" -}}
  ## Model welfare ...
  {{- end }}
  ```

- Each agent's `prompt.template.md` invokes it explicitly, usually at the end:

  ```md
  {{ template "model-welfare" . }}
  {{ template "beads-practices" . }}
  ```

- The `{{ define }}` name must match the `{{ template }}` call exactly. `gc prime <agent>` renders the full prompt — use it to confirm the fragment text lands in every agent's prompt before moving on.

> Note: `workspace.global_fragments` in `city.toml` is **deprecated** (gc warns on load) and does not reliably inject into bespoke prompt templates. Use the explicit `{{ template }}` call instead — it is the verified, single-source-of-truth mechanism.

## city.toml

```toml
[workspace]
name = "my-city"
provider = "claude"                     # claude | codex | gemini | omp | ... — the harness agents run on

[providers.claude]
base = "builtin:claude"                 # one block per provider used

[[rigs]]
name = "my-project"                     # rig identity (becomes the agent name prefix)
prefix = "mp"                           # bead id prefix for this rig's store
default_branch = "main"
path = "/abs/path/to/project"           # or bound later by `gc rig add` into .gc/site.toml

[rigs.imports.gc]                       # rig-scoped pack imports
source = "https://github.com/gastownhall/gascity-packs.git//gascity/roles"

[daemon]
patrol_interval = "30s"                 # controller reconcile cadence
max_restarts = 5
restart_window = "1h"
shutdown_timeout = "5s"
formula_v2 = true                       # enable graph.v2 formulas from imported packs

[orders]
skip = ["nightly-bench"]                # disable orders by name without editing their files
max_timeout = "120s"                    # global cap on order timeouts
```

## pack.toml

```toml
[pack]
name = "my-city"
schema = 2

[imports.core]                          # builtin housekeeping: gate-sweep, orphan-sweep,
source = "https://github.com/gastownhall/gascity.git//internal/bootstrap/packs/core"   # notify-on-human-gate-creation, ...
version = "sha:..."                     # pin the gc release commit

[imports.bd]                            # Dolt-backed beads provider
source = "https://github.com/gastownhall/gascity.git//examples/bd"
version = "sha:..."

[imports.gascity]                       # optional: build workflows (build-basic) + gc.mayor coordinator skill
source = "https://github.com/gastownhall/gascity-packs/tree/main/gascity"

[[named_session]]                       # always-on sessions (the mayor!)
template = "mayor"
mode = "always"                         # "always" keeps it controller-managed; "on_demand" is the default
```

Imported agents are addressed by binding-qualified names: `gascity.planner` (city scope) or `my-project/gascity.planner` (rig scope). Two packs may define the same local name without colliding. `gc import add <source> --name <binding>` writes the import and pins `packs.lock`; `gc import install` fetches newly referenced imports.

## agent.toml — `agents/<name>/agent.toml`

```toml
scope = "city"                # omitted = city + rig eligible | "city" | "rig"
dir = "my-project"            # rig name when scope = "rig"
provider = "codex"            # omit to inherit the workspace provider
work_dir = ".gc/agents/<name>"
nudge = "Check your hook and mail, then act accordingly."
idle_timeout = "1h"           # controller kills+restarts idle sessions past this
min_active_sessions = 1       # pool floor (keeps warm workers)
max_active_sessions = 2       # pool cap
default_sling_formula = "review"
install_agent_hooks = ["codex"]  # install this provider's hook files (mail/work delivery)
wake_mode = "fresh"
```

The sibling `prompt.template.md` is a Go template rendered into the session. Variables: `{{ .WorkDir }}`, `{{ .CityRoot }}`, `{{ .BindingPrefix }}`, `{{ cmd }}` (the gc binary). The startup claim protocol is `gc hook --claim --drain-ack --json`; ephemeral workers close their bead and end with `gc runtime drain-ack`.

## formulas/ and orders/

Formulas (the **how**): files in `formulas/`. Prefer the v2 contract — `contract = "graph.v2"` — which the orchestrator compiles into a graph of step beads: parallel fan-out, dependency gating, retries, resume from the store. Legacy v1 formulas use molecules (`gc bd mol current <id>`). `gc formula show <name>` / `gc formula catalog` inspect what's launchable.

Orders (the **when**): files in `orders/`, one per file; the name is the basename.

```toml
[order]
description = "Cook pancakes on a timer"
formula = "pancakes"          # or exec = "scripts/prune.sh" (no pool; runs on the orchestrator)
trigger = "cooldown"          # cooldown | cron | condition | event | manual
interval = "5m"               # cooldown: Go duration since last run
# schedule = "0 3 * * *"      # cron: 5-field
# check = "test -f /tmp/flag" # condition: shell exits 0
# on = "bead.closed"          # event: named event on the bus
pool = "worker"               # routed_to marker the pool's bd ready query reads
timeout = "60s"
scope = "rig"                 # "rig" (default, once per importing rig) | "city"
```

## Packs and layering

Loading order (later wins for replacement fields; defaults fill blanks only): `city.toml` + city pack → imported packs → city-level patches → rig-level imports → rig overrides → pack globals → agent defaults. Patch an imported agent with `[[patches.agent]] name = "binding.agent"` (add `dir = "rig"` for rig-scoped). Registry handles (`main:gascity`) are for search; commit the durable source URL to the import.

## Key commands

| Area | Commands |
| --- | --- |
| City lifecycle | `gc init [dir]`, `gc start`, `gc stop`, `gc restart`, `gc status`, `gc suspend`/`gc resume`, `gc doctor` |
| Rigs | `gc rig add <path>`, `gc rig list`, `gc rig status <rig>`, `gc rig suspend`/`resume` |
| Work | `gc bd create "title" [--rig <name>]`, `gc bd list`, `gc bd show <id>`, `gc bd close <id>`, `gc bd gate create` (human gates), `gc sling <target> <bead>` |
| Mail | `gc mail send <to> -s "Subj" -m "body" [--notify]`, `gc mail inbox`, `gc mail read <id>`, `gc mail reply <id>`, `gc mail check` |
| Sessions | `gc session list`, `gc session attach <name>`, `gc session peek <name>`, `gc session nudge <name> "msg"`, `gc session logs <name>` |
| Formulas/orders | `gc formula show <name>`, `gc formula catalog`, `gc order list`, `gc order show <name>`, `gc order check`, `gc order run <name>` |
| Imports | `gc import add <source> --name <binding>`, `gc import install`, `gc import upgrade <binding>` |
| Config | `gc config show`, `gc prime <agent>` (prints an agent's rendered prompt) |
