---


name: parcel-delivery-tracking
description: "Track parcel status and carrier disruption news."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
hermes:
tags: [Parcels, Shipping, DHL, PostNL, Tracking, Logistics]
related_skills: [google-workspace, blocked-page-recovery]


---


# Parcel Delivery Tracking

## When to Use

Any "where is my package", "is it stuck at the sorting centre", "is there a
carrier strike / delay" question — DHL, PostNL, Amazon, Marktplaats, a webshop
order — when the answer needs live carrier status rather than the user's memory
of it.

Answer "where is my parcel / is it stuck / is there a strike" from live carrier
tracking plus mail evidence — never from the user's description alone.

## Procedure

1. **Enumerate what is actually in flight, from mail.** Search both accounts for
the carrier and for tracking-number shapes, then read the matching messages:

  ```bash
  G="$HOME/config/google"
  $G/gpers gmail search "from:dhl OR from:postnl OR JVGL newer_than:30d" --max 30
  $G/gpers gmail get <MESSAGE_ID>        # JSON with a plain-text body
  ```

  Regex the tracking numbers out of `subject` + `snippet` and group by number.
  A number whose last mail says *collected / delivered / in handen* is closed —
  still confirm on the live page before telling the user it landed.

1. **Pull live status per number** with the carrier's consumer track-and-trace
URL (patterns in `references/carriers-nl.md`). These are JS SPAs, so load
them in the browser and read `document.body.innerText` after a ~5 s settle —
`curl` returns only "You need to enable JavaScript to run this app".

1. **Judge whether it is actually stalled before calling it stalled.** Compare
the newest tracking event with the timestamp of the newest carrier mail. The
notification is sent at the moment of the event, so *"processed at the
sorting center"* on the same day as the "going to a locker" mail is normal
movement — a stall is the same status with no new event across days.

1. **Only then check for disruption** (strike, sorting-centre outage) — and
only when it would change the advice. News search via Google News RSS beats
an engine that may be captcha-walled:

  ```javascript
  https://news.google.com/rss/search?q=DHL+staking+when:45d&hl=nl-NL&gl=NL&ceid=NL:nl
  https://news.google.com/rss/search?q=DHL+Netherlands+strike+when:45d&hl=en-US&gl=US&ceid=US:en
  ```

  Run the query in both languages and with several phrasings (`staking`,
  `stakingen`, `sorteercentrum`, `vertraging`); parse `<title>` + `<pubDate>`
  from the XML.

1. **Report per parcel**: tracking number, sender, one-line live status, the
next expected event, what is missing, and one recommended action. State
plainly that a news check found nothing and give the window searched.

## Rules

- **A citation-free "stuck" is not allowed.** Quote the literal tracking status
string and the time it was reached; otherwise say status unknown.

- **The status headline renders without a postcode; the event timeline does
not.** If detail matters, ask for the postcode — never guess one, and never
present the headline as if the full history were read.

- **A parcel the user mentions but mail does not show is a gap, not a licence to
substitute.** Name the searches that came back empty and ask for the tracking
number or sender. Do not quietly answer about the nearest open parcel instead.

- **One live check per parcel per session is enough.** Don't offer a standing
watch unless asked; if offered, say what it would alert on (e.g. the pickup
code landing).

- Locker/service-point parcels that were never collected become returns after
the carrier's hold period — mention the deadline when a parcel is sitting
ready for pickup.

## DHL eCommerce NL — essentials inline

Tracking URL (browser only, JS SPA):
`https://my.dhlecommerce.nl/go-track-trace?role=consumer-receiver&tc=<BARCODE>`

Status strings and what they mean, in delivery order:

`JVGLP` + 8 digits = locker/service-point parcel; `JVGL` + 20 digits = home
delivery. Barcodes the user pastes that have **no mail at all** in either
mailbox are sender-side or third-address shipments — say so.

## Carriers

`references/carriers-nl.md` — NL endpoint patterns, tracking-number formats, and
what each DHL eCommerce status string means.