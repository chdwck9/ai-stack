---


name: mcp-integration
uuid: 41424dc8-ccd9-81b3-9dc4-d0254e428a10
description: "Debug MCP tool_call failures: quote escaping, auth injection."
version: 1
author: clarity
license: proprietary
scope: local
thinking: "Low"
temperature: 0.2
metadata:
hermes:
tags: [mcp, integration, troubleshooting, tool-call]


---


# MCP Tool Integration Pitfalls

Use when debugging MCP tool call failures — quote escaping in content fields, runtime token injection, or Python syntax issues after patching.

## Pitfalls

### Quote mangling in string content fields

The Hermes MCP wrapper rejects certain quote patterns inside string values passed to `content:` or body fields. Specifically:

- Double quotes inside inline HTML/XML like `<embed source="file-upload://ID" />`

- Em-dashes, smart quotes, backticks used in place of ASCII equivalents

- Multiline strings with unescaped newlines in nested objects

**Fix:** Strip all internal double quotes and use flat text. Replace `source="value"` with `source=value`. If validation still fails with `invalid control character` or `Expecting delimiter`, replace remaining non-ASCII characters (em-dash u2014, curly quotes, etc.) with plain ASCII equivalents and retry. For complex embedded markup, upload the content as a file first and reference it by upload ID instead of embedding raw markup.

### Python script edits require immediate syntax verification

After applying a `patch()` to a `.py` file, always run `python3 -c 'import py_compile; py_compile.compile(path)'` before executing the full script. Fuzzy matchers can introduce subtle syntax errors (e.g. stray HTML span-closing fragments inside f-strings) that pass lint checks but fail at runtime with unhelpful tracebacks.

### MCP tool discovery via tool_search returns canonical names only

When `tool_search` returns matches, invoke them using the exact name from `tool_describe` results. Do not guess aliases or shorten names. A tool listed as `mcp__notion__fetch` must be invoked with that exact identifier — omitting parts of the namespace causes silent "not a known tool name" errors.

### Auth tokens are injected at runtime, never read from .env

The Notion integration token (and other MCP credentials) are injected into the MCP server process by Hermes' client layer. They do NOT appear in `.env` files and should never be extracted with grep. Always use MCP tools directly rather than trying to parse and reuse tokens manually.