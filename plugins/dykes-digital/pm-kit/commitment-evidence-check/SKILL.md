---


uuid: 41324dc8-ccd9-819a-be03-c08064a4012f
name: commitment-evidence-check
description: "Use when verifying an appointment or booking exists."
version: 1.0.0
author: Clarity (Hermes Agent)
license: MIT
platforms: [macos, linux]
metadata:
hermes:
tags: [Email, Calendar, Verification, Evidence, Appointments, Personal-Assistant]
related_skills: [google-workspace, email-inbox-triage, calendar-capacity]


---


# Commitment Evidence Check

Answer the question "did we actually have X booked, and when?" with cited evidence, not recollection. The user's memory of an appointment is the *hypothesis*; the mail thread and the calendar are the record. A vague memory ("I thought we had an intake this month but we never saved it") is frequently half-wrong in one direction or the other — the thing exists but is filed under a name nobody would search for.

## When to use

- "Check something for me — did we ever book/get invited to …?"

- "I can't remember whether that appointment is this month."

- "We never saved that as an event, right?"

- Any request to confirm a date, time, address, or counterparty for an appointment the user believes exists.

Don't use for general inbox triage (use `email-inbox-triage`) or raw Gmail/Calendar operations (use `google-workspace`).

## Procedure

### 1. Search mail by every plausible handle, not one keyword

Start from the organisation or person name, then widen. Multi-account: Richard's personal Gmail and his work Workspace account are pinned by separate `HERMES_HOME` wrappers (`~/config/google/gpers` = personal [chdwck9@gmail.com](mailto:chdwck9@gmail.com), `~/config/google/gwork` = [dykes.digital](http://dykes.digital/)). Personal matters (children, school, healthcare, family) live in **gpers**; use `gwork` only when the thread plausibly touched work.

```bash
~/config/google/gpers gmail search 'kentalis' --max 50
~/config/google/gpers gmail search 'Arthur intake' --max 20
```

Run 2–4 varied queries (org name, person name, the subject noun in the sender's language) and print `date | from | subject` for each hit rather than reading bodies blindly. Postal/agency mail arrives in the local language — search the Dutch/German term too (`intakegesprek`, `afspraak`, `Termin`), not only the English one.

### 2. Read the thread, not the subject line

A subject like "Invitation: X @ Mon Nov 23" is the confirmation; the substantive letter is usually a separate message. Read the *earliest authoritative* message (the organisation's own letter), not just the newest reminder.

Bodies often come back empty from `gmail get` when the payload is nested multipart (calendar invitations) — use `scripts/gmail_body.py` from this skill, which walks parts recursively and prints only `text/plain`. Never dump headers: they are thousands of characters of DKIM and flood the context.

### 3. Check the calendar before repeating the user's premise

Search a **narrow window**, not the whole month:

```bash
~/config/google/gpers calendar list --start 2026-11-18T00:00:00+01:00 --end 2026-11-28T00:00:00+01:00
```

`calendar list` silently caps its result set (≈25 events) — a month-wide range on a busy calendar truncates before the date you care about, which reads as "no event". Query the week around the candidate date, then the exact day when you need the event's `location`/`id`.

Match on **location and time**, not title: an accepted invite frequently lands as a bare-titled event ("Kentalis") with no description, so title search fails while the event is sitting there confirmed.

### 4. Reconcile the three sources

State explicitly which of these is true and on what evidence:

- Mail invitation exists → date/time/address/counterparty, quoted from the letter.

- Calendar event exists → its actual summary/location/status, and how it differs from the letter (bare title, wrong duration, missing description).

- An attendance confirmation was actually sent → only claim this if you can read the reply. Replies sent inside an encrypted provider are unreadable to Gmail; treat confirmation as **unknown** and say so.

### 5. Report and offer the smallest fix

Shape the answer as: what the mail says (with sender, date, quoted key sentence) → whether/where it is already on the calendar → recommendation → open loop → "Needs Richard".

Correcting the user's premise is part of the job; do it in one clause ("found it — and one correction: it is on your calendar already, under a bare title") and move on, never with an apology or a lecture.

When the event exists but is uninformative, offer to make it self-explanatory (title naming the purpose, person and subject; description with address and source mail). Editing summary/description of an event that has other guests can notify them — offer, and wait for a yes, before writing.

## Pitfalls

- **Never report "not saved" from a single keyword or a wide calendar range.** Both failure modes produce confident false negatives; a factual negative needs a narrow-window calendar query plus two mail searches.

- **`gmail get`**** returning ****`"body": ""`**** is a payload shape, not an empty message.** Calendar invitations and secure-mail copies nest `multipart/alternative` inside `multipart/mixed`; only a recursive walk reaches the text.

- **Don't trust an event title as the fact.** Verify against the letter and match on address/time instead.

- **Encrypted notifications are not the content.** Secure-mail provider notices are stubs; their "Copy:" twins often carry the full plaintext. See `references/secure-mail-providers.md`.

- **Don't equate "invitation received" with "we said yes".** Attendance confirmed only by a readable reply.

- **Keep the sensitive content minimal.** Quote the one sentence that fixes the date; do not reproduce a child's clinical letter in chat or in notes.

## Verification

- [ ]Mail searched under org name, person name, and the local-language term.

- [ ]At least one message body read from the actual letter (recursive part walk), not a subject or snippet.

- [ ]Calendar queried by narrow window; both presence and absence are evidenced.

- [ ]Reply/confirmation status stated as confirmed, unknown, or outstanding — never assumed.

- [ ]Any proposed calendar edit is offered, not applied.

## Support files

- `scripts/gmail_body.py` — print readable `text/plain` bodies for Gmail message IDs, walking nested multipart.

- `references/secure-mail-providers.md` — Zivver/secure-mail message anatomy and how to get the content.