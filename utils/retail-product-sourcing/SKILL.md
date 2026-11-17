---


uuid: 41324dc8-ccd9-81da-aaea-e0ffaa7d02f6
name: retail-product-sourcing
description: "Use when shortlisting purchasable products against a spec."
version: 1.1.0
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

- "What are my options / what should I replace X with" in a fast-moving gadget category (AR glasses, VR headsets, handhelds).

- Deciding whether a supplier is accessible to a private individual.

## Hard rules

1. **Shortlist only — never buy, add to cart, or "just handle it".** Deliver product + price + specs + link.

1. **Prefer consumer-accessible suppliers.** Richard has no KVK/company registration: Sligro, Hanos, Makro and other card-only trade wholesalers are out unless he already holds a card. Flag a gated supplier as gated rather than recommending it.

1. **Be honest about the spec.** If nothing meets the bar, say so with the evidence (e.g. gauge inferred from weight) rather than overselling the closest compromise. Label derived values as estimates, never as verified facts. Same rule for software-dependent capability: when a feature (multi-screen, spatial anchoring, app support) decides the purchase, quote the manufacturer page or mark it "confirm before buying" — a feature the vendor's own software used to provide can be dropped by an app cancellation, so hardware-only claims are the ones worth trusting.

1. **Price the variant, not the model.** One model splits into separate listings per colour/storage, each with its own price and often its own seller — enumerate every variant before calling anything cheapest (same 1TB phone in one shop: black €1,819 vs white €2,089; across shops: €1,445 vs €1,819). When the cheapest listing is a marketplace partner rather than the shop itself, quote the seller name, its rating and who fulfils, and check that same seller on other marketplaces — one partner was €84 cheaper on Amazon than on its own bol listing, and another sat at 7.6/10. The buyer is choosing a warranty counterparty, not just a number.

## Access routing (what actually works)

- [**Amazon.nl**](http://amazon.nl/) — primary, scrapeable. `~/.hermes/scripts/amazon_nl_search.py "q1" "q2" ...` runs curl search and parses `data-asin` + `€` price rows to JSON. Space queries: a burst of many gets rate-limited (stub ~1KB, 0 ASINs) — cooldown ~30s, then retry one query at a time. Other Amazon locales (`.de`) serve the bot page to plain curl and parse to **0 rows** — don't add them to the same script run; use [amazon.nl](http://amazon.nl/) or the browser. Fetch retailer HTML with `--compressed`: without it Amazon answers gzipped and the binary parses to zero rows. Add `&s=price-asc-rank` to the search URL for cheapest-first and skip the price parse entirely. The seller/fulfilment line is **not** in the curl HTML — open `/dp/<ASIN>` in the browser and read `document.body.innerText` around `Shipper / Seller` (plus `Only N left in stock` and the delivery date) to name who actually ships it; that is the difference between Amazon-retailed stock and a partner listing.

- **Coolblue** — `https://www.coolblue.nl/zoeken?query=<q>` answers 200 to curl (~130 KB), but the search page is now a Next.js app: the per-card `application/ld+json` Product blocks are **gone** and regexing them returns 0 rows. Extract the `/product/(\d+)/([a-z0-9-]+)` hrefs from the search HTML instead, then fetch each PDP (`curl -sL https://www.coolblue.nl/en/product/<id>/x`) and take the **first** `"price":<n>,` in the page — that is the product price; later matches are recommendations and accessory bundles. Colour variants are distinct product ids at genuinely different prices, so price every variant you found, not just the first. Range is mainstream consumer only: enthusiast peripherals (Keychron, Razer, Zowie, ProtoArc, Kensington) return an empty set. Empty from Coolblue means "not stocked here", not "not sold in NL" — fall back to [Amazon.nl](http://amazon.nl/).

- [**Bol.com**](http://bol.com/) — `curl -sL --compressed` answers **200** on both `https://www.bol.com/nl/nl/s/?searchtext=<q>` and the product pages, so try curl before reaching for the browser. Product page: price in `De prijs van dit product is ([\d.]+) euro(?: en (\d+) cent)?`, list price in `De adviesprijs is`, seller in `Verkoop door…Verkoop door <NAME> beoordeeld met een <x> uit 10`. Ignore the `'{{euros}}' euro en '{{cents}}' cent` hit — that is the i18n template in the JS bundle, not a price; take the first literal-price match. Colours are separate product pages (pull `/nl/nl/p/<slug>/<id>/` hrefs from the search HTML) and each carries a different partner at a different price, so harvest them all. A `Black Friday deal` line followed by `Meestal <was-price>` and `Adviesprijs <list-price>` is bol's live discount flag. Bol carries AR/VR glasses and consoles that Coolblue misses, but not every niche headset.

- **Marktplaats** — `~/.hermes/scripts/marktplaats_search.py "q1" "q2" ...` returns title, price, condition, location, url from the Next.js payload. Many listings are `priceType: BIDDING` and print as `-`/`bieden`: a dash means *no asking price*, never "cheap". Mobile-phone-case and accessories noise drowns generic queries ("pico 4" returns water pumps) — use brand + model and filter titles in Python.

- **Dutch PC/enthusiast shops** — Megekko answers 200 but is a JS SPA (only a site-level `ld+json`, no product rows); Azerty 403s; Alternate `/search?q=` 404s. Don't scrape these for prices — [Amazon.nl](http://amazon.nl/) is the reliable path for enthusiast brands.

- **MediaMarkt / Action / Wehkamp / BCC** — plain pages return 200. MediaMarkt search is a Next.js app: names sit in `"name":"…"` and prices in `"price":{"__typename":"CofrPriceFeaturePrice","amount":1799,"discount":150,…}` — `amount` is the current price and `discount` the cut off list price, so a live promo is visible without opening the PDP. BCC's `/zoeken?q=` 404s while `/search?q=` answers 200, and Wehkamp doesn't stock phones.

- [**Samsung.com/nl**](http://samsung.com/nl)** buy pages** (`/smartphones/<model>/buy/`) are the price-and-voucher oracle for a new Samsung: the page JSON carries `"displayName":"1 TB｜16 GB RAM","price":"2149","promotionPrice":"1999","stockLevelStatus":"inStock"` per storage option, and `specialMessage` carries live discount codes (e.g. `-10% met code: <CODE>`, period in `priceBarDisclaimerText`). Quote the official price net of the code — it is often within €50–100 of the cheapest retailer and is the fallback when partner stock is thin.

- **Dutch supermarkets (AH, Jumbo, Dirk) are not a source for specialist imports.** They carry the mainstream range only, and their sites do not serve product data to curl (AH's public search API answers "Access Denied"; Jumbo/Dirk return no rows). For French/Italian/specialist goods go straight to a specialist deli or an EU importer — see the food reference.

- **JS single-page shops** (e.g. Horecaplein) return an empty shell to curl and ignore `?q=`/`?s=` server-side. Use the browser, or read a product URL the user pastes.

- **Cloudflare-fronted pro shops** (e.g. Nisbets) show "Just a moment..." to curl but work in a real browser; they sell to the public, so they are a valid answer to "consumer-accessible", just not scrapable.

- **Shopify shops** (detect `cdn.shopify` / `Shopify.theme` in the HTML): `https://<shop>/products.json?limit=250&page=N` returns the whole catalogue — title, `price`, `compare_at_price` (the "was" price = current specials), handle. No auth, ~250 products per request. This is the fastest way to benchmark a competitor's entire range and spot their live discounts in one call.

- **WooCommerce shops**: `/wp-json/wc/store/products` frequently 404s (Store API disabled). Fall back to the `product-categorie/<slug>/` listing pages and split on `<li class="product">`; titles are in `woocommerce-loop-product__title`. See the pitfalls table for the price parse.

- **Availability oracle before spec sheets.** For a category you don't follow closely, first prove whether a product is sold in NL at all: the manufacturer's own site search (e.g. `samsung.com/nl/search/?searchvalue=<product>`) answering "Geen resultaten", plus no listing on bol/Coolblue/[Amazon.nl](http://amazon.nl/), means *not sold here* — say that and stop writing spec prose about it. Models that exist only as third-party accessories on Amazon (cases, lens caps) are a strong hint the device itself isn't in NL retail yet.

- **Brand stores and tabbed product pages** ([viture.com](http://viture.com/), [xreal.com](http://xreal.com/)): `Specs` and `What's in the Box?` are client-rendered and only exist after a click. Click the *leaf* element whose trimmed text equals the tab label (`e.children.length === 0`) — clicking a wrapper that merely contains the label does nothing — then read `document.body.innerText`. The box-contents list is the fastest way to answer "what else must be bought", and it varies between sibling SKUs of the same device.

- **Tweakers Pricewatch** sits behind a "bevestig dat je geen robot bent" wall in the browser; use bol/Coolblue/[Amazon.nl](http://amazon.nl/) as the price landscape instead of retrying it.

- **When general search fails** (Bing/DuckDuckGo return unrelated junk or bot-wall on localized queries), stop fighting it: probe candidate domains with `curl -s -o /dev/null -w '%{http_code}' -A "$UA" https://www.<domain>/` in a loop, and walk a known directory/aggregator for that niche instead of a search engine.

## Deriving specs listings hide

- **Item weight is the best thickness proxy for metal pans.** A 40×30×2.5 cm 304 tray at ~1.2 mm weighs ~1.1–1.4 kg; at ~0.6 mm ~0.6–0.8 kg. Read `Gewicht van item`.

- **Normalise multi-packs.** The headline weight is for the SET — divide by pack count (grep `set van N`, `N stuks`, `N-delig`). A 4-pack at 1.7 kg is ~0.43 kg/pan = thin, not thick.

- **Gastronorm (GN) shallow pans are the pro equivalent of sheet pans** and are consumer-buyable: GN 1/1 = 530×325 mm (≈ half-sheet, but longer than US 460×330 — check oven width); GN 1/2 = 325×265 mm (≈ quarter-sheet). A 20 mm rim acts as a stiffener, so a rimmed GN pan resists warping better than a flat tray of the same gauge.

- **Material codes:** 304 / AISI 304 / 18-10 = food-grade stainless; "gelegeerd staal" = alloy steel, not stainless.

- **Fitted parts (tyres, tubes, filters, belts):** the machine maker's site rarely lists the size. Read the marking on the existing part — a tyre sidewall ETRTO such as `55-406` (or `20 x 2.15`) is authoritative. Where exactly one variable cannot be verified remotely (valve type Schrader/Presta/Dunlop), give the correct product for each variant, state that it is the one unknown, and ask for that single check — do not guess or pad with gear he did not ask for.

- **Same product, two SKUs ("universal" vs "for Mac", "S" vs plain):** the difference is almost always **box contents or connectivity**, not the device. Coolblue product pages embed `"includedInBox":[...]` and `"price"` in their JSON — fetch both SKU URLs and diff that array. (Logitech's "for Mac" MX Master 4 ships **without** the Logi Bolt receiver; the universal includes it, at the same price.) Product URLs are extractable from the search HTML as `"https://www.coolblue.nl/product/<id>/<slug>.html"`.

## Pitfalls

## Timing a purchase (Black Friday / sale windows)

- Black Friday is the last Friday of November; [Amazon.nl](http://amazon.nl/)'s event lands in the last third of the month and bol starts tagging deals weeks earlier. Check bol's `Black Friday deal` + `Meestal` lines before claiming "no discount yet".

- Give each candidate a **target price** derived from the current best price (typically 10–20% below), not a vague "wait for a sale". Offer a daily price watch (see the `product-price-monitor` skill) rather than suggesting he check manually.

- Where a second use case is only *partly* served by one device, price the split (cheap device for job A + used device for job B) — it is often the same money as the one compromise device and each half is good at its job.

## Presenting the shortlist

For a "cheapest price on X" request, lead with the single cheapest **verified** listing in full (price, seller, stock, delivery date, returns window), then the rest as a short ladder with the gap to the leader ("+€54", "+€374") so he can see what the convenience costs. Flag spec contradictions between listings of the same SKU rather than quietly picking one.

Group by size/spec, one line each: **name — spec (material, size, gauge estimate) — €price — link**. Then a short honest verdict: does it meet the bar, and if not, what the next step is (heavier gauge, different supplier). Keep it tight; no menus of process narration.

For food/meat sourcing — Dutch cut names, direct-farm suppliers, wholesaler gating, cross-border shops, EU importers (tinned confit, French specialities) and long-sous-vide value cuts: `references/nl-food-and-farm-direct.md`.

For display wearables — AR glasses vs VR headsets, 3DoF vs 6DoF anchoring, diopter support, accessory tiers, and what a USB-C hub actually has to pass: `references/wearable-displays.md`.