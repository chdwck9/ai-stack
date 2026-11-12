---


uuid: 41324dc8-ccd9-8126-9a1a-f13b0fe50cef
name: product-shortlisting
description: "Use when shortlisting products to a spec."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
hermes:
tags: [shopping, research, scraping, shortlist, retail]


---


# Product shortlisting

Research and rank purchasable products against a stated spec, returning a link-bearing shortlist with honest confidence. Never purchase.

## When to Use

- "Shortlist X for me", "find the best Y under these constraints", "which of these won't do Z".

- A spec includes both a hard material/feature constraint and a behavioural one ("stainless **and** won't warp").

## Core rules (always apply)

1. **Separate the hard constraint from the real problem.** "Stainless steel is a must" and "must not warp" are different requirements: material vs gauge/thickness. Solve the mechanism, keep the hard constraint, and say which is which.

1. **Probe access before promising a shortlist.** Test each retailer with a browser user-agent and check HTTP status *and* body size; a 200 can still be a bot-challenge page. If a site is walled, do not fabricate listings — try the browser, an API, or offer accessible alternatives.

1. **Search by the physical attribute, not the market's name.** US product names ("half sheet", "quarter sheet") do not map onto EU listings; search dimensions in cm and local language terms.

1. **Extract structured fields and dedupe by SKU.** Each row needs title, price, identifier, and URL.

1. **Never invent an unpublished spec.** When the decisive attribute is missing (gauge, thickness, wattage), derive it from a physical proxy and label the estimate as such.

1. **Normalise per unit.** Multi-packs inflate the headline weight; divide by pack count before comparing.

1. **Be honest when nothing meets the hard spec.** Recommend the better source class (specialist/commercial supplier) rather than dressing a compromise as a fit.

1. **Never purchase.** Shortlists and links only; buying needs the user's account and payment.

## Procedure

1. **Restate requirements.** Write the hard constraints vs the soft ones.

1. **Probe retailers.** For each candidate site: `curl -s -o /dev/null -w '%{http_code} %{size_download}' -A "<browser UA>" -L URL`. A real search page is large; a 403 or a tiny body is a wall.

1. **Search variants.** Query dimensions and synonyms; collect product IDs (e.g. ASIN).

1. **Parse results.** Use the recipe in `references/retail-scraping.md`; dedupe across queries.

1. **Open detail pages** for shortlisted items and pull structured spec fields (material, dimensions, weight).

1. **Derive missing specs** from a proxy (weight → thickness for sheet metal), and compute per-unit figures.

1. **Rank** by the decisive spec for the user's real problem, not by price alone.

1. **Write the shortlist:** rank, name, price, decisive spec + confidence, link. Then state the verdict plainly, including "nothing truly meets X".

## Pitfalls

- **Multi-pack weight treated as per-unit** → overstates thickness/gauge. Divide by pack count.

- **Title says "stainless" but the material field says alloy/aluminised** → trust the structured field, not the marketing title.

- **Assuming a retailer is scrapable, or blocked, without probing** → access varies run to run; test each time.

- **Presenting a proxy estimate as a hard spec** → always label "≈ / estimated".

- **Confusing material with the property the user cares about** (warping is gauge, not steel type; heat is conductivity, not brand).

## Verification

- [ ]Every item has a working link and a price.

- [ ]The decisive spec is sourced, or explicitly labelled as a proxy estimate.

- [ ]Per-unit normalisation applied to multi-packs.

- [ ]The verdict states whether the hard requirement is truly met.