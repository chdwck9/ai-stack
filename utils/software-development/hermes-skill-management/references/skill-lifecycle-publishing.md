# Publishing skill lifecycle events (on_skill_lifecycle)

Depth for the "publish skill edits to a hub" procedure. Read when wiring a plugin that mirrors
Hermes skill changes into an external system.

## The hook

`on_skill_lifecycle` is a plugin **observer** hook (registered via `ctx.register_hook`), fired from
the single authoritative write path (`tools/skill_usage.py`) after every foreground `skill_manage`
call — CLI and gateway alike. Return value is ignored; it can never block or mutate a write.

Payload (accept `**kwargs` for forward compatibility):

| field | meaning |
|---|---|
| `action` | `created` \| `patched` \| `edited` \| `loaded` \| `installed` \| `archived` \| `stale` \| `restored` \| `deleted` |
| `skill_name` | the skill's name (resolved by the plugin to a path) |
| `provenance` | `agent_created` \| `learn` \| `installed` \| `external` \| `local` \| `unknown` |
| `task_id`, `session_id` | opaque ids (may be empty) |
| `use_count`, `reused`, `reuse_after_patch` | present on `loaded` |

**Filter to content changes**: `{created, patched, edited}` (and `deleted` for an archive signal).
`loaded` fires on every *use* of a skill, not an edit — publishing it floods the hub.

## Minimal plugin

`~/.hermes/plugins/<name>/plugin.yaml`
```yaml
name: skill-publisher
version: "1.0"
description: Publish skill edits to n8n on every touch.
provides_hooks:
  - on_skill_lifecycle
optional_env:
  - name: SKILL_PUBLISH_WEBHOOK
    description: "n8n webhook URL for skill write-back"
    prompt: "skill write-back webhook URL"
    password: false
```

`~/.hermes/plugins/<name>/__init__.py`
```python
import json, logging, os, threading, urllib.request
from pathlib import Path

logger = logging.getLogger("plugins.skill_publisher")
_PUBLISH = {"created", "patched", "edited"}


def _targets():
    """dir -> external Type. Derive from config, or default to the skill roots."""
    from agent.skill_utils import get_external_skills_dirs, get_skill_create_dir
    out = [{"dir": Path(d), "type": "Skills"} for d in get_external_skills_dirs()]
    cd = get_skill_create_dir()
    if cd is not None:
        out.append({"dir": Path(cd), "type": "Utilities"})
    return out


def _post(url, payload):
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(req, timeout=10).read(256)
    except Exception:
        logger.warning("publish failed for %s", payload.get("skill"), exc_info=True)


def on_skill_lifecycle(action, skill_name, provenance="", session_id="", **kwargs):
    if action not in _PUBLISH and action != "deleted":
        return
    url = os.environ.get("SKILL_PUBLISH_WEBHOOK", "").strip()
    if not url:
        return
    # resolve <root>/<name>/SKILL.md across roots (create_dir first), pick the target dir,
    # read content, build payload {action, skill, notion_type, content, ...}, then:
    threading.Thread(target=_post, args=(url, payload), daemon=True).start()


def register(ctx):
    ctx.register_hook("on_skill_lifecycle", on_skill_lifecycle)
```

## Scope by directory, tag by Type

A hub often holds several skill *types* in one database, distinguished by a property (e.g.
`Type = Skills` vs `Type = Utilities`). Map each local directory to its Type and publish only
skills that resolve inside a target dir; anything else (the local `~/.hermes/skills` store,
bundled/hub skills) is silently skipped. Make the map configurable so a new type is a config edit,
not a code change.

## Testing the plugin without Hermes running

Load the module by path and fire the hook against a local `http.server` listener, using Hermes'
own interpreter:

```python
import importlib.util
spec = importlib.util.spec_from_file_location(
    "skill_publisher", "/Users/<you>/.hermes/plugins/skill-publisher/__init__.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
mod.on_skill_lifecycle(action="patched", skill_name="some-skill")
```

Run it with `~/.hermes/installs/*/environments/*/venv/bin/python3*` (Hermes' interpreter). A bare
`python3` may be < 3.10 and fail to import the agent modules (`X | Y` type unions).

## Multi-endpoint convergence model

When several endpoints (Hermes, Claude, Open WebUI, …) edit the same skills and a nightly job syncs
Notion -> files: each endpoint **write-throughs** its edits to the hub immediately, and the nightly
pull is the convergence point. Best case the write-through already matched (no-op overwrite); worst
case another endpoint's hub edit replaces the local file at midnight. Design the publisher as
fire-and-forget so a hub outage never blocks a local edit.
