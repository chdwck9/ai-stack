---

name: capture-sketch

uuid: 41324dc8-ccd9-81ad-b43a-d774a54c1b51

version: 2

description: "Capture Sketch"

return: "An Inkscape-native SVG, a clean raw SVG and three PNG exports (charcoal, transparent black, transparent white) of the cleaned-up drawing, written to the Ship destination — /Volumes/Ship/--- or /Volumes/Ship/\<project>/--- — and the absolute paths"

last-used: "2026-11-09"

thinking: "Medium"

temperature: 0.3

resources:

- "@AI-Hub"

---

# Capture Sketch

Turn a photo, screenshot or PNG export of a hand-drawn diagram or icon into clean, editable vector linework that still reads as pencil work. Geometry is tidied — straight runs straighten, circles round, breaks close — while low-frequency wobble, round caps and a faint second pass keep it human.

The engine is `~/.hermes/scripts/refine_sketch.py`, run with `~/.hermes/venvs/sketch/bin/python`. Every run emits a full delivery set: an Inkscape-native SVG (named layers: Paper / Ink / Pencil overlay, stable `stroke-NNN` ids), a clean raw SVG for use as an asset, and three PNGs — charcoal ground with white ink, transparent with black ink, transparent with white ink. Affinity cannot be scripted; Inkscape can, and is installed (`/opt/homebrew/bin/inkscape`, 1.4.4) when geometry needs real surgery.

## When to use

- Richard sends a screen pic, note export or phone photo of a sketch, diagram, flow or icon.
- A drawing must become a vector asset without losing the hand-made feel.
- A sketch needs the charcoal/white chalk cover-art language.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Intake.** Get the image path (the attachment he just sent, or `--latest`-style newest image if he says "the one I just dropped"). Get the title: his words, else the thread/chat title, else a 2–4 word name derived from what the drawing actually shows. Get the project: if he names one, resolve it against the folder names in `/Volumes/Ship`; if he names none, destination is `/Volumes/Ship/---`.

1. **Look before tracing.** Open the image and read it. Note ground polarity (ink on paper vs white lines on dark), ink density (line art vs solid fills), and whether the strokes are continuous or broken. This decides flags before the first run, not after.

1. **Run.** `~/.hermes/venvs/sketch/bin/python ~/.hermes/scripts/refine_sketch.py <input> --title "<Title>" [--project "<Project>"] [--bg paper|dark] --json`. Defaults are tuned for notes exports: paper background, `#1E1E1E` ink, stroke engine, wobble 0.9, 2400 px wide. Use `--bg dark` for the cover-art language (`#1E1E1E` ground, white chalk linework, no colour).

1. **Judge the render, not the log.** Open the emitted PNG at full size. Check: shapes closed, no dashed gaps, no speckle debris, no shadow blotch, no doubled ghost lines, and that it still reads hand-drawn rather than mechanical. Iterate with flags only — never hand-edit the SVG.

1. **Place and report.** The script writes the whole set into the destination, versioning the stem (`-v2`, `-v3`) rather than overwriting. Report the five absolute paths and the engine used; state that the Inkscape file opens with three named layers and the transparent PNGs have no ground. If the drawing still needs geometry work rather than re-tracing, do it with Inkscape's headless verbs (`inkscape in.svg --actions="select-all;object-to-path;path-union;export-filename=out.svg;export-plain-svg;export-do"`) and say what you changed.

## Flags that matter

- `--engine stroke|contour|auto` — stroke traces centrelines (restylable weight, for diagrams and line icons); contour traces fills (solid art). Auto picks by ink density.
- `--bg paper|dark|none` — sets the ground *inside the two SVGs* only. The PNG set is fixed (charcoal + two transparent), so this is a choice about the editable master, not the exports.
- `--wobble <px>` — hand displacement in source px. 0 mechanical, 0.6–1.2 relaxed hand, above 2.5 scrappy.
- `--weight <mult>` — 0.7 pencil, 1.0 default, 1.4 marker.
- `--bridge <px>` — join distance across broken strokes (default 28; 40–60 for shadowed photos).
- Also: `--min-area`, `--invert yes|no`, `--ink <hex>`, `--width`, `--overlay`, `--dest`, `--seed`.

## Output contract

- `<slug>.svg`: Inkscape-native SVG 1.1 — `inkscape`/`sodipodi` namespaces, `namedview`, three layers labelled **Paper**, **Ink**, **Pencil overlay**, per-path ids (`stroke-NNN`, `fill-NNN`, `overlay-NNN`), no rasters, no external references, no text elements.
- `<slug>-raw.svg`: the same artwork as plain SVG 1.1 with none of the Inkscape scaffolding, for embedding or handoff.
- `<slug>-dark.png` white ink on `#1E1E1E`; `<slug>-black.png` `#000000` ink; `<slug>-white.png` `#FFFFFF` ink — the last two transparent. All 1400 px on the long edge.
- Result JSON: `svg`, `raw_svg`, `pngs{dark,black,white}`, `engine`, `paths`, `ink_coverage`, `size`, `crop_box`.
- Before finishing, verify the SVG parses, the file exists at the reported path, and the preview actually looks like the input. Anything missing → do the work; do not finish.

## Examples

- **Notes export of a flow diagram, title "Travel Saya Flow".** Line art on white, stroke engine, `--bg paper --weight 0.9`; five files land in `/Volumes/Ship/---/` as `travel-saya-flow.*`, preview checked for closed boxes and joined connectors.
- **Phone photo in bad light.** `--bridge 55 --min-area 140`; dark wood ground needs `--invert yes`.
- **Cover-art sketch.** `--bg dark --weight 1.1 --wobble 1.3` for white chalk linework on `#1E1E1E`, matching the `create-cs` contract.
- **Solid icon.** `--engine contour`; circles snap true, fills stay solid.

## Boundaries

- Never hand-author or hand-fix path data; fix the flags or the input instead.
- Never overwrite an existing SVG or PNG in the destination — version it.
- Never send a file outside `/Volumes/Ship` or a scratch folder without being asked.
- Typed text in the source is traced as shapes, not recognised as editable text. Say so when it happens; do not pretend labels are editable.
- The script does not write `.afdesign`. Never imply it did.
- Never hand-write Inkscape XML or rename layers; the layers come from the script.
- Do not claim quality you did not look at: every delivery is judged on the rendered preview.

## Next steps

Send the image and a title (and a project name if it belongs to one); the result lands in that project's `---` folder ready to open in Affinity Designer.
