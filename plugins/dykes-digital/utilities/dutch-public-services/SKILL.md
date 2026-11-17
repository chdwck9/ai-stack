---


uuid: 41924dc8-ccd9-8187-9cba-d71fba8b554d
name: dutch-public-services
description: "Use when applying via a Dutch school, gemeente or agency."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
hermes:
tags: [Netherlands, Gemeente, School, Administration, VOG, Subsidie]
related_skills: [blocked-page-recovery, local-service-availability]


---


# Dutch Public Services

Routing work through Dutch institutions — a basisschool, a gemeente desk, a
public body — for Richard (NL resident, children at a Dutch primary school).
The task is rarely "find information"; it is "which door do I knock on, in what
order, and what will they demand before saying yes".

## When to Use

Load when a task has to be done through a Dutch institution: starting an
activity or training at a school, hiring a municipal hall or gym, applying for a
permit, subsidy or VOG, or any "who do I ask, and in what order" question about
a gemeente, school board or public body. Also load when the user names a Dutch
school or municipality and asks about routes, cost or deadlines.

## Procedure

1. **Establish the municipality first.** Almost every page, tariff and subsidy
is per-gemeente. Without the place name (or the exact school, which implies
it) no specific link can be given — say so and ask, rather than offering a
national page as if it were the local answer.

1. **Answer in order of what actually gates the outcome**, not in order of the
org chart. Usually the constraint is availability of space/money/one
signature, and the org that owns that constraint goes first.

1. **Verify every link before sending it.** Open it and confirm title plus body
text. Never hand over a URL assembled from a naming convention.

1. **State which claims are verified and which are standard practice.** When a
source check was blocked, say the check failed and label the rest as
domain knowledge. Richard makes the call; he needs the confidence level.

1. **Close with the one or two facts you still need** (place, acronym, which
school) and what you will do with them.

## Desk vocabulary

The same function is named differently per municipality — search for the
function word, not the abstract concept:

- `sportaccommodaties`, `gymzaal huren`, `accommodatieverhuur` — building hire

- `sportloket`, `sportbedrijf` — larger cities run a separate delivery body

- `maatschappelijk vastgoed` — where the building portfolio actually sits

- `buurtsportcoach`, `beweegcoach` — the person who can host activity at a school

Searching for `subsidie` routes to a different desk than the one that rents
space; keep them separate.

## Standing gates

- **VOG** (Verklaring Omtrent het Gedrag) for every adult who will be present
with minors. Issued only by Justis, [https://www.justis.nl/producten/vog/](https://www.justis.nl/producten/vog/) ,
typically 1–4 weeks. Charge lead time against any start date; it is the
slowest item in most proposals.

- **Aansprakelijkheidsverzekering** for the activity, and parental consent for
participation.

- Commercial delivery to minors pulls in ondernemer/BTW and can collide with an
existing contract the school or its BSO partner already holds.

## Proposal shape that gets a yes

One page to the beslisser: what, which groups, which timeslot, which space,
cost to parents, who supervises, VOG, insurance. Attach nothing else. The
second page of a proposal is read only after the first page is approved.

## Pitfalls

- Do not guess an acronym the user typed. A garbled discipline or programme
name does not change the routing answer, so give the routes, then ask what it
stands for — do not silently substitute a plausible-looking expansion.

- Do not present a municipality-agnostic national link as "the gemeente route".
It answers a different question and costs a round trip.

- An after-hours school building is frequently contracted to the BSO provider;
school permission alone is not sufficient.

- Under-lesson-time use touches onderwijstijd and therefore usually needs MR
instemming, not just the directeur's goodwill.

## References

- `references/school-activities.md` — routes for running an activity or training
at a basisschool, ordered by gating factor.