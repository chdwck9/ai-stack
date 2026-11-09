---


name: image-generation
uuid: 40524dc8-ccd9-81b1-93ee-d6fc4c5a15f3
version: 2
description: "Image Generation"
last-used: "2026-10-27"
thinking: "Medium"
temperature: 0.3
author: clarity
license: proprietary
metadata:
hermes:
tags: [image, avatar, generation, vision, assets]
related_skills: [clarity-capabilities, create-persona, honcho-memory-service]


---


# Image generation (Hermes)

Produce a picture the user asked for and hand back a file they can use. The work is: pick a backend,
generate, **look at the result**, regenerate if it is off-model, deliver the path.

## When to Use

- The user asks for a picture: an avatar or persona portrait, an illustration, a logo mark, a social asset.

- An existing asset needs a variant (different colourway, closer crop, transparent background).

- An image-generation step belongs in a larger task (a persona being created, a report needing a cover).

## Key fact

Hermes ships image backends as plugins under `$HERMES_HOME/hermes-agent/plugins/image_gen/<name>/`.
The `image_gen` **toolset** is only a wrapper over them and may be disabled in this config — a
disabled toolset is **not** a missing capability. Load the provider class from a script and call
`generate()` directly; this works from any session (interactive, cron, webhook) with no restart. Only
enable the toolset when the user wants the `image_gen` *tool* every turn — `hermes tools enable<br>image_gen` needs a gateway restart from **outside** the gateway process.

## Procedure

1. **Pick the backend** — `ls $HERMES_HOME/hermes-agent/plugins/image_gen/`. Preference order:

  - `openai-codex` — `gpt-image-2` through the ChatGPT/Codex OAuth in `~/.hermes/auth.json`. No API
  key, **no per-image spend** (subscription-covered). Default choice.

  - `openrouter` — needs `OPENROUTER_API_KEY`; chat-completions image output plus a dedicated image
  API (gpt-image-2, Krea, Qwen Image, Grok Imagine).

  - `fal` — needs `FAL_KEY`; flux / nano-banana / recraft. **Bills per image — treat as spend.**

  - Also on disk: `xai`, `krea`, `deepinfra`, `openai`, `meta-ai`.

1. **Generate** with `scripts/gen_image.py` (`--prompt --aspect --provider --model`). It loads the
plugin by path, so it needs the repo root on `sys.path` and `HERMES_HOME` exported:
`HERMES_HOME=~/.hermes ~/.hermes/hermes-agent/venv/bin/python gen_image.py --prompt "..." --aspect square`
Aspect is `square`/`portrait`/`landscape`; the result JSON carries `image` (absolute PNG path),
`pixel_size` and `reported_quality`.

1. **QA with ****`vision_analyze`**** on the returned path before showing anything.** Check: whole subject
inside the frame with margin (feet, antennae, hands and top-of-head are the usual crop victims); no
text, watermark or stray glyphs; the style matches the ask; no melted or duplicated geometry.
Regenerate rather than presenting a defect as a style choice.

1. **For an avatar/persona image, judge it at real size.** `sips -Z 256 in.png --out preview.png`.
Detail that reads well at 1254px vanishes at 32px — a close-up head/shoulders framing beats a
full-body shot for a small round avatar.

1. **Deliver.** Copy winners out of the cache (`$HERMES_HOME/cache/generated/images/` — pruned) to a
stable path such as `$HERMES_HOME/assets/<name>.png`, then put `MEDIA:/abs/path` lines in the
reply. Offer 2–3 candidates with a named recommendation.

## Pitfalls

- **OpenAI's safety filter rejects trademarked / franchise wording.** A film franchise, a specific
character or droid model, or a studio as the target style returns HTTP 400 "rejected by the safety
system". Rephrase as an original generic description and retry — do not switch backends over it.
Stray innocent phrasing can trip it too, so when a prompt is refused, **trim clauses, don't expand**.

- **Ask for cel-shading explicitly**, or "anime style" returns a painted 3D render: name the technique
("cel-shaded, flat colour blocks, hard-edged shading, clean ink linework, no 3D render look").

- **Never overwrite an existing asset** (`~/.hermes/assets/avatar.png`) or push to an external surface
(Discord avatar, remote profile picture) without asking — neither is reversible and one is
human-facing. Deliver candidates; let the user choose.

- **State cost honestly**: OAuth-backed generation is subscription-covered; FAL and OpenRouter bill per
image. Prefer the covered backend unless the user asks for a specific model.

- **Do not paste the backend's URL or the prompt back as the deliverable** — the file path is the
answer.

## Verification

- `vision_analyze` on the returned path described a real image whose subject matches the request.

- The delivered file is an absolute path **outside** the pruned cache dir, with non-zero size.

- For avatar work: the 256px preview was inspected, not just the full-size render.

- Any claim of "no image capability" must survive `ls $HERMES_HOME/hermes-agent/plugins/image_gen/`.

## Support files

- `scripts/gen_image.py` — backend-agnostic generator: loads the provider plugin by path, tries
providers in preference order, prints the result JSON.

- `references/prompt-recipes.md` — known-good prompt clauses (style / framing / background) and the
safety-filter rephrasing table.