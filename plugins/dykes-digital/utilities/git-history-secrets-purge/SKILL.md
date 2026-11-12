---


uuid: 41324dc8-ccd9-813c-85a0-d8ccbe3dfc48
name: git-history-secrets-purge
version: 1
description: "Use when purging secrets or PII from git history."
thinking: "Medium"
temperature: 0.3
author: Clarity
license: proprietary
metadata:
hermes:
tags: [git, security, secrets, gitignore, filter-repo, public-repos]
related_skills: [github, selfhosted-app-deployment]


---


# Purging secrets and PII from a repo's history

Deleting a file from `HEAD` unpublishes nothing. If the repo is public, the rules to fix are: ignore
it, purge it from every commit, then verify from outside.

## When to Use

- "Add a gitignore for anything sensitive and remove it from history."

- A tracked tree contains `.env`, key material, databases, raw dumps or transcripts — especially in a
repository that turns out to be **public**.

## Procedure

1. **Inventory before you rewrite.** Scan tracked content for key material rather than trusting names:
provider prefixes (`sk-`, `ghp_`, `github_pat_`, `AKIA`), `-----BEGIN … PRIVATE KEY-----`, stored
bearer tokens, and separately emails/PII. Report what you found *by category* (`Memory/raw-*.json`,
`._*`, `state/*.db`) and say plainly when there were **no** credentials — an accurate "no keys, only
PII and metadata" is more useful than a dramatic purge.

1. **Back up first:** `git bundle create /tmp/<repo>-backup-$(date +%Y%m%d-%H%M).bundle --all`.

1. **Work on a clone, not the live working copy**, and prefer cloning from the remote — it is local
disk, fast, and immune to a flapping network mount.

1. **Harden ****`.gitignore`**** by merging**, never overwriting: keep the user's existing rules and append
sections for secrets (`.env*`, `.secrets*`, `*.pem`, `*.key`, `id_*`, `*_ed25519`, token dirs),
machine state (`*.db`, `*.db-wal`, `*.db-shm`, `*.sqlite*`), backups (`*.bak*`, `*.orig`, `*.tmp`),
macOS/Synology metadata (`@eaDir/`, `._*`), and named PII paths (`Memory/raw-*.json`,
`Memory/sessions/`).

1. **Rewrite:** `brew install git-filter-repo` then
`git filter-repo --force --invert-paths --path-glob '._*' --path-glob '*/._*' --path-glob '@eaDir/*'<br>   --path-glob '*.env' --path-glob '*.env.*' --path-glob '*.bak*' --path-glob '*.db*'<br>   --path '<explicit pii path>' …`. Path globs match the full path, so include both `._*` and `*/._*`.
Confirm the file count dropped and that `git ls-files | grep -E '…'` returns nothing.

1. **Commit the new ****`.gitignore`****, then ****`git push --force origin <branch>`** (filter-repo removes
`origin`; re-add it).

1. **Reconcile the live working copy or the purge gets undone.** With the checkout open on the old
history: `git fetch origin && git reset --mixed origin/main` — `--mixed`, **not** `--hard`, so the
purged files stay on disk as ignored-untracked data instead of being deleted. Then
`git checkout origin/main -- .gitignore` (a mixed reset leaves the *old* ignore file in the worktree,
which is how `git add -A` re-adds everything you just purged). Verify with
`git check-ignore -v <path>` and `git add -An` before letting any nightly commit job run.

1. **Verify from the outside**: repo tree via API shows no junk paths, the purged file returns **404**,
and `git ls-remote` HEAD matches your new commit.

## Pitfalls

- **A force-push does not unpublish.** The old commit stays fetchable by SHA on the host until GC
(`GET /commits/<old-sha>` → 200). Say so, and name the real remedy (support purge request, or
delete/recreate the repo) rather than implying the exposure is closed.

- **Every other clone must be re-cloned or reset.** A different edge still on the old history will push
it straight back; call that out explicitly when the repo is synced across machines.

- **A stale ****`index.lock`**** looks like a broken repo.** A network hiccup or interrupted run leaves it and
every command reports "may have crashed in this repository earlier"; check no git process is running,
delete `index.lock`/`config.lock`, retry.

- **PII is not a secret but it is still an exposure.** Transcripts, derived notes and peer profiles in
a public repo are readable by anyone; if purging them would destroy the user's backup, offer making
the repo private instead of deciding for them.

- **Ignoring a path does not untrack it.** `git ls-files -ci --exclude-standard` must come back empty
after the rewrite, or the file is still tracked and the ignore rule does nothing.