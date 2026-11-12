---


uuid: 41324dc8-ccd9-8176-9268-d9e6e7e91d4b
name: git-history-hygiene
description: "Use when purging secrets or PII from git history."
version: 1.0.0
author: clarity
license: proprietary
thinking: "Medium"
temperature: 0.2
metadata:
hermes:
tags: [git, secrets, privacy, filter-repo, gitignore, github]
related_skills: [github, external-account-access]


---


# Purging secrets/PII from a repo — and hardening what can be committed

Deleting a file in a later commit does **not** remove it: it stays in every clone and remains readable
by SHA. A purge is a history rewrite plus a `.gitignore` that stops the next `git add -A` from
reintroducing it.

## When to Use

- A repo is public (or about to be) and carries credentials, env files, dumps or transcripts.

- A `.gitignore` needs to encode what this user considers uncommittable.

- A history rewrite is already done and other clones are now out of sync.

## Procedure

1. **Inventory before rewriting — report patterns, never values.** Scan every *tracked* file with a
Python regex pass (API keys, `gh[pousr]_`, `AKIA…`, `xox[baprs]-`, `-----BEGIN … PRIVATE KEY`,
bearer headers, emails) and print `file -> {pattern: count}`. Then list what history ever held:
`git log --all --pretty=format: --name-only | sort -u | grep -E '…'`. A clean headline ("no key
material tracked") with a second, honest line ("74 email addresses, N transcripts") is the deliverable.

1. **Back up before touching anything:** `git bundle create ~/backup-$(date +%Y%m%d-%H%M).bundle --all`.
Say where the bundle is in the closeout; it is the only undo.

1. **Rewrite on a LOCAL clone, never in the live working copy.** Clone to `~/repos/<name>-rewrite`
(a shared/NFS checkout is a bad place for a rewrite: reads fail mid-command and leave stale
`.git/index.lock`, which then breaks every later git call until removed). Clear a stale lock with
`rm -f .git/index.lock` **only after** `pgrep -fl git` shows no git process running — the symptom is
`fatal: Unable to read current working directory: No such file or directory` or
`may have crashed in this repository earlier`, on every command including `git status`.

1. **Install and run filter-repo** (`brew install git-filter-repo`):

  ```bash
  git filter-repo --force --invert-paths \
    --path-glob '._*' --path-glob '*/._*' --path-glob '*/*/._*' \
    --path-glob '@eaDir/*' --path-glob '*/@eaDir/*' \
    --path-glob '*.env' --path-glob '*.env.*' --path-glob '.env' \
    --path-glob '*.secrets*' --path-glob '*.bak' --path-glob '*.bak-*' \
    --path-glob '*.db' --path-glob '*.db-wal' --path-glob '*.db-shm' \
    --path 'Memory/raw-dump.json' --path-glob 'Memory/sessions/*'
  ```

  It also removes `origin` — re-add it before pushing. Check the count afterwards
  (`git ls-files | wc -l`) and grep the tree for the purged classes; empty output is the pass.

1. **Harden ****`.gitignore`**** by MERGING the existing file** (read it first; keep the user's own rules) and
add: `@eaDir/`, `._*`, `**/._*`, `.env`/`.env.*`/`*.env*`, `.secrets*`, `*.pem`, `*.key`, `id_*`,
`*_rsa`, `*_ed25519`, `mcp-tokens/`, `credentials*`, `*.token`, `*.db` + `-wal`/`-shm`,
`*.sqlite*`, `*.bak*`, `*.orig`, `*.tmp`, and any per-repo PII trees (dump files, transcripts).
Then confirm nothing tracked is now ignored: `git ls-files -ci --exclude-standard` must be empty.

1. **Commit, force push, verify from the remote** — `git push --force origin main`, then
`git ls-remote` for the new HEAD and the provider API for the tree (`contents/` should not list the
purged paths).

1. **Reconcile every other clone, or the purge gets undone.** In each checkout:

  ```bash
  git fetch origin && git reset --mixed origin/main
  git checkout origin/main -- .gitignore   # reset --mixed does NOT update the worktree
  git check-ignore -v <purged paths>       # must now report .gitignore rules
  git add -An | head                       # must not list purged files
  ```

  Without the explicit `.gitignore` checkout, the *old* ignore file stays in the worktree and the next
  scheduled `git add -A` re-adds everything that was purged.

## Pitfalls

- **A rewrite is not an unpublish.** GitHub keeps unreachable objects: the old commit still answers
`HTTP 200` at `api.github.com/repos/<o>/<r>/commits/<sha>`. Say so plainly; a true purge needs a
provider support request or delete-and-recreate.

- **Force-push strands every other clone** — any push from one restores the old history wholesale.
Reconcile them in the same session (step 7) and name them in the closeout.

- **Files removed from history are not removed from disk.** After `reset --mixed` they become
untracked-but-present, which is usually what the user wants (data kept, version control dropped).
Verify with `ls` before claiming the data survived.

- **Scan AppleDouble ****`._*`**** files** — Synology/macOS metadata shadows often carry the *names* of the
secrets that were meant to be ignored (`.env`, `.secrets`), which is how you find out they existed.

- **`git status`**** dirty with mass ****`D`**** of ****`._*`**** files is not damage** — it is the leftover of a cleanup
pass; treat it as local state, not as something to commit.

- **Do not purge working data the user still needs** (memory dirs, indexes, configs) without saying
what it costs. Rewriting memory out of a repo removes the off-machine backup too — surface that as a
decision, and prefer making the repo private when the content is data rather than credentials.

## Verification

- `git ls-files | wc -l` dropped by the expected count; no purged path appears in `git ls-files`.

- `git ls-files -ci --exclude-standard` is empty; `git add -An` in every clone lists nothing purged.

- Provider API confirms the new HEAD and a tree without the purged paths; old SHA still 200 is reported
as a known limitation, not a failure.