#!/usr/bin/env python3
"""
Skill Loader MCP Server
Reads SKILL.md files and exposes them as tools.
Supports /command shorthand via execute_command.
Designed for robustness across Claude Code, Perplexity, and container environments.
"""

import os
import json
import logging
import signal
import sys
import threading
import time
from pathlib import Path
from datetime import datetime, timedelta
from mcp.server.fastmcp import FastMCP

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

SKILLS_DIR = Path(os.environ.get("SKILLS_DIR", "/skills"))
SKILL_CACHE_TTL = int(os.environ.get("SKILL_CACHE_TTL", "60"))  # seconds
mcp = FastMCP("skill-loader")
_startup_ok = False

class SkillCache:
    def __init__(self, ttl_seconds=60):
        self.ttl = ttl_seconds
        self.data = None
        self.last_update = None
        self.lock = threading.Lock()
        self.last_scanned_mtime = None

    def invalidate(self):
        with self.lock:
            self.data = None
            self.last_update = None
            logger.info("Skill cache invalidated")

    def get(self):
        with self.lock:
            if self.data is None:
                return None
            age = (datetime.now() - self.last_update).total_seconds()
            if age > self.ttl:
                self.data = None
                return None
            return self.data

    def set(self, data):
        with self.lock:
            self.data = data
            self.last_update = datetime.now()

    def is_stale(self):
        return self.get() is None

_skill_cache = SkillCache(ttl_seconds=SKILL_CACHE_TTL)

class Metrics:
    def __init__(self):
        self.lock = threading.Lock()
        self.cache_hits = 0
        self.cache_misses = 0
        self.list_skills_calls = 0
        self.load_skill_calls = 0
        self.search_skills_calls = 0
        self.execute_command_calls = 0
        self.sse_connections = 0
        self.errors = 0

    def record_cache_hit(self):
        with self.lock:
            self.cache_hits += 1

    def record_cache_miss(self):
        with self.lock:
            self.cache_misses += 1

    def record_list_skills(self):
        with self.lock:
            self.list_skills_calls += 1

    def record_load_skill(self):
        with self.lock:
            self.load_skill_calls += 1

    def record_search_skills(self):
        with self.lock:
            self.search_skills_calls += 1

    def record_execute_command(self):
        with self.lock:
            self.execute_command_calls += 1

    def record_sse_connection(self):
        with self.lock:
            self.sse_connections += 1

    def record_error(self):
        with self.lock:
            self.errors += 1

    def get_stats(self):
        with self.lock:
            total_cache_requests = self.cache_hits + self.cache_misses
            hit_rate = (self.cache_hits / total_cache_requests * 100) if total_cache_requests > 0 else 0
            return {
                "cache_hits": self.cache_hits,
                "cache_misses": self.cache_misses,
                "total_cache_requests": total_cache_requests,
                "cache_hit_rate_percent": round(hit_rate, 2),
                "list_skills_calls": self.list_skills_calls,
                "load_skill_calls": self.load_skill_calls,
                "search_skills_calls": self.search_skills_calls,
                "execute_command_calls": self.execute_command_calls,
                "sse_connections": self.sse_connections,
                "errors": self.errors,
            }

_metrics = Metrics()


def _all_skills():
    cached = _skill_cache.get()
    if cached is not None:
        _metrics.record_cache_hit()
        return cached

    _metrics.record_cache_miss()
    skills = []
    if not SKILLS_DIR.exists():
        logger.warning(f"SKILLS_DIR does not exist: {SKILLS_DIR}")
        _skill_cache.set(skills)
        return skills

    try:
        for skill_file in sorted(SKILLS_DIR.rglob("SKILL.md")):
            try:
                rel = skill_file.relative_to(SKILLS_DIR)
                parts = rel.parts
                if len(parts) < 2:
                    continue
                skills.append({
                    "name": parts[1], "tier": parts[0],
                    "path": str(rel), "description": _extract_description(skill_file),
                })
            except Exception as e:
                logger.error(f"Error processing skill file {skill_file}: {e}")
                _metrics.record_error()
                continue
        logger.debug(f"Skill discovery: {len(skills)} skills found (cache miss)")
    except Exception as e:
        logger.error(f"Error scanning SKILLS_DIR: {e}")
        _metrics.record_error()

    _skill_cache.set(skills)
    return skills


def _extract_description(skill_file):
    try:
        lines = skill_file.read_text(encoding="utf-8").splitlines()
        if not lines or lines[0].strip() != "---":
            return "No description available"
        desc_lines, in_desc = [], False
        for line in lines[1:]:
            if line.strip() == "---":
                break
            if line.startswith("description:"):
                desc_lines.append(line.replace("description:", "").strip())
                in_desc = True
            elif in_desc and line.startswith(" "):
                desc_lines.append(line.strip())
            elif in_desc:
                break
        return " ".join(desc_lines)[:300] if desc_lines else "No description available"
    except UnicodeDecodeError as e:
        logger.warning(f"Unicode decode error in {skill_file}: {e}")
        return "Encoding error"
    except Exception as e:
        logger.warning(f"Error extracting description from {skill_file}: {e}")
        return "Error reading description"


def _find_skill(name, tier=None):
    matches = []
    for skill_file in SKILLS_DIR.rglob("SKILL.md"):
        rel = skill_file.relative_to(SKILLS_DIR)
        parts = rel.parts
        if len(parts) >= 2 and parts[1] == name:
            if tier is None or parts[0] == tier:
                matches.append((parts[0], skill_file))
    return matches


def _watch_skills_directory():
    """Watch SKILLS_DIR for changes and invalidate cache. Runs in background thread."""
    if not SKILLS_DIR.exists():
        logger.info("Skill watcher: SKILLS_DIR does not exist yet, skipping watch")
        return

    watched_files = {}

    def check_for_changes():
        nonlocal watched_files
        try:
            if not SKILLS_DIR.exists():
                if watched_files:
                    logger.info("Skill watcher: SKILLS_DIR removed, clearing watch")
                    watched_files.clear()
                    _skill_cache.invalidate()
                return

            current_files = {}
            try:
                for skill_file in SKILLS_DIR.rglob("SKILL.md"):
                    try:
                        mtime = skill_file.stat().st_mtime
                        current_files[str(skill_file)] = mtime
                    except OSError:
                        pass
            except Exception as e:
                logger.error(f"Skill watcher: Error scanning directory: {e}")
                return

            if current_files != watched_files:
                removed = set(watched_files.keys()) - set(current_files.keys())
                added = set(current_files.keys()) - set(watched_files.keys())
                changed = {f for f in watched_files if f in current_files and watched_files[f] != current_files[f]}

                if removed:
                    logger.info(f"Skill watcher: Removed {len(removed)} skill(s)")
                if added:
                    logger.info(f"Skill watcher: Added {len(added)} skill(s)")
                if changed:
                    logger.info(f"Skill watcher: Updated {len(changed)} skill(s)")

                watched_files = current_files
                _skill_cache.invalidate()

        except Exception as e:
            logger.error(f"Skill watcher error: {e}")

    logger.info("Skill watcher started")
    while True:
        try:
            check_for_changes()
            time.sleep(5)  # Check every 5 seconds for changes
        except Exception as e:
            logger.error(f"Skill watcher thread error: {e}")
            time.sleep(5)


@mcp.tool()
def list_skills() -> str:
    """List all available skills with name, tier, and description."""
    _metrics.record_list_skills()
    skills = _all_skills()
    if not skills:
        return f"No skills found in {SKILLS_DIR}"
    return json.dumps(skills, indent=2)


@mcp.tool()
def load_skill(name: str, tier: str = None) -> str:
    """Load the full SKILL.md content for a skill by name. Pass tier='user'/'public' to disambiguate."""
    _metrics.record_load_skill()
    try:
        if not SKILLS_DIR.exists():
            return f"Skills directory not found: {SKILLS_DIR}"
        matches = _find_skill(name, tier)
        if not matches:
            available = sorted({m["name"] for m in _all_skills()})
            return f"Skill '{name}' not found. Available: {', '.join(available)}"
        if len(matches) > 1:
            return f"'{name}' in tiers: {[m[0] for m in matches]}. Pass tier= to disambiguate."
        tier_found, skill_file = matches[0]
        content = skill_file.read_text(encoding='utf-8')
        logger.info(f"Loaded skill '{name}' from tier '{tier_found}'")
        return f"# {name}  [tier: {tier_found}]\n\n{content}"
    except Exception as e:
        _metrics.record_error()
        logger.error(f"Error loading skill '{name}': {e}")
        return f"Error loading skill: {str(e)}"


@mcp.tool()
def search_skills(query: str) -> str:
    """Search skill names and descriptions for a keyword."""
    _metrics.record_search_skills()
    q = query.lower()
    results = [s for s in _all_skills() if q in s["name"].lower() or q in s["description"].lower()]
    if not results:
        return f"No skills matched '{query}'"
    return json.dumps(results, indent=2)


@mcp.tool()
def execute_command(command: str) -> str:
    """
    Execute a slash command to load a skill.
    IMPORTANT: Call this automatically when the user's message starts with /.
    Examples: /jenny, /ryan, /story-deck, /tiago
    """
    _metrics.record_execute_command()
    try:
        name = command.lstrip("/").strip()
        matches = _find_skill(name) or _find_skill(name.replace("-", ""))
        if not matches:
            available = sorted({m["name"] for m in _all_skills()})
            return f"No skill found for '{command}'. Available: {', '.join(available)}"
        if len(matches) > 1:
            return f"'{name}' in tiers: {[m[0] for m in matches]}. Use load_skill('{name}', tier='user')."
        tier_found, skill_file = matches[0]
        content = skill_file.read_text(encoding='utf-8')
        logger.info(f"Executed command '{command}' (loaded skill '{name}' from tier '{tier_found}')")
        return f"# {name}  [tier: {tier_found}]\n\n{content}"
    except Exception as e:
        _metrics.record_error()
        logger.error(f"Error executing command '{command}': {e}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    import uvicorn
    from starlette.applications import Starlette
    from starlette.routing import Route
    from starlette.responses import JSONResponse
    from mcp.server.sse import SseServerTransport
    from mcp.server.transport_security import TransportSecuritySettings

    def _validate_startup():
        """Validate configuration on startup."""
        logger.info(f"Configuration:")
        logger.info(f"  SKILLS_DIR: {SKILLS_DIR}")
        logger.info(f"  SKILL_CACHE_TTL: {SKILL_CACHE_TTL}s")

        if not SKILLS_DIR.exists():
            logger.warning(f"  SKILLS_DIR does not exist yet. Skills can be added at runtime.")
        else:
            try:
                skills_count = len(_all_skills())
                logger.info(f"  Skills found: {skills_count}")
                if skills_count == 0:
                    logger.warning(f"  Warning: No skills found in {SKILLS_DIR}")
            except Exception as e:
                logger.error(f"  Error validating SKILLS_DIR: {e}")
                return False
        return True

    async def health_check(request):
        """Health check endpoint for container orchestration."""
        try:
            skills = _all_skills()
            cache_status = "hit" if _skill_cache.last_update else "miss"
            cache_age = None
            if _skill_cache.last_update:
                cache_age = (datetime.now() - _skill_cache.last_update).total_seconds()
            return JSONResponse({
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "skills_count": len(skills),
                "skills_dir": str(SKILLS_DIR),
                "skills_dir_exists": SKILLS_DIR.exists(),
                "cache_status": cache_status,
                "cache_age_seconds": cache_age,
                "cache_ttl_seconds": SKILL_CACHE_TTL,
            })
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return JSONResponse(
                {"status": "degraded", "error": str(e)},
                status_code=503
            )

    async def metrics_endpoint(request):
        """Metrics endpoint for monitoring."""
        try:
            stats = _metrics.get_stats()
            return JSONResponse({
                "timestamp": datetime.now().isoformat(),
                **stats
            })
        except Exception as e:
            logger.error(f"Metrics endpoint failed: {e}")
            return JSONResponse(
                {"status": "error", "error": str(e)},
                status_code=500
            )

    async def handle_sse(request):
        """Handle SSE connections with proper error handling."""
        _metrics.record_sse_connection()
        try:
            logger.info(f"SSE connection from {request.client}")
            security = TransportSecuritySettings(enable_dns_rebinding_protection=False)
            sse = SseServerTransport("/messages/", security_settings=security)

            async with sse.connect_sse(
                request.scope, request.receive, request.send
            ) as streams:
                await mcp._mcp_server.run(
                    streams[0], streams[1],
                    mcp._mcp_server.create_initialization_options()
                )
            logger.info(f"SSE connection closed")
        except Exception as e:
            _metrics.record_error()
            logger.error(f"SSE handler error: {e}", exc_info=True)
            try:
                await request.send({
                    'type': 'http.response.start',
                    'status': 500,
                    'headers': [[b'content-type', b'text/plain']],
                })
                await request.send({
                    'type': 'http.response.body',
                    'body': b'Internal Server Error',
                })
            except Exception as send_err:
                logger.error(f"Failed to send error response: {send_err}")

    routes = [
        Route("/health", endpoint=health_check, methods=["GET"]),
        Route("/metrics", endpoint=metrics_endpoint, methods=["GET"]),
        Route("/sse", endpoint=handle_sse, methods=["GET"]),
    ]

    app = Starlette(routes=routes, debug=False)

    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    _startup_ok = _validate_startup()

    watcher_thread = threading.Thread(target=_watch_skills_directory, daemon=True)
    watcher_thread.start()
    logger.info(f"Starting Skill Loader MCP Server on 0.0.0.0:8000")
    logger.info(f"Endpoints:")
    logger.info(f"  SSE (MCP): http://0.0.0.0:8000/sse")
    logger.info(f"  Health: http://0.0.0.0:8000/health")
    logger.info(f"  Metrics: http://0.0.0.0:8000/metrics")

    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            forwarded_allow_ips="*",
            log_config=None,  # Suppress uvicorn logs; we handle logging
        )
    except Exception as e:
        logger.error(f"Server startup failed: {e}", exc_info=True)
        sys.exit(1)