---


uuid: 3ff24dc8ccd981d3b2dcdf48f8a0209f
name: blender-print-prep
description: "Use when preparing a Blender model for 3D printing."
version: 1
author: clarity
license: proprietary
metadata:
hermes:
tags: [3d-printing, blender, stl, manifold, slicer]
related_skills: [blender-headless-scripting, image-to-3d-model, blender-printable-models]


---


# Blender → 3D print setup

Take a finished model to the printer: real units, a manifold solid, correct tolerances, a clean export, and a slicer handoff. Applies to any mesh — modelled, scanned, or generated.

## When to Use

- "Make this printable", "export an STL/3MF", "will this print?", "fix non-manifold edges".

- Any model destined for an FDM or resin printer.

- Don't use for: *creating* the model (see `blender-printable-models`, `image-to-3d-model`).

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Units → real mm.** Set `scene.unit_settings`; confirm actual dimensions. State whether a quoted height includes the base.

1. **Make it manifold.** `remove_doubles`, `normals_make_consistent(inside=False)`; run a watertight / non-manifold check and **fix before export** — a non-watertight mesh slices to garbage.

1. **Printability pass.** Wall thickness ≥ 0.8–1.2 mm (FDM); no zero-thickness faces; no intersecting/overlapping shells; no sub-nozzle detail (< ~0.8 mm); **chamfer** over fillet on downward overhangs (45° is self-supporting).

1. **Orient for strength and stability.** Layer seams are the weak axis — orient so loads run across layers, not along the seam. Give it a flat, broad base; minimise overhangs so the slicer needs little support.

1. **Split if needed.** > build-plate size, unavoidable steep overhangs, or different orientations → separate parts with proper joints/clearance. Each part gets its own file.

1. **Export at true mm scale.** Prefer **3MF** (units + multiple objects); **STL** as the universal fallback.

1. **Slice, don't assume.** Open it in the slicer (Bambu Studio for the GUI path) and confirm it slices; report the authorititative weight/time from the slicer.

1. **Hand off.** Files, material, orientation, slicer settings, assembly order — a summary the user can print from without re-reading the chat.

## Division of labour: Blender vs the slicer

- **Blender owns geometry** — shape, walls, holes, chamfers, tolerances, mating features.

- **The slicer owns the print strategy** — infill, supports, perimeters, layer height.

- Do **not** model infill or supports. The slicer does both, better.

## Boundaries

- Default to **filament-only**, single-piece prints. Only design around hardware (bearings, magnets, screws, inserts) when the function genuinely requires it.

- Never hand over an STL without stating its measured bounding box in mm and its manifold status.

## Verification

- Manifold and watertight **before** export; slice in the slicer rather than assuming.

- Report bbox in mm and poly count; confirm measured height against the spec.

## Pitfalls

- Non-manifold geometry → slicer garbage; fix it in Blender first.

- Doing the slicer's job in Blender (modelling infill/supports) wastes material and time.

- Wrong units/scale → a tiny trinket or an unprintable giant.

- Faceted/low-poly styles print *well* on FDM (planes align with layers) — a smooth curved surface does not.

## References

- `blender-printable-models` — the front half: photos/measurements → the model itself.