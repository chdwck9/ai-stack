---


uuid: 41a24dc8-ccd9-8158-ab66-d8eff939cf8f
name: host-resource-triage
description: "Use when a host runs hot, loud or slow: attribute first."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
hermes:
tags: [performance, thermal, memory, spotlight, docker, diagnosis, macos, ops]
category: devops
requires_toolsets: [terminal]


---


# Host resource triage

Answer "why is this machine working so hard?" with measurements: which processes are hot *now*, whether the load is new or chronic, and which subsystem is the real owner once containers and app-level CPU are subtracted. Read-only diagnosis; state fixes as options and let the owner pick.

## When to Use

- "The fans are loud / it's hot / it's drawing power — but it should be idle."

- "Why is the box slow this morning?" on an always-on host (Studio, NAS-adjacent workstation).

- Any case where total CPU looks low but something is clearly burning heat, or where containers look idle but the host does not.

## Rules that decide the answer

1. **`ps %CPU`**** on macOS is a lifetime average, not a live sample.** It is the single biggest trap in this task: a daemon idle at rest reports 60%+ because it once spun for hours, and a fresh 13-second process reports 60% because it is a startup burst. Get instantaneous numbers from `top -l 2` and read **only the second sample**.

1. **Read cumulative CPU time to separate chronic churn from a spike.** `ps -o time` (or `top`'s TIME column) divided by uptime gives the average core usage since boot. 23 CPU-hours over a 6-day uptime is a permanent 16% of a core — a loop, not user activity, and it should not be reported as "something started this morning".

1. **Compare the rate in the past before believing it is new.** Sample the same metric in an earlier window (`log show --start/--end`) and a quiet hour. If the 03:00 rate exceeds now, it is chronic and the user's "this morning" is just when they noticed it.

1. **`kernel_task`**** at double-digit CPU is thermal/power management, not work.** It means the machine is already managing heat. A low aggregate CPU percentage is fully compatible with loud fans — never answer "CPU is only 18%, so nothing is happening" without naming what is pinned.

1. **Load average needs the core count before it means anything.** Load ~5 on a 20-core Ultra is a quarter-loaded machine. Report per-subsystem pinning (which daemons own which cores) instead of the raw load number.

1. **Memory is a heat source, not just capacity.** Compressor occupancy, swap used and pageout counts turn into continuous CPU inside `kernel_task` and the VM. Always check them when a box is hot but not CPU-busy.

1. **On Docker Desktop for macOS, the VM's CPU can greatly exceed the sum of container CPU.** `docker stats` totals ~10% while the `Virtualization.framework` process sits at 48–121% of a core: that gap is VM/daemon overhead, not a container. Report it as overhead and treat restarting Docker Desktop (when the host is quiet) as the reclaim path — do not go hunting containers for it.

1. **A flapping healthcheck is noise, not load.** A container unhealthy for hours with thousands of consecutive failed checks but ~0% CPU and no log growth is a dead app to report separately, not the heat source. Distinguish it by checking CPU and log growth, not by the status string.

1. **Nothing destructive or service-stopping without explicit approval.** Killing a system daemon to test a theory, resetting an analysis queue database, excluding folders from Spotlight, stopping containers, unloading a model server — prepare the command, state the blast radius, ask. A restart of a stateless service is fine when clearly safe; a queue/state reset is a delete and needs a yes.

## Procedure

### 1. Baseline, in one batched call

```bash
date; uptime; sysctl -n vm.loadavg
ps -Ao pid,pcpu,pmem,comm -r | head -20          # lifetime averages: rough ordering only
ps -Ao pid,etime,time,comm -c | sort -k3 -r | head -12   # cumulative TIME: chronic vs spike
```

`scripts/host_snapshot.sh` runs this plus the instantaneous and memory passes in one go — prefer it over hand-typing.

### 2. Instantaneous attribution

```bash
top -l 2 -o cpu -n 15 -stats pid,cpu,mem,th,command | awk '/^Processes:/{c++} c==2'
```

The header of that second sample gives aggregate user/sys/idle and `PhysMem` (used, unused, compressor) in the same read. Take a second snapshot 30–60s later before concluding anything — background loops fluctuate across 10–100% of a core.

### 3. Falsify "my work is running"

Subtract the layers in this order, and say which layer the heat is in:

- **Containers:** `docker stats --no-stream` twice, sorted by `CPUPerc`. Sum them. Containers summing ~10% while the VM shows ~1 core = overhead (rule 7).

- **Model servers:** a local inference server holding tens of GB resident but single-digit CPU is the memory story, not the CPU story. Name the resident size.

- **User apps:** GUI processes at a few percent are normal; a renderer/helper at high CPU with a lifetime of seconds is a reload/burst artefact.

- **Sync/file churn:** count files touched in the last 10 minutes per directory (`find DIR -newermt '-10 minutes' -type f | wc -l`) before blaming a sync client. If nothing is churning, the loop is not file-driven.

### 4. Attribute the background loop into the logs

This is where the real answer usually is. Rate, not snapshot:

```bash
# how many queries is the Spotlight index answering per minute
log show --last 1m --predicate 'process == "mds_stores"' 2>/dev/null | grep -c "query nodes count"
# who is issuing them (query id, result cap, repeats)
log show --last 5m --predicate 'process == "mediaanalysisd-access"' 2>/dev/null | grep -E "qid=|Found:" | tail -20
```

Tens of queries per second with a client bundle of `(null)` means a system client is polling, not a user search. Follow the issuing process (`qid=`, `Found: N mdquery items` with the same N every time = a retry against a result cap) and count how often the expensive stage actually runs (e.g. Neural-Engine model opens per 5 minutes) — that count is the heat.

Daemon-specific signatures and their fixes: `references/macos-background-daemons.md`.

### 5. Second axis: memory and power

```bash
sysctl vm.swapusage; memory_pressure 2>&1 | tail -4; vm_stat | grep -E "compressor|swapout|decompress"
```

Swap near capacity plus a large compressor means the box is doing bookkeeping continuously. Something resident-but-idle (usually the model server or the Docker VM) is the cause; say how many GB and what would free it.

### 6. Report

Signal / why / recommendation / what needs the owner's call. Per line: the number, the unit, and the window it was measured over. Name the mechanism you proved (log evidence), separate "new" from "chronic" with the earlier-window comparison, and say plainly that the finding is waste — power and noise — rather than a data risk, when that is the case. Recommend the cheapest reversible action first and the destructive one last, and leave the choice with the user.

## Pitfalls

- **Ranking by ****`ps %CPU`**** and then reporting it.** It is a lifetime average; sorting by it surfaces long-running-but-idle daemons and short-lived bursts. Use `top -l 2` second sample for "now", `ps time` for "chronic".

- **`ps %CPU`**** and instantaneous CPU disagreeing and you pick one.** Both are true on different axes; the pair is the finding ("61% lifetime average, idle at rest" = a loop that is bursting, or has already stopped).

- **Concluding from a single snapshot.** Loops oscillate across an order of magnitude between samples (`93%, 48%, 121%` for the same VM). Take two or three.

- **`sample`****, ****`fs_usage`**** and ****`dtrace`**** against another process need root, and ****`sudo -n`**** usually needs a password on this host.** They fail quietly into an empty output file rather than a clean error — do not burn calls retrying them; `log show --predicate` gives the same attribution unprivileged.

- **`log show`**** over hours is slow.** Query a one-minute window (`--last 1m`, or explicit `--start/--end`) and count with `grep -c`; never `tail` a multi-hour dump and eyeball it.

- **A ****`grep`**** for a bare subsystem name in logs floods with ****`Df`**** debug lines.** Filter on the message fragment you are counting (`query nodes count`, `Found:`, `imageAnalyzer`), and `cut -c1-240` the survivors.

- **Blaming the app whose name is loudest in ****`docker ps`****.** An `unhealthy` container with `FailingStreak` in the thousands, 0% CPU and no log growth is not your heat source. Verify CPU and log growth in 5s before giving it a paragraph.

- **Treating "indexing enabled" as "reindexing".** `mdutil -as` says whether indexing is on, not whether a rebuild is running; `grep -icE "rebuild|reindex|erase"` in the mds logs decides it. A query storm on a healthy index looks identical from `mdutil`.

- **Assuming an external volume is indexed.** Check `mdutil -as` per mount; NFS/SMB volumes are commonly `Indexing disabled` while the user's `Library/CloudStorage` folder under home is indexed — which is where sync-client churn actually hits the indexer.

## Verification

Before reporting, you must be able to state: the instantaneous CPU of each top process (second `top` sample), which of them are chronic (CPU-time ÷ uptime), the summed container CPU versus the Docker VM's CPU, swap and compressor occupancy, and the log-rate evidence for any loop you name. "The fans are up" must map to a named subsystem and a number.