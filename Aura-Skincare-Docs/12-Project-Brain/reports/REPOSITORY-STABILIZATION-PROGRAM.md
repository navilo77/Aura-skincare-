# Aura Skincare — Repository Stabilization Program (Enterprise Edition)

**Date:** 2026-10-06
**Branch:** `release/v1.1`
**HEAD:** `81d4df0` (merge: integrate 1-5 features into v1.1)
**Status:** Feature development PAUSED — Repository Stabilization Phase ACTIVE
**Constraint:** READ-ONLY AUDIT — no files modified, no commits made

---

## Executive Summary

The Aura Skincare repository contains **production-quality code** but is in a **highly unstable state** from a repository management perspective. The working tree diverges sharply from the index (282 unstaged changes vs 90 staged), critical security gaps exist (`backend/.env` and `certs/` are untracked and not gitignored), and the AI routing architecture contains a functional bug (RouterAgent bypass). The documentation structure is excellent and comprehensive, but the git state, security posture, and commit readiness are **BLOCKED** for any push to remote.

**Overall Assessment:**
- Code quality: **Good** (well-structured FastAPI + Next.js, consistent patterns)
- Architecture: **Mostly compliant** with one critical violation (RouterAgent bypass)
- Security: **Poor** (secrets at risk of being committed)
- Git hygiene: **Poor** (massive unstaged divergence, dependency closure failure)
- Documentation: **Good coverage, unreliable SSoT** (contradictions between docs and implementation)
- Testing: **Adequate** for core modules, missing tests for new modules

This roadmap provides a complete, prioritized stabilization plan to transform the repository into a professional, maintainable, production-ready, enterprise-grade development environment.

---

## Repository Health Score

| Area | Score (1-10) | Rationale |
|------|:---:|-----------|
| **Architecture** | 7/10 | Modular monolith is well-structured; one critical violation (RouterAgent bypass); duplicate agent systems (`app/agents/` vs `modules/ai/agents/`) |
| **Backend** | 8/10 | Consistent module structure, strong typing, good patterns; some dead code, incomplete modules (payment, notification), missing services in customer/inventory/order |
| **Frontend** | 8/10 | Clean Next.js App Router structure, consistent with backend modules; missing tests, test artifacts in public/, no error boundary |
| **AI Platform** | 7/10 | Sophisticated LangGraph + RAG implementation; Router bypass is critical bug; heuristic intent detection limits scalability |
| **Documentation** | 6/10 | Comprehensive coverage (20 sections) but unreliable SSoT — `00-Project-Memory` contradicts implementation, duplicate IDs, missing ADRs |
| **Security** | 3/10 | 🔴 **CRITICAL** — `backend/.env` and `certs/` not gitignored; hardcoded n8n tokens; PII in test_checkout.json; insecure defaults in settings.py |
| **Testing** | 6/10 | Good unit test coverage for core modules; missing tests for payment, marketing_ai, order_automation, knowledge; zero frontend tests |
| **DevOps** | 6/10 | CI exists (ruff, mypy, pytest, docker build); no CD pipeline; dev-only docker-compose; no production deployment config |
| **Git** | 4/10 | 🔴 **CRITICAL** — 282 unstaged changes invisible to commit; dependency closure failure; 3 messy local commits; dummy migration staged for deletion |
| **Maintainability** | 7/10 | Consistent naming, strong typing, good module boundaries; some duplication (password hashing, token creation), missing docstrings, Bengali strings in code |

**Composite Score: 6.2/10 — STABILIZATION REQUIRED**

---

## Critical Findings

### P0 — Critical (Blocking; Fix Before ANY Git Commit)

| # | Finding | Location | Impact |
|---|---------|----------|--------|
| P0-1 | `backend/.env` contains real Supabase + JWT secrets and is **NOT gitignored** | `backend/.env` | Secrets would be committed by `git add -A` |
| P0-2 | `certs/` contains 16 private keys (ca.key, client/key.pem, server/key.pem) and is **NOT gitignored** | `certs/` | TLS private keys would be committed |
| P0-3 | 282 unstaged changes create **dependency closure failure** — staged AI files import unstaged modules | `backend/app/modules/ai/routes/ai.py` → unstaged imports | ImportError if only staged set is pushed |
| P0-4 | `langgraph_service.py:50` hardcodes `next_agent = "customer"`, bypassing RouterAgent | `backend/app/modules/ai/services/langgraph_service.py:50` | Router is dead code; routing architecture broken |
| P0-5 | `test_checkout.json` contains PII (email, full name, address) | `test_checkout.json` | Privacy violation; must delete |
| P0-6 | `.kilo/node_modules/` is untracked and would be staged by `git add -A` | `.kilo/node_modules/` | Pollutes repo with tooling dependencies |

### P1 — High (Fix Within Week 1-2)

| # | Finding | Location | Impact |
|---|---------|----------|--------|
| P1-1 | n8n sandbox tokens hardcoded in `docker-compose.yml` (identical values for API key + registration token) | `docker-compose.yml:21,23,46,47,54,123` | Secrets in committed file |
| P1-2 | `settings.py` has insecure defaults (`secret_key = "change-me"`) with no fail-loud behavior | `backend/app/config/settings.py:17-18` | App runs insecurely if `.env` missing |
| P1-3 | `.env.example` was deleted — no onboarding boilerplate remains | `.env.example` (deleted) | New developers cannot bootstrap environment |
| P1-4 | Payment module appears incomplete (stubs in models, repositories, routes, schemas, services) | `backend/app/modules/payment/` | Runtime errors if endpoints are hit |
| P1-5 | Notification module incomplete (missing services, routes in some areas) | `backend/app/modules/notification/` | Inconsistent API surface |
| P1-6 | `profile/` module has routes only — no models, services, schemas | `backend/app/modules/profile/` | Incomplete module |
| P1-7 | `customer/` and `inventory/` modules missing services | `backend/app/modules/customer/`, `inventory/` | Incomplete module structure |
| P1-8 | `OrderService` directly imports `ProductRepository` — cross-module dependency violation | `backend/app/modules/order/services/order.py` | Tight coupling; violates module boundaries |
| P1-9 | Duplicate password hashing: `shared/security/jwt.py` vs `shared/security/password.py` | `backend/app/shared/security/` | Dead code, inconsistency risk |
| P1-10 | Duplicate token creation in `auth/services/token.py` reimplements `shared/security/jwt.py` | `backend/app/modules/auth/services/token.py` | Dead code, inconsistency risk |
| P1-11 | `00-Project-Memory` docs claim AI is out of scope — contradicts implementation | `Aura-Skincare-Docs/00-Project-Memory/` | Unreliable SSoT; AI session boot uses false data |
| P1-12 | Duplicate Document IDs (GOV-001, GOV-002, SEC-002, AUTO-007) | `Aura-Skincare-Docs/01-Governance/`, `15-Security/`, `17-Automation/` | Governance traceability broken |
| P1-13 | `15-Security/authentication-policy.md` is a misnamed duplicate of `authorization-policy.md` | `Aura-Skincare-Docs/15-Security/` | Missing actual Authentication Policy |
| P1-14 | Missing ADRs: ADR-003 (LangGraph) and ADR-004 (Supabase) referenced but not existing | `Aura-Skincare-Docs/06-SAD/architecture-decisions.md` | Architecture decisions undocumented |
| P1-15 | 3 local commits are mixed (database fixes + features + merge) — not squashed or organized | git log | Poor commit history |

### P2 — Medium (Fix Within Week 2-4)

| # | Finding | Location | Impact |
|---|---------|----------|--------|
| P2-1 | Bengali fallback strings hardcoded in `customer_agent.py` | `backend/app/modules/ai/agents/customer_agent.py:145-177` | Blocks i18n; non-English strings in code |
| P2-2 | `frontend/public/` contains test artifact images (timestamped filenames) | `frontend/public/skincare_*.jpg` | Unprofessional; repo bloat |
| P2-3 | `tsconfig.tsbuildinfo` is tracked in git | `frontend/tsconfig.tsbuildinfo` | Should be gitignored |
| P2-4 | `frontend/.env` may not be gitignored at root level | `frontend/.env` | Potential secret leak |
| P2-5 | `AUDIT_REPORT.md` and `AURA-REPO-AUDIT.md` at root are temporary audit artifacts | Root directory | Repo pollution |
| P2-6 | `staged_files.txt` and `pycache_warning.txt` are debug dumps at root | Root directory | Repo pollution |
| P2-7 | Empty shared modules: `events/`, `types/`, `utils/`, `exceptions/` | `backend/app/shared/` | Unused placeholders |
| P2-8 | Duplicate `get_with_relations` pattern across repositories | Multiple repositories | Code duplication |
| P2-9 | `ProductListItem` schema defined but never used | `backend/app/modules/product/schemas/product.py` | Dead code |
| P2-10 | Missing frontend tests (no `__tests__/`, `jest.config.js`, or `vitest.config.ts`) | `frontend/` | Zero frontend test coverage |
| P2-11 | No global error boundary in `layout.tsx` | `frontend/src/app/layout.tsx` | Poor error UX |
| P2-12 | `12-Project-Brain/project-status.md` claims backend is upcoming (45% complete) — contradicts reality | `Aura-Skincare-Docs/12-Project-Brain/` | Unreliable project tracking |
| P2-13 | `10-Implementation/repo-structure.md` lists non-existent root folders (`Infrastructure/`, `Scripts/`, `Docs/`) | `Aura-Skincare-Docs/10-Implementation/` | Documentation drift |
| P2-14 | Corrupted frontmatter in governance/security docs (stray path prefixes as first line) | `01-Governance/`, `15-Security/` | Doc quality issue |
| P2-15 | Missing root OSS docs: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHANGELOG.md` | Root directory | OSS readiness gap |
| P2-16 | No doc validation CI (markdown lint, YAML schema validation) | `.github/workflows/ci.yml` | Documentation quality unchecked |

### P3 — Low (Fix Within Week 4-8)

| # | Finding | Location | Impact |
|---|---------|----------|--------|
| P3-1 | `.verify_index/` is empty Kilo-generated artifact | `.verify_index/` | Minor repo pollution |
| P3-2 | `frontend/.next/` and `backend/.venv/` present despite `.gitignore` | Working tree | Already ignored; cleanup only |
| P3-3 | `98-Archive/` contains only 1 file — may be incomplete | `Aura-Skincare-Docs/98-Archive/` | Archive hygiene |
| P3-4 | Missing docstrings on most service/repository classes | `backend/app/modules/*/services/*.py` | Maintainability |
| P3-5 | Inconsistent `__init__.py` exports across modules | Multiple modules | Import clarity |
| P3-6 | `tailwind.config.js` has very long lines | `frontend/tailwind.config.js` | Formatting |
| P3-7 | No integration tests for checkout flow, AI chat, product search | `backend/tests/` | Regression risk |
| P3-8 | No coverage reporting in CI | `.github/workflows/ci.yml` | Quality metrics missing |
| P3-9 | No Prettier config for frontend | `frontend/` | Formatting consistency |
| P3-10 | `shared/security/jwt.py` password functions duplicated in `password.py` | `backend/app/shared/security/` | Minor dead code |

---

## Technical Debt Register

| # | Debt Item | Impact | Priority | Estimated Effort |
|---|-----------|--------|:---:|:---:|
| TD-01 | RouterAgent bypass — hardcoded `next_agent="customer"` | High — routing architecture broken | P0 | 2h |
| TD-02 | Dependency closure failure — staged imports unstaged modules | High — push would break | P0 | 1h |
| TD-03 | `backend/.env` and `certs/` not gitignored | Critical — secrets at risk | P0 | 30m |
| TD-04 | Delete `test_checkout.json` (PII) | High — privacy violation | P0 | 5m |
| TD-05 | Insecure defaults in `settings.py` (`change-me` secrets) | High — silent insecure startup | P1 | 1h |
| TD-06 | Hardcoded n8n tokens in `docker-compose.yml` | Medium — secrets in committed file | P1 | 30m |
| TD-07 | Missing `.env.example` | Medium — onboarding blocker | P1 | 1h |
| TD-08 | Incomplete payment module | High — runtime errors | P1 | 4h |
| TD-09 | Incomplete notification module | Medium — inconsistent API | P1 | 2h |
| TD-10 | Incomplete `customer/`, `inventory/`, `profile/` modules | Medium — missing services | P1 | 8h |
| TD-11 | Cross-module violation: `OrderService` → `ProductRepository` | Medium — tight coupling | P1 | 4h |
| TD-12 | Duplicate password hashing (`jwt.py` vs `password.py`) | Low — dead code | P2 | 2h |
| TD-13 | Duplicate token creation in `TokenService` | Low — dead code | P2 | 1h |
| TD-14 | Bengali strings in `customer_agent.py` | Low — blocks i18n | P2 | 2h |
| TD-15 | `00-Project-Memory` contradicts implementation | High — unreliable SSoT | P1 | 4h |
| TD-16 | Duplicate/missing Document IDs in docs | Medium — governance broken | P1 | 2h |
| TD-17 | Missing ADRs (LangGraph, Supabase) | Medium — undocumented decisions | P1 | 2h |
| TD-18 | Missing tests: payment, marketing_ai, order_automation, knowledge | Medium — regression risk | P1 | 16h |
| TD-19 | No frontend tests | Medium — zero FE coverage | P2 | 16h |
| TD-20 | No CD pipeline | Medium — manual deployments | P2 | 8h |
| TD-21 | No doc validation CI | Low — doc quality unchecked | P2 | 2h |
| TD-22 | `ProductListItem` dead schema | Low — unused code | P3 | 30m |
| TD-23 | Empty shared modules (`events/`, `types/`, `utils/`) | Low — unused placeholders | P3 | 1h |
| TD-24 | No global error boundary in frontend | Low — poor error UX | P2 | 2h |

**Total Estimated Effort: ~85 hours (~3 weeks with 1 engineer)**

---

## Repository Stabilization Roadmap

### Phase 0: Immediate Blockers (Do Before ANY Git Commit)
**Duration:** 2 hours | **Owner:** Dev | **Blocking:** Yes

| # | Action | Area | Est. |
|---|--------|------|:---:|
| 0.1 | Add `backend/.env`, `certs/`, `backend/venv`, `.kilo/node_modules/`, `__pycache__/`, `*.pyc`, `staged_files.txt`, `pycache_warning.txt`, `test_checkout.json`, `frontend/public/skincare_*.jpg` to `.gitignore` | Security/Git | 30m |
| 0.2 | Delete `test_checkout.json` from working tree | Security | 5m |
| 0.3 | Stage ALL files required by staged AI imports together (dependency closure) | Git | 1h |
| 0.4 | Verify zero secrets in staged/indexed files (`git diff --cached \| Select-String "api_key\|secret\|password"`) | Security | 15m |

**Phase 0 Gate:** No commit proceeds until 0.1–0.4 pass.

---

### Phase 1: Git Hygiene (Week 1)
**Duration:** 1 day | **Owner:** Dev

| # | Action | Area | Est. |
|---|--------|------|:---:|
| 1.1 | Unstage `AUDIT_REPORT.md` and `AURA-REPO-AUDIT.md`; relocate to `Aura-Skincare-Docs/12-Project-Brain/reports/` or delete | Git/Docs | 30m |
| 1.2 | Stage all 68 unstaged deletions (obsolete root docs, old graphify skills, 98-Governance) | Git | 30m |
| 1.3 | Stage all 214 unstaged modifications (backend modules, frontend, tests) | Git | 2h |
| 1.4 | Squash 3 local commits into logical units: Foundation Cleanup → Product Architecture → AI Core → RAG Integration → Docs Consolidation | Git | 2h |
| 1.5 | Force-push cleaned `release/v1.1` to origin (coordinate with team) | Git | 15m |
| 1.6 | Delete `integration-v1.1` branch | Git | 5m |
| 1.7 | Set branch protection on `main` and `release/v1.1` | Git/DevOps | 15m |

---

### Phase 2: Security Hardening (Week 1-2)
**Duration:** 1 day | **Owner:** Dev + Security

| # | Action | Area | Est. |
|---|--------|------|:---:|
| 2.1 | Replace hardcoded n8n tokens in `docker-compose.yml` with `${VAR}` interpolation | Security | 30m |
| 2.2 | Add `backend/.env.example` back with all variables documented | Security | 1h |
| 2.3 | Fix insecure defaults in `settings.py` — fail-loud if secrets are `change-me` in production | Security | 1h |
| 2.4 | Add `SECURITY.md` with vulnerability disclosure policy | Docs/Security | 30m |
| 2.5 | Add pre-commit hook for secret scanning (`detect-secrets` or `gitleaks`) | DevOps | 1h |
| 2.6 | Rotate any potentially exposed secrets (Supabase, Gemini, JWT) | Security | 30m |
| 2.7 | Audit all environment variables for unnecessary exposure | Security | 1h |

---

### Phase 3: Architecture Alignment (Week 2-3)
**Duration:** 3 days | **Owner:** Architect + Dev

| # | Action | Area | Est. |
|---|--------|------|:---:|
| 3.1 | Fix RouterAgent bypass in `langgraph_service.py` — wire conditional routing or document intentional single-agent fallback | AI/Arch | 2h |
| 3.2 | Refactor `routes/ai.py` to inject `EmbeddingService`, `VectorStore`, `GeminiProvider` via FastAPI `Depends` | AI/Backend | 2h |
| 3.3 | Resolve cross-module violation: `OrderService` → `ProductRepository` — extract product availability to shared service or event | Backend/Arch | 4h |
| 3.4 | Complete or remove `payment` and `notification` incomplete modules | Backend | 4h |
| 3.5 | Complete `customer/`, `inventory/`, `profile/` missing services/repositories | Backend | 8h |
| 3.6 | Consolidate duplicate agent systems: clarify relationship between `app/agents/` and `modules/ai/agents/` | Architecture | 4h |
| 3.7 | Add `knowledge` routes and services to expose RAG management API | Backend | 4h |
| 3.8 | Validate all modules against `06-SAD/module-boundaries.md` | Architecture | 4h |
| 3.9 | Remove dead code: `ProductListItem`, `ProductDetail` schemas; consolidate password/token logic | Backend | 2h |

---

### Phase 4: Documentation Synchronization (Week 3-4)
**Duration:** 3 days | **Owner:** Dev + Tech Writer

| # | Action | Area | Est. |
|---|--------|------|:---:|
| 4.1 | Reconcile `00-Project-Memory` with reality — update `ARCHITECTURE.md`, `PROJECT_STATE.md`, `CURRENT_STATE.md`, `AI_RULES.md`, `CHANGELOG.md` | Docs | 2h |
| 4.2 | Fix duplicate Document IDs (GOV-001, GOV-002, SEC-002, AUTO-007) | Docs | 1h |
| 4.3 | Fix `15-Security/authentication-policy.md` — rewrite as actual Authentication Policy or delete duplicate | Docs | 1h |
| 4.4 | Create missing ADRs: ADR-003 (LangGraph), ADR-004 (Supabase) | Docs | 2h |
| 4.5 | Remove corrupted path-prefix lines from governance/security docs | Docs | 1h |
| 4.6 | Add root `CONTRIBUTING.md` with branch strategy, PR process, commit conventions | Docs | 1h |
| 4.7 | Add root `CODE_OF_CONDUCT.md` | Docs | 30m |
| 4.8 | Add root `CHANGELOG.md` and archive `00-Project-Memory/CHANGELOG.md` | Docs | 1h |
| 4.9 | Translate or remove `Aura-Skincare-Docs/open.md` (Bengali quick-start) | Docs | 30m |
| 4.10 | Add `Aura-Skincare-Docs/README.md` as docs index/navigation | Docs | 1h |
| 4.11 | Archive `00-Project-Memory/` session files to `98-Archive/` or delete | Docs | 30m |
| 4.12 | Add doc validation CI (markdown lint, YAML schema validation) | DevOps | 2h |
| 4.13 | Expand `backend/README.md` and `frontend/README.md` or fold into root README | Docs | 2h |

---

### Phase 5: Code Quality (Week 4-5)
**Duration:** 3 days | **Owner:** Dev

| # | Action | Area | Est. |
|---|--------|------|:---:|
| 5.1 | Externalize Bengali fallback strings from `customer_agent.py` to `prompts/customer.md` or i18n system | Code Quality | 2h |
| 5.2 | Fix all `ruff` and `mypy` violations | Code Quality | 4h |
| 5.3 | Add `ruff format .` to pre-commit and CI | Code Quality | 30m |
| 5.4 | Add Prettier configuration for frontend | Code Quality | 1h |
| 5.5 | Add docstrings to all public classes and methods | Code Quality | 4h |
| 5.6 | Standardize `__init__.py` exports across all backend modules | Code Quality | 2h |
| 5.7 | Remove debug artifacts: `staged_files.txt`, `pycache_warning.txt`, `AUDIT_REPORT.md`, `AURA-REPO-AUDIT.md` | Code Quality | 15m |
| 5.8 | Add code review checklist to `CONTRIBUTING.md` | Code Quality | 30m |

---

### Phase 6: Testing (Week 5-6)
**Duration:** 1 week | **Owner:** Dev

| # | Action | Area | Est. |
|---|--------|------|:---:|
| 6.1 | Add `test_payment_routes.py`, `test_payment_services.py`, `test_payment_repositories.py` | Tests | 4h |
| 6.2 | Add `test_order_automation_services.py`, `test_order_automation_validators.py` | Tests | 4h |
| 6.3 | Add `test_knowledge_repositories.py`, `test_knowledge_services.py` | Tests | 4h |
| 6.4 | Add `test_marketing_ai_routes.py`, `test_marketing_ai_services.py` | Tests | 4h |
| 6.5 | Add frontend tests (Vitest + React Testing Library) | Tests/FE | 8h |
| 6.6 | Add Playwright E2E tests for checkout and AI chat flows | Tests | 8h |
| 6.7 | Add coverage reporting to CI (`pytest-cov`, Codecov or similar) | DevOps | 2h |
| 6.8 | Add database migration test job in CI (`alembic upgrade head` on test DB) | DevOps | 2h |
| 6.9 | Add AI evaluation tests per `09-Validation/ai-evaluation.md` | Tests/AI | 4h |

---

### Phase 7: DevOps & Release (Week 6-7)
**Duration:** 1 week | **Owner:** DevOps + Dev

| # | Action | Area | Est. |
|---|--------|------|:---:|
| 7.1 | Split `docker-compose.yml` into `docker-compose.yml` (prod) and `docker-compose.dev.yml` (dev with sandbox, volumes, reload) | DevOps | 4h |
| 7.2 | Add multi-stage Dockerfile for backend | DevOps | 2h |
| 7.3 | Add CD pipeline for staging + production deployment | DevOps | 8h |
| 7.4 | Add `/health` smoke test to CI | DevOps | 1h |
| 7.5 | Add release automation (semantic-release or GitHub Releases) | DevOps | 4h |
| 7.6 | Add environment separation (dev/staging/prod configs) | DevOps | 4h |
| 7.7 | Add `compose.override.example.yml` usage documentation | Docs | 1h |
| 7.8 | Add frontend CI job (lint, typecheck, build) | DevOps | 2h |
| 7.9 | Add security scanning CI (Snyk, Trivy, or similar) | DevOps | 2h |

---

### Phase 8: AI Platform Completion (Week 7-8)
**Duration:** 1 week | **Owner:** AI Engineer + Dev

| # | Action | Area | Est. |
|---|--------|------|:---:|
| 8.1 | Implement Admin AI agent or remove `agents/admin/` directory | AI | 4h |
| 8.2 | Implement Marketing AI agent or remove `agents/marketing/` directory | AI | 4h |
| 8.3 | Replace heuristic `_select_tools()` with LLM-based intent detection using structured output | AI | 8h |
| 8.4 | Replace heuristic `_build_rag_query()` with LLM-based knowledge retrieval trigger | AI | 4h |
| 8.5 | Add Redis connection health check and fallback in `RedisSessionStore` | AI/Backend | 2h |
| 8.6 | Add streaming responses for `/ai/chat` endpoint | AI/Backend | 4h |
| 8.7 | Add conversation summarization to manage context window | AI | 4h |
| 8.8 | Add AI evaluation tests per `09-Validation/ai-evaluation.md` | AI/Tests | 4h |
| 8.9 | Document AI architecture decisions in `13-AI-Execution/` | Docs/AI | 2h |

---

## Commit Strategy

Design logical, reviewable commit groups. Avoid large mixed commits.

### Commit 1: `security: harden gitignore and remove secrets at risk`
**Files:** `.gitignore` (modified), deletion of `test_checkout.json`
**Purpose:** Block secret leakage before any other work
**Pre-condition:** Phase 0 complete

### Commit 2: `Foundation cleanup: remove obsolete & duplicate documents`
**Files:** 68 deletions of root reports, 98-Governance, graphify skills, stale root configs
**Purpose:** Clean repository root; all content preserved in `Aura-Skincare-Docs/12-Project-Brain/reports/`
**Note:** Pure deletions — no code changes

### Commit 3: `Product: metadata models, repositories, schemas, services + ProductSearchFilter`
**Files:** 68 staged adds + product module modifications + product test updates
**Purpose:** Complete product metadata expansion (benefits, ingredients, routines, skin types/concerns, tags)
**Dependencies:** None

### Commit 4: `AI: core agents, LangGraph router, providers, memory, tool_manager, customer_memory`
**Files:** Staged AI core + unstaged AI submodules (providers, memory, customer_memory, session_state, tool_manager, knowledge, integrations, payment, notification, marketing_ai, Alembic migrations)
**Purpose:** Complete AI platform with dependency closure
**Critical:** ALL unstaged AI imports must be included; verify `routes/ai.py` compiles

### Commit 5: `RAG: business-knowledge layer, embeddings, vector store, chunking + docs + tests`
**Files:** `Aura-Skincare-Docs/13-AI-Execution/RAG/` (6 docs + README), `backend/app/modules/ai/services/rag/` (9 files), `prompt_builder.py`, `test_rag_service.py`, `test_ai_rag_integration.py`
**Purpose:** Complete RAG pipeline with documentation and tests
**Dependencies:** Commit 4

### Commit 6: `docs: consolidate governance, reports, and fix documentation health`
**Files:** `Aura-Skincare-Docs/01-Governance/` (7 files), `12-Project-Brain/reports/` (32 files), `05-PRD/features/FEAT-005.yaml`, `15-Security/Sec-005-Supabase-Auth-Storage-Integration.md`
**Purpose:** Commit relocated documentation; fix duplicate IDs and corrupted frontmatter
**Dependencies:** Phase 4 complete

### Commit 7: `chore: update configs, fix gitignore, and remove debug artifacts`
**Files:** `Makefile`, `docker-compose.yml`, `backend/pyproject.toml`, `backend/uv.lock`, `frontend/package.json`, `frontend/package-lock.json`, `backend/alembic/env.py`, deletion of dummy migration `ee4283811b61`
**Purpose:** Final config hygiene and dummy migration removal
**Dependencies:** Phase 2, 7 complete

---

## Success Criteria

The Repository Stabilization Program is complete only when ALL of the following are verified:

1. **Git working tree is clean.** `git status` shows no unstaged changes, no untracked files except `.gitignore`d artifacts.
2. **Dependency closure is verified.** All imports in staged files resolve; `cd backend && uv run python -c "import app"` succeeds.
3. **Secrets are protected.** `backend/.env`, `certs/`, `test_checkout.json` are gitignored and removed. `git diff --cached | Select-String "api_key\|secret\|password"` returns nothing.
4. **Documentation matches implementation.** `00-Project-Memory` updated; no contradictions between docs and code; all ADRs exist.
5. **Architecture complies with SSoT.** RouterAgent wired or removed; module boundaries validated; no cross-module violations.
6. **Tests pass.** `cd backend && uv run pytest` passes with >80% coverage for core modules.
7. **CI passes.** All checks in `.github/workflows/ci.yml` pass on clean clone.
8. **Repository is production-ready.** Docker Compose works with `.env.example` only; no hardcoded secrets.
9. **Development can safely resume.** Branch protection enabled; CONTRIBUTING.md exists; pre-commit hooks active.

---

## Final Decision

### ⛔ RELEASE BLOCKED

**Reason:** The repository cannot be safely pushed to `origin/release/v1.1` in its current state due to:

1. **Security Gate FAIL:** `backend/.env` and `certs/` are untracked and NOT gitignored. A single `git add -A` would commit production secrets and TLS private keys.
2. **Dependency Closure FAIL:** Staged AI files import modules that are unstaged and untracked. Pushing only the staged set (90 files) would cause `ImportError` at runtime.
3. **Architecture Gate FAIL:** RouterAgent bypass (`langgraph_service.py:50`) is a functional bug that breaks the documented AI routing architecture.
4. **Git Hygiene FAIL:** 282 unstaged changes are invisible to `git commit`. The working tree and index represent different realities.

**Required Actions Before Release:**
1. Complete **Phase 0** (Immediate Blockers) — estimated 2 hours
2. Complete **Phase 1** (Git Hygiene) — estimated 1 day
3. Complete **Phase 2** (Security Hardening) — estimated 1 day
4. Complete **Phase 3** (Architecture Alignment) — estimated 3 days

**Minimum Viable Release Path:** Phases 0-3 must be complete (estimated 5 days) before `git push origin release/v1.1` is permitted.

---

## Appendix A: Immediate Next Actions (Next 24 Hours)

1. **Add security entries to `.gitignore`:**
   ```gitignore
   # Aura Security
   backend/.env
   backend/.venv
   certs/
   *.pem
   *.key
   __pycache__/
   *.pyc
   .kilo/node_modules/
   staged_files.txt
   pycache_warning.txt
   test_checkout.json
   frontend/public/skincare_*.jpg
   ```

2. **Delete `test_checkout.json`:**
   ```powershell
   Remove-Item -LiteralPath "test_checkout.json"
   ```

3. **Stage dependency-closure set:**
   ```powershell
   git add backend/app/modules/ai/schemas/ai.py
   git add backend/app/modules/ai/agents/router_agent.py
   git add backend/app/modules/ai/providers/base.py
   git add backend/app/modules/ai/services/tool_manager.py
   git add backend/app/modules/ai/memory/redis_session_store.py
   git add backend/app/modules/ai/memory/memory_manager.py
   git add backend/app/modules/ai/services/customer_memory/
   git add backend/app/modules/ai/services/session_state.py
   git add backend/app/modules/ai/services/tool_call_log.py
   # ... plus all other unstaged required files
   ```

4. **Run pre-commit secret scan:**
   ```powershell
   cd backend; uv run pip install detect-secrets; detect-secrets scan --baseline .secrets.baseline
   ```

5. **Verify imports compile:**
   ```powershell
   cd backend; uv run python -c "import app"
   ```

---

## Appendix B: Risk Register

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|:---:|:---:|-----------|
| 1 | Secrets committed to history | Medium | Critical | Phase 0 + 2; run `git filter-repo` if needed |
| 2 | ImportError after partial commit | High | High | Phase 0.3 — stage all dependency-closure files together |
| 3 | RouterAgent bypass causes incorrect AI behavior | Medium | Medium | Phase 3.1 — fix or document before next feature |
| 4 | Incomplete payment/notification modules cause runtime errors | Medium | High | Phase 3.4 — complete or gate behind feature flags |
| 5 | n8n sandbox tokens exposed in docker-compose | Low | Medium | Phase 2.1 — replace with env vars |
| 6 | Alembic multiple heads cause migration conflicts | Medium | High | Verify migration graph; resolve heads in Phase 1 |
| 7 | Frontend test images committed to git | High | Low | Phase 0.1 — gitignore or delete |
| 8 | `.kilo/node_modules/` staged accidentally | High | Low | Phase 0.1 — gitignore immediately |
| 9 | Missing tests for payment/notification cause production bugs | Medium | High | Phase 6 — add tests before feature completion |
| 10 | Hardcoded Bengali strings block i18n | Medium | Low | Phase 5.1 — externalize strings |
| 11 | `00-Project-Memory` docs mislead AI-assisted development | High | High | Phase 4.1 — reconcile with reality |
| 12 | Duplicate Document IDs break governance traceability | Medium | Medium | Phase 4.2 — assign unique IDs |

---

## Appendix C: Open Source Checklist

Before opening the repository to public contributors:

- [ ] `LICENSE` is appropriate (MIT present — verify it covers all code)
- [ ] `CONTRIBUTING.md` with setup, run, test, PR instructions
- [ ] `CODE_OF_CONDUCT.md`
- [ ] `SECURITY.md` with vulnerability reporting instructions
- [ ] `README.md` with badges (build, coverage, license)
- [ ] `CHANGELOG.md` at root
- [ ] `.gitignore` covers all secrets and artifacts
- [ ] No hardcoded credentials in any file
- [ ] CI passes on clean clone
- [ ] Docker Compose works with `.env.example` only
- [ ] Issue templates in `.github/ISSUE_TEMPLATE/`
- [ ] PR template in `.github/pull_request_template.md`
- [ ] Dependabot or Renovate config for dependency updates
- [ ] Code of conduct enforcement plan
- [ ] All ADRs documented and linked
- [ ] Architecture diagrams in `06-SAD/` are up-to-date

---

*End of Repository Stabilization Program — Enterprise Edition*
*Document becomes the official master plan for the Aura Repository Stabilization Program.*
