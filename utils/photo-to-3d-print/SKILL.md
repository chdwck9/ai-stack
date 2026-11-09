---


name: photo-to-3d-print
uuid: 3ff24dc8ccd981eb8c6cef15f9dc3bdf
version: 2
description: "Photo To 3D Print"
last-used: "2026-10-27"
thinking: "Medium"
temperature: 0.3
author: clarity
license: private
metadata:
hermes:
tags: [3d-printing, photogrammetry, blender, fdm, mpfb]
related_skills: [blender-headless-scripting, blender-print-prep]


---


# Photo → 3D-printable model

Turn ordinary photos — or a single picture, or a measurement — into a mesh that prints well,
optionally stylised into a faceted "chipped stone" look. Runs locally and headless:
`blender -b --factory-startup -P script.py`.

## When to Use

- "Make a 3D model / STL from this photo / picture."

- A figurine, bust or diorama for an FDM printer.

- Any request to stylise a scan (low-poly, faceted, crystalline, carved).

- Judging whether an existing photo set can build a mesh.

Do NOT reach for rig-and-repose (Step 5). Finish in `blender-print-prep`; Blender mechanics in
`blender-headless-scripting`.

## Step 1 — Pick the source first (this decides quality)

- **Real photos of the subject → photogrammetry.** The only route that gives *measured* shape, and
the only one that bands a real person.

- **No viable photos, or an un-scannable pose → MPFB2 base human** (proportions measured or
supplied): `references/mpfb2-human-bases.md`.

- **One image, plausible object → single-image neural** (TRELLIS / Hunyuan3D / TripoSR). Fast, but
**the unseen side is invented, not measured**.

- **One clean photo of a man-made object → camera-match** (fSpy → Blender camera + image plane).
Precise; slow.

**State the fidelity ceiling and let Richard choose.** A base model gives correct height, build
and pose but **never facial likeness** — that is a painter's job, not geometry.

## Step 2 — Feasibility-test the photos before promising a build

Never judge a photo set by eye. Run the pycolmap script in
`references/photogrammetry-capture.md` and report **registered-image count, 3D point count, and
the largest azimuth gap**.

## Step 3 — Capture

Hand `references/photogrammetry-capture.md` to Richard *before* he shoots — bad photos cannot be
recovered. The three that break scans: **even light only** (no sun or flash); **arms out ~25–35°**
in a relaxed A-pose, bodies near but **not touching** (contact surfaces fuse into one blob);
**~75% overlap**, subject filling the frame and holding still. Frame counts and the
separate-vs-together choice: `references/scan-workflow.md`.

## Step 4 — Toolchain and reconstruction

venv + `pip install pycolmap open3d trimesh`, then clean, fix scale from one known dimension, and
verify by re-projection — full commands and the reason to prefer pycolmap over a Homebrew `colmap`
binary are in `references/scan-workflow.md`.

## Step 5 — Do not rig-and-repose a scan

A photogrammetry mesh is a hollow skin — auto-weighting fails and every retopo step smears detail.
**Scan close to the final pose**; rig only when a large re-pose is unavoidable, and state the
fidelity cost first. Detail and posing method: `references/scan-workflow.md`,
`references/headless-posing.md`.

## Step 6 — Style, review, print

- Faceted finish (quadriflow → dissolve → bevel → `shade_flat`): `references/faceted-styling.md`.
Validate on a **placeholder figure first** with `scripts/facet_style_probe.py` (under a minute
per CPU render). Keep the **head softest** so geometry survives for hand-painted features.

- Review in two materials — clay (roughness ~0.45) and obsidian (near-black, coat ~0.6) — CPU
Cycles ~128 samples + denoise. Look at the renders yourself; send them via `MEDIA:`.

- FDM: flat facets print **cleanly** (planes align with layers); a **compact pose** (arms down)
beats an A-pose; **0.2 mm nozzle, ~0.08 mm layers** for small faces. Confirm whether a quoted
height means the diorama or the figures.

- Print prep and export: `blender-print-prep`.

## Pitfalls

- **Lights and the camera added via ****`bpy.data`**** do not aim themselves** (default −Z → a black
silhouette). Add a `TRACK_TO` constraint (`TRACK_NEGATIVE_Z`, `UP_Y`) targeting an empty at the
figure centre.

- `quadriflow_remesh` **silently no-ops on a non-manifold mesh** — merge doubles and recalc
normals first; `Decimate DISSOLVE` needs `delimit=set()` or the plate look never appears.

- **Floating islands** — a capsule endpoint that misses the next part leaves a detached blob.
Inspect the render for disconnected pieces.

- Occlusion, invented backs, symmetry, faceting limits: `references/scan-workflow.md`.

## Verification

- Render after **every** shape or pose change and look at it — numbers alone miss a bad pose.

- Confirm manifold and watertight before STL, then run it through the slicer.

- Report the final poly count and measured bounding-box height against Richard's stated target.

## References

- `references/photogrammetry-capture.md` — capture protocol + the pycolmap feasibility test.

- `references/scan-workflow.md` — toolchain, clean/scale/verify, counts, faceting recipe, pitfalls.

- `references/faceted-styling.md` · `references/mpfb2-human-bases.md` · `references/headless-posing.md`