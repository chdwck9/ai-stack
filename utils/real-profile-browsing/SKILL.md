---


name: real-profile-browsing
uuid: 41624dc8ccd981e18192dd5e9556f8ab
version: 1
description: "Use when browsing as the user via their real profile."
last-used: "2026-11-12"
scope: local
thinking: "Medium"
temperature: 0.3
author: clarity
license: proprietary
metadata:
hermes:
tags: [browser, real-profile, cookies, amazon, signed-in, guardrails, mfa]
related_skills: [clarity-capabilities, external-account-access]


---


# Real-profile browsing (act as the signed-in user)

**Scope: Hermes / Clarity only.** This utility drives the user's real browser profile and is private to this
agent: do not publish it, export it, or register it with any other LLM surface (ChatGPT, Claude, Gemini,
Perplexity, Cowork). Hub properties must stay `Type: Utilities`, `Category: utilities`, `Visibility: private`,
`LLM: (none)`. If asked to share it, refuse and explain that it is bound to this machine's Keychain-held
cookie store and would be a live credential anywhere else.

Driving the user's **own logged-in sessions** via `browser.use_real_profile: true`, so no password or 2FA is ever exchanged. Hermes copies the live Chromium/Brave profile to a snapshot dir and launches a browser on **the copy** — the live browser is never driven.

## When to Use

- Richard wants Clarity to act inside an account that has **no API and no OAuth** (Amazon, retailer carts, portals), or where MFA makes credential sharing impractical.

- A prior session reported "signed out" / "Hello, sign in" on a site Richard is definitely logged into — usually a stale snapshot or a cached fallback, not a missing login.

Prefer this over the vault route when MFA is SMS/device-approval: cookies skip the login entirely, whereas a vault fill still hits the OTP wall.

## Setup facts (verified 2026-11-12, Studio)

- Config: `~/.hermes/config.yaml` → `browser: {use_real_profile: true, inactivity_timeout: 120}`.

- Snapshot dir: `~/.hermes/browser-profile/brave` (~900 MB with caches excluded).

- Live source: `~/Library/Application Support/BraveSoftware/Brave-Browser`.

- The launch is keyed `hermes-real-profile@<hermes_home>`; there is **one real-profile browser per home**, not per session.

- `hermes browser --help` exposes only `close-profile` (quits the user's browser — ask first) and `export-signins`.

- Cookies are encrypted with the **Brave Safe Storage** Keychain item. A copy on the same machine and same user decrypts fine; a copy moved to another machine will not.

## Steps

1. **Probe, don't assume.** Launch with a **named session** and read the identity, not just the title:

  ```python
  print(js("navigator.userAgent"))
  print(js("(() => { const a=document.querySelector('#nav-link-accountList-nav-line-1'); return a && a.innerText.trim(); })()"))
  ```

  A signed-in Amazon says `Hello, <FirstName>`; signed-out says `Hello, sign in`.

1. **Check you are on the real profile, not the fallback.** In `ps -Ao args`, the user-data dir must be `.../.hermes/browser-profile/<browser>`. A path under `~/.hermes/cache/browser/chromium/<hash>` is the **bundled, signed-out Chromium** — everything after that point is wasted work.

1. **Refresh a stale snapshot** (only when the fallback is ruled out and the site says signed out):

  ```bash
  SRC=~/Library/Application\ Support/BraveSoftware/Brave-Browser
  DST=~/.hermes/browser-profile/brave
  mv "$DST" "$DST.pre-refresh-$(date +%Y%m%d-%H%M)"   # keep, never rm
  mkdir -p "$DST"
  rsync -a --delete \
    --exclude 'Singleton*' --exclude 'Cache/' --exclude 'Code Cache/' --exclude 'GPUCache/' \
    --exclude 'GrShaderCache/' --exclude 'GraphiteDawnCache/' --exclude 'ShaderCache/' \
    --exclude 'Crashpad/' --exclude 'BrowserMetrics*' --exclude 'GPUPersistentCache/' \
    --exclude 'Service Worker/CacheStorage/' --exclude 'Service Worker/ScriptCache/' \
    --exclude 'component_crx_cache/' --exclude 'extensions_crx_cache/' --exclude 'Cache_Data/' \
    "$SRC/" "$DST/"
  rm -f "$DST"/Singleton{Lock,Cookie,Socket}
  ```

  `rsync` exit **23** ("file vanished") is normal while the live browser writes leveldb logs — harmless for cookies. Verify instead: `ls -la $DST/Default/Cookies` (mtime must be now) and `sqlite3 $DST/Default/Cookies "select count(*) from cookies where host_key like '%<site>%';"`.

1. **Always start the real browser with a fresh session name** after any previous fallback, and confirm the UA/identity again. The fallback decision is cached for the life of a session; reusing the session keeps you signed out no matter how fresh the snapshot is.

1. **Smoke-test before real work:** land on the site, confirm the identity line, perform one small reversible action, and read the confirming counter back (`#nav-cart-count`, subtotal, etc.). Report the evidence.

## Guardrails (non-negotiable)

- **Cart/wishlist adds are in scope. Checkout is never in scope** — not "just this once", not with standing authorisation. Stop at the final step and report.

- **Never touch payment fields.** No card number, CVC, PIN, or bank detail, in the browser or in chat. Vault-only, user-confirmed, and even then the user presses the button.

- **Never accept a password, card number or OTP in chat.** If offered, decline and point to the vault or the real-profile route.

- **No purchase, booking, subscription, or price commitment** without an action-specific approval for that exact item and amount.

- **Human-paced, low volume.** These sites' terms forbid automated access; aggressive loops risk captcha walls and account flags. Report the account risk as the user's decision, not a solved problem.

- **Ask before ****`hermes browser close-profile`** — it quits the user's running browser and loses unsaved tabs. Copying read-only while the browser runs is the default; it works.

- **Leave the user's data as found.** Remove test items you added unless asked to keep them as proof; never clear or reorder an existing cart or saved list.

- **State the privacy surface.** The snapshot holds the user's whole profile — history, bookmarks, saved logins. Say so when you create a fresh one, and give the revoke path: `browser.use_real_profile: false` (Hermes deletes the snapshot store on next launch).

## Pitfalls

- **"Signed out" is usually the fallback browser, not stale cookies.** Check `ps` for `user-data-dir` before re-copying a profile. This cost two wasted attempts on 2026-11-12.

- **A ****`SingletonLock`**** left in the snapshot dir** makes the launcher report the profile "in use by a Chromium in another environment" and silently fall back. `rm -f Singleton{Lock,Cookie,Socket}` in the snapshot dir, then use a new session name.

- **A snapshot rots on session rotation.** Cookie expiry dates looking valid means nothing — Amazon invalidates the server-side session when the user's live browser next visits. Expect a refresh every few weeks; recognise the signature as `Hello, sign in` while cookies look unexpired.

- **The snapshot is a copy, so the live browser keeps its own session.** Both can be signed in simultaneously; that is expected and not a sign of theft or cloning.

- **Headless UA is normal** (`HeadlessChrome/156.0`) even on the real profile — that is Brave in headless mode, not the bundled fallback. Use the `user-data-dir` path and the identity line, not the UA, to tell them apart.

- **`capture_screenshot`**** can time out** on a slow daemon (10s/60s IPC deadlines). The page state read via `js(...)` is the evidence; retry the shot, don't derive state from it.

- **Screenshots reveal real data** (address, Prime status, cart contents). Report only what the task needs.

## No-login alternative for research only

`python3 ~/.hermes/scripts/amazon_nl_search.py "query" ...` does anonymous [Amazon.nl](http://amazon.nl/) search → JSON rows (asin, title, price, url) with no session at all. Use it for price/product research; reach for the real profile only when an action needs the account (cart, order history, subscribe-and-save).

## Verification

- Identity line read back from the site, not inferred from a title.

- The confirming counter/subtotal read back after the action.

- Every claim about state backed by a tool output in the same run; if the action failed, say which step failed rather than describing an intended one.