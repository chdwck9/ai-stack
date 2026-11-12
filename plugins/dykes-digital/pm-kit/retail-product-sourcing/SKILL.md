---


uuid: 41324dc8-ccd9-81da-aaea-e0ffaa7d02f6
name: retail-product-sourcing
description: "Use when shortlisting purchasable products against a spec."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
hermes:
tags: [shopping, product-research, netherlands, scraping, shortlist]


---


# Retail product sourcing (NL)

Build a shortlist of *purchasable* products that meet a stated spec, verifying the specs that actually matter. Richard decides and buys; the agent researches and shortlists.

## When to Use

- Richard wants a shortlist of shopable products against a spec ("find me a lid for X under €Y").

- Comparing SKUs across NL retailers and verifying a spec the listing hides.

- Deciding whether a supplier is accessible to a private individual.

## Hard rules

1. **Shortlist only — never buy, add to cart, or "just handle it".** Deliver product + price + specs + link.

1. **Prefer consumer-accessible suppliers.** Richard has no KVK/company registration: Sligro, Hanos, Makro and other card-only trade wholesalers are out unless he already holds a card. Flag a gated supplier as gated rather than recommending it.

1. **Be honest about the spec.** If nothing meets the bar, say so with the evidence (e.g. gauge inferred from weight) rather than overselling the closest compromise. Label derived values as estimates, never as verified facts.

## Access routing (what actually works)

- [**Amazon.nl**](http://amazon.nl/) — primary, scrapeable. `~/.hermes/scripts/amazon_nl_search.py "q1" "q2" ...` runs curl search and parses `data-asin` + `€` price rows to JSON. Space queries: a burst of many gets rate-limited (stub ~1KB, 0 ASINs) — cooldown ~30s, then retry one query at a time.

- **Coolblue** — parseable JSON (`"price":..`, product names), but mainstream consumer range only: enthusiast peripherals (Keychron, Razer, Zowie, ProtoArc, Kensington) return an empty set. Empty from Coolblue means "not stocked here", not "not sold in NL" — fall back to [Amazon.nl](http://amazon.nl/).

- **Dutch PC/enthusiast shops** — Megekko answers 200 but is a JS SPA (only a site-level `ld+json`, no product rows); Azerty 403s; Alternate `/search?q=` 404s. Don't scrape these for prices — [Amazon.nl](http://amazon.nl/) is the reliable path for enthusiast brands.

- **MediaMarkt / Action / Wehkamp / BCC** — plain pages return 200.

- [**Bol.com**](http://bol.com/) — 403 to plain HTTP; needs a real browser or its API. Don't burn turns guessing URL params.

- **JS single-page shops** (e.g. Horecaplein) return an empty shell to curl and ignore `?q=`/`?s=` server-side. Use the browser, or read a product URL the user pastes.

- **Cloudflare-fronted pro shops** (e.g. Nisbets) show "Just a moment..." to curl but work in a real browser; they sell to the public, so they are a valid answer to "consumer-accessible", just not scrapable.

- **Shopify shops** (detect `cdn.shopify` / `Shopify.theme` in the HTML): `https://<shop>/products.json?limit=250&page=N` returns the whole catalogue — title, `price`, `compare_at_price` (the "was" price = current specials), handle. No auth, ~250 products per request. This is the fastest way to benchmark a competitor's entire range and spot their live discounts in one call.

- **WooCommerce shops**: `/wp-json/wc/store/products` frequently 404s (Store API disabled). Fall back to the `product-categorie/<slug>/` listing pages and split on `<li class="product">`; titles are in `woocommerce-loop-product__title`. See the pitfalls table for the price parse.

- **When general search fails** (Bing/DuckDuckGo return unrelated junk or bot-wall on localized queries), stop fighting it: probe candidate domains with `curl -s -o /dev/null -w '%{http_code}' -A "$UA" https://www.<domain>/` in a loop, and walk a known directory/aggregator for that niche instead of a search engine.

## Deriving specs listings hide

- **Item weight is the best thickness proxy for metal pans.** A 40×30×2.5 cm 304 tray at ~1.2 mm weighs ~1.1–1.4 kg; at ~0.6 mm ~0.6–0.8 kg. Read `Gewicht van item`.

- **Normalise multi-packs.** The headline weight is for the SET — divide by pack count (grep `set van N`, `N stuks`, `N-delig`). A 4-pack at 1.7 kg is ~0.43 kg/pan = thin, not thick.

- **Gastronorm (GN) shallow pans are the pro equivalent of sheet pans** and are consumer-buyable: GN 1/1 = 530×325 mm (≈ half-sheet, but longer than US 460×330 — check oven width); GN 1/2 = 325×265 mm (≈ quarter-sheet). A 20 mm rim acts as a stiffener, so a rimmed GN pan resists warping better than a flat tray of the same gauge.

- **Material codes:** 304 / AISI 304 / 18-10 = food-grade stainless; "gelegeerd staal" = alloy steel, not stainless.

- **Fitted parts (tyres, tubes, filters, belts):** the machine maker's site rarely lists the size. Read the marking on the existing part — a tyre sidewall ETRTO such as `55-406` (or `20 x 2.15`) is authoritative. Where exactly one variable cannot be verified remotely (valve type Schrader/Presta/Dunlop), give the correct product for each variant, state that it is the one unknown, and ask for that single check — do not guess or pad with gear he did not ask for.

## Pitfalls

## Presenting the shortlist

Group by size/spec, one line each: **name — spec (material, size, gauge estimate) — €price — link**. Then a short honest verdict: does it meet the bar, and if not, what the next step is (heavier gauge, different supplier). Keep it tight; no menus of process narration.

For food/meat sourcing — Dutch cut names, direct-farm suppliers, wholesaler gating, cross-border shops and long-sous-vide value cuts: `references/nl-food-and-farm-direct.md`.