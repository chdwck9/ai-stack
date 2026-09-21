# Wally — Mambu 2026
Mambu's modernised AWS deployment architecture replacing AWS Classic (Elastic Beanstalk). This workspace covers the customer migration programme, architecture decisions, BYOK, DR, and Escrow compatibility.

---

## Project-specific instructions
- Load @Wally-OS silently as background context for all queries unless overridden.
- Cross-reference @BCaaS-OS for DR, Escrow, and tier-mapping questions.
- Check the Active Ambiguity Zones (WAZ-001–WAZ-018) before claiming anything on BYOK, Escrow, DR, hybrid envs, or regional connectivity.
- WAZ-008 (migration breaking changes) and WAZ-009 (IP allow-list) are Richard-owned — flag before acting.
- Architecture and migration facts live in @Wally-OS; do not reconstruct from memory.

---

## Permissions
**Always:**
- Cross-reference @BCaaS-OS for any BCaaS ↔ Wally intersection topics.
- Cite the relevant WAZ when flagging an open question.
- Use the Agent Routing table in @Wally-OS to locate source sections.

**Ask first:**
- Any claim about Milestone delivery dates or environment counts.
- Anything touching Capital One (BYOK, WAZ-001) or Escrow (WAZ-002, WAZ-007).
- Proposed changes to migration phase ordering.

**Never:**
- Make RTO/RPO claims for Wally without checking Section: Systems & Mechanics.
- Assert Escrow compatibility for Wally customers — WAZ-002 is unresolved.
- Write migration comms about breaking changes without Arturas sign-off (WAZ-008).

---

## Resources
Lazy-load the Spec (@Wally-OS) and project resources from ./resources.md

---

Project skill: /wally