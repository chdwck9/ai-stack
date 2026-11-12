---


uuid: 41324dc8-ccd9-815c-851a-c10540b8eac6
name: gmail-bulk-operations
description: "Use when bulk-filing mail or drafting replies in Gmail."
version: 1
author: Richard Dykes, Hermes Agent
license: MIT
metadata:
hermes:
tags: [mail, gmail, inbox, triage, bulk]
related_skills: [triage-inbox, monday, morning, google-workspace]


---


# Gmail bulk operations

The harness for actually moving mail: scan both accounts, file noise into named labels, draft replies.
Policy and disposition rules live in `$triage-inbox`; this skill is the commands, the accounts, and the
failure modes.

## When to Use

- A triage run was requested, or the Monday/morning reset never reached its inbox step.

- Bulk-filing noise out of an inbox into named labels.

- Drafting a reply without sending it.

- Checking how much mail is actually sitting in which account.

## Accounts and wrappers

Always go through the wrappers. Re-pointing `HERMES_HOME` by hand is how the two accounts get mixed.
Scripts that are not wrapper-invoked take `HERMES_HOME=<account dir>` in the environment.

**Reachable mail surfaces: these two only.** The Mambu mailbox (`richard.dykes@mambu.com`) is NOT a
mail surface — only its calendar is shared into the work account. Never claim inbox coverage of it;
name it in one line instead.

## Commands

Run Google-API scripts with the Hermes venv python (`~/.hermes/hermes-agent/venv/bin/python`), which
has the `google` libs; the system python3 does not.

- **Scan** both inboxes → JSON per account:
`~/.hermes/scripts/mail_scan.sh <outdir>` → `work_unread.json`, `pers_unread.json`
(searches `in:inbox`, so presence in the inbox is the scope, not the read flag).

- **Count / list precisely** when the cap matters:
`~/config/google/gwork gmail search "in:inbox" --max 300` (prints `No messages found.` when empty).

- **Labels**: `HERMES_HOME=<dir> gmail_bulk.py labels` · `create-label "Name"`.

- **File mail**: `gmail_bulk.py archive --ids ID ... --label NAME` → adds the label, removes `INBOX`.
`bulkmod --add A,B --remove INBOX --ids ...` for finer moves. Nothing is ever deleted.

- **Draft** (never sends): `gmail_draft.py --account work|pers --to ADDR --subject SUBJ [--thread THREADID] --body-file PATH`.
Pass `--thread` to keep the reply in context.

- **Read one message**: `<wrapper> gmail get <message_id>` (positional, not `--id`).

## Procedure

1. Scan both accounts. Note the count *before* and whether a cap was hit.

1. Classify with sender rules, not subject sentiment: job alerts → `jobs`; order/delivery
notifications → `orders`; marketing, newsletters, social notifications → `newsletters`;
account-security notices → `security`; statements/invoices → `finance`; school/childcare portal →
`school`. No rule fits → leave it in the inbox and list it.

1. Read any foreign-language school/childcare mail in full before filing — Dutch notices hide dates,
deadlines and money behind innocuous subjects (`Weekmenu`, `kinderkapper`).

1. Archive in one call per label per account; report the label each batch went to.

1. Draft replies for real humans in thread context; leave them unsent and name them in the report.

1. Turn commitments found in mail into Ship rows (minimum fields, phone-readable name, date = the
deadline the mail states, not the day you read it).

1. Re-query `in:inbox` on both accounts and report the counts after; a run that claims inbox zero
must show the number.

## Pitfalls

- **`mail_scan.sh`**** caps at 60 per account.** A file with exactly 60 entries means "60 or more" —
re-count with a higher `--max` before reporting the inbox size.

- **Never send.** Drafts only; a triage run has no authority to send. Archiving and labelling need no
per-item approval, deleting is never allowed.

- **A wrong label is worse than a generic one.** `newsletters` for a club reminder about a dated event
buries it; if the item carries a date the user must act on, make a Ship row first, then file it.

- **Don't re-triage set-aside mail** (`later`, `snoozed`, `[imap]/archive`) — it is already acted on.

- **Report per surface.** "Personal 84 → 2, work 6 → 0" beats "inbox cleared"; an unconnected mailbox
is a stated gap, not a silent one.

> Full operational depth for the sibling Notion/Ship work lives in `@Ship-DB-Rules` and
`@Calendar-To-Ship` under `/Volumes/Live/@Edge/.ai/resources/standards/` — durable standards go
there, never into a `references/` folder inside a skill directory (the nightly Hub→local sync wipes
those).

## Verification

- Both accounts re-queried with `in:inbox` after the run; counts match the report.

- Every archived id came back with the label applied and `INBOX` removed.

- Each draft exists as a draft (has an id) and was not sent.