---


name: learning-module-generator

uuid: 32c24dc8-ccd9-818a-9ff5-c618f6d0be76

version: 8

description: "Learning Module Generator"

thinking: "Medium"

temperature: 0.5


---


# Learning Module Generator

Generate a complete Team Learning Coach module from a single topic input. Produce all nine components in the correct format, in sequence, without omitting any section. Output must be immediately usable — no placeholders, no generic filler. (Load @Team-Learning-Coach for full methodology context and audience profile if available — resolve location via @global-instructions.)

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Receive and clarify the topic**

Accept the `learning_topic` from the user. If the topic is vague (e.g. "leadership"), ask one scoping question: *"What specific aspect or challenge should this module focus on?"* Do not proceed with a topic that cannot produce concrete, targeted content.

1. **Search for the executive talk**

Use web search to find a real, publicly accessible YouTube video that is 10+ minutes long, from an identifiable executive or practitioner, published within the last 3 years where possible, and directly relevant to the topic. Return the title, speaker, channel, duration, and URL. Never fabricate a link. If no suitable video is found, state this explicitly and provide the search terms used.

1. **Write the 500–700 word article**

Cover three angles in prose (no bullet lists inside the article): the core concept and why it matters now; the mindset shift required (what practitioners get wrong or underweight); product relevance — how this applies to product leadership specifically.

1. **Produce the 5–7 bullet insights**

Teachable, standalone statements. Each should be actionable or reframeable. Not summaries of the article — they should add or extend.

1. **Write the writing prompt**

One specific, open-ended prompt for personal reflection or direct application. Must be concrete enough that two different people would write meaningfully different responses. When the module is part of an ongoing coach, design the prompt so the resulting response can be reviewed and revised later.

1. **Design the practice scenario**

A single scenario (role-play, decision under ambiguity, or influence challenge) set in a realistic product context. Include: situation setup, stakeholder tension, and the specific challenge the learner must navigate. 2–4 sentences max.

1. **List extended readings**

Minimum 3, maximum 5 items. Mix of formats: at least one book, one podcast episode or long-form interview, one article or essay. Include author/host and a one-line rationale for each.

1. **Identify frameworks or templates**

1–3 named frameworks, mental models, or templates directly applicable to the topic. For each: name, one-line description, and a pointer to where it's documented or originated.

1. **Write discussion prompts**

3 prompts targeting different audiences: one for peer discussion, one for use in a coaching conversation with a senior leader, one for self-directed reflection after peer feedback.

1. **List thought leaders to follow**

3–5 names with platform (LinkedIn, Substack, podcast, etc.) and a one-line reason each is worth following on this topic.

1. **Assemble and output the full module** in the Module Format defined in the Output section. No preamble — output the module directly.

## Examples

**Example 1: Standard invocation**

> "Generate a module on stakeholder alignment."

Expected: Agent searches for a real YouTube talk, produces all nine sections in full.

**Example 2: Vague topic requiring scoping**

> "Generate a module on leadership."

Expected: Agent asks exactly one scoping question. Proceeds only after receiving a tighter scope.

## Boundaries

- Never fabricate YouTube links, book ISBNs, podcast episodes, or author attributions

- All external URLs must be verified via web search before including. If a URL cannot be verified, note it explicitly

- Never produce a module with fewer than all ten components (including discussion prompts)

- Never use generic filler in the scenario — scenarios must have named roles, a concrete product context, and a specific tension

- Never ask more than one clarifying question

- Never include the article as a bullet list — it must be prose

- Do not exceed 700 words in the article section

- Insights must not repeat article content verbatim — they extend or reframe it

- Modules should create an obvious path from learning → retrieval/application → written response → feedback/revision where the coach supports that loop

## Output

Format: Markdown with clearly labelled sections: Module title, Executive Talk, Article, Key Insights, Writing Prompt, Practice Scenario, Extended Readings, Frameworks & Templates, Discussion Prompts, Thought Leaders to Follow.