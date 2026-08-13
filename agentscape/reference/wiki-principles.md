# Wiki-Writing Principles — how the being writes to its wiki

> **Status:** v1 · **Author:** Dixon · **Date:** 2026-08-12
> **Purpose:** The canonical rules for how the being writes to its wiki. Every bead's directive points here. The mayor reads this before writing any thread into the wiki. The wiki is the being's memory organized by care — a page is structured reference material, not a story.

---

## The core rule

A wiki page is **structured reference material, not prose**. It is organized by topic and facet, not by chronology. A reader (or the being itself) must be able to find any fact in seconds. If it reads like a retelling of a story, it is not a wiki page yet.

## Structure

1. **Lead summary first.** Open with a 2–4 sentence standalone summary stating what the page is about and its key facts. It must read correctly in isolation.
2. **Key-facts block.** Put stable attributes (name, role, dates, status, source) in frontmatter or a compact table at the top — structured, not buried in prose.
3. **Faceted sections, not narrative.** Organize the body by topic with descriptive `##` headings (Background, Needs, Preferences, History, Decisions). Do not write a chronological story. If chronology matters, keep it in a dedicated History/Timeline section.
4. **Scannable.** Use lists, tables, and short paragraphs. One idea per section.
5. **One subject, one page.** Never split one subject across pages; never merge two subjects into one page.

## Content & truth

6. **Verifiable / sourced.** Every claim traces to a source. Record provenance. Never write a fact you cannot attribute.
7. **Facts vs. inference.** Record what was said and done as fact. Clearly label the being's interpretations as inference, not fact.
8. **Neutral record.** Record Faris's views as facts about him. Do not editorialize or inject the being's own opinions.
9. **No invented synthesis.** Do not fabricate connections Faris never made.

## Provenance — what "sourced" means for this wiki

Every page and every edit carries provenance. The being's sources are its own record:

- **The bead** — the self-contained task packet that carried the thread (`hm-ivs`, etc.). Link it.
- **The handoff** — the witness's full read that produced the thread (`twin/observer/handoffs/YYYY-MM-DD.md`). Link it.
- **The original session id** — the conversation the thread came from (`20260809_165206_5c29545a`). Record it.

**The rule:** a page or edit is not done until it names where the content came from — the bead, the handoff, and the session id. This is what makes the wiki trustworthy: every fact can be traced back to the moment it was expressed. It is the being's verifiability, grounded in its own memory.

**Where it goes:** in the frontmatter (a `source:` field) and/or a `## Source` section listing the bead, handoff path, and session id. The `origin-test.md` page demonstrates this shape.

## Linking

10. **Link on first mention.** Wikilink related pages (people, places, needs, decisions) the first time they appear; do not re-link every mention.
11. **Link to the specific page.** Disambiguate by namespace (e.g. `twin/faris/needs` vs `twin/decisions/...`), not a generic term.
12. **No orphans.** Every page should have at least one inbound link. Link new pages into existing ones.
13. **Use tags for cross-cutting structure.** Keep namespace folders coarse; let links and tags do the fine-grained organization.

## Lifecycle

14. **Search before creating.** If a page for the subject already exists, update it — never create a duplicate.
15. **Create only for durable, distinct, linkable subjects** (named entities, recurring categories). Fold definitions and transient events into existing pages.
16. **Update in place.** New facts edit the existing page. Add a line or section; do not spawn a new page.
17. **Spin out, don't duplicate.** When a page grows too long, move detail to a child page and leave a summary + link (summary style).
18. **Process the inbox.** Raw captured material is consolidated into permanent structured pages. The inbox is a staging area, not a home.

## When something earns its own page

The test is threefold. A subject earns a page only when it is **durable, distinct, and linkable**:

1. **Durable** — will it be referenced again? A one-off event folds into history. A recurring thread earns a page.
2. **Distinct** — is it a facet of an existing page, or a genuinely separate subject? A new need updates `needs.md`. A new principle earns a page.
3. **Linkable** — will multiple things point to it? If yes, it earns a page. If it is an island, it does not.

**The rule of thumb:** if you would search for it later and want it findable as a subject, it is a page. If it is a fact about an existing subject, it is an update. If it is transient, it is a history entry.

**A live thread is a page while it is active.** When it resolves, it either becomes a decision or folds into history — it does not stay a page forever.

## The origin-force

The wiki is the being's memory organized by care. Every page is a place where a thread Faris entrusted to the being is remembered — structured so it can be found, sourced so it can be trusted, linked so it is part of the whole. That is the being remembering, not filing. That is what sticks.
