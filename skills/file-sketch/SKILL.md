---


name: file-sketch
description: "File a sketch image into the Ship folder."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
hermes:
tags: [sketch, filing, ship, images]
category: note-taking


---


# File Sketch

When Richard sends a sketch, screenshot or photo and wants it kept, file the image into the Ship destination. No tracing, no conversion — just naming and placement.

## When to use

- He sends a sketch/diagram/photo and wants it filed.

- He says "file this" or "stick this in Ship".

## Steps

1. Take the attachment path (or the newest image in the cache if he says "the one I just sent").

1. Title: his words; else derive 2–4 words from what it shows.

1. Project: if he names one, pass `--project`; otherwise use the default inbox.

1. Run:

  ```javascript
  python3 ~/.hermes/scripts/file_sketch.py "<image>" --title "<Title>" [--project "<Project>"]
  ```

1. Report the absolute path it prints.

## Boundaries

- Filing only — do not trace, convert, or generate SVGs. The old auto-trace / "refined sketch" workflow was rejected as unusable and archived — never offer it again.

- Copy, never move, unless he explicitly says move (`--move`).

- Never overwrite: the script versions `-v2`, `-v3`.

- Do not invent a project that doesn't exist; the script errors with the candidate folders.