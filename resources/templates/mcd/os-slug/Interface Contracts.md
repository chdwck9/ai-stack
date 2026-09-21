---
doc_id:
  - os-slug/interface-contracts
version:
  - inherit from parent
last updated:
  - YYYY-MM-DD
tags:
  - api
  - interfaces
  - contracts
  - endpoints
  - auth
  - schema
  - integrations
use_when:
  - Building or verifying API integrations; generating client code or stubs; auth model queries; "what does endpoint X return" queries; SLA and error handling questions; any task that requires knowing the exact contract between this system and its consumers.
agent_notes:
  - This section is conditional — only present for software/platform/API subjects. Contracts here are canonical — if they conflict with §4 (Structure) or §7 (Context & Relationships), flag the contradiction rather than silently overriding. Request/response schemas MUST use machine-readable format (OpenAPI, Zod, JSON Schema) — prose descriptions of shapes are not sufficient. Contracts here describe the current version; for history see §12.
---

## What this section is for

The formal contract layer. An agent or developer building against or rebuilding this system must be able to derive the exact API surface, auth model, and error behaviour from this section alone — without reading source code.

**Reverse-engineering note:** Pull from existing API documentation, OpenAPI/Swagger specs, Postman collections, or Confluence integration specs. If none exist, derive from observed behaviour and mark as `[INFERRED]`.

---

## Building Blocks

### Endpoint Inventory

_List all public and internal endpoints this system exposes. For each, specify the contract in enough detail to generate a working client stub._

|ID|Method|Path|Description|Auth required|Rate limit|SLA (p99)|
|---|---|---|---|---|---|---|
|EP-01|GET / POST / PUT / DELETE / PATCH|||Yes / No / API-key / JWT|||

---

### Request / Response Shapes

_For each endpoint, define request and response schemas in machine-readable format. Prose descriptions of fields are not sufficient — agents cannot reliably implement from prose._

**Format selection:**

|Scenario|Format|
|---|---|
|Cross-service or external-facing API|OpenAPI 3.x YAML block (preferred)|
|TypeScript / same-codebase consumer|Zod schema or TypeScript interface|
|Agent output / function calling validation|JSON Schema in strict mode|

_Author rule: specify field-level constraints (required, type, format, enum values, min/max). Do not describe implementation — "amount must be a positive integer ≤ 10,000" not "use Number.isInteger() to validate"._

---

**EP-01 — [Endpoint name]**

Request _(choose ONE format, delete others)_:

```yaml
# OpenAPI 3.x request body schema
requestBody:
  required: true
  content:
    application/json:
      schema:
        type: object
        required:
          - [field]
        properties:
          [field]:
            type: [string|integer|boolean|array|object]
            description: "[description]"
            # [format | enum | minimum | maximum | pattern as applicable]
        additionalProperties: false
```

```tsx
// Zod request schema
const [EndpointName]Request = z.object({
  [field]: z.[type]().[constraints](), // [description]
});
```

Response (200) _(choose ONE format, delete others)_:

```yaml
# OpenAPI 3.x response schema
responses:
  '200':
    description: "[description]"
    content:
      application/json:
        schema:
          type: object
          required:
            - [field]
          properties:
            [field]:
              type: [string|integer|boolean|array|object]
              description: "[description]"
```

```tsx
// TypeScript response type
type [EndpointName]Response = {
  [field]: [type]; // [description]
};
```

Error responses:

|HTTP status|Error code|Meaning|Recoverable?|
|---|---|---|---|
|400|||Yes|
|401|||Yes|
|404|||Yes|
|422|||Yes|
|500|||No|

_Repeat EP-NN block for each endpoint in the Endpoint Inventory. Mark `[INFERRED]` on any schema derived from observed behaviour rather than confirmed documentation._

---

### Authentication Model

_Describe the auth mechanism(s) in full. An agent must be able to construct a valid authenticated request from this section._

|Mechanism|Scope|Token format|Expiry|Refresh method|
|---|---|---|---|---|
||e.g. OAuth2 / API key / mTLS / JWT||||

---

### Error Catalogue

_Canonical list of error codes this system returns. Include enough context to distinguish recoverable from non-recoverable errors._

|Code|Meaning|Recoverable?|Recommended action|
|---|---|---|---|
|||Yes / No||

---

### Versioning Policy

_How are breaking changes communicated? What is the deprecation timeline?_

[ANSWER]

---

### Webhooks / Events _(if applicable)_

_Outbound event schema for event-driven integrations._

|Event type|Trigger|Payload schema|Retry policy|
|---|---|---|---|
|||||