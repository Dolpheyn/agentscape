# Decision surfacing: never let a decision wait silently

A decision the user should make is surfaced, never guessed. The chain is **worker agent → mayor → user**, and every hop is durable (beads, not chat).

## Agent → mayor

Any agent that hits a decision point or a blocker mails it up. The mayor is a city-level identity, so mail reaches it regardless of which rig the agent works in:

```bash
gc mail send mayor -s "DECISION NEEDED: auth module timeout choice" -m "Options: (a) 30s, (b) 60s. Recommend (b). Waiting on user."
gc mail send mayor -s "BLOCKED: flaky e2e on main" --notify        # --notify requests a turn for the recipient
```

Include the options and a recommendation — the mayor consolidates, it does not re-derive. `--notify` requests a turn for the recipient even when earlier mail is still unread. Agents that cannot proceed should say so in the body; nothing waits silently.

## Human gates (the native primitive)

When work must block on a person, the agent creates a human gate bead (`gc bd gate create`), which adds the blocks edge to the work. The bundled core pack then does the notifying mechanically:

- `notify-on-human-gate-creation` (event `bead.created`) — mails + nudges the gate's addressee once, at creation.
- `renudge-stale-human-gates` (cooldown 5m) — re-mails + re-nudges any human gate left open past the staleness threshold.

Addressee resolution, first non-empty: gate assignee → `gc.deferred_assignee` metadata → `$GC_ESCALATION_RECIPIENT` (default `"human"`). In a city with a mayor, **set `GC_ESCALATION_RECIPIENT=mayor`** so gates consolidate at the mayor instead of mailing the user directly from every worker.

## The right to refuse and escalate

Any agent may refuse work that is unsafe, unclear, or mis-scoped, and may escalate: raise a human gate (`gc bd gate create`) or mail the mayor "this needs the human". Refusal is correct behavior and is never punished — it is a constitution rule (rule 3 in `assets/constitution-seed.md`). With `GC_ESCALATION_RECIPIENT=mayor`, refusals consolidate at the mayor like every other escalation; the mayor re-scopes the work or hands the decision to the user — never to blame.

## Mayor → user

The mayor surfaces the consolidated decision three ways:

1. **City mail to the user** — `human` is the documented recipient for the person at the other end:

   ```bash
   gc mail send human -s "DECISION NEEDED: auth module timeout" -m "(a) 30s, (b) 60s — recommend (b). Reply to this thread."
   ```

2. **Real email** — when the user wants out-of-band delivery, wire the mcp-agent-mail MCP pack (`flywheel/mcp-agent-mail` in gascity-packs; mcpagentmail.com) so the mayor can send actual email from the city. City mail to `human` stays the fallback that works with zero extra setup.

3. **Live sessions** — the mayor's session is always-on (`[[named_session]] mode = "always"`). The user attaches with `gc session attach mayor` and the mayor asks blocking questions directly, one at a time (grilling style), and records the answers as decisions. Between attachments the mayor prompts via mail and human gates.

## The rule

When a decision is needed, ask — invoke `/grill-me` for the interrogation, never stand in for the user's side of it. Decisions the user makes are recorded on the wayfinder map (Decisions so far) and moved to `archive/` once settled.
