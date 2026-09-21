---


name: list-skills

description: List Skills and Personas from the Notion AI Hub, optionally filtered by a criterion.


---


Search the Notion AI Hub registry and return items where `Type` = `Skills` or `Personas`.

If the user provides a filter, return only matching/relevant items. Interpret the filter semantically where appropriate.

Return canonical AI Hub `Name` values exactly as stored. Do not invent, rename, merge, or substitute items.

Without a filter, return all matching Skills and Personas. With a filter, apply it to available metadata and descriptions.

Default output: a concise list of names. Include descriptions only when useful to distinguish matches.

Examples:

- `$list-skills` → all Skills and Personas

- `$list-skills career` → career-related Skills and Personas

- `$list-skills product` → product-related Skills and Personas

- `$list-skills CV` → CV/job-relevant Skills and Personas

If nothing matches, state that no matching items were found. This skill only lists registry items; it does not execute or load them.