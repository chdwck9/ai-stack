---


name: hermes-approvals
uuid: 40524dc8-ccd9-81df-bf5a-ee4dcf3e71b5
version: 2
description: "Hermes Approvals"
last-used: "2026-10-27"
thinking: "Medium"
temperature: 0.3
author: Clarity
license: MIT
metadata:
hermes:
tags: [hermes, approvals, security, gateway, discord, i18n]
related_skills: [hermes-services, handle-delegated-task]


---


# Hermes dangerous-command approvals

The gate that stops a dangerous shell command (`rm -rf`, `git reset --hard`, sudo, service stops)
before it runs, and the prompt the user answers.

## When to Use

- Explaining why a command was blocked, timed out, or ran unprompted.

- Tuning behaviour per surface: chat gateway vs cron vs webhook/API vs one-shot `-q`.

- Acting on "I want one Allow, not a prompt per command" / "make it stick".

- Extending the approval prompt or its buttons.

## The model — where the decision is made

The terminal guard runs its checks in a fixed order (`tools/approval.py`):

1. hardline floor + user `approvals.deny` globs — **non-overridable**, block even under YOLO;

1. session YOLO → approve;

1. permanent `command_allowlist` match → approve;

1. detection → smart guardian verdict, or a human prompt.

So **only YOLO and the allowlist skip a prompt.** A guard-added command category can be *blocked*
(step 1) but never *pre-approved* except through those two.

## Config keys (`approvals:` in config.yaml) — set with `hermes config set`

- `mode` — `smart` (default): an aux LLM auto-approves low-risk once, auto-denies genuinely
dangerous, prompts on uncertain. `manual`: always prompt. `off`: global `--yolo`.

- `timeout` — default `300`: messaging approvals are a push notification, so the window must survive
the user being away.

- `cron_mode` / `single_query_mode` / `unattended_mode` — `deny` (default) or `approve`. They govern
the headless contexts where **no human can answer**: cron, `hermes chat -q`, and the unattended
platforms (webhook, msgraph_webhook, api_server). `deny` blocks instantly so the agent finds
another path; `approve` auto-approves everything there.

- `deny` — case-insensitive fnmatch globs; the lever to make a category never run.

- `smart_policy` — extra rules appended to the guardian's prompt.

- `denial_breaker_threshold` — default `3`; consecutive DENYs before a hard-stop.

A surface that cannot prompt declares that in config — never leave a run to block for the full
timeout with nobody watching.

## Tiers and "allow everything"

The card offers **Allow Once / Allow Session / Always Allow / Deny** (plus
`/approve [session|always|all]`, `/deny <reason>`). `once` persists nothing; `session` / `always`
persist the command's coarse **pattern key** (e.g. `recursive delete`) — never "everything", so a
later command in a different category prompts again. Do not describe "Always Allow" as "allow
everything". Session YOLO (`/yolo`) is the only per-session blanket: saved with the session, checked
before the allowlist, keyed by session. Full detail — including the smart-DENY card rule and the
Discord **Allow Everything** button: `references/tiers-and-yolo.md`.

## Pitfalls

- **Do not trust a job to request approval on a surface that cannot answer.** A delegated/automated
run pushed onto `webhook` / `api_server` gets `unattended_mode` — deny by default — so the command
is refused instantly and the run reports a failure that looks like a tooling or permissions
problem. If a job needs a human Allow, it must run on a chat platform.

- A click after the wait timed out must not report success — resolve first, and claim "Approved" only
when the queue yielded an entry.

- `command_allowlist` entries match literally or as shell globs **and are skipped entirely for
commands containing shell operators** (pipes, `&&`, redirection). "Pre-approve everything" is not
achievable by stuffing a glob in there.

- Approval is keyed by **session**, not by user or chat — resolving the wrong session key unblocks
nothing and the card greys out as "expired".

- UI extension traps and tier/YOLO behaviour:
`references/extending-approval-ui.md`, `references/tiers-and-yolo.md`.

## Verification

- Read the setting back with `hermes config get <dotted.key>`; never assume the write landed.

- Config the guard reads per-check applies immediately; anything the **gateway** snapshots at startup
needs a restart — report it as "configured, needs restart", never "active".

- UI change: `scripts/verify_approval_card.py` — buttons materialise and localise, smart deny
suppresses the extra tier, and a click flips session YOLO on, resolves the pending entry with
`once`, and rejects a re-click.

- i18n change: `scripts/locale_key_parity.py --check` — zero mismatches across all locales.

## Support files

- `references/extending-approval-ui.md` — adding a button or tier safely: where an affordance may
live, the pinning invariants, and the i18n parity rule.

- `scripts/locale_key_parity.py` — catalog key parity against `en.yaml`;
`scripts/verify_approval_card.py` — drive the real Discord approval view.