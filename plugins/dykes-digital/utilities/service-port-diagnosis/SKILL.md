---


uuid: 40d24dc8-ccd9-81ab-8ec6-dc695b6c6117
name: service-port-diagnosis
description: Use when a service is unreachable on its port.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
hermes:
tags: [ports, networking, docker, diagnosis, lsof, postgres, ssh, remote, selfhosted]
category: devops
requires_toolsets: [terminal]


---


# Service / port reachability diagnosis

Work out *what is actually answering* when a service or database "can't be reached" on its port. Covers local and remote hosts, Docker-published ports, and host-native services that contend for the same port number.

## When to Use

- "I can't connect to <db/service> on port N" — connection refused, or an auth error that names the *wrong* server.

- A container reports healthy and its port mapping looks right, but clients still fail.

- A port was remapped to dodge a conflict and something broke afterwards.

- Any diagnosis where the answer must be the real owner of a port, not a guess.

## Core principle

**"Port is open" is not "the right server answered."** Two processes can hold the same port number on different bind addresses, and the client's *vantage point* decides which one it reaches. Always establish (a) every listener on the port, (b) which address each is bound to, and (c) which one the failing client's host actually routes to.

## Procedure

### 1. Listener inventory on the host that owns the service

```bash
lsof -nP -iTCP:PORT -sTCP:LISTEN          # macOS
ess -ltnp 'sport = :PORT'                  # Linux
```

Read the **bind address**, not just the command name. A wildcard bind (`*:PORT`, `0.0.0.0:PORT`) and a specific `127.0.0.1:PORT` / `[::1]:PORT` can coexist on the same port number — the specific bind wins for clients that resolve to that interface. Two entries for one port is the single most common cause of "it's up but I can't reach it".

### 2. Probe from every vantage point

Loopback and the host's routable IP are different servers when a specific bind exists.

```bash
nc -zv -w2 localhost PORT
nc -zv -w2 127.0.0.1 PORT
nc -zv -w2 <LAN-or-Tailscale-IP> PORT
# and once from the client's own machine, not just the server
```

### 3. Confirm the responder's identity, not just connectivity

Ask the responding process something that reveals *which* instance it is. A successful TCP connect against the wrong server is the whole failure mode of this skill.

- Postgres: `psql "postgres://USER:PW@HOST:PORT/DB" -c 'select current_database(), current_user, inet_server_port(), version()'` — `inet_server_port()` reports the **container-internal** port, so a published `5433:5432` answering `5432` proves you reached the container and not a host-native server sharing 5433.

- HTTP: `curl -s -o /dev/null -w '%{http_code}' http://HOST:PORT/health` plus a body/identity field (server name, build id).

- Auth errors are evidence: `FATAL: role "X" does not exist` means you reached *a* Postgres that does not hold that schema — the correct conclusion is "wrong server", not "database broken". Do not report the DB as damaged on that error alone.

### 4. When a loopback bind is shadowing Docker (or vice versa)

Identify the owner and decide whether it comes back:

```bash
ps -o pid,ppid,lstart,etime,command -p PID      # start time, PPID, full argv (data dir + flags)
lsof -p PID | grep -E 'cwd|DATA'                # what it was pointed at
brew services list                              # managed service?
ls -1 ~/Library/LaunchAgents | grep -i NAME     # login agent?
launchctl list | grep -i NAME                   # actually loaded?
```

- A `PPID 1` process with no brew service and no LaunchAgent was started **detached** (nohup / `&` / `pg_ctl start`) and will not self-restart — but *something* started it, so say so rather than assuming it stays dead.

- Docker's own port ownership: `docker ps --format '{{.Names}}\t{{.Status}}\t{{.Ports}}'`.

- When the compose project directory has moved and you need to find where the running stack actually lives:

```bash
docker inspect -f '{{index .Config.Labels "com.docker.compose.project.working_dir"}}' <container>
docker inspect -f '{{json .Mounts}}' <container>   # bind mounts + named volumes, with real host paths
```

### 5. Report a workaround before a fix; never stop the other service yourself

- A client that works over the host's routable IP is **unblocked now** — offer that first; it changes nothing on the host.

- Stopping the shadowing process is a **service stop**: state the command and get the user's OK. Do not kill it to "tidy up".

- Report shape that works: signal (both listeners + bind addresses), one-line root cause, the verified fact that the target service itself is healthy (volume/data intact, row counts), the zero-change workaround, the durable fix with its exact command, and what you did *not* do.

- Fixes on a remote host belong on that host — dispatch the change there rather than acting on the machine you are running on.

## Pitfalls

- **A wildcard bind does not lock out a specific-IP bind.** `docker run -p 5433:5432` succeeding tells you nothing about whether `localhost:5433` reaches it. Check the bind addresses, then test both loopback and the routable IP.

- **Moving a published port to dodge a conflict invites the conflict to follow you.** After any port remap, re-check both the old and the new port for a shadowing native service — a native server can be reconfigured onto the port you just vacated for it.

- **`ping`**** failing while TCP succeeds means ICMP is filtered, not that the host is down.** Never infer "host unreachable" from ping; confirm with a TCP probe.

- **macOS ships no ****`timeout(1)`****.** Use `nc -w N` / `nc -G N` or `ssh -o ConnectTimeout=N` instead of `timeout N cmd` — do not write probes that depend on GNU coreutils.

- **Do not ****`grep -r`**** a large tree for a bare port number to find its config.** Model caches and lockfiles contain such digit strings incidentally and drown the result in megabytes of noise. Search the project dirs, `~/.hermes`, and known config paths; or ask the running process (`ps`, `docker inspect`) instead of grepping.

- **Never nest quoting to build a remote command.** `===` and `?` inside `ssh host '...'` get parsed by the remote shell as test/glob syntax and produce confusing failures (`==PID not found`, `no matches found`). Write the probe to a file and pipe it: `ssh host 'bash -s' < probe.sh` — `bash -s` (not `zsh -lc`) is the non-interactive choice for probes.

- **A remote non-login shell lacks the Homebrew/package PATH.** `ssh host 'docker ...'` can fail with `command not found` while the binary exists; resolve it once with `ssh host 'zsh -lc "command -v docker"'` and use the absolute path, or wrap the probe in `zsh -lc`.

- **"Nothing is listening" from one vantage is not global.** `localhost:PORT` refused on a client machine says nothing about the server's own listeners — always probe the host that owns the service.

## Verification

Before reporting, you must be able to state: every process listening on the port, the bind address of each, which one the failing client reaches, and the command output that proves the target service itself is healthy. A connectivity test that passes against the *wrong* server is the failure this skill exists to catch.