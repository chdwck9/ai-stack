---


uuid: 41324dc8-ccd9-8124-a937-d8313ee8f5a0
name: local-service-availability
description: "Use when finding a nearby service with price and slots."
version: 1.0.0
author: clarity
license: MIT
metadata:
hermes:
tags: [local, availability, booking, barber, salon, treatwell, overpass, postcode, nearby]
category: productivity
requires_toolsets: [terminal, code_execution]


---


# Local Service Availability

"Find me X near <postcode> with availability and a low price this week." The
answer is only useful if it carries **distance, price, and the earliest real
bookable slot** — a list of names with phone numbers does not answer it.

Work the three layers in order: geo → provider inventory → live availability.

## When to Use

- "Find a barber / salon / dentist / repair shop near <postcode>" with a price
and a day constraint (this week, tomorrow, after work).

- Any request where "who is nearby" is not enough and the answer must include
what it costs and when they can actually take you.

- Not for travel or product sourcing — those have their own skills.

## 1. Anchor the area

```bash
MAPS=~/.hermes/skills/productivity/maps/scripts/maps_client.py
python3 $MAPS search "2015EA Nederland"          # postcode -> lat/lon
python3 $MAPS reverse 52.3841068 4.6072928        # sanity-check the street
```

Always include the country in the search string; a bare postcode is ambiguous
across countries. Print the reverse-geocoded street back to the user so they
can confirm the anchor is really their address.

## 2. Enumerate providers (OpenStreetMap)

The maps client's category list has no hairdresser/barber — use Overpass for
any `shop=*` niche. Keep the query small and retry across mirrors, because the
public endpoints 502 and stall under load:

```javascript
[out:json][timeout:60];
nwr(around:1500,<lat>,<lon>)["shop"="hairdresser"];
out center tags;
```

Run it from Python with a mirror loop (`overpass-api.de` → `overpass.private.<br>coffee` → `overpass.kumi.systems`) and short timeouts. A single `nwr` query
with 2-3 retries beats one huge multi-category query that times out and loses
the whole cell.

## 3. Get prices and LIVE slots

Booking platforms are the only source that has both price and availability.
Fetch their **listing** pages with plain HTTP — the listing HTML is
server-rendered and carries everything (per-venue JSON state plus price and
availability chips). Do not chase individual venue detail pages; they usually
sit behind a bot challenge. See `references/treatwell-nl.md` for the exact
URL shapes, the `window.__state__` structure, and the chip parsing.

Distances: haversine from the postcode point, reported in metres (straight
line). Say "straight line" once; do not present it as walking time.

## Output contract

This user wants a shortlist they can act on, not a directory:

- Bucket by **best value** (cheap + good reviews + slots), **closest**,
**cheapest** — one or two lines each: name, address, distance, price,
earliest slot times, rating with review count, opening hours.

- One explicit **recommendation** with the reason (price, review base,
travel time), plus the alternative that fits a different constraint
(evening slot, Sunday, walkable).

- Close with the coverage caveat: platform-listed shops only — local walk-in
shops are often cheaper and publish nothing online.

- Never claim a slot is held or a booking made. Offer to prepare the booking
or to call a shop; the commitment stays with the user.

## Pitfalls

- **Query strings are ignored by Treatwell; filters are PATH segments.**
`?sort=price_asc`, `?page=1`, `?priceMax=` all return the default page — check
`browse.pagination` / `browse.specification.sort` in the returned state to
confirm a filter actually applied instead of trusting the URL.

- **Confirm "this week" against the clock before ranking.** A late-evening run
means today's slots are gone; the first chips will be tomorrow.

- **The closest provider is often not the fastest.** Check the chips before
recommending: a 1.2 km shop whose next slot is ten days out loses to a 2.5 km
shop with tomorrow morning free.

- **Separate the services.** Many venues publish haircut, wash+cut, clipper and
beard bundles as different menu items at different prices; match the one the
user actually asked for and quote that price, not the entry-level lure price.

- **Thin review counts are a real signal.** A 4.7 from 12 reviews is untested;
say so rather than ranking it top on price alone.