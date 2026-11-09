---


uuid: 3ff24dc8ccd981538e4cf43fd773a0cb
name: blender-headless-scripting
description: "Use when scripting Blender headless: scenes, rigs, renders."
version: 1
author: clarity
license: proprietary
metadata:
hermes:
tags: [blender, automation, headless, rigging, rendering]
related_skills: [blender-printable-models, blender-print-prep]


---


# Blender headless scripting

Drive Blender from the command line and Python instead of the GUI: build and modify scenes, rig and pose characters, render review passes, and export — reproducibly and in batch. Runs entirely locally.

## When to Use

- Automating Blender: batch renders, parametric scenes, asset generation, repeatable edits.

- Rigging or posing a character from a script (MPFB / MakeHuman standard rig, Rigify).

- Any "run Blender without the UI" task.

- Don't use for: interactive hand-modelling or sculpting — do those in the viewport.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Probe.** `terminal(command="blender --version")`; confirm the input `.blend` path exists (`search_files target='files'`).

1. **Script, then run headless:** `terminal(command="blender -b --factory-startup -P script.py")`. `--factory-startup` gives determinism; drop it only to inherit user prefs, and then enable each add-on explicitly.

1. **Set real units first** (`scene.unit_settings`); work in metres or mm consistently.

1. **Build/modify** objects, collections, modifiers, materials.

1. **Rig/pose** if needed — world-space aiming + analytic IK (below). Never guess Euler angles.

1. **Render a review pass and LOOK at it** (`vision_analyze`). Numbers alone miss a broken pose or a black frame.

1. **Save and export.** Back up the input `.blend` before overwriting (`cp`); Blender keeps its own `.blend1`.

## Posing a rig headlessly (the part that bites)

Guess-work does not converge. Aim bones in **world space** and solve arms with **analytic 2-bone IK**:

- `PoseBone.matrix` is in **armature space** — convert with `arm.matrix_world.inverted()`.

- Aim with a **minimal-twist** rotation so roll is preserved: `q = cur_dir.rotation_difference(target)`, `R = q.to_matrix() @ pb.matrix.to_3x3()`. A track-quat (`to_track_quat`) flips the head backwards.

- MakeHuman arms are **two bone-pairs per segment** (`upperarm01`+`upperarm02` = one upper arm). Rotate only the `01` bone; measure IK length head → far tip, not the first sub-bone (≈4 cm vs the real ≈18 cm — the classic ballooned-shoulder bug).

- Set bones **root → tip**, calling `bpy.context.view_layer.update()` after each so children move.

- Verify in a **~1 s render loop** (Workbench, `shading.color_type='OBJECT'`, a different colour per body). Six loops beats sixty guesses.

Working helpers: `scripts/poselib.py`.

## Verification

- Render and inspect with vision after **every** geometry change.

- Read the **evaluated** mesh for bounds and floor-drops: `obj.evaluated_get(depsgraph).to_mesh()`. `obj.data.vertices` is the REST mesh and will float.

- Print dimensions in mm (`obj.dimensions`) and compare to the spec.

## Pitfalls

- Lights and cameras created via `bpy.data` point down −Z: add a `TRACK_TO` constraint (`TRACK_NEGATIVE_Z`, `UP_Y`) or every render is a black silhouette.

- Enable an add-on (`preferences.addon_enable`) **before** importing its services, or the import breaks.

- Do not delete objects between successive `mpfb.create_human` calls — it invalidates the earlier Python reference (`ReferenceError: StructRNA of type Object has been removed`).

- Blender's bundled Python is minimal — no PIL/numpy. Compose contact sheets in a side venv.

- Cycles CPU is fast enough for review; EEVEE needs a GPU context headless. Workbench is the fastest diagnostic.

- `--factory-startup` disables non-default add-ons — re-enable them in-script.

## References

- `scripts/poselib.py` — world-space `aim`, analytic `two_bone_ik`, `drop_to_floor`; the exact helpers that made an arm-wrapping pose converge.