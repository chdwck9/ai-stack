# Skill Loader MCP Server — Operational Guide

## Overview
This MCP server exposes your agent skills as tools, accessible via Claude Code, Perplexity, and any MCP-compatible client. It's designed for robustness, daily updates without restart, and production container environments.

---

## Quick Start

```bash
export SKILLS_DIR=/path/to/skills
python3 skill_loader.py
```

Server starts on `0.0.0.0:8000`. The skill watcher detects changes every 5 seconds.

---

## Configuration

### Environment Variables

| Var | Default | Notes |
|-----|---------|-------|
| `SKILLS_DIR` | `/skills` | Path to directory containing `tier/skill_name/SKILL.md` files. Supports daily updates without restart. |
| `SKILL_CACHE_TTL` | `60` | Cache TTL in seconds. Reduce to 10-30s for very frequent skill updates; increase to 300+ if changes are rare. |

### Directory Structure
```
/skills/
├── user/
│   ├── jenny/
│   │   └── SKILL.md
│   ├── ryan/
│   │   └── SKILL.md
├── public/
│   ├── bcaas/
│   │   └── SKILL.md
```

Tiers organize skills by scope. `user` skills are personal; `public` are shared.

---

## Endpoints

### SSE (MCP) – `/sse`
- **Method:** GET
- **Purpose:** Server-Sent Events transport for MCP protocol
- **Used by:** Claude Code, Perplexity, and other MCP clients
- **Why two implementations?** Claude Code and Perplexity handle HTTP gateways differently. This server uses a public API (`request.send`) rather than private members to ensure compatibility with both.

### Health Check – `/health`
```bash
curl http://localhost:8000/health
```
Returns JSON with skill count, cache age, and directory status. Used by container orchestration (Kubernetes, Docker, etc.) to determine readiness.

### Metrics – `/metrics`
```bash
curl http://localhost:8000/metrics
```
Returns JSON with:
- Cache hit/miss rate
- Endpoint call counts (`list_skills`, `load_skill`, etc.)
- SSE connection count
- Error count

Use for monitoring cache efficiency and usage patterns.

---

## Daily Skill Updates (No Restart Required)

The skill watcher runs in a background thread and checks `SKILLS_DIR` every 5 seconds for changes.

**Adding a new skill:**
```bash
mkdir -p /skills/user/my_new_skill
cat > /skills/user/my_new_skill/SKILL.md << 'EOF'
---
name: my-new-skill
description: Does something awesome
---
# Skill content here
EOF
```

Within 5 seconds:
1. Watcher detects the new file
2. Cache is invalidated
3. Next `list_skills()` call discovers the new skill
4. No server restart needed

**Updating a skill:**
Edit the `SKILL.md` file. Same process — detected within 5 seconds.

**Removing a skill:**
Delete the `SKILL.md` file. Detected within 5 seconds.

---

## Logging & Debugging

All logs go to stderr in structured format:
```
2026-06-29 14:32:15,123 [INFO] Loaded skill 'jenny' from tier 'user'
2026-06-29 14:32:16,456 [INFO] SSE connection from 127.0.0.1:54321
2026-06-29 14:32:17,789 [INFO] Skill watcher: Added 1 skill(s)
```

### Log Levels
- `DEBUG`: Cache misses, detailed skill discovery (only if logging is set to DEBUG)
- `INFO`: Normal operation, skill loads, connections, config
- `WARNING`: SKILLS_DIR missing, 0 skills found
- `ERROR`: File I/O errors, encoding issues, handler exceptions

Set log level in startup code if needed (defaults to INFO).

---

## Monitoring in Production

### Health Check (Readiness Probe)
```yaml
# Example Kubernetes readinessProbe
readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 10
```

### Metrics (Alerting)
Check `/metrics` endpoint for:
- **Cache hit rate** — should be 80%+ after warmup. Low rate = `SKILL_CACHE_TTL` too short or frequent skill changes.
- **Error count** — should be 0 or very low. Rising errors indicate filesystem issues or malformed SKILL.md files.
- **SSE connections** — should match expected client connections. Zero = clients can't reach the server.

### Logs (Debugging)
Watch for:
- `SKILLS_DIR does not exist` — configuration issue
- `Skill watcher: Added N skill(s)` — skills detected successfully
- `SSE handler error:` — client connection issue, likely a transport incompatibility

---

## Known Limitations & Workarounds

### Limitation: No Real-Time File System Events
The watcher uses polling (every 5s) instead of OS-level events (inotify, FSEvents). Why? Container environments (Docker, K8s) often have strange filesystem semantics, and polling is more reliable.

**Workaround:** If you need sub-second updates, reduce `SKILL_CACHE_TTL` to 5s and let the cache expire faster.

### Limitation: No Built-In Rate Limiting
The server will happily handle 1000 concurrent requests. For very high concurrency, add rate limiting at the container/load balancer level.

**Workaround:** Use a reverse proxy (nginx, Envoy) with rate limits in front of the server.

---

## Suggested Improvements

### 1. Skill Versioning
Track skill update history:
```yaml
# In SKILL.md
---
name: jenny
version: "1.2.3"
updated: "2026-06-29T14:32:00Z"
---
```
Benefits: Clients can cache by version; easier rollback.

### 2. Skill Dependencies
Declare which skills depend on others:
```yaml
---
name: bcaas-integrator
requires:
  - jenny
  - ryan
---
```
Benefits: Clients can detect incompleteness; easier dependency management.

### 3. Skill Metadata & Tags
Add structured metadata:
```yaml
---
name: jenny
tier: user
tags:
  - agent
  - voice
  - conversational
scope: personal  # or "team", "public"
owner: richard.dykes@mambu.com
---
```
Benefits: Rich search, access control, usage tracking.

### 4. Skill Health Endpoint
Each skill could declare a health/liveness check:
```yaml
---
name: jenny
health_check: /health/jenny
---
```
The server could aggregate these into `/health` for end-to-end monitoring.

### 5. Skill Signing & Integrity
Sign skills with a private key; verify signature on load:
```yaml
---
name: jenny
signature: "base64-encoded-ed25519-signature"
---
```
Benefits: Detect tampering; ensure skills come from trusted sources.

### 6. Multi-Source Skill Discovery
Load skills from multiple locations:
```python
SKILLS_PATHS = ["/skills", "/mnt/shared/skills", "s3://bucket/skills"]
```
Benefits: Share skills across teams; centralized management.

### 7. Skill Caching by Hash
Cache skill content by content hash, not just TTL:
```python
def _skill_hash(content):
    return hashlib.sha256(content.encode()).hexdigest()
```
Benefits: Invalidate only when content actually changes.

### 8. Grafana Dashboard
Export metrics in Prometheus format:
```python
# /metrics endpoint could return Prometheus-formatted metrics
# HELP skill_cache_hits Total cache hits
# TYPE skill_cache_hits counter
skill_cache_hits{tier="user"} 1234
```
Benefits: Integrate with existing observability stacks.

---

## Deployment Examples

### Docker
```dockerfile
FROM python:3.11-slim
RUN pip install mcp starlette uvicorn
COPY skill_loader.py /app/
ENV SKILLS_DIR=/data/skills
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=5s CMD curl -f http://localhost:8000/health || exit 1
CMD ["python3", "/app/skill_loader.py"]
```

Mount skills volume:
```bash
docker run -v /local/skills:/data/skills -p 8000:8000 skill-loader
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: skill-loader
spec:
  replicas: 1
  selector:
    matchLabels:
      app: skill-loader
  template:
    metadata:
      labels:
        app: skill-loader
    spec:
      containers:
      - name: skill-loader
        image: skill-loader:latest
        ports:
        - containerPort: 8000
        env:
        - name: SKILLS_DIR
          value: /data/skills
        - name: SKILL_CACHE_TTL
          value: "60"
        volumeMounts:
        - name: skills
          mountPath: /data/skills
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
      volumes:
      - name: skills
        emptyDir: {}  # or: persistentVolumeClaim: { claimName: skills-pvc }
```

---

## Troubleshooting

**Q: Perplexity can't connect to the server.**
A: Check that the server is running and the SSE endpoint is accessible. Perplexity may use a different HTTP gateway than Claude Code. Verify logs for transport errors.

**Q: Skills aren't updating after I add a new file.**
A: The watcher checks every 5 seconds. Wait up to 10 seconds, then test `list_skills()`. If still missing, check file permissions and SKILLS_DIR path.

**Q: Cache hit rate is very low (< 50%).**
A: Reduce `SKILL_CACHE_TTL`. If you're updating skills frequently, set it to 10-30 seconds. Or check if clients are creating new server instances per request.

**Q: Server crashes when handling SSE connections.**
A: Check logs for `SSE handler error:`. This is usually a transport incompatibility. The refactored code uses the public `request.send` API, which should work with both Claude Code and Perplexity.

**Q: Health check returns "degraded".**
A: Check SKILLS_DIR path and permissions. Logs will indicate the exact error.

---

## Performance Notes

- **Startup time:** ~100ms (depends on skill count)
- **Skill discovery:** O(n) where n = skill files. Cached for 60s by default.
- **Memory:** ~5-10MB baseline + skill content. Scale: ~100KB per skill.
- **SSE connection overhead:** ~1KB per connection.

For 1000+ skills, consider:
1. Increasing `SKILL_CACHE_TTL` to reduce disk I/O
2. Splitting into multiple tiers or directories
3. Using a reverse proxy with caching

---

## Support & Feedback

Logs are detailed. If something breaks:
1. Check the logs (`stderr`)
2. Verify SKILLS_DIR path and permissions
3. Test endpoints manually:
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/metrics
   curl http://localhost:8000/sse  # This won't return until the client sends MCP messages
   ```
4. If the issue persists, add more logging and report with full logs and configuration.
