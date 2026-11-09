---


name: chat-surface-verbosity
uuid: 40524dc8-ccd9-814a-a7f7-e8450d5b4eb1
version: 2
description: "Chat Surface Verbosity"
last-used: "2026-10-27"
thinking: "Low"
temperature: 0.2
author: clarity
license: proprietary
metadata:
hermes:
tags: [hermes, config, discord, verbosity, display, gateway]
related_skills: [clarity-capabilities, hermes-agent]


---


# Chat surface verbosity

When Richard says the conversation is a wall of scroll — or too quiet — the fix is almost never
"write shorter answers". It is the machine room around the answer: tool-progress lines, interim
commentary, reasoning blocks, busy acks. Tune those keys first, then agree a length rule for prose.

## When to Use

- Richard says replies are too long, too noisy, or he is scrolling to find the answer.

- He asks to see less (or more) of the work happening between replies.

- Any request about `/verbose`, tool-progress lines, reasoning display, or per-platform formatting.

## Richard's standing bar

- **Trackability without scroll**: he wants to see that work is happening, not a transcript of it.
One progress bubble per turn is the ceiling in Discord.

- Answers stay short by default — ~6 lines unless he asked for depth or the material is a decision he
must make. No preamble, no restating the question, no "done!" coda.

- Prefer chat-native formatting: bold labels and bullets. **Never tables on Discord** — it does not
render them; the desktop app renders full GFM, so tables are fine (often clearest) there.

- **A question is not an investigation.** When he asks whether something is possible, or what a
number is, answer from what is already in hand — the answer plus the one piece of evidence that
settles it, not a multi-step probe of the system. He will say so outright ("this doesn't need a
long thinking round"); treat that as the signal to stop gathering and answer, naming any gap.

- Never silence everything to fix noise: keep `long_running_notifications` on so a long job does not
look dead.

## Diagnose first

The scroll comes from four separable sources — name which are firing instead of guessing:

1. **`display.tool_progress`** — one line per tool call. Biggest offender when set to `all`.

1. **`display.interim_assistant_messages`** — commentary between tool calls; each is a new message.

1. **`display.show_reasoning`** — reasoning blocks echoed under each reply.

1. **`display.busy_ack_detail`** — "still working, iteration N, tool: …" acks.

`display.tool_progress_grouping: accumulate` (the default) already edits one bubble rather than
posting per tool; if someone set `separate`, that alone explains a wall of messages.

## Procedure

1. Read current effective values, not assumptions:

  ```bash
  hermes config get display.platforms.discord
  hermes config get display.tool_progress
  hermes config get display.tool_progress_grouping
  ```

1. Write **per-platform overrides**, never by flattening the global defaults — Richard uses several
surfaces and only one is noisy:

  ```bash
  hermes config set display.platforms.discord.tool_progress new
  hermes config set display.platforms.discord.interim_assistant_messages false
  hermes config set display.platforms.discord.show_reasoning false
  hermes config set display.platforms.discord.busy_ack_detail false
  hermes config set display.platforms.discord.long_running_notifications true
  ```

  Resolution order (first non-None wins): `display.platforms.<platform>.<key>` → `display.<key>` →
  platform tier default → `_GLOBAL_DEFAULTS`. Source of truth: `gateway/display_config.py`.

1. Give him live control rather than a config edit per mood:

  ```bash
  hermes config set display.tool_progress_command true   # enables /verbose in the gateway
  ```

  `/verbose` cycles `off → new → all → verbose` per chat.

1. Verify the write landed and did not corrupt YAML — an indentation slip breaks the live gateway:

  ```bash
  ~/.hermes/hermes-agent/venv/bin/python -c "import yaml;d=yaml.safe_load(open('$HOME/.hermes/config.yaml'));print(d['display']['platforms']['discord'])"
  hermes gateway status
  ```

1. Tell him it applies from the next message, and offer the one-line reversal. A verbosity change he
cannot undo in a sentence is not a favour.

## Pitfalls

- **Never hand-edit ****`config.yaml`** — always `hermes config set`. A stray indent takes down the
running gateway, and it is the one file whose failure mode is "everything stops".

- `hermes config get display.tool_progress` prints `⚠ not a recognized config key` yet returns the
real value — a schema-registration gap, not a broken key. Do not "fix" it by moving the setting.

- Bare `python3` on this host has no `yaml` module; use `~/.hermes/hermes-agent/venv/bin/python`.

- Discord tier defaults already differ (`reasoning_style: subtext`). Set what you mean explicitly.

- Turning off everything makes a long run look frozen — silence `busy_ack_detail` but keep the
long-running heartbeat.