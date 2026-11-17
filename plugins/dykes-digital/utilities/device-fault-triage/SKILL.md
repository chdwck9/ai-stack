---


uuid: 41924dc8-ccd9-81d8-86e7-fa63f89ad232
name: device-fault-triage
description: "Use when a device misbehaves: isolate before replacing."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
hermes:
tags: [hardware, diagnosis, usb-c, smartphones, repair]


---


# Device fault triage

Work out *which part* is broken — cable, port, accessory, host, or firmware gate — before recommending a repair or a purchase. Richard is technically fluent: give the mechanism and the measurement, not reassurance.

## When to Use

- "My phone/glasses/dock isn't charging / not connecting / intermittent."

- An accessory works somewhere but not somewhere else, so the fault is one of the two ends.

- Deciding whether a fault is worth repairing, claiming, or replacing.

## Procedure

1. **Falsify the cheapest part first — the cable.** Known-good e-marked cable plus known-good charger, both device orientations, no case or adapter in the chain. A magnetic USB-C adapter tip is a prime suspect and must be asked about explicitly: it populates only some pins, traps lint behind itself and wears the receptacle springs.

1. **Cross-test the accessory on a known-good host** (laptop for DP Alt Mode / data, another phone for power). If it works there, the accessory is exonerated and the remaining device's port is the fault. Say so plainly — that one test removes half the search space.

1. **Measure, don't guess.** A USB-C power meter inline records V/A in each orientation. Healthy PD shows ~9V/2A+; a fallback shows 5V under 1A. That number distinguishes "negotiation failing" from "cable is junk" and is what a repair desk takes seriously.

1. **Read what the OS says.** Charging notification wording is a free negotiation report — "cable charging" vs "fast/super fast charging" tells you whether USB-PD succeeded. Use the vendor's own diagnostic tool if one exists (Samsung Members → Diagnostics covers wired charging and USB connection) and screenshot it: it is your evidence trail.

1. **Inspect at an angle with a torch**, then clean properly if warranted: **99% isopropyl** (never 70% — the water is the problem), soft brush or carved wooden/plastic pick, no metal, no compressed air into the port (it drives debris deeper), 30 min to dry, power on with nothing plugged in. Salt/sweat corrosion, not pocket lint, is what a brush fails to fix.

1. **Data test:** a data-capable cable to a computer, both orientations, check enumeration. Enumerates one way only = CC/data lane fault, independent of charging.

1. **Then decide:** repair, warranty/insurance claim, or replace — with the economics stated.

## Rules that decide the answer

- **USB-C is reversible by design. Needing to flip the cable is a fault, not a quirk.** It points at the CC (configuration channel) pin of one orientation; once CC negotiation fails the device falls back to 5V and charges slowly. Never normalise it as "just how this one behaves".

- **A moisture warning with no water exposure is a port-board fault, not a software bug.** USB-C moisture sensing measures leakage across the pins; a corroded or arcing-damaged pin reads as water. While that flag is up, phones deliberately block cable charging *and* USB accessory/Alt Mode connections — which explains "my AR glasses stopped connecting" as the same root cause, not a second fault.

- **There is no supported software bypass for a moisture/leakage gate.** The check lives in the charger IC / USB-PD controller firmware, below the OS: not a setting, not an adb toggle, not in recovery. Root/custom kernel trips Knox, usually loses warranty, and on modern Samsung builds the OEM-unlock toggle is often gone anyway. The gate exists because leakage plus current is how a €150 port board becomes a dead mainboard — decline to help bypass it and say why.

- **Two legitimate last tests before declaring hardware:** charge with the device powered off (some models skip the gate), and safe mode plus cache-partition wipe (clears a stale flag, rules out a third-party app).

- **IP ratings cover water, not sweat salts.** IP48/IP68 does not mean the contacts are immune; corrosion on the centre tongue is normal wear in a pocket.

- **Foldables change the repair economics, not the diagnosis.** The port sits on a sub-assembly; authorised service swaps the board rather than reflowing, third-party work is cheaper but usually breaches the ingress gasket. Say that trade-off out loud and let him choose.

- Repairs of this size are a legitimate **insurance / Samsung Care+ / statutory-conformity** question, not just a cash question — raise it before he pays.

## Bridge advice while a repair is pending

- Wireless charging covers daily top-ups and bypasses the port path entirely; USB file transfer is blocked by the same gate, so use Quick Share / wireless Smart Switch / cloud instead.

- Warn once against repeatedly churning a half-dead receptacle: current concentrates on fewer contacts and heats them, which is how a fixable port becomes a mainboard job.

## Style

Lead with the diagnosis and the mechanism, then the shortest decisive test. State probabilities honestly ("almost certainly", not "maybe"), and say what would change your answer. Offer the pre-repair cleaning as one cheap shot, explicitly labelled as the last cheap shot rather than a fix.