---


name: conversation-recall
description: "Use when recalling prior Hermes conversations and results."
version: 0.1.0
author: Hermes Agent
license: MIT
created_by: agent
metadata:
hermes:
tags: [sessions, recall, history, search]


---


# Conversation Recall

## When to Use

Use this when Richard asks what happened in a previous Hermes session, where a task was left, or to recover results from earlier work.

## Procedure

1. **Search history first, then inspect likely sessions.** Use `session_search` with a concise query and `role_filter="user,assistant,tool"` when tool outputs likely contain the result. If the discovery search returns no results or says zero sessions searched, browse recent sessions and use titles/previews to pick likely candidates.

1. **Read or scroll, do not summarize from the hit alone.** Open the likely session with `session_id` alone for a broad view, then scroll around specific `around_message_id` anchors. Tool outputs often contain the actual extracted data, while assistant messages may contain only a plan or partial self-report.

1. **Use multiple search phrasings.** Search for service names, hostnames, URLs, synonyms, and task nouns. If a user says “Jellyseerr searches,” also try adjacent terms such as “Jellyfin,” “requests,” “watchlist,” “anime,” or the host URL if known.

1. **Separate completed findings from attempted work.** Report what was actually verified, what data was extracted, and where the work stalled. Do not present unresolved attempts as a working method or completed result.

1. **Give the session handle inline.** When referring Richard to the recovered session, include the returned `link` value verbatim inline so Hermes can render it as a session reference.

## Output Shape

- **Session:** inline session link.

- **Recovered result:** concise bullets with the verified data.

- **Incomplete / caveat:** what was not completed and why.

- **Next action:** the smallest concrete continuation if Richard wants to resume.

## Pitfalls

- **`session_search`**** is a window, not an enumeration.** A discovery query returns the top-N *matching* sessions and browse shows only a handful of recent ones; neither lists the whole history. To enumerate every session in a date range (a backfill, an audit), read the session store directly — see `references/session-store-queries.md`.

- Do not stop after a failed full-text search; browsing recent sessions can reveal a matching preview even when the FTS query misses.

- Do not trust an assistant self-report over tool output; read the surrounding tool messages before stating that something succeeded.

- Do not expose secrets, passwords, QR codes, booking references, or other sensitive artifacts that may appear in recalled screenshots or tool logs.

## References

- `references/session-store-queries.md` — direct reads of the session store: enumerate sessions across a date range and pull each one's goal and close-out without flooding context.