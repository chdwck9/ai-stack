---


name: active-background-check
uuid: 40e24dc8-ccd9-817a-b76d-f963e35b8f23
version: 1
description: "Use when verifying identity of unknown contacts."


---


# Active Background Check

Use when verifying identity of unknown contacts.

## When to Use

Unsolicited outreach from an unverified person, recurring cold-contact names that appear on and off, or any name Richard is asked to check before engaging.

## Procedure

### Step 1 — Gather handles & anchors

Read existing records:

```bash
grep -ri '<name>' ~/.hermes/cache/scratch/morning/pers_unread.json
```

Extract identifiers: email(s), phone, LinkedIn URL, company, social handles, any known domain.

**Pitfall:** Don't skip local records — prior emails often contain more anchors than the current message.

### Step 2 — Search engines (rendered, not curl)

Use browser tool, NOT `web_extract`, because Google/Bing HTML returned by curl is fragmented and selector-dependent. Also `web_extract` fails with OpenAI Native backend (search-only).

```python
import subprocess, time
subprocess.run(['osascript', '-e', 'tell application "Brave" to quit'])
time.sleep(8)
subprocess.run(['pkill', '-9', 'brave'], capture_output=True)
time.sleep(3)
new_tab("https://www.google.com/search?q=%22Full+Name%22+%22company%22", session="bg_search")
wait_for_load()
```

Extract via JS `querySelectorAll('h3')`. Navigate links in same session. Get body text with `document.body.innerText.substring(0, 6000)`.

**Pitfall:** DuckDuckGo HTML mode and raw curl against Google/Bing return mangled markup. Use browser JS extraction for SERP parsing.

### Step 3 — LinkedIn verification

Navigate to found LinkedIn URL. Extract publicly visible data via `document.body.innerText`. Accept partial:

- Headline + employer = verified employment claim

- Follower count + posting history = active professional, not throwaway account

- Education = corroborating detail

**Pitfall:** Do NOT scrape hidden experience sections — they require auth. Assess from what IS visible.

### Step 4 — Corporate email domain match

Verify job-posted emails match claimed employer's domain. A corporate email at verified subdomain confirms employment. Gmail with no corporate alias = yellow flag (common for agency recruiters or personal preference). Typosquats = note as error, don't immediately assume fraud.

If only Gmail exists, flag it but don't dismiss.

### Step 5 — Cross-reference social profiles

Check Twitter/X handle, GitHub, other public footprint. Look for consistency: same name, related activity, bio coherence.

### Step 6 — Compile report

Output compact summary:

- **Verified identity** table (name, role, employer, location, key URLs)

- **Corporate email verification** status

- **Scope & activity** observed

- **Signals assessment** (positive indicators, neutral/worth-noting items)

- **Bottom line** assessment

- **Recommendation** (how to proceed)

Format for Discord: bullet lists, tables where helpful, max ~30 lines.

## Pitfalls

- **Brave lock:** browser_exec blocks silently while Brave holds SQLite locks. Kill Brave first (`osascript` quit + wait + `pkill`), then retry.

- **Login walls:** LinkedIn, [Apollo.io](http://apollo.io/), RocketReach all require auth or show bot-blocks. Extract what's visible; stop after one attempt.

- **Search result fragmentation:** Google snippets in curl output are unreliable. Always use browser JS extraction.

- **One-off Gmail is not proof of fraud:** Many legitimate professionals use personal email for recruiting outreach.

- **Never assume scope from title alone:** A Senior TA Partner at a large org may handle specific divisions only.