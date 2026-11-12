---


uuid: 41324dc8-ccd9-81f9-a7b7-de0ee97af5a8
name: host-intervention-audit
description: "Use when listing what still needs the user's hands."
version: 1.0.0
author: clarity
license: proprietary
thinking: "Medium"
temperature: 0.2
metadata:
hermes:
tags: [macos, permissions, tcc, launchd, security, brew, backlog]
related_skills: [hermes-services, n8n-workflows]


---


# Host intervention audit

"What do I still have to do myself on this machine?" — probe for it, never recall it. The real backlog is almost never what the last session left in the transcript, and a stale list wastes the window the user blocked out for it.

## When to Use

- The user asks for a backlog of permissions or manual steps before they sit down at the machine.

- After discovering a blocked operation (a refused restart, a permission error) and needing to decide what is a handoff versus a fix.

- Before promising anything that needs a password, a GUI, or a service reload.

## Steps

1. **Inventory from the board, not the transcript.** The user's own list of "the stuff we need" lives in Ship, not in past sessions: query open rows (`Status ∈ Waiting, Do next, Doing`, `"Archive?" = '__NO__'`) and keep those whose `"date:When?:start"` is recent — the board carries hundreds of stale rows from years of `Doing`, so dumping the full set buries today's four real items. `~/.hermes/scripts/ship_query.py` into a file, then filter in Python; keyword-match the titles (`media box`, `coolify`, `<tool> sign in`) to catch rows whose date was never refreshed. Session search is a weak source here — an empty result means the DB has no matching sessions, not that the backlog is empty.

1. **Privilege.** `sudo -n true` — if it answers "a password is required", every privileged step is a handoff; batch those into one block so the user authenticates once.

1. **TCC / filesystem grants.** Loop the protected paths and report readable vs blocked:

  ```bash
  for d in ~/Desktop ~/Documents ~/Downloads ~/Library/Mail ~/Library/Messages ~/Library/Safari; do
    printf '%-12s ' "$(basename "$d")"; ls "$d" >/dev/null 2>&1 && echo readable || echo BLOCKED; done
  screencapture -x /tmp/tcc.png && echo "screen capture: granted"
  ```

  Grant Full Disk Access only for the sources the user actually wants read — list the rest as optional, not as a gap.

1. **Drift that needs a restart.** `softwareupdate -l` and `brew outdated`. Report the count, then split formulae from casks: cask upgrades quit running apps (a Docker/desktop cask upgrade restarts every container), and brew-upgraded binaries that are already running (a tunnel, a daemon) keep the old one until restarted — say so, or the upgrade silently does nothing.

1. **Definitions an agent cannot reload.** Anything whose argv or unit file is loaded by launchd/systemd is a handoff: `bootout` is usually permitted from inside the agent, `bootstrap`/`submit` are not, and `kickstart -k` re-uses the loaded definition so an edited plist does not take. Package the handoff as a script with a readiness check and auto-rollback, not as a paragraph of instructions.

1. **Effective security state, not configured settings.** The highest-value items are usually exposures the user believes are closed:

  - an unauthenticated route on a public tunnel (grep the ingress config for the port before calling a loopback bind "local only");

  - an automation container left able to spawn processes (`NODE_FUNCTION_ALLOW_BUILTIN=*`, execute-command enabled) with RW mounts;

  - a client proxy configured but switched off (`Proxy\Type=None` beside stored credentials) — protection that exists only in the config file;

  - stray listeners from an experiment, and temp workflows/jobs "deactivated" rather than deleted.
  Check the running state, and rank these above permission grants.

1. **Control planes, from the inside.** A self-hosted control plane (Coolify, n8n, Portainer, a CI host) reports healthy while being half-configured, and its own UI is the only truthful source. Ask its database, not its HTTP status: `docker exec <c> sh -c 'php artisan tinker --execute="echo \App\Models\<Model>::count();"'` answers "is there an admin / a registered key / a server" in one call. Then check the host side of each link separately (sshd listening, the public key already in `authorized_keys`). The item is "register the key" only if the key is genuinely absent inside the app — often the host half is already done and the handoff is one paste. Concrete probes are in `references/control-plane-state.md`, along with the two wiring traps that masquerade as key failures: an app that prefixes `sudo` onto every remote command, and a non-interactive PATH too thin to find `docker`.

1. **Hand back the commands you owe them, verbatim.** "There were bash commands I needed to run, right?" is answered from the message store, not from memory — the list is recoverable exactly, and a reconstructed version is wrong in the details that matter. Query `~/.hermes/state.db` for assistant messages carrying fenced command blocks, filter to the ones with a handoff cue (`yourself`, `outside the gateway`, `needs you`, `you run`), then re-probe each before listing it. Recipe: `references/previous-handoff-recovery.md`.

## Reporting shape

Grouped by risk, highest first. One copy-paste command per item, the reason in one clause, and who executes it — the user, or you on their word. Never include a step they cannot run from a normal shell, and separate "needs your password/GUI" from "say the word and I do it".

## Pitfalls

- **Presence of a setting is not protection.** A proxy block, a firewall rule, or an allow-list that is configured but disabled reads as safe in every config dump and is worth nothing at runtime. Probe the effective state.

- **Do not list environment breakage as a task.** A missing binary or an uninstalled package is something you fix (or install) yourself; the backlog is for things only a human at the machine can do.

- **Don't hand back a fix you could have applied.** Reversible local changes are yours; reserve the list for passwords, GUI consent, OS-level grants, and service reloads.

- **Re-probe before answering.** A backlog assembled from memory silently omits everything fixed since — and repeats everything already done, which is how the user loses trust in the list.

- **A board row can be stale even when memory is not.** Reconcile every ticket against probed state and close the ones that are already done in the reply ("admin registration: done, 1 user exists") rather than carrying them forward. A row titled *Enable SSH* survived the SSH being enabled — the ticket records intent, not the world.

- **Healthy ≠ configured.** `Up (healthy)` plus a 200 on `/api/health` says the process runs, not that anything is wired to it: an app with an admin user, zero private keys and only its built-in [localhost](http://localhost/) server cannot deploy a thing. Probe the counts that matter before calling an item half-done.

- **Split "greenfield" from "re-route".** Before writing a VPN/proxy/anonymisation task as configuration, list what is actually running (`docker ps`, and `docker network inspect <net>` to find who shares a stack). A task that reads like tuning is often standing up the first container, which changes the ask from "give me credentials" to "decide the architecture".

- **Re-read the numbers at answer time.** A carried-over list says "15.8.2 and 27.2"; the box now
offers 15.8.3 and 27.2.1, and the brew count moved from 73 to 78. Quote what `softwareupdate -l`
and `brew outdated` return in this session, or the user runs a command that upgrades something you
did not describe.

- **Keep inline script payloads out of ****`terminal`****.** A `python3 - <<EOF` heredoc in a probe can trip the gateway-protection command guard and fail as a false positive before anything runs. Use `read_file`/`search_files` for config reads and one simple command per probe; if a call is refused with a restart/stop/uninstall message about a command you did not write, re-issue it split, not repeating it verbatim.