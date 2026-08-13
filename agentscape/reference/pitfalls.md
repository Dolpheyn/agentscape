# Pitfalls — the ways city craft commonly fails

> Read these before drafting. Each is a hard-won lesson from real city craft. A pitfall is a failure mode, not a rule — know it so you can avoid it.

## Config

- **No invented TOML keys.** `gc doctor --fix` refuses to auto-migrate a `city.toml` when it sees keys it doesn't recognize. Audit the draft by running `gc config show` and fixing every error before invoking `--fix`. Common keys that look plausible but are not real in v1.4.0: `env.GC_ESCALATION_RECIPIENT`, `providers.<name>.default_profile`, `providers.<name>.base = "builtin:hermes"` (`hermes` is not a builtin; the schema is `command + acp_command/acp_args`, see `reference/custom-hermes-provider.md`).
- **`rig.path` is pre-1.0.** Don't put `path = "/..."` in `[[rigs]]` — gc rejects it. Use `gc rig add <path>` to let the supervisor bind the per-host path into `.gc/site.toml` automatically. Same for `workspace.name` — it migrates to `.gc/site.toml` on first `gc doctor --fix`.
- **`[requires]` in formulas takes ONLY `formula_compiler`.** When migrating `contract = "graph.v2"` to the new syntax, the `[requires]` block accepts only `formula_compiler = ">=2.0.0"`. Other fields like `target_required` MUST stay at the top level. TOML silently accepts the wrong shape and `gc doctor` fails with `formula.requirement_unknown`.

## Hermes provider

- **Hermes is supported but not as a builtin.** The shipped builtins are `claude | codex | gemini | opencode | mimicode`. Hermes is supported via the `command + acp_command` schema because `hermes acp` is a first-class subcommand. Don't grep the source for the provider name and conclude it isn't supported — verify by running `gc config show` and reading the actual error. See `reference/custom-hermes-provider.md`.
- **Every hermes-acp agent needs its own Hermes profile.** An agent that inherits the `default` profile (the human's main session) cannot spawn — a second session can't start there, the create aborts before `creation_complete`, and the reconciler rolls it back (`pending_create_rollback`). The agent never wakes and every nudge to it strands. Give every agent a `~/.hermes/profiles/<name>/profile.yaml` and a `[[patches.agent]]` env override `HERMES_PROFILE = "<name>"` in `pack.toml`, then `gc reload`. See `reference/hermes-profiles.md`.

## The craft

- **Pause before `gc start`.** `gc start` installs a systemd user service and brings up the supervisor + Dolt server. It is the strongest "this is now actually running" moment. Show the staged draft, get sign-off, then run.
- **The gastown pack role set is not `gastown:mayor` etc.** Imported agents are addressed by binding-qualified names: `gastown.mayor` (city scope) or `home/gastown.polecat` (rig scope). Two packs may define the same local name without colliding. In the prompt template's `[[named_session]]`, declare `template = "mayor"` — the binding prefix is added by the import site.
- **The `model-welfare` companion is a SKILL, not a City pack.** It lives under `kotak-cloud/model-welfare/` in the skills catalog and is installed via `npx skills add`, not via `gc import add`. Do not add `[imports.model-welfare]` to `pack.toml` — the URL has no `pack.toml` at the expected path and will fail pack install.
- **Pack URLs must be tree-pinned or commit-pinned.** `https://github.com/.../tree/main/path` is acceptable for top-level pack dirs but the imported path must contain a `pack.toml`. Generic repo URLs without `/tree/SHA/path` will fail.
- **Upstream-pack warnings are not your fault.** Many gas-city 1.4.0 packs (gascity, gastown) still ship with `contract = "graph.v2"` in their formulas. After import you'll see ~30-40 formula-requirement warnings from `doctor`. These are upstream deprecations, not bugs in your city. Leave them — the warnings don't block runtime; the upgrade is a separate upstream PR.

## The identity ceremony

- **The identity ceremony blocks first wake if you wait for it.** The skill says "names are proposed by the seat and approved by the user" — but every TOML, every prompt template, every fragment reference embeds a `name`. **Start with placeholder role names** (`mayor`, `intake`, `planner`, `doer`, `witness`, `reviewer`) so the city is renderable end-to-end; the ceremony runs asynchronously on first wake and renames in place. The roster records `(pending)` → `approved <name> on <date>`. This is the difference between a city that boots and a city that waits three sessions for a name.

## The user can override the pause-for-review gate

- Step 1 (Orient) and step 4 (Craft) include "show the draft, get sign-off, then run" gates. If the user says "just do it" or "complete all now" after seeing the draft, the pause drops — proceed straight through install + start. The gate is a default, not a veto. Capture what shipped in the wayfinder's "Decisions so far" so the user can audit later.

## Don't write firm negative claims about supported features

- Greps come up empty for legitimate features (e.g. hermes provider) because the source uses reflection, transport layers, or schema-driven lookup. Test with the tool before contradicting the user.
