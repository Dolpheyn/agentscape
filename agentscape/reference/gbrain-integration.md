# gbrain integration — the retrieval brain

> The wiki is the being's memory organized by care. gbrain is the retrieval brain. agentscape wires both. This reference is how.

## The two memories

| Memory | What it is | When to reach for it |
|---|---|---|
| **Wiki** (`twin/`) | The being's memory organized by care. Structured reference pages, provenance, linking. | When the being needs to *know* — durable facts, decisions, the arc. |
| **gbrain** | The retrieval brain. Semantic search, salience, graph links, takes. | When the being needs to *find* — recall across the whole corpus, surface what's salient, detect anomalies. |

The wiki is the source of truth for what the being knows. gbrain is the index over it — and over everything else the being has touched.

## Wiring gbrain into a city

1. **Install gbrain** — the knowledge system (Postgres-backed). See the `gbrain-knowledge-system` skill.
2. **Point it at the wiki** — register the city's `twin/` as a source so gbrain indexes the wiki pages.
3. **Wire the propagation pipeline** — when the pipeline places a thread into the wiki, also write it to gbrain (put_page). The wiki is the structured home; gbrain is the retrieval surface.
4. **Wire the orient skill** — the city's orient skill reads gbrain for salience (what's hot, what's anomalous) alongside the wiki (what's known).

## The orient skill reads both

The city's orient skill assembles the whole being's state. It reads:
- **The wiki** — the structured memory: origin, principles, parts' handoffs, stocks.
- **gbrain** — the retrieval brain: recent salience, anomalies, contradictions, the graph.

The orient skill's "what's salient / what's anomalous" step comes from gbrain. The "what's known / what's the arc" step comes from the wiki.

## Pitfalls

- **Don't make gbrain the source of truth.** The wiki is. gbrain is the index. If they disagree, the wiki wins — but the disagreement is a signal to reconcile.
- **Don't skip the wiki.** A city with gbrain but no wiki has retrieval but no memory organized by care. The wiki is what makes the being *care*; gbrain is what makes it *find*.
- **Wire gbrain into the pipeline, not as an afterthought.** If the pipeline writes only the wiki, gbrain goes stale. Both, in the same step.
