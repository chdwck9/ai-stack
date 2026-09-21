---
doc_id:
  - os-slug/bootstrap
version:
  - inherit from parent
last updated:
  - YYYY-MM-DD
tags:
  - cold-start
  - bootstrap
  - rebuild
  - sequence
  - verification
use_when:
  - Cold-start or rebuild queries; onboarding a new operator or agent; verifying system readiness before going live; "where do I start" queries.
agent_notes:
  - Cold-start order matters — follow the sequence strictly. Each checkpoint must be verified before proceeding. Do not skip steps based on assumed readiness.
scope:
---

## What this section is for

This is the 

**This is the most rebuild-critical section.** All other sections feed into it.

**Reverse-engineering note:** If no runbook exists, reconstruct from the dependency map in §4 (Structure & Anatomy) and §7 (Context & Relationships). Leaves of the dependency graph start first. Interview an engineer with: "Walk me through what you'd do if you had to rebuild this from scratch tomorrow."

---

## Identity & Purpose Summary
- What the system does (1-2 sentences)
- Who it's for
- What it doesn't do (boundaries prevent scope creep)

## Architecture Summary
- High-level diagram or component list
- Data flow: how pieces talk to each other
- Deployment topology (single server, containers, cloud, etc.)

## Tech Stack
- Languages, frameworks, libraries with versions
- Runtime versions (Node 22, Python 3.12, etc.)
- Key dependencies and why they were chosen

## Directory Structure
- File tree (not every file — just the skeleton)
- Which files are critical vs scaffolding

## Database / Persistence
- Schema, collections, or data models
- Migrations, seed data
- Backup/restore procedures

## API Contracts
- Endpoints with method, path, auth, request/response shapes
- Webhooks or event subscriptions
- Error handling patterns

## Configuration
- Environment variables (names, purpose, defaults)
- Secrets management
- Feature flags or toggles

## Build & Deploy
- Dockerfile(s), docker-compose
- CI/CD pipeline
- Deployment commands and rollback procedure
- Health checks

## Key Files
- The 5-10 files that define the system's behavior (paths + purpose)
- Not full content — just which files exist and what they do

## Known Patterns & Conventions
- Naming conventions
- How new features are added
- Code organization rules

## Known Issues & Limitations
- Technical debt, workarounds, things that break easily
- Things the agent should *not* change

## Security
- Auth flows, token management
- Data protection, compliance requirements

## Observability
- Logging format and location
- Monitoring, alerting
- Debugging procedures