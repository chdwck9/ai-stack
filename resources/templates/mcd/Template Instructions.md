## How to use this template

This document is designed so that an AI agent — given only its contents — can reconstruct the described system from scratch. Every section follows the same decomposition pattern:

> **Building block = Question to ask + Who to ask + How to verify the answer**

For each section, instructions are in _italics_. Delete them once the section is populated.

Populate sections in order. Sections 1–4 establish what the thing is. Sections 5–7 establish how it works. Sections 8–10 establish how to rebuild it. Sections 11–15 are operational memory. Section 16 (Interface Contracts) is conditional — software/API subjects only.

---

## Section Header Format

Every child section page — whether created by an agent or filled in manually — **must open with this metadata block**. Agents use these fields for routing and scoping without reading the full section body.

---
doc_id: [os-slug/section-slug]
version: [inherit from parent]
last updated: [YYYY-MM-DD]
tags: tag1, tag2, tag3
use_when: [1–2 sentences. Describe exactly which agent task types should fetch this section. Be specific enough that a routing agent can decide without reading body content.]
agent_notes: [1–3 hard guardrails. What should agents NOT assume from this section? Flag contradictions, scope limits, or required cross-references to other sections.]

---

The `use_when` field is the agent's routing key — if it's vague, agents will over-fetch. The `agent_notes` field is the override layer — any claim made elsewhere in the MCD that this section contradicts or scopes down should be flagged here.

---
