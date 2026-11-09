---


name: mambu-cost-analysis

uuid: TBD

version: 7

last-used: 2026-10-22

description: "Mambu Cost Analysis"

return: session notebook, findings doc, insights doc

thinking: High

temperature: 0.3

resources:

  - "@Mambu-Cost-Analysis-MCD"


---


# Mambu Cost Margin Analysis

Cost triangulation, resource-sizing, and interpretable tiered-pricing model across Mambu's customer base, built from Salesforce CRM (via BigQuery), CSP billing (CUR-equivalent, BigQuery), and Grafana/Prometheus observability. Standalone initiative — not part of BCaaS or Wally; closest adjacent domain is pricing/packaging work, but not nested under it.

End goal: defensible, human-readable expected-cost predictions to inform FY27 commercial tiering/packaging decisions.

**Current phase**: Discovery complete (sessions 1–2). Session 3: cost k-means tiering + NNLS overhead/product-rate model. **Session 4: k-means tiering replaced by the commercial price-list thresholds** — round 1 = max accounts × 0.98 and max daily API v1/v2 × 0.98 (robust 6σ days), highest dimension wins, below-XS → XS for Dedicated; round 2 = cost floors (cheapest round-1 client per tier), clients only move up — **retired in session 13**. All cost now in EUR from the source's EUR columns, annual Production cost with spike months flattened (4σ), plus `adjusted_cost_eur` (gross × (1 − standard CSP discount)). **Session 13: round 2 retired; round 1 (usage tier) is the cost-tier basis.** On Tiago's CBE-only basis (AWS lines tagged `''`/`monolith`/`mambu`/`cbe`; no `platform` layer, no add-ons; AWS only) minimum floors collapsed (EUR 264 to 58k, each set by one client), P10 floors were non-monotonic and P25 fitted the catalogue worse than round 1, so cost-floor tiering is dropped. Cost is reported on two bases side by side: all-in (the platform layer is a flat ~EUR 41–47k a year per environment) and CBE-only. Round-1 CBE-only median is 0.74×/0.81×/0.85× of the catalogue `base_cost` at XS/S/M. Next: test the non-AWS multiple (≈1.9× all-in) with AWS add-ons put back (non-AWS add-ons sit inside the base), regenerate session-3 Postgres tables in EUR, then modifiers (DR/MPO/SSO). Session 6: platform add-ons (`findings/session-6-addon-cost.md`) — mostly flat € per client, audit trail v2 usage-driven, ~€400k run-rate excess in named clients. Session 8: Tiago's DS-984 sizing compared (the pricing catalog's Dedicated `base_cost` is his recommended cost with his XS dropped, so catalog XS = his XXS) and customer contracts loaded (`findings/session-8-tiago-ds984-comparison.md`). Python env now lives off the drive at `~/.venvs/cost-margin` (in-drive `.venv` is stale); Postgres is on port 5433. Always read `findings/` first — it's the hand-off mechanism between sessions.

## Project instructions

- Ground truth for cost is the CSP billing/CUR export (`gold_csp_cost`), never Grafana/Prometheus (sampled, not billing-grade) — observability data is a feature/allocation-weight source only.

- Every cost/pricing model must expose human-readable coefficients: GLM/GAM as the default (Poisson/Gamma family, log link, `statsmodels`), SHAP only as a bridge from a boosted model when GLM residuals show unexplained variance — and even then, deliver SHAP plots, not the raw model.

- Account-level grain is primary: one fact row per account per billing month (`fact_account_month`). Shared environments are special-cased — cost there is pre-pooled, so the target becomes "share of shared-env cost" (metered/regression allocation), not a directly observed number. Dedicated joins ~1:1 per account.

- **Reporting currency is EUR, cost unit is annual Production cost per client** (mean monthly × 12 over a trailing 12-month window). Gross on-demand is the tiering/comparison basis; `adjusted_cost_eur` is the "after discounts" view.

- No production pipeline until the target schema is agreed and validated. Discovery/schema work only for now: no scheduled jobs, no writes to shared systems. Code should be exploration-friendly and reproducible locally.

- Record BigQuery dataset/table names and Grafana dashboard/datasource names discovered in session back into the project MCD's Resources section — do not leave them undocumented.

## Known traps (do not re-derive these mistakes)

- **`account.hosting_spend`****, ****`.est_margin`****, ****`.mpo_software_spend`** — manually-maintained finance/CSM estimates, not derived from CSP billing. Validation baseline only; never a training feature (would leak the answer).

- **Shared-environment costs are not in ****`daily_unified_costs`** — that table pools Shared costs under `client=NULL`. Use `shared_and_dedicated_customer_costs` with `filter_customer=<name>` instead for any Shared account. Check `account.cloud_service_provider` for "Shared" first.

- **`on_demand_cost`****/****`net_cost`**** in ****`gold_csp_cost`**** are in each row's billing currency** (AWS USD; GCP/Azure/OCI EUR). Never sum them raw. Use `od_cost_in_eur`/`net_cost_in_eur` (source FX, ~1.16 USD/EUR); a standard 1.2 USD/EUR applies only to sources with no EUR column. Session 4 found sessions 3–4 had GCP/Azure EUR mislabelled as USD (understated ~14% vs AWS).

- **Grafana-derived "count" metrics were found fractional** (e.g. `api_requests_count=88038.64`) — a PromQL `avg_over_time()`/`rate()` vs `sum()`/`increase()` bug. Treat every Grafana-extracted metric as untrustworthy until `src/cost_margin/grafana.py`'s query logic is re-audited. Exception: API v1/v2 use `sum(increase([1d]))` — fractions are extrapolation, magnitudes valid.

- **The Grafana daily API cache has systemic spike days** (3 Aug, 27 Aug, 7 Sep 2026: 29/32 clients' max v2 day at 70–110× their median day). Never take a raw max of daily usage — filter with a robust σ first (`threshold_tier.drop_outlier_days`, 6σ).

- **A client can own several production tenants** (League Data 40, UALA/Finvivir/Resurs 3). A Dedicated environment serves all of them — sum usage across tenants (`threshold_tier.client_tenants`), drop noise names (test/temp/demo…), and keep only the resolved subdomain when the sheet's account match doesn't contain it (Vision Bank / Mutual Vision cross-match).

- **Untagged ****`aws_tag_type`**** Master/ReadReplica/Frontend/Background/Cron cost is the core application stack, not a legacy leftover** — present on 83/116 AWS Dedicated clients, ~35% of AWS Dedicated Production cost. A heavy share (Sonae 64%, Check24 65%, TBC 60%) is a real usage–cost mismatch, not removable.

- **Large negative lines in ****`gold_csp_cost`**** are unattributed** — `SavingsPlanRecurringFee` reversals (−€8M), 2022–23 EDP `Discount` lines, refunds: no client, `environment_type` Unassigned. Client-level discount already lives in `net_cost_in_eur` per line; don't add these back without confirming with the table owner.

- **Mean-over-months-present × 12 misleads for anything launched or retired mid-window.** Session 6 first reported audit trail v1 at €954k/yr after it had been switched off (actual 12-month spend €398k, €0 since Jul 2026), and Mambu Insights ×12 from a single month. For add-ons/features use actual 12-month spend plus a run rate (last 3 months × 12, clients present in all 3).

- **Add-on capability tags exist on AWS only**; GCP/Azure add-on cost is inside their base. `streamingapi` carries ~€0 — its cost probably sits in `nakadi` (S3). `aws_detailed_costs` covers only part of the AWS accounts (no usable KMS usage-type split).

- **`Mambu_Subscription__c`**** feature flags are sparse** — filter to active subscriptions before judging population, don't assume NULL means "off."

- **Tiago's DS-984 figures are CBE-only USD, Aug 2024 (S12).** The summary tab labels them EUR but they are USD (his working copy: `OnDemandCostInUSD`; reproduced exactly from BigQuery). CBE-only excludes the `platform` capability layer, a flat ~$40-42k a year per environment that equals the fixed footprint in our cost fit. The catalog `base_cost` is on that basis: compare it with CBE-only cost, never with all-in cost (S11's 'small tiers 2.7x drift' was this basis gap).

- **`aws_tag_capability`**** is not stable over time (S12).** A new `cbe` tag appeared in 2025-26 (>$650k/month by Aug 2026) while untagged fell from 62% to 19% of cost; a CBE filter without `cbe` fakes a 55% fall. For trends use all-Production cost (no tag filter).

- **Single-month discounts are unreliable (S12).** The median AWS client discount ran 17% (Aug 2024), 35% (Oct 2024), 17% (Jan 2026), 55% (Jun 2026 true-up), 26% (Aug 2026). Compare gross for cost trends, and net only on 12-month windows or the standard CSP rate.

- **CBE-only cost exists for AWS only (S13).** Capability tags are AWS-only, so GCP/Azure cannot be restated; clients now off AWS keep a small pre-migration AWS CBE remnant (Bank Ina Perdana) — key the CBE figure on the client's current CSP. A client can also carry almost no CBE-tagged cost while on AWS (Prospa: EUR 264 of EUR 10k all-in). Always state which basis (all-in or CBE-only) a tier ladder or ratio is on; the non-AWS ≈1.9× is all-in and may be overstated by the add-on asymmetry.

- **Pricing catalogue semantics and access (S12).** `@Mambu Pricing & CPQ/.../catalog` returns stale Synology file handles for some files; read it from the SMB share with a guest read-only mount (`mount_smbfs -N -o rdonly //guest@192.168.2.6/Ship <dir>`, path `@Mambu/@Mambu Pricing & CPQ/Mambu Pricing v20`), copy what is needed, unmount. Products are graduated staircases (band width x band rate, summed), environments one flat fee per tier; `minimum_units` is not applied by the calc code; Business Lending equals Mortgages (placeholder); product prices are labelled `$` (converted at the catalogue's 1.2) and environment fees taken as EUR. Loaded to `raw.catalog_*` by `scripts/load_pricing_catalog.py`; maths in `cost_margin.catalog_pricing`.

- **A derived categorical/tier output can pass every internal consistency check while still being wrong for individual entities.** Session 3: GCP/Azure account-count bucketing looked monotonic in aggregate but put 5 of 8 named clients in tiers that contradicted their own cost. Spot-check derived categorical outputs against named, real-world cases the user knows — an aggregate check is not a named-entity check.

## Permissions

**Always:** read-only exploration of BigQuery/Grafana via MCP; draft schema/code locally; read the project MCD and `findings/`.

**Ask first:** any write to BigQuery, Grafana, or Postgres; any change to pricing/tier assumptions that would inform FY27 decisions; updates to the project MCD or Ship record.

**Never:** treat Prometheus/Grafana data as billing ground truth; ship a pricing coefficient without a plain-English explanation; build a full production pipeline before the target schema is agreed.

## Working standards (confirmed over sessions)

- **Reuse before re-deriving.** Check the Postgres cache (`raw`/`staging`/`marts`/`samples`) and `src/cost_margin/` before re-pulling or hardcoding anything. Fresh pull only once the cache is confirmed missing or stale.

- **Document as modular Python + a notebook, every time.** Reusable logic in `src/cost_margin/` (library) or `scripts/`; narrative in a paired `notebooks/0N_*.ipynb` that imports from `cost_margin`.

- **Pilot before fan-out.** Run ~5 units, measure cost, extrapolate, get sign-off before scaling multi-agent/multi-call batches.

- **Notebook-first execution — one notebook per session.** Every session starts `notebooks/0N_<topic>.ipynb`; all Python runs as notebook cells via `uv run jupyter nbconvert --to notebook --execute --inplace` (kernel `cost-margin`). Promote reusable logic to `src/cost_margin/`. Read-only MCP discovery queries are unaffected.

- **Session-based workflow.** Each session produces the notebook, a findings doc and an insights doc (plus optional `sql/00N_*.sql` and library code).

  - **Findings** (`findings/session-N-*.md`) — **Data analysed**, **Processing & method**, **Summary output**.

  - **Insights** (`insights/session-N-*.md`) — **Initial hypotheses** (written before analysis, never back-filled), **What we found** (confirmed / refuted / inconclusive + evidence), **Unexpected or interesting observations**.

- **Question log drives each session.** `insights/README.md` is a running list of **Open** and **Answered** questions, not a session index. Questions are theme-level hypotheses/insight questions about cost, pricing and growth (roughly one per session theme) — data-source and method questions stay in `findings/` open items. It is a plain Markdown numbered list (no bespoke IDs, so Richard can drop in `1. question`); each question is tagged with the session that raised it, e.g. `(S4)`. At session start, either work the questions Richard names, or add new questions to **Open** from the prompt's context before analysis begins. When a question is answered, move it to **Answered** with a one-sentence answer and the answering session tag — in addition to the full evidence in that session's insights file. New open items found during a session go into **Open** too.

- **Match the comparator's basis before calling anything drift.** Session 11 read a 2.7× gap to the catalogue as stale costs; it was an all-in vs CBE-only basis difference (the flat platform layer). Reproduce the benchmark's number exactly on its own basis first, then compare.

- **Codify every adjustment where it's applied.** Rates/thresholds that change a cost or tier (price-list bounds, standard CSP discounts, σ cut-offs) live as named constants with a docstring saying what they are, how they were derived and how to re-derive them (`sizing.PRICE_LIST_UPPER_BOUNDS`, `discounts.STANDARD_DISCOUNT` + `derive_standard_discounts`) — applied on pull where possible, and drift-checked in the notebook.

## Data science taste (read before modeling)

- Interpretability is non-negotiable — this model will justify commercial pricing decisions to non-technical stakeholders. Simplest model family that fits (GLM/GAM) first; boosted-model + SHAP is a diagnostic escalation, not a destination.

- Prefer domain-grounded features (portfolio value, active accounts, environment type) over proxies of unverified semantics — check Prometheus HELP text/labels before promoting a metric to a feature.

- Validate against manual estimates (`account.est_margin` etc.) as a sanity check, never as a label.

- Favor fewer, well-reconciled data sources over more, loosely-joined ones.

- Flag data-quality anomalies (fractional counts, sparse flags, systemic spike dates) as blockers before building on top of them.

- When a coefficient is domain-constrained to a sign, constrain the fit (NNLS) — and budget for bootstrap inference, documenting that bootstrap p-values are optimistic near the zero boundary.

- Before adopting a sequential/two-stage fit, check it's actually distinct from the joint fit — run both and diff (session 3: bit-for-bit identical).

- **Outliers: use a robust σ (1.4826 × MAD around the median), never mean ± kσ.** Spikes inflate an ordinary std so much that a 6σ cut keeps them all (session 4: with ~60 days and 3 spike days, max z ≈ 4–5). Check whether spikes cluster on shared dates — clustering means a collection artefact, not behaviour.

- **Don't test a variable on tiers it helped build.** Comparing cost across CSPs within cost-floored tiers is circular; test on the usage-only tiers (round 1) with a GLM (`cost ~ C(tier) + C(csp)`) and report exp(coef) as a cost multiple.

- **Floors/boundaries set by a single entity are fragile.** A tier minimum is one client; a cheap, usage-heavy client lowers it and pulls everyone above it up. Check floor monotonicity and name the client behind each floor. Session 13: on CBE cost the minimum floors fell to EUR 264–58k and a P10 floor was non-monotonic; with 4–8 clients in most tiers a percentile floor is still one or two clients, so tier by usage and report cost per tier instead.

- **Discounts are a CSP property, not a customer property** — effective discount doesn't scale with client spend (AWS 24–27% across all bands), so model one standard rate per CSP, re-derived as commitment coverage changes.

## Taste

- Sizing inputs → use the max over the window, not the median ("change it to max figures, not median").

- Outlier handling → robust σ filtering (4–6σ) preferred over dropping named dates.

- Currency → EUR everywhere; source EUR columns first, standard 1.2 USD/EUR only where none exists.

- Cost unit → total annual Production cost per client, not monthly.

- Dedicated below XS → XS (Shared has its own smaller tiers); start with Dedicated.

- Monthly cost spikes → assume a temporary extra workload and flatten to the client's median month.

- Just over a usage threshold → likely paying overages, not a tier up (×0.98, not ×1.1 headroom).

- Discount adjustment → keep only consistent, recurring reductions; ignore one-offs and small sporadic values.

- Broken credentials → Richard supplies a new one; don't build workaround data paths around an auth failure.

- Question log → business themes ("does the CSP change cost?"), not analysis/data detail ("are v1/v2 fractions a bug?").

## Resources

Key tables discovered (see `findings/session-1-discovery.md` and `session-2-discovery.md` for full detail): `silver_salesforce.{account, tenant__c, Mambu_Subscription__c, tenantmetric__c, tenantproductmetric__c}`; `gold_csp_cost.{daily_unified_costs, monthly_unified_costs, monthly_unified_discounted_costs, shared_and_dedicated_customer_costs, aws_detailed_costs}`. Account↔tenant-subdomain crosswalk: "All Mambu Tenants for Active Customers" Google Sheet, refreshed daily from Salesforce report `00OQF0000092b372AA` — also logged in the MCD manifest's Resources table now. `gold_csp_cost.client` → `account.name` fuzzy-match reconciliation is still open (see MCD Open Questions).

## Skills

## Agent rules

- Resources are lazy-loaded unless marked eager.

- Resolve @handles from this table first.

- Treat the project MCD as source of truth for scope, goals, constraints and decisions.

- Maintain decision/rationale, risk/blocker, dependency, milestone and hand-off state where relevant.

- Use `$track-project` for weekly project review; use `$mcd-sync` for durable context synchronisation.

## Agent mode

**Auto-approved:** BigQuery/Grafana read queries, local file/code edits, schema drafts.

**Ask first:** any Notion write beyond this project's own MCD/Ship record, any BigQuery/Grafana/Postgres write, any pricing-model conclusion shared outside this project.

**Never:** present a cost/pricing coefficient without a plain-English explanation; use sampled observability data as invoiced cost.

## Global coding standards (from AI Hub `Coding Standards`)

- Prefer small, cohesive, composable units with clear boundaries; reuse existing repo code, stdlib, or installed dependencies before adding new abstractions.

- Don't build speculative abstractions, base classes, or framework layers before real reuse exists.

- Comments explain intent, constraints, or non-obvious decisions — not mechanics.

- Keep code concise; remove indirection and defensive boilerplate guarding against scenarios that can't happen in a read-only, local-first analysis project.

## Reinforcement & skill-update policy

`/reinforce` and skill-creation/editing for anything specific to *this project* updates the local `CLAUDE.md` and local memory only — do not push project-specific skill changes up to the AI Hub.

**Exception**: this skill (`mambu-cost-analysis`) is the one project-specific skill that lives in the AI Hub by design. Whenever this project is reinforced, update this Notion page first, then copy the result back down into the project's local `CLAUDE.md` — Notion stays the source of truth; `CLAUDE.md` is its local mirror.