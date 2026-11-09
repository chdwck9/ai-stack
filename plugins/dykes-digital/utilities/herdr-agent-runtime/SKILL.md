---


uuid: 40524dc8ccd981d5a82decc964498fba
name: herdr-agent-runtime
description: "Use herdr to run agents on remote machines."
version: 7
last-used: "2026-10-26"
author: Hermes Agent
license: MIT
thinking: "Medium"
temperature: 0.3
metadata:
hermes:
tags: [herdr, agents, remote, ssh, orchestration, runtime]
related_skills: [local-inference-serving]


---


# herdr — remote agent runtime

herdr (`herdrdev/herdr`, Apache-2.0, a single Rust binary) is an **agent runtime**, not an app: a
background server owns real terminals on the machine, the coding agents live inside those panes,
and every UI — its own TUI included — is just a client that attaches. That split is what makes it
driveable from elsewhere: a controller on host A can create panes and prompt agents on host B over
the CLI/socket API.

## When to Use

- Running coding agents on a remote or always-on machine, or "kicking off a task" remotely.

- Keeping agent sessions alive after a client closes or an SSH connection drops.

- Driving another machine's agents from a controller over the CLI/socket API.

## Install and verify

- `brew install herdr` (Homebrew **core**; prefer it to `curl -fsSL https://herdr.dev/install.sh | sh`
for a clean upgrade path). Alternatives: `mise use -g herdr`, the Nix flake, or a raw release
binary (`herdr-macos-aarch64`, `herdr-linux-x86_64`, …) when installers are blocked.

- `herdr --version`; `herdr status` prints client + server state and the socket path.

## Host and client

- **Host:** `herdr` (server + TUI) or `herdr server` (headless). One server per machine; each
machine keeps its own server, sessions and running processes.

- **Register a remote host from the controller:** `herdr machine add <ssh-target>` — interactive,
and it may install/update the remote package after approval. Manage with
`herdr machine list|status|reconnect|remove`.

- **Route a command to a saved machine:** `herdr --machine <label-or-id> <command>`. IDs and agent
names are scoped to one server, so selecting a machine in the TUI does **not** retarget CLI calls.

- Non-interactive contexts use the `default` session unless you pass `--remote-session <name>`.

## Drive agents (the point)

Most commands print **JSON** — parse it and read IDs out of responses; never predict an ID.

- `pane` is a raw terminal (it exists with or without an agent); `agent` is the recognised coding
agent currently inside a pane.

- `herdr --machine <m> agent start <name> --kind claude --pane <pane-id>` — kinds include `claude`,
`codex`, `pi`, `omp`, `hermes`, `opencode`, `cursor`, `grok`. `agent start` requires an existing
shell pane sitting at its prompt; it never creates layout.

- `herdr --machine <m> agent prompt <name> "…" --wait --until idle --until done` submits and waits.
Lifecycle state is semantic: `working` / `blocked` / `done` / `idle`. **`blocked`**** means the agent
hit an approval or question UI** — prompting a blocked agent returns `agent_blocked` without
sending; answer the dialog with `agent send-keys`.

- **A prompt can be typed but not submitted — verify the submit, never the status.**
`agent prompt` may leave the whole text sitting on the input line after the agent's `❯` prompt
while `agent_status` still reads `idle`. An unsubmitted prompt and a genuinely idle agent are
**indistinguishable from the status field**, so `idle` immediately after a prompt means
*unverified*, never success. Check `pane read <pane-id>`: if the text is still on the input line,
send the newline yourself with `agent send-keys <name> Enter` and re-check for `working`.

- Plain shell work: `pane run <pane> "<cmd>"`, then `pane read <pane>` (or `pane wait-output --regex`).

## Lay out a project set once — reuse the layout, not the conversation

A herdr **space is a workspace**, and one workspace **per project** is what this user wants — not a
single workspace holding a tab per project. Build them once and dispatch by name:

herdr --machine <m> workspace create --cwd "$ROOT/<project>" --label "<Project>" --no-focus
herdr --machine <m> workspace list                      # ids are not stable across restarts
herdr --machine <m> workspace get <id>                  # confirm the cwd before dispatching
# A NEW TASK = a new TAB in the project's existing space, with its own Claude session:
herdr --machine <m> tab create --workspace <project-ws> --cwd "$ROOT/<project>" --label "<task>" --no-focus
#   → capture .[result.tab](http://result.tab/).root_pane.pane_id  (ids are not stable across restarts)
herdr --machine <m> agent start <task> --kind claude --pane <new-pane>

**One task = one tab + its own Claude session, inside the project's space.** A new task never gets a
new *space* — the space **is** the project, and a second space for a project that already has one
fragments the project across spaces (this is the mistake to avoid). Equally, do **not** *resume* the
project's existing agent conversation for a different task: that conversation belongs to its own
task. Create a fresh tab and start a fresh agent in it.

- **On a task host, send ****`/remote-control`**** as the session's first input, before the task prompt.**
Once the Claude agent is up (trust prompt cleared), prompt `/remote-control`, confirm it engaged in
`pane read`, and only then send the task prompt — the command must come first so the session is
attachable from [claude.ai/mobile](http://claude.ai/mobile) before work starts.

Leave a space's first tab as a plain shell until a task arrives — starting an agent in every space
burns login sessions and tokens for panes nobody is reading.

- **Never nest quoting to pass a label.** `ssh host 'zsh -lc "... --label \"A & B\""'` mangles the
label to a literal `A \& B`; write the commands into a script and **pipe it in** — `ssh host 'bash -s' < script.sh`
needs no copy and no nested quotes; `scp` it only when the host must keep the script. Shell
metacharacters (`===`, `?`, `(`) inside a remote one-liner are parsed by the *remote* shell and
fail confusingly (`==PID not found`, `no matches found`), which is why the script goes in over
stdin rather than through the command string.

- **Verify the label, not just the exit code.** `workspace create` succeeds with a corrupted label,
so re-list and compare — a bad label is invisible to `workspace get <id>`'s id alone.

- **`tab rename`**** takes positional args:** `herdr tab rename <TAB_ID> <LABEL>...`. There is no
`--label` flag on it — passing one silently labels the tab with the literal string `--label X`.
Only `tab create` and `workspace create` take `--label`.

- Full command map, JSON shapes and the wait/state recipe: `references/control-surface.md`.

## Pitfalls

- **Driving from outside a pane uses the CLI/socket layer, never the bundled agent skill.** herdr's
shipped skill gates on `HERDR_ENV=1` and tells an agent to stop when it is not inside a
herdr-managed pane — so a controller on another host drives via the CLI.

- **A non-interactive SSH shell usually lacks the Homebrew bin dir on PATH, but herdr still finds a
remote ****`herdr`** by checking common Homebrew/mise/Nix paths — do not add PATH hacks for herdr
itself. Other remote binaries invoked by bare name still need a login shell, so resolve them with
`ssh <host> 'zsh -lc "command -v <tool>"'`.

- **`launchctl bootstrap`**** / LaunchAgent installs are blocked inside the Hermes gateway.** Install
autostart from an external shell; inside the gateway, run a long-lived server as a Hermes
background process with `persist_on_release` so it survives the session.

- **Detach is not reboot persistence.** herdr restores the saved layout and may resume supported
agent sessions after a server or machine restart, but the original pane processes do not survive.

- **`machine add`**** needs working SSH auth first.** Verify `ssh <target>` by key; an interactive
password/MFA prompt cannot be completed by the controller.

- **Confirm the machine is up before building layout on it:** `herdr machine status <m>` prints
`<id>\t<label>\treachable|unreachable`. Do not create workspaces against an unreachable host.

- **Create the workspace with ****`--cwd`**** at the project root**, then start the agent in its root pane —
the agent inherits that directory and therefore the project's own `CLAUDE.md` / `AGENTS.md`.
Prompting from `~` silently loses the project instructions.

- **Resolve a project's ****`CLAUDE.md`**** before trusting it — a dangling symlink is a location signal.**
Instructions files are often symlinked into a synced folder; if the target path does not exist on
the controller, the rules live on a *different* machine, which is itself the answer to "where must
this session run?". Check with `ls -la <file>` and read the target through the shared mount rather
than concluding the instructions are missing.

- **`agent read`**** can return an empty string while the pane is full.** It reports the agent's
conversation view; when a read comes back blank, use `pane read <pane-id>` for the literal screen
before concluding the agent produced nothing.

- **Verify the artefact on the machine that did the work — a completion status is not evidence.**
`agent_status: idle` (or a `done` banner in the pane) only says the agent stopped talking; it does
not say it produced anything. Before reporting a remote task complete, list the files it claims to
have written *on that host* — `pane run <plain-shell-pane> "ls -lat <dir>"` then `pane read` — and
check size and mtime. Two traps make an empty result look like a finished one: the controller's
copy of a synced folder can lag the executing host by days, so the mount showing nothing is not
proof of no work; and the reverse — a green status plus a shipped-looking row marker is not proof
of work either. Read the produced file, then report.

## Safety

Launching agents that edit repositories or send messages on someone's machine is a human-impacting
action: prepare the command and confirm before firing unless a scoped standing authorization exists,
and treat work devices more strictly than personal ones.

**Standing authorisation — a task the owner wrote themselves.** When one of the user's own delegated
tasks names the destination, or the destination is inferable from it, the dispatch is pre-approved:
creating the workspace, starting the agent and prompting it are **execution, not approval points**.
Do not stop to ask "shall I send this to the workbox?" — route it and go. The exemption covers the
hand-off, not the contents: what the agent is asked to *do* still obeys the task's own limits
(spend, destructive or irreversible actions, outbound messages).

## References

- `references/control-surface.md` — workspace/tab/pane/agent command map, JSON conventions, and the
agent lifecycle/wait recipe.

- `references/remote-kickoff-options.md` — decision table for kicking off remote agent work: herdr
vs T3 Code vs ACP vs SSH + headless Claude Code vs Anthropic Remote Control.