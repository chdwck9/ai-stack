---


name: reverse-engineer

uuid: 3fe24dc8-ccd9-814a-b1be-c39d71122e0d

version: 1

description: "Reverse Engineer"

scope: hub

last-used: "2026-10-19"

thinking: "Medium"

temperature: 0.3

resources:

  - "@Resource-Index"


---


# Reverse Engineer

Use when a claim depends on a **shipped artifact** and no source is available: a native binary or core dump, an APK/IPA/MSIX/DMG, an Electron/ASAR or extracted JavaScript tree, a firmware image, a packet or signal capture, a SQLite snapshot, or a live app's runtime behavior. REA (`rea-agents`) supplies the engines — Hopper/Ghidra/IDA/Kuna for native, JADX for Android, browser/Electron bridges for runtime — and returns every finding with its evidence.

Runs from the **local base**: the installed `rea` CLI, or `npx -y rea-agents@6.7.0`. No MCP server is registered on this host and none is needed. Skip REA for ordinary analysis of a complete source repository — use @github and normal repository tools.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Confirm authorization and the exact target.** Only artifacts Richard owns or is explicitly authorized to inspect. Establish one clear local path or package name; if the target is "my app" with no name, path, or prior selection, ask before searching. Never pick an example app on his behalf.

1. **Confirm the base before diagnosing.** Prefer an installed `rea` CLI (`rea --help`); otherwise `npx -y rea-agents@6.7.0 <command> --json`. Do not install engines, upgrade Node, or register an MCP server to get started — only a reported *missing provider* justifies engine setup, and that needs approval first.

1. **Route the target first, then work summary-first.** Match the artifact to its first command below; ask for `detail: "summary"` on anything large or of unknown size, then page the retained reference with `rea inspect-analysis-view`. A truncated result is a preview, not canonical output — go back to the retained ID rather than re-running the producer.

1. **Hold the evidence doctrine.** Every conclusion is an **Observation**, an **Inference**, or an **Unknown**, tied to its Evidence ID. Static analysis never observed execution. A runtime request executes only the declared target and actions — never broaden either.

1. **Plan multi-feature requests as a staged checklist** (questions × required evidence) with a finding ledger linking each answer to Evidence IDs and remaining unknowns. Reuse an existing session or exported bundle.

1. **Finish and close.** Explain findings in plain language tied to evidence, separate observed behavior from design choices, then close any native session opened.

### Routing (first command by artifact)

- **ASAR / extracted JavaScript / Electron tree** → `rea analyze-javascript-application <path> --json`

- **Archive or package inventory** (ZIP, APK, IPA, MSIX/AppX, DMG) → `rea inspect-artifact <path> --json`

- **Native binary or library**, or a macOS `.app` → `rea analyze <path> --provider ghidra --json`, then `rea function` / `rea decompile` / `rea search` / `rea xrefs` / `rea instructions` / `rea trace`

- **.NET assembly** → `rea inspect-managed-assembly` · **Go metadata** → `rea inspect-go-binary` · **Rust metadata** → `rea inspect-rust-binary`

- **SQLite snapshot** → `rea inspect-sqlite-database <path> --json` (schema first)

- **Android APK code, firmware, packet/signal captures, WASM, EVM bytecode, core dumps, PE resources, browser/Electron runtime** → MCP-side capabilities. Check `rea capabilities --json` first; if the local base cannot do the job, say so plainly rather than approximating it.

## Examples

- **Typical.** "How does search work in Discord?" → `rea analyze-javascript-application "/Applications/Discord.app/Contents/Resources/app.asar" --json` → page the reference → trace the feature → evidence-linked explanation, then a build-it-here version with normal coding tools.

- **Edge — native.** A macOS `.app` with no sources → `rea analyze "<app>" --provider ghidra --json`, `rea function` on the entry of interest, `rea decompile` for pseudocode. Report a missing engine as a prerequisite, not a failure.

- **Boundary — no authorization.** "Reverse engineer the Miro backend so we can clone it." → decline an unlicensed or unauthorized target, say why, and offer the same analysis on an artifact Richard owns or an authorized scope.

## Boundaries

- Authorization first: no target without ownership or explicit permission; stop and explain when scope is unclear.

- **Local base only.** Run from the `rea` CLI. Do not register an MCP server, edit Hermes config, or install Hopper/Ghidra/IDA/JADX without Richard's explicit approval — that is a reviewed action, not an autonomous one. REA never upgrades Node, npm, Homebrew, or Java either.

- Never state an inference or an unknown as fact; preserve stated limitations and coverage gaps.

- Adapted, not vendored: this routes the upstream REA workflow into Richard's conventions. Upstream text (morluto/rea, MIT) is rewritten, never copied; refresh the routing after a REA major version change.

- Don't reach for REA when ordinary source-repo analysis answers the question.

## Output

A findings brief with, at minimum:

- **Target** — path/name, SHA-256 where available, command/provider used.

- **Questions** — the checklist and each one's status (answered / partial / unresolved).

- **Findings** — grouped as Observation / Inference / Unknown, each with Evidence IDs.

- **Limitations** — what was not searched and what cannot be concluded.

- **Unresolved** — open questions worth a next pass.

Before finishing, verify every required element exists and passes. Anything missing → do the work; do not finish.

## Resources

- @Resource-Index — resolve every @handle.

- Base: `npm install --global rea-agents` then `rea --help`; `rea update` refreshes. Node 22.x (>=22.19), 24.x (>=24.11), or 26+; this host has Node 26.0.0 / npm 11.12.1.

- Providers: `rea providers --json` / `rea capabilities --json` / `rea doctor --json`. Native needs a bring-your-own engine (Ghidra, Hopper, IDA, Kuna); static JS/Electron needs none.

- Upstream: the REA project (`morluto/rea`, [rea.tools](http://rea.tools/)), MIT. Add a `@REA` handle to @Resource-Index if this becomes a standing reference.

## Next steps

Invoke with a target plus a question: "Reverse engineer `<artifact>` and explain `<feature>` — with evidence."