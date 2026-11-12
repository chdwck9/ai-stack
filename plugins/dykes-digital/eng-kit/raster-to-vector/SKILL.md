---


uuid: 41324dc8-ccd9-81f1-a793-d85b54ac9828
name: raster-to-vector
description: "Use when vectorising a sketch or screenshot to SVG."
version: 1
author: Hermes Agent
license: MIT
thinking: "Medium"
temperature: 0.3
metadata:
hermes:
tags: [vector, svg, trace, sketch, potrace, skeleton, opencv, affinity, line-art]
related_skills: [refine-sketch, architecture-diagram, claude-design]


---


# Raster to Vector

Turn a bitmap drawing — pencil sketch, note export, screenshot, phone photo of paper — into an **editable** vector that keeps the original's hand. Geometry gets tidied (straight runs straighten, near-circles snap, small breaks close); a low-frequency wobble, round caps and a faint second pass keep it human rather than plotter-clean.

Richard's packaged front end for this is the `refine-sketch` skill and `~/.hermes/scripts/refine_sketch.py` (Ship placement, paper/charcoal styles, title and destination conventions). Use that for delivery; use this skill for the decision-making underneath it, or when writing a new vectoriser.

## When to Use

- A screenshot, note export or phone photo of a hand-drawn diagram, flow or icon has to become editable vector artwork.

- A clean vector exists but loses the sketch's character, or a trace comes back hollow, dashed, blotchy or duplicated.

- A new vectoriser is being written and needs the thresholding and skeleton rules that are not obvious from the libraries.

For Richard's Ship delivery path and paper/charcoal styling, run the `refine-sketch` skill instead — it wraps this material.

## Steps

1. **Read the image before touching it.** Ground polarity (dark ink on light vs light lines on dark), ink density (thin line art vs solid fills), stroke continuity, and whether it is a clean export or a photo with shadow and blur. These four answers pick the engine and every flag.

1. **Pick the representation, not just the tool.** Two shapes of output, and they are not interchangeable:

  - *Centreline* (skeletonise → polylines → stroked paths): restylable line weight, editable as lines, right for diagrams, flows, line icons.

  - *Contour* (trace ink boundaries → filled paths): faithful to solid fills and organic shapes, but each stroke becomes an outline you cannot re-weight.
  Default by ink coverage — dense coverage means fills and warrants contour.

1. **Threshold for structure first.** A global (Otsu) mask carries solid fills; an adaptive pass only recovers faint pencil, and must be gated by the global mask so it cannot fire across solid interiors. See `references/vectorisation-pitfalls.md` before writing or debugging any of this — the polarity and background-estimate rules there are the ones that silently produce hollow shapes.

1. **Clean the graph, then smooth it.** Close hairline breaks before thinning; bridge open ends only when the direction of travel continues; close a broken loop only when its gap is small relative to the path length. Simplification (Douglas–Peucker) runs before smoothing, never after.

1. **Preserve the hand deliberately.** Wobble is low-frequency perpendicular displacement with endpoints anchored (so junctions stay joined) — not random jitter per point. Amplitude of roughly 0.5–1 px at source resolution reads as a relaxed hand; per-point noise reads as a broken scanner.

1. **Verify by looking.** Render the SVG to PNG and inspect it. Path count, ink fraction and a successful exit all stay green on output that is visibly wrong.

## Boundaries

- Never hand-patch generated path data. Fix the threshold, the graph rule or the flag.

- Never claim `.afdesign` (or any other proprietary binary) was written. SVG opens in Affinity Designer as editable curves; saving native is a manual step.

- Typed or printed text inside the source traces to outline shapes, not editable text. Say so rather than implying labels are live.

- Never overwrite an existing vector in a delivery folder; version the filename.

- Do not report a result you have not rendered and looked at.

## References

- `references/vectorisation-pitfalls.md` — polarity detection, background estimation, adaptive-threshold sign, skeleton graph hygiene, and headless-render gotchas. Load before changing a vectoriser or diagnosing a bad trace.