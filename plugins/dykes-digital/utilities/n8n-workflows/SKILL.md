---


uuid: 40524dc8-ccd9-8169-b216-d8643725a4ea
name: n8n-workflows
description: "N8n Workflows"
version: 2
last-used: "2026-10-27"
thinking: "Low"
temperature: 0.2
author: clarity
license: proprietary
metadata:
hermes:
tags: [n8n, automation, workflow, mcp, docker, synology]
related_skills: [hermes-skill-library, selfhosted-api-access, docker-fleet-healthcheck]


---


# n8n workflows

Change a node in a live n8n workflow and prove it on a real run. The n8n MCP is fine for *reading* and triggering runs; it is the **wrong tool for editing a node** — its workflow has credentials stripped. Prefer export → edit → import → reactivate. For REST API POST/PUT (programmatic node creation/editing): `references/api-editing.md`. Notion AI Hub pipeline: `references/notion-export-pipeline.md`; path mapping, run limits, pitfalls: `references/edit-loop-and-pitfalls.md`.

## When to Use

- Editing, adding, or removing a node (especially a Code node).

- Running a workflow to verify a change, or diagnosing a scheduled run.

- Any workflow that writes files, commits to git, or calls an API with a stored credential.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Find the instance** (n8n may run on another machine):

  - **Via SSH + docker**: `ssh <nas-host> 'sudo -n /usr/local/bin/docker ps --format "{{.Names}}"`. Read the mounts to translate paths (container `/data/<Share>/…`, NAS host `/volume1/<Share>/…`, agent over NFS/SMB `/Volumes/<Share>/…`), never assume: `docker inspect <ctr> --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}'`

  - **Direct from agent machine** (when host port is mapped and reachable over LAN/Tailscale): scan compose YAMLs for `<host-port>:<container-port>` — `grep -r 'ports:' <compose-dir> | grep 5678`. The API lives at `http://<host-ip>:<mapped-port>/api/v1/workflows`. Bypasses SSH but still requires a valid API key.

1. **Export the live workflow from inside the container** (preserves credential *references*); keep `wf-original.json` as rollback:
`ssh <nas-host> 'sudo -n /usr/local/bin/docker exec <ctr> n8n export:workflow --id=<id> --output=/tmp/wf.json'`
`ssh <nas-host> 'sudo -n /usr/local/bin/docker exec <ctr> cat /tmp/wf.json' > wf-original.json`

1. **Edit the JSON with a script, not by hand** — parse, locate the node by `name`, replace the parameter, `json.dump`; print a `difflib` diff so the change is reviewable.

1. **Stage where the container can see it** (`scp` to the host `/tmp` is often refused):
`cat wf-edited.json | ssh <nas-host> 'cat > /volume1/<Share>/wf-edited.json'`
`ssh <nas-host> 'sudo -n /usr/local/bin/docker cp /volume1/<Share>/wf-edited.json <ctr>:/tmp/wf-edited.json'`
`ssh <nas-host> 'sudo -n /usr/local/bin/docker exec <ctr> n8n import:workflow --input=/tmp/wf-edited.json'`

1. **Reactivate — ****`import`**** DEACTIVATES an active workflow** (prints `Deactivating workflow "<name>". Remember to activate later.` and leaves it *off*; a scheduled workflow then stops silently). Re-activate via MCP `publish_workflow` (or the UI) in the same operation.

1. **Verify by re-exporting and diffing**, then assert credentialled nodes still carry credentials:
`ssh <nas-host> 'sudo -n /usr/local/bin/docker exec <ctr> n8n export:workflow --id=<id> --output=/tmp/after.json'`
`ssh <nas-host> 'sudo -n /usr/local/bin/docker exec <ctr> cat /tmp/after.json' > wf-after.json`
Check `active` is true, only the intended parameter changed, and `{name: list(node['credentials'].keys()) for node in nodes if node.get('credentials')}` matches before/after.

1. **Delete the staging copies** from the shared folder and container when done.

## Running a workflow to verify

`execute_workflow` (`executionMode: manual`) and `n8n execute --id=<id>` **start at the Manual trigger**, not your branch; the scheduled-branch rewiring and the `Task Broker's port 5679 is already in use` workaround (`-e N8N_RUNNERS_TASK_BROKER_PORT=<free port>`) are in `references/edit-loop-and-pitfalls.md`.

## Pitfalls

- **Never rebuild a workflow from ****`@n8n/workflow-sdk`**** code to change one node** — `get_workflow_details` strips `credentials`, so generated nodes lack them and the next run fails to authenticate. Edit the exported JSON.

- **`import:workflow`**** deactivates the workflow** — reactivate and confirm `active: true` in a fresh export. A green run isn't proof: a `try/catch` Code node returning `{success:false}` completes without throwing — **verify the side effect** (files, git commit, DB row).

- **Adding a destination means editing the fetch filter in the same change** — a class the filter doesn't name is never fetched, silently.

- **Only add a root to a blanket clear node if the workflow fully owns every file in it** — diff the source and clean orphans with targeted deletes; a delete-and-rewrite node is destructive by design — snapshot first.

- **A node absent from ****`connections`**** never runs** — read `nodes[]` as a menu, `connections` as truth; a stale `…Subprocess` node can embed a `workflowJson` with credentials. Also: `update_workflow` (MCP SDK) rejects destructuring, `var`, and backtick template literals; use `const` only, `require()`, `expr('')`. On 3rd parse failure fall back to full JSON export/import.

- **No static ****`N8N_API_KEY`**** lives in compose or ****`.env`**** files.** `docker-compose.yaml` carries `N8N_ENCRYPTION_KEY` and `N8N_USER_MANAGEMENT_JWT_SECRET`; none of these are the programmatic API key. The key is generated by the running instance and must be created via the web UI (Settings → Credentials) or via `docker exec <ctr> n8n api-key:create`. Without it, every `/api/v1/*` call returns `401 'X-N8N-API-KEY' header required`.

- **A Code node writing loader-indexed files must emit ****`<name>/SKILL.md`**** and nothing beside it** (a flat `<name>.md` collides — see `hermes-skill-library`); fix the writer, not the store. Other gotchas (`.git/index.lock`, `sudo` path, `sh -lc` gate): `references/edit-loop-and-pitfalls.md`.

## Verification

- Re-export and diff: only the intended parameter differs; `active: true`; credentials present on every credentialled node.

- The side effect exists on disk / in git / in the target system — asserted directly, not inferred from run status.

- A generated tree is **set-equal** to the source of truth, both directions (extras = mis-routing; missing = filter gap).

- Temporary rewiring is reverted and re-verified.