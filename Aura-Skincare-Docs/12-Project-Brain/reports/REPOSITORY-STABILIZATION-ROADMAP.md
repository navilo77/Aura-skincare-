# Aura Skincare — Repository Stabilization & Open Source Readiness Roadmap

**Date:** 2026-10-06
**Branch:** `release/v1.1`
**HEAD:** `81d4df0` (merge: integrate 1-5 features into v1.1)
**Status:** Feature development PAUSED — Repository Stabilization Phase ACTIVE
**Constraint:** READ-ONLY AUDIT — no files modified, no commits made

---

## Executive Summary

The Aura Skincare repository is in a **highly unstable state** despite containing significant production-quality code. The working tree diverges sharply from the index (282 unstaged changes vs 90 staged), critical security gaps exist (`backend/.env` and `certs/` are untracked and not gitignored), and the AI routing architecture contains a functional bug (RouterAgent bypass). The documentation structure is excellent, but the git state, security posture, and commit readiness are **BLOCKED** for any push.

This roadmap provides a complete, prioritized stabilization plan to transform the repository into a professional, maintainable, production-ready, open-source quality codebase.

---

## 1. Repository Structure

### Current State

| Path | Status | Action |
|---|---|---|
| `backend/` | ✅ Source of truth | Keep |
| `frontend/` | ✅ Source of truth | Keep |
| `Aura-Skincare-Docs/` | ✅ SSoT for docs | Keep |
| `.github/` | ✅ CI present | Keep |
| `.kilo/` | ⚠️ Tooling with `node_modules/` | Gitignore `node_modules/`, evaluate committing agent definitions |
| `certs/` | 🔴 Untracked, NOT gitignored | Add to `.gitignore`, never commit |
| `.env` (root) | ⚠️ Untracked, gitignored | Keep gitignored, verify no real secrets |
| `backend/.env` | 🔴 Untracked, NOT gitignored | Add to `.gitignore`, never commit |
| `database/` | 🗑️ Deleted (old root) | Confirm no references remain |
| `infrastructure/` | 🗑️ Deleted (old root) | Confirm no references remain |
| `shared/` | 🗑️ Deleted (old root) | Confirm no references remain |
| `automation/` | 🗑️ Deleted (old root) | Confirm no references remain |
| `ai/` | 🗑️ Deleted (old root) | Confirm no references remain |
| `tools/` | 🗑️ Deleted (old root) | Confirm no references remain |
| `tests/` | 🗑️ Deleted (old root) | Confirm no references remain |

### Issues Found

1. **Orphaned root artifacts**: `AUDIT_REPORT.md`, `AURA-REPO-AUDIT.md`, `staged_files.txt`, `pycache_warning.txt`, `test_checkout.json` sit at root and are untracked.
2. **Stale top-level READMEs deleted**: `backend/README.md` and `frontend/README.md` are 3-line stubs; root `README.md` references `backend/.env.example` which is deleted.
3. **`.kilo/node_modules/`** is untracked and would be staged by `git add -A`. It must be gitignored.
4. **`certs/`** contains 16 private keys (`ca.key`, `client/key.pem`, `server/key.pem`) and is **not** in `.gitignore`.

### Recommendations

- [ ] Confirm zero references to deleted root directories (`database/`, `infrastructure/`, `shared/`, `automation/`, `ai/`, `tools/`, `tests/`) in any committed or staged file.
- [ ] Decide fate of root audit artifacts: relocate to `Aura-Skincare-Docs/12-Project-Brain/reports/` or delete.
- [ ] Move `backend/README.md` and `frontend/README.md` content into root `README.md` and delete the stubs, or expand them.
- [ ] Add `.kilo/node_modules/` to `.gitignore`.
- [ ] Never commit `certs/` — treat as local development artifact only.

---

## 2. Git Repository

### Current State

| Metric | Count |
|---|---|
| Branch | `release/v1.1` (HEAD), `main` (v1.1.0-rc1), `integration-v1.1` |
| Ahead of origin | 3 commits (local only) |
| Staged (index) | 90 files (68 added, 21 modified, 1 deleted) |
| Unstaged (working tree) | 282 files (68 deleted, 214 modified) |
| Untracked | 154 files |
| Deleted (unstaged) | 68 files |

### Critical Issues

1. **Massive unstaged divergence**: 282 unstaged changes are invisible to `git commit`. A plain `git commit` would ship only the 90 staged files, leaving the working tree in a different state than history.
2. **Dependency closure failure**: Staged AI files import modules that are **unstaged** and will cause `ImportError` if only staged set is pushed:
   - `backend/app/modules/ai/schemas/ai.py` (unstaged modified)
   - `backend/app/modules/ai/agents/router_agent.py` (unstaged modified)
   - `backend/app/modules/ai/providers/base.py` (untracked)
   - `backend/app/modules/ai/services/tool_manager.py` (untracked)
   - `backend/app/modules/ai/memory/redis_session_store.py` (untracked)
   - `backend/app/modules/ai/services/customer_memory/` (untracked)
   - `backend/app/modules/ai/services/session_state.py` (untracked)
3. **Mixed commits**: The 3 local commits (`539f66f`, `6467328`, `81d4df0`) combine database fixes, feature additions, and a merge. They are not squashed or organized by concern.
4. **Dummy migration staged for deletion**: `backend/alembic/versions/ee4283811b61_create_users_table.py` is staged deleted. It is an empty `pass` migration. `38240b68e837` has `down_revision: None` and is the real users table migration. Safe to delete, but must verify no other migration references it.

### Branch Strategy Assessment

| Branch | Purpose | Health |
|---|---|---|
| `main` | v1.1.0-rc1 tag | ✅ Clean, protected |
| `release/v1.1` | Active development | ⚠️ 3 local commits ahead of origin, messy working tree |
| `integration-v1.1` | Merge reference | ✅ Points to same commit as HEAD |

### Recommendations

- [ ] **BLOCKER**: Resolve unstaged dependency closure before any commit. Stage ALL files required by staged imports together.
- [ ] Adopt **Trunk-Based Development** with `main` as protected trunk and short-lived feature branches.
- [ ] Rename `release/v1.1` to `develop` or `main` if this is the primary integration branch, or protect `release/v1.1` and require PRs.
- [ ] Squash the 3 local commits into logical units before push, or rebase onto `origin/release/v1.1`.
- [ ] Delete `integration-v1.1` branch — it is redundant.
- [ ] Create `CONTRIBUTING.md` with branch naming convention (`feat/`, `fix/`, `chore/`, `docs/`).
- [ ] Create `.gitignore` update commit FIRST, before any code commits, to prevent secrets from being staged.

---

## 3. Documentation

### Current State

`Aura-Skincare-Docs/` follows a numbered folder convention:

```
00-Foundation/       (vision, mvp-scope, non-goals, glossary)
01-Governance/       (change-management, document-lifecycle, documentation-policy, ownership-matrix, repository-standards, review-process, versioning-policy, roles-and-approval)
02-SSoT/             (ssot.data.yaml, ssot.summary.md)
03-Agent-Contracts/  (admin, customer, development, marketing, router)
04-Schemas/          (11 JSON schemas + spec)
05-PRD/              (features, personas, requirements, roadmap, user-flows)
06-SAD/              (ai-architecture, architecture-decisions, component-diagrams, data-flow, dependency-rules, deployment, error-handling, module-boundaries, sequence-diagrams, tech-stack)
07-Database/         (audit, backup, data-model, er-diagram, indexing, migration, naming, seed, soft-delete)
08-API/              (versioning, authentication, error-handling, endpoints)
09-Validation/       (acceptance-criteria, ai-evaluation, test-cases, test-strategy)
10-Implementation/  (branching, coding-standards, development-workflow, env-config, repo-structure)
11-Decisions/        (adr/, decisions-log)
12-Project-Brain/    (INDEX, backlog, milestones, project-status, reports/)
13-AI-Execution/     (agent-workflow, conversation-flows, escalation, hallucination-guardrails, memory-strategy, prompt-library, router-logic, RAG/)
14-Operations/       (backup, deployment, docker, incident, monitoring, observability, scaling)
15-Security/         (audit-logging, authentication-policy, authorization-policy, data-protection, prompt-security, Sec-005, secrets-management, threat-model, zero-trust)
16-Integrations/     (ai-providers, analytics, courier, email, instagram, messenger, payment, webhook-policy, whatsapp)
17-Automation/       (glossary, overview, content-pipeline, event-driven, failure-handling, marketing-automation, n8n-workflows, retry-policy, scheduled-jobs, workflow-standards)
18-Analytics/        (ai-metrics, analytics-strategy, automation-metrics, business-metrics, conversion, cost, customer, dashboards, feedback-loop, marketing, sales)
19-Testing/          (acceptance, ai, api, integration, performance, regression, security, testing-checklist, testing-strategy, unit)
98-Archive/         (AURA-DEV-001)
99-Templates/        (agent-contract, api-endpoint, architecture, business-rule, constraint, data-model, feature, new-adr, requirement, solution)
```

### Issues Found

1. **Duplicate governance docs**: `98-Governance/*.md` (staged for deletion) and `01-Governance/*.md` (untracked) have overlapping filenames (`change-management.md`, `document-lifecycle.md`, etc.). The `01-Governance` versions appear to be the canonical ones.
2. **Root reports duplicated**: Identical copies of root `*-REPORT.md` files exist in `Aura-Skincare-Docs/12-Project-Brain/reports/`. Root copies are staged for deletion; docs copies are untracked.
3. **Stale docs in 00-Project-Memory/**: `AI_RULES.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, `CURRENT_STATE.md`, `NEXT_TASK.md`, `PROJECT_STATE.md`, `SESSION_BOOT.md` appear to be session-level scratch documents, not project memory. They should be archived or removed for OSS.
4. **`open.md` contains Bengali instructions**: For open source, documentation should be in English. This file appears to be a personal startup guide.
5. **Missing root docs for OSS**:
   - `CONTRIBUTING.md` — no contribution guidelines
   - `CODE_OF_CONDUCT.md` — absent
   - `SECURITY.md` — absent (though `15-Security/secrets-management.md` exists in docs)
   - `CHANGELOG.md` — absent at root (exists in `00-Project-Memory/`)
6. **Schema validation gap**: `04-Schemas/` defines YAML schemas, but there is no automated validation that actual documents conform to them.

### Recommendations

- [ ] **Consolidate governance**: Commit `01-Governance/*.md`, delete `98-Governance/*.md` permanently.
- [ ] **Consolidate reports**: Commit `12-Project-Brain/reports/*.md`, delete root `*-REPORT.md` and `*-STATUS.md` files.
- [ ] **Archive 00-Project-Memory/**: Move session-specific files to `12-Project-Brain/reports/` or `98-Archive/`. Replace with a proper `CHANGELOG.md` at root.
- [ ] **Translate or remove `open.md`**: Replace with English `QUICKSTART.md` or remove entirely.
- [ ] **Add root OSS docs**: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHANGELOG.md`.
- [ ] **Add doc validation CI**: Lint markdown, validate YAML schemas in `04-Schemas/` and `05-PRD/`.
- [ ] **Add `docs/README.md`** as an index/table of contents for `Aura-Skincare-Docs/`.

---

## 4. Architecture

### Current Architecture: Modular Monolith

```
backend/app/
├── main.py                    # FastAPI app, CORS, middleware, health checks
├── config/
│   └── settings.py            # Pydantic Settings, env vars
├── api/
│   ├── router.py              # Top-level router
│   ├── dependencies/          # auth, rbac
│   ├── middleware/            # audit_log
│   ├── public/                # public routes (checkout)
│   └── v1/                    # versioned API routes
├── modules/                   # 16 domain modules
│   ├── admin/
│   ├── ai/
│   ├── analytics/
│   ├── auth/
│   ├── cart/
│   ├── customer/
│   ├── inventory/
│   ├── knowledge/             # NEW: knowledge chunks, embeddings
│   ├── marketing_ai/
│   ├── notification/
│   ├── order/
│   ├── order_automation/
│   ├── payment/               # NEW: incomplete
│   ├── product/               # EXPANDED: metadata models
│   ├── profile/
│   └── wishlist/
├── shared/                    # Cross-cutting concerns
│   ├── database/              # Base, session
│   ├── security/              # JWT, password
│   ├── exceptions/
│   ├── events/
│   ├── types/
│   └── utils/
├── integrations/              # External services
│   ├── email/                 # sendgrid
│   ├── payment/               # stripe
│   ├── redis.py
│   ├── storage/               # S3
│   ├── n8n/
│   ├── scrapling/
│   ├── seo/
│   ├── whatsapp/
│   └── ...
└── agents/                    # AI agents (admin, customer, developer, marketing, router)
```

### Architectural Violations Found

1. **RouterAgent bypass (CRITICAL)**:
   - `backend/app/modules/ai/services/langgraph_service.py:50` hardcodes `state["next_agent"] = "customer"`.
   - The LangGraph graph only has `router` and `customer` nodes — no `admin`, `marketing`, or `support` nodes.
   - `RouterAgent.handle()` returns different agents per `router.md` ("Only route"), but its output is discarded.
   - **Impact**: Router is non-functional dead code. Any future agent expansion requires graph refactoring.
   - **Fix**: Either wire conditional routing (`next_agent = response.tool_calls[0]["agent"]`) or remove RouterAgent and inline routing logic.

2. **AI boundary violation**:
   - `routes/ai.py` instantiates `EmbeddingService()` and `VectorStore(db)` directly in the route handler. These are infrastructure concerns that should be injected via dependencies.
   - `GeminiProvider` is instantiated at module level in `routes/ai.py` using `settings`. This makes testing difficult and couples route to provider implementation.

3. **Knowledge module coupling**:
   - `vector_store.py` imports `app.modules.knowledge.models.knowledge_chunk.KnowledgeChunk` and `app.modules.knowledge.schemas.knowledge.ChunkMetadata`. This is correct internal coupling, but the `knowledge` module has no routes or services exposed yet — it is a persistence layer only.

4. **Payment module incompleteness**:
   - `app/modules/payment/` has `models/`, `repositories/`, `routes/`, `schemas/`, `services/` directories but they appear to be stubs or partial implementations. This creates an incomplete module in production code.

5. **Notification module incompleteness**:
   - `routes/preference.py` and `services/delivery.py` are untracked additions. The notification module is not fully implemented per project memory.

### Dependency Direction Assessment

```
modules/ -> shared/          ✅ Correct
modules/ -> integrations/    ✅ Correct (via service injection)
ai/ -> product/              ✅ Correct (tools use ProductService)
ai/ -> knowledge/            ✅ Correct (RAG uses KnowledgeChunk)
routes/ -> services/         ✅ Correct
services/ -> repositories/   ✅ Correct
repositories/ -> models/     ✅ Correct
```

**No circular dependencies detected** in staged code.

### Recommendations

- [ ] **P0**: Fix RouterAgent bypass in `langgraph_service.py` — either wire routing or document it as intentional single-agent fallback.
- [ ] **P1**: Refactor `routes/ai.py` to inject `EmbeddingService`, `VectorStore`, and `GeminiProvider` via FastAPI dependencies.
- [ ] **P1**: Complete or remove `payment` and `notification` modules before next feature commit.
- [ ] **P2**: Add `app/modules/knowledge/routes/` and `app/modules/knowledge/services/` to expose knowledge management API.
- [ ] **P2**: Create `docs/architecture/` diagram (C4 model or similar) from existing `06-SAD/component-diagrams.md`.
- [ ] **P3**: Validate all modules against `06-SAD/module-boundaries.md` to ensure no coupling violations.

---

## 5. Backend

### Module Inventory

| Module | Models | Repositories | Services | Routes | Schemas | Status |
|---|---|---|---|---|---|---|
| admin | 7 | 6 | 6 | 1 | 6 | ✅ Complete |
| ai | 3 | 3 | 8+ | 1 | 2 | ⚠️ Incomplete staging |
| analytics | 1 | 4 | 3 | 2 | — | ✅ Complete |
| auth | 6 | 2 | 1 | 3 | — | ✅ Complete |
| cart | 1 | 1 | 1 | 1 | 1 | ✅ Complete |
| customer | 2 | — | — | 1 | — | ⚠️ Missing services |
| inventory | 6 | 1 | — | 6 | — | ⚠️ Missing services |
| knowledge | 1 | — | — | — | 1 | ⚠️ New, no routes/services |
| marketing_ai | 1 | 2 | 2 | 1 | 1 | ⚠️ Incomplete |
| notification | 1 | 2 | 2 | 1* | — | ⚠️ Incomplete |
| order | 4 | — | 1 | 4 | — | ⚠️ Missing repositories |
| order_automation | 1 | 2 | 1 | 1 | 1 | ✅ Complete |
| payment | 1 | 2 | 1 | 1 | 1 | ⚠️ Stub/incomplete |
| product | 16 | 14 | 14 | 5 | 15 | ✅ Complete |
| profile | — | — | — | 2 | — | ⚠️ Thin |
| wishlist | 1 | 1 | 1 | 1 | 1 | ✅ Complete |

### Code Quality Issues

1. **Dead code**: `prompt_manager.py` deleted and replaced by `prompt_builder.py`. Verified all staged callers migrated.
2. **Inconsistent naming**: `product_search_filter.py` uses snake_case (correct), but some schemas in other modules use mixed case.
3. **Long lines**: `tailwind.config.js` has very long lines (200+ chars). Python files generally comply with 88-char ruff limit.
4. **Missing type hints**: Some route handlers and services lack return type annotations.
5. **Hardcoded strings**: `customer_agent.py` has Bengali fallback responses hardcoded in `_generate_fallback_response()`.
6. **Unused imports**: Potential in some route files (not fully audited).

### Test Coverage Gaps

| Module | Unit Tests | Integration Tests | Status |
|---|---|---|---|
| admin | test_admin_routes.py | — | ⚠️ Routes only |
| ai | test_ai_routes.py, test_rag_service.py, test_ai_rag_integration.py | — | ✅ Good |
| analytics | test_analytics_repositories.py, test_analytics_services.py | — | ✅ Good |
| auth | test_auth_services.py, test_auth_repositories.py, test_auth_routes.py | — | ✅ Good |
| cart | test_cart_services.py, test_cart_wishlist_routes.py | — | ✅ Good |
| customer | test_customer_repositories.py, test_customer_routes.py, test_customer_services.py | — | ✅ Good |
| inventory | test_inventory_repositories.py, test_inventory_services.py | — | ✅ Good |
| notification | test_notification_services.py, test_notification_repositories.py | — | ⚠️ Missing routes |
| order | test_order_routes.py, test_order_repositories.py, test_order_services.py | — | ✅ Good |
| payment | — | — | 🔴 None |
| product | test_product_repositories.py, test_product_routes.py, test_product_services.py | — | ✅ Good |
| profile | test_profile_routes.py | — | ⚠️ Thin |
| wishlist | test_wishlist_services.py | — | ⚠️ Missing routes |

### Recommendations

- [ ] **P0**: Fix RouterAgent bypass (see Architecture section).
- [ ] **P1**: Add payment module tests (`test_payment_*.py`).
- [ ] **P1**: Add notification route tests.
- [ ] **P1**: Complete `customer`, `inventory`, and `order` repository/service implementations.
- [ ] **P2**: Remove Bengali hardcoded strings from `customer_agent.py` — move to `prompts/customer.md` or i18n system.
- [ ] **P2**: Add missing return type annotations across all route handlers.
- [ ] **P2**: Run `ruff check .` and `mypy .` and fix all violations.
- [ ] **P3**: Add integration tests for critical paths (checkout flow, AI chat, product search).
- [ ] **P3**: Add test coverage reporting (pytest-cov) to CI.

---

## 6. Frontend

### Current Structure

```
frontend/
├── .env
├── .next/
├── next-env.d.ts
├── next.config.js
├── node_modules/
├── package.json
├── postcss.config.js
├── public/
│   ├── skincare_hero_banner_1790835275248.jpg  ⚠️ Test artifact
│   └── skincare_product_1_1790835301413.jpg    ⚠️ Test artifact
├── README.md
├── src/
│   ├── app/
│   │   ├── admin/             (8 admin pages)
│   │   ├── ai/                (AI chat page)
│   │   ├── api/               (28 API route handlers)
│   │   ├── auth/              (login, register, forgot-password, reset-password)
│   │   ├── cart/              (cart page)
│   │   ├── checkout/          (checkout page)
│   │   ├── marketing/         (campaigns, content, history, templates)
│   │   ├── products/          (product listing + detail)
│   │   ├── profile/           (addresses, change-password, orders, edit)
│   │   ├── wishlist/          (wishlist page)
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx           (homepage)
│   ├── components/
│   │   ├── admin/             (admin-layout, admin-sidebar)
│   │   ├── ai/                (float-button)
│   │   ├── auth/              (password-strength)
│   │   ├── cart/              (cart-drawer)
│   │   ├── layout/            (footer, mobile-bottom-nav, navbar)
│   │   ├── providers/         (query-provider, theme-provider)
│   │   └── ui/                (badge, button, card, input, skeleton)
│   └── lib/
│       ├── api.ts
│       ├── hooks/            (useProducts.ts)
│       ├── services/         (auth, cart, product)
│       └── store/            (useAuthStore, useCartStore, useWishlistStore)
└── tailwind.config.js
```

### Issues Found

1. **Test artifacts in `public/`**: `skincare_hero_banner_*.jpg` and `skincare_product_1_*.jpg` are timestamped test images. They should be removed or replaced with real assets.
2. **Missing error handling**: No global error boundary in `layout.tsx`.
3. **API layer duplication**: `src/app/api/` contains route handlers that duplicate logic in `src/lib/services/`. Some API routes appear to be thin wrappers around service calls.
4. **No environment validation**: `frontend/.env` exists but is not gitignored at root level (it is inside `frontend/`, so it may be gitignored by frontend-specific rules — verify).
5. **Missing tests**: No frontend tests (`__tests__/`, `jest.config.js`, or `vitest.config.ts` absent).
6. **`tsconfig.tsbuildinfo`** is tracked in git — should be gitignored.

### Recommendations

- [ ] **P1**: Remove test images from `frontend/public/` or add them to `.gitignore` with a whitelist for real assets.
- [ ] **P1**: Add `frontend/.env` and `frontend/.env.local` to root `.gitignore` (or verify they are already covered).
- [ ] **P1**: Add `tsconfig.tsbuildinfo` to `.gitignore`.
- [ ] **P2**: Add error boundary component and global error handling in `layout.tsx`.
- [ ] **P2**: Consolidate API route handlers with `src/lib/services/` to avoid duplication.
- [ ] **P3**: Add frontend tests (Playwright or Vitest) and include in CI.
- [ ] **P3**: Add `frontend/README.md` with setup, run, build instructions.
- [ ] **P3**: Add ESLint + Prettier config if not already present (package.json shows `eslint-config-next`).

---

## 7. AI Platform

### Current State

**LangGraph Flow:**
```
RouterAgent -> CustomerAIAgent -> END
```

**Components:**

| Component | File | Status |
|---|---|---|
| RouterAgent | `agents/router_agent.py` | ⚠️ Bypassed |
| CustomerAIAgent | `agents/customer_agent.py` | ✅ Functional |
| LangGraphAIService | `services/langgraph_service.py` | ⚠️ Hardcoded routing |
| PromptBuilder | `services/prompt_builder.py` | ✅ New, replaces prompt_manager |
| RAGService | `services/rag/rag_service.py` | ✅ Complete |
| EmbeddingService | `services/rag/embedding_service.py` | ✅ Present |
| VectorStore | `services/rag/vector_store.py` | ✅ Uses pgvector |
| Retriever | `services/rag/retriever.py` | ✅ Present |
| ChunkBuilder | `services/rag/chunk_builder.py` | ✅ Present |
| KnowledgeRepository | `services/rag/knowledge_repository.py` | ✅ Present |
| CustomerMemoryService | `services/customer_memory/` | ✅ Present |
| MemoryManager | `memory/memory_manager.py` | ✅ Present |
| RedisSessionStore | `memory/redis_session_store.py` | ✅ Present |
| GeminiProvider | `providers/base.py` | ✅ Functional |
| ToolManager | `services/tool_manager.py` | ✅ Present |
| Tools | `tools/*.py` (9 tools) | ✅ Present |
| Prompts | `prompts/*.md` (4 files) | ✅ Present |
| Schemas | `schemas/ai.py` | ✅ Present |

### Architecture Compliance

**Aura AI Architecture Rules (from project memory):**

| Rule | Status | Finding |
|---|---|---|
| AI owns Intent Detection, Entity Extraction, Filter Creation, Recommendation Explanation | ⚠️ Partial | Intent detection exists in RouterAgent (bypassed). Entity extraction is keyword-based in `_select_tools()`. |
| AI never owns SQL, Repository, Database, Business Rules | ✅ Compliant | AI uses `ProductService` and `ProductSearchFilter` via tools. No direct SQL. |
| Backend owns Business Rules, Filtering, Sorting, Validation, Pagination | ✅ Compliant | `ProductRepository.get_list()` owns all filtering. |
| Only one product search tool: `search_products(filters)` | ✅ Compliant | `search_products.py` uses `ProductSearchFilter`. |
| Single query builder, no duplicated SQL | ✅ Compliant | `ProductRepository` uses one query builder. |

### Issues Found

1. **RouterAgent bypass**: As noted in Architecture section. This violates the documented routing architecture.
2. **Intent detection is heuristic**: `customer_agent.py:_select_tools()` uses keyword matching instead of LLM-based intent detection. This is functional but not scalable.
3. **RAG query detection is heuristic**: `customer_agent.py:_build_rag_query()` uses keyword matching for knowledge queries. Functional but limited.
4. **No Admin AI or Marketing AI agents implemented**: `agents/admin/` and `agents/marketing/` directories exist but are not wired into LangGraph.
5. **Memory persistence**: `RedisSessionStore` uses `app.integrations.redis.redis_client` which is a module-level singleton. No connection pooling or fallback.

### Recommendations

- [ ] **P0**: Fix RouterAgent bypass OR document intentional single-agent design and remove RouterAgent dead code.
- [ ] **P1**: Implement Admin AI and Marketing AI agents or remove their directories to avoid confusion.
- [ ] **P1**: Replace heuristic `_select_tools()` and `_build_rag_query()` with LLM-based intent/entity extraction using structured output.
- [ ] **P2**: Add Redis connection health check and fallback in `RedisSessionStore`.
- [ ] **P2**: Add AI evaluation tests (LLM-as-judge) per `09-Validation/ai-evaluation.md`.
- [ ] **P3**: Implement streaming responses for AI chat endpoint.
- [ ] **P3**: Add conversation summarization to prevent context window overflow.

---

## 8. Security

### Findings Summary

| Asset | Location | Git Status | Risk |
|---|---|---|---|
| Supabase pooler URL + password | `backend/.env` | Untracked, **NOT gitignored** | 🔴 HIGH |
| Supabase anon + service_role keys | `backend/.env` | Untracked, **NOT gitignored** | 🔴 HIGH |
| JWT_SECRET_KEY / SECRET_KEY | `backend/.env` | Untracked, **NOT gitignored** | 🔴 HIGH |
| GEMINI_API_KEY | `.env` (root) | Untracked, gitignored | ✅ Safe |
| `certs/ca.key` | `certs/` | Untracked, **NOT gitignored** | 🔴 HIGH |
| `certs/client/key.pem` | `certs/` | Untracked, **NOT gitignored** | 🔴 HIGH |
| `certs/server/key.pem` | `certs/` | Untracked, **NOT gitignored** | 🔴 HIGH |
| n8n sandbox tokens | `docker-compose.yml` | Committed | ⚠️ Hardcoded but sandbox-only |
| PII test data | `test_checkout.json` | Untracked | 🚨 Must delete |
| Secrets in committed code | — | None found | ✅ Safe |

### Detailed Issues

1. **`backend/.env` not gitignored**: Contains real production credentials. A single `git add -A` would stage it. This is the **highest priority security fix**.
2. **`certs/` not gitignored**: Contains CA private key, client private key, server private key. These are TLS private keys. If pushed, they compromise the entire n8n sandbox TLS infrastructure.
3. **Hardcoded n8n tokens in `docker-compose.yml`**: `SANDBOX_API_KEYS=gJfMktswaSiD4G2cOp1Louz0l57UHVFC` and `SANDBOX_RUNNER_REGISTRATION_TOKEN` are identical hardcoded values. While these are sandbox artifacts, they should use `${VAR}` interpolation with a `.env` file.
4. **`test_checkout.json`**: Contains email, full name, address — PII that should not be in the repository.
5. **`.env` at root**: Contains GEMINI_API_KEY and other secrets. It is gitignored, but verify it is not accidentally staged.

### Recommendations

- [ ] **P0**: Add `backend/.env` to `.gitignore`.
- [ ] **P0**: Add `certs/` to `.gitignore`.
- [ ] **P0**: Delete `test_checkout.json` from working tree.
- [ ] **P0**: Verify no secrets are in staged/indexed files (`git diff --cached | grep -i "api_key\|secret\|password"`).
- [ ] **P1**: Replace hardcoded n8n tokens in `docker-compose.yml` with environment variable references.
- [ ] **P1**: Add `backend/.env.example` back (it was deleted) with placeholder values.
- [ ] **P1**: Add `SECURITY.md` with vulnerability disclosure policy.
- [ ] **P2**: Audit `docker-compose.yml` for any other hardcoded secrets.
- [ ] **P2**: Add pre-commit hook to scan for secrets (e.g., `detect-secrets` or `gitleaks`).
- [ ] **P3**: Rotate any secrets that may have been exposed in local `.env` files.

---

## 9. Testing

### Current Test Suite

| Test File | Module | Type |
|---|---|---|
| `test_admin_routes.py` | admin | Route |
| `test_ai_routes.py` | ai | Route |
| `test_ai_rag_integration.py` | ai | Integration |
| `test_rag_service.py` | ai | Unit |
| `test_analytics_repositories.py` | analytics | Repository |
| `test_analytics_services.py` | analytics | Service |
| `test_auth_services.py` | auth | Service |
| `test_auth_repositories.py` | auth | Repository |
| `test_auth_routes.py` | auth | Route |
| `test_auth.py` | auth | Unit |
| `test_authz_repositories.py` | authz | Repository |
| `test_authz_services.py` | authz | Service |
| `test_cart_services.py` | cart | Service |
| `test_cart_wishlist_routes.py` | cart/wishlist | Route |
| `test_customer_repositories.py` | customer | Repository |
| `test_customer_routes.py` | customer | Route |
| `test_customer_services.py` | customer | Service |
| `test_inventory_repositories.py` | inventory | Repository |
| `test_inventory_services.py` | inventory | Service |
| `test_notification_repositories.py` | notification | Repository |
| `test_notification_services.py` | notification | Service |
| `test_order_repositories.py` | order | Repository |
| `test_order_routes.py` | order | Route |
| `test_order_services.py` | order | Service |
| `test_product_repositories.py` | product | Repository |
| `test_product_routes.py` | product | Route |
| `test_product_services.py` | product | Service |
| `test_profile_routes.py` | profile | Route |
| `test_wishlist_services.py` | wishlist | Service |

### Gaps

1. **No payment tests**: `test_payment_*.py` missing entirely.
2. **No marketing_ai tests**: `test_marketing_ai_*.py` missing.
3. **No order_automation tests**: `test_order_automation_*.py` missing.
4. **No knowledge tests**: `test_knowledge_*.py` missing.
5. **No integration tests for checkout flow**: `test_checkout.json` exists but no automated test uses it.
6. **No frontend tests**: Zero frontend test coverage.

### CI/CD Testing

Current GitHub Actions CI runs:
- `ruff check .`
- `mypy`
- `pytest` with SQLite fallback
- `docker compose build backend`

Missing:
- Frontend lint/test
- Security scanning
- Coverage reporting
- Database migration test (`alembic upgrade head` on test DB)

### Recommendations

- [ ] **P1**: Add `test_payment_routes.py`, `test_payment_services.py`, `test_payment_repositories.py`.
- [ ] **P1**: Add `test_order_automation_services.py`, `test_order_automation_validators.py`.
- [ ] **P1**: Add `test_knowledge_repositories.py`, `test_rag_service.py` (already added).
- [ ] **P2**: Add frontend tests with Vitest + React Testing Library.
- [ ] **P2**: Add end-to-end tests with Playwright (`.playwright-mcp/` already exists).
- [ ] **P2**: Add coverage reporting to CI (`pytest-cov`, `codecov` or similar).
- [ ] **P2**: Add database migration test job in CI.
- [ ] **P3**: Add performance/load tests for AI endpoints and product search.

---

## 10. DevOps

### Current State

**Docker:**
- `docker-compose.yml` defines: `redis`, `sandbox-api`, `sandbox-runner`, `backend`, `n8n`.
- `backend/Dockerfile` exists.
- No multi-stage builds or production-optimized images.
- No Docker Compose override for production.

**Makefile:**
- Targets: `install`, `dev`, `test`, `lint`, `format`, `clean`, `docker-up`, `docker-down`.
- Targets work correctly.

**CI/CD:**
- GitHub Actions: `ci.yml` with `lint-test` and `docker-build` jobs.
- Runs on all branch pushes and PRs.
- No CD pipeline (no auto-deploy).
- No environment separation (dev/staging/prod).

**Environment:**
- `backend/.env.example` exists but is deleted in working tree.
- `compose.override.example.yml` exists but appears unused.
- No `.env` file committed (correct).

### Issues Found

1. **No production Docker Compose**: `docker-compose.yml` is development-only (volumes, `uv run uvicorn --reload`).
2. **No CD**: Manual push required. No staging environment.
3. **n8n sandbox in production compose**: The n8n sandbox services (`sandbox-api`, `sandbox-runner`) should not be in the same compose file as the backend for production. They are development/automation tools.
4. **No health check endpoints tested in CI**: `/health` and `/health/ready` exist but are not validated in CI.
5. **`backend/.env.example` deleted**: Needs to be restored or recreated.

### Recommendations

- [ ] **P1**: Split `docker-compose.yml` into `docker-compose.yml` (prod) and `docker-compose.dev.yml` (dev with sandbox, volumes, reload).
- [ ] **P1**: Add CD pipeline for staging deployment (Vercel for frontend, Render/Railway/Fly.io for backend).
- [ ] **P1**: Restore `backend/.env.example` with all required variables.
- [ ] **P2**: Add Docker multi-stage build for smaller production images.
- [ ] **P2**: Add `docker-compose.override.yml` for local development overrides.
- [ ] **P2**: Add CI job for `/health` endpoint smoke test after deploy.
- [ ] **P3**: Add infrastructure-as-code (Terraform/Pulumi) for cloud resources if applicable.
- [ ] **P3**: Add release automation (semantic-release or GitHub Release action).

---

## 11. Code Quality

### Current State

**Linting/Formatting:**
- `ruff` configured in `pyproject.toml` (target Python 3.12, line-length 88).
- `mypy` configured with `strict = true`.
- No Prettier for frontend (only `eslint-config-next`).

**Naming Consistency:**
- Backend: snake_case for files and functions (consistent).
- Frontend: PascalCase for components, camelCase for functions (consistent).
- Database: snake_case for tables/columns (consistent).

**Issues:**

1. **`pycache_warning.txt`** (38KB) and **`staged_files.txt`** (48KB) are tracked/untracked debug dumps that should be deleted.
2. **`tailwind.config.js`** has very long lines and could be formatted.
3. **Bengali text in code**: `customer_agent.py` has Bengali fallback responses. For OSS, strings should be externalized.
4. **Missing docstrings**: Most service and repository classes lack docstrings.
5. **Inconsistent `__init__.py` exports**: Some modules use explicit imports, others use wildcards or minimal exports.

### Recommendations

- [ ] **P1**: Delete `pycache_warning.txt`, `staged_files.txt`, `test_checkout.json`.
- [ ] **P1**: Add `ruff format .` to pre-commit or CI.
- [ ] **P1**: Add Prettier for frontend (`prettier.config.js`).
- [ ] **P2**: Externalize all user-facing strings to `locales/` or prompt files.
- [ ] **P2**: Add docstrings to all public classes and methods.
- [ ] **P2**: Standardize `__init__.py` exports across all backend modules.
- [ ] **P3**: Add code review checklist to `CONTRIBUTING.md`.

---

## 12. Custom Agent Ecosystem

### Current State

`.kilo/` contains Kilo-specific agent and skill definitions:

```
.kilo/
├── agents/
│   ├── aura-architect.md
│   ├── aura-developer.md
│   ├── aura-reviewer.md
│   └── code-simplifier.md
├── skills/
│   ├── agent-md-refactor/
│   ├── data-investigation/
│   ├── databricks-jobs/
│   ├── graphify/
│   ├── langsmith-fetch/
│   ├── searching-mlflow-docs/
│   └── senior-data-engineer/
├── node_modules/            ⚠️ Large, should be gitignored
├── kilo.json
├── plans/
│   └── 1790232999901-aura-skincare-master-implementation-plan.md
└── setup-script.ps1
```

### Issues Found

1. **`.kilo/node_modules/`** is untracked and would be staged by `git add -A`. It must be gitignored.
2. **`.kilo/` contents are personal tooling**: These are Kilo AI agent definitions and skills, not part of the Aura Skincare product.
3. **`kilo.json`** references `.kilo/skills` paths — this is Kilo configuration, not project configuration.

### Recommendations

- [ ] **P0**: Add `.kilo/node_modules/` to `.gitignore`.
- [ ] **P0**: Decide whether `.kilo/` (excluding `node_modules/`) should be committed:
  - **Option A**: Keep `.kilo/agents/` and `.kilo/skills/` committed — they are project-specific AI agent definitions.
  - **Option B**: Move `.kilo/` to a separate `dotfiles` repo or `~/.config/kilo/` and remove from project.
- [ ] **P1**: If `.kilo/` stays, add a `.kilo/README.md` explaining its purpose.
- [ ] **P1**: Move `kilo.json` to `.config/kilo/kilo.json` or remove it if Kilo is not part of the open-source repo.

---

## Prioritized Stabilization Roadmap

### Phase 0: Immediate Blockers (Do Before ANY Git Commit)

| # | Action | Area | Owner | Est. |
|---|---|---|---|---|
| 0.1 | Add `backend/.env`, `certs/`, `backend/venv`, `.kilo/node_modules/`, `__pycache__/`, `*.pyc`, `staged_files.txt`, `pycache_warning.txt`, `test_checkout.json`, `frontend/public/skincare_*.jpg` to `.gitignore` | Security/Git | Dev | 30m |
| 0.2 | Delete `test_checkout.json` from working tree | Security | Dev | 5m |
| 0.3 | Stage ALL files required by staged AI imports together (dependency closure) | Git | Dev | 1h |
| 0.4 | Verify zero secrets in staged/indexed files | Security | Dev | 15m |

### Phase 1: Git Hygiene (Week 1)

| # | Action | Area | Owner | Est. |
|---|---|---|---|---|
| 1.1 | Unstage `AUDIT_REPORT.md` and `AURA-REPO-AUDIT.md`; relocate to `Aura-Skincare-Docs/12-Project-Brain/reports/` or delete | Git/Docs | Dev | 30m |
| 1.2 | Stage all 68 unstaged deletions (obsolete root docs, old graphify skills, 98-Governance) | Git | Dev | 30m |
| 1.3 | Stage all 214 unstaged modifications (backend modules, frontend, tests) | Git | Dev | 2h |
| 1.4 | Squash 3 local commits into logical units: Foundation Cleanup → Product Architecture → AI Core → RAG Integration → Docs Consolidation | Git | Dev | 2h |
| 1.5 | Force-push cleaned `release/v1.1` to origin (coordinate with team) | Git | Dev | 15m |
| 1.6 | Delete `integration-v1.1` branch | Git | Dev | 5m |
| 1.7 | Set branch protection on `main` and `release/v1.1` | Git | DevOps | 15m |

### Phase 2: Security Hardening (Week 1-2)

| # | Action | Area | Owner | Est. |
|---|---|---|---|---|
| 2.1 | Replace hardcoded n8n tokens in `docker-compose.yml` with `${VAR}` interpolation | Security | Dev | 30m |
| 2.2 | Add `backend/.env.example` back with all variables documented | Security | Dev | 1h |
| 2.3 | Add `SECURITY.md` with vulnerability disclosure policy | Docs/Security | Dev | 30m |
| 2.4 | Add `pre-commit` hook for secret scanning (`detect-secrets` or `gitleaks`) | DevOps | Dev | 1h |
| 2.5 | Rotate any potentially exposed secrets | Security | Dev | 30m |
| 2.6 | Audit all environment variables for unnecessary exposure | Security | Dev | 1h |

### Phase 3: Architecture Fixes (Week 2-3)

| # | Action | Area | Owner | Est. |
|---|---|---|---|---|
| 3.1 | Fix RouterAgent bypass in `langgraph_service.py` or document intentional design | AI/Arch | Dev | 2h |
| 3.2 | Refactor `routes/ai.py` to inject dependencies via FastAPI `Depends` | AI/Backend | Dev | 2h |
| 3.3 | Complete or remove `payment` and `notification` incomplete modules | Backend | Dev | 4h |
| 3.4 | Add `knowledge` routes and services to expose RAG management API | Backend | Dev | 4h |
| 3.5 | Add `customer`, `inventory`, `order` missing repository/service implementations | Backend | Dev | 8h |
| 3.6 | Validate all modules against `06-SAD/module-boundaries.md` | Architecture | Architect | 4h |

### Phase 4: Documentation & OSS Readiness (Week 3-4)

| # | Action | Area | Owner | Est. |
|---|---|---|---|---|
| 4.1 | Add root `CONTRIBUTING.md` with branch strategy, PR process, commit conventions | Docs | Dev | 1h |
| 4.2 | Add root `CODE_OF_CONDUCT.md` | Docs | Dev | 30m |
| 4.3 | Add root `CHANGELOG.md` and archive `00-Project-Memory/CHANGELOG.md` | Docs | Dev | 1h |
| 4.4 | Translate or remove `Aura-Skincare-Docs/open.md` | Docs | Dev | 30m |
| 4.5 | Archive `00-Project-Memory/` session files to `98-Archive/` or delete | Docs | Dev | 30m |
| 4.6 | Add `docs/README.md` index for `Aura-Skincare-Docs/` | Docs | Dev | 1h |
| 4.7 | Add doc validation CI (markdown lint, YAML schema validation) | DevOps | Dev | 2h |
| 4.8 | Expand `backend/README.md` and `frontend/README.md` or fold into root README | Docs | Dev | 2h |

### Phase 5: Testing & Quality (Week 4-5)

| # | Action | Area | Owner | Est. |
|---|---|---|---|---|
| 5.1 | Add `test_payment_*.py` (routes, services, repositories) | Tests | Dev | 4h |
| 5.2 | Add `test_order_automation_*.py` (services, validators) | Tests | Dev | 4h |
| 5.3 | Add `test_knowledge_*.py` (repositories, RAG service) | Tests | Dev | 4h |
| 5.4 | Add frontend tests (Vitest + React Testing Library) | Tests/FE | Dev | 8h |
| 5.5 | Add Playwright E2E tests for checkout and AI chat flows | Tests | Dev | 8h |
| 5.6 | Add coverage reporting to CI | DevOps | Dev | 2h |
| 5.7 | Fix all `ruff` and `mypy` violations | Quality | Dev | 4h |
| 5.8 | Add pre-commit hooks for ruff, mypy, trailing whitespace | DevOps | Dev | 1h |

### Phase 6: DevOps & Release (Week 5-6)

| # | Action | Area | Owner | Est. |
|---|---|---|---|---|
| 6.1 | Split `docker-compose.yml` into prod + dev overrides | DevOps | Dev | 4h |
| 6.2 | Add multi-stage Dockerfile for backend | DevOps | Dev | 2h |
| 6.3 | Add CD pipeline (staging + production) | DevOps | Dev | 8h |
| 6.4 | Add `/health` smoke test to CI | DevOps | Dev | 1h |
| 6.5 | Add release automation (semantic-release or GitHub Releases) | DevOps | Dev | 4h |
| 6.6 | Add `compose.override.example.yml` usage documentation | Docs | Dev | 1h |

### Phase 7: Frontend Hardening (Week 6-7)

| # | Action | Area | Owner | Est. |
|---|---|---|---|---|
| 7.1 | Remove test images from `frontend/public/` or add real assets | Frontend | Dev | 1h |
| 7.2 | Add `frontend/.env.local` to `.gitignore` | Frontend/Security | Dev | 15m |
| 7.3 | Add `tsconfig.tsbuildinfo` to `.gitignore` | Frontend | Dev | 15m |
| 7.4 | Add global error boundary in `layout.tsx` | Frontend | Dev | 2h |
| 7.5 | Consolidate API route handlers with `src/lib/services/` | Frontend | Dev | 4h |
| 7.6 | Add Prettier configuration for frontend | Frontend | Dev | 1h |
| 7.7 | Add loading states and skeleton UI for all data-fetching pages | Frontend | Dev | 8h |

### Phase 8: AI Platform Completion (Week 7-8)

| # | Action | Area | Owner | Est. |
|---|---|---|---|---|
| 8.1 | Implement Admin AI agent or remove `agents/admin/` directory | AI | Dev | 4h |
| 8.2 | Implement Marketing AI agent or remove `agents/marketing/` directory | AI | Dev | 4h |
| 8.3 | Replace heuristic tool selection with LLM-based intent detection | AI | Dev | 8h |
| 8.4 | Add Redis connection fallback and health check in `RedisSessionStore` | AI/Backend | Dev | 2h |
| 8.5 | Add streaming responses for `/ai/chat` endpoint | AI/Backend | Dev | 4h |
| 8.6 | Add conversation summarization to manage context window | AI | Dev | 4h |
| 8.7 | Add AI evaluation tests per `09-Validation/ai-evaluation.md` | AI/Tests | Dev | 4h |

---

## Risk Register

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| 1 | Secrets committed to history | Medium | Critical | Add `.gitignore` fixes, run `git filter-repo` if needed |
| 2 | ImportError after partial commit | High | High | Stage all dependency-closure files together |
| 3 | RouterAgent bypass causes incorrect AI behavior | Medium | Medium | Fix or document before next feature |
| 4 | Incomplete payment/notification modules cause runtime errors | Medium | High | Complete or gate behind feature flags |
| 5 | n8n sandbox tokens exposed in docker-compose | Low | Medium | Replace with env vars |
| 6 | Alembic multiple heads cause migration conflicts | Medium | High | Resolve heads, test migrations |
| 7 | Frontend test images committed to git | High | Low | Remove or gitignore |
| 8 | `.kilo/node_modules/` staged accidentally | High | Low | Add to `.gitignore` immediately |
| 9 | Missing tests for payment/notification cause production bugs | Medium | High | Add tests before feature completion |
| 10 | Hardcoded Bengali strings in AI responses block i18n | Medium | Low | Externalize strings |

---

## Success Criteria

The repository is considered **stabilized** when:

1. `git status` is clean (no unstaged changes, no untracked files except `.gitignore`d artifacts).
2. `git push origin release/v1.1` succeeds without security warnings.
3. `cd backend && uv run ruff check .` passes with zero errors.
4. `cd backend && uv run mypy .` passes with zero errors.
5. `cd backend && uv run pytest` passes with >80% coverage for core modules.
6. `backend/.env` and `certs/` are confirmed gitignored (`git check-ignore` returns the path).
7. No secrets found in `git diff --cached` or commit history.
8. All modules have at least unit tests.
9. Frontend has lint + typecheck passing (`npm run lint`, `npm run build`).
10. CI passes on all checks.

---

## Appendix A: Immediate Next Actions (Next 24 Hours)

1. **Add security entries to `.gitignore`**:
   ```
   # Aura Security
   backend/.env
   backend/.venv
   certs/
   *.pem
   *.key
   __pycache__/
   *.pyc
   .kilo/node_modules/
   ```

2. **Delete `test_checkout.json`**: `Remove-Item -LiteralPath "test_checkout.json"`

3. **Stage dependency-closure set**:
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

4. **Run pre-commit secret scan**: `detect-secrets scan --baseline .secrets.baseline`

5. **Verify imports compile**: `cd backend && python -c "import app"` (or `uv run python -c "import app"`)

---

## Appendix B: Open Source Checklist

Before opening the repository to public contributors:

- [ ] `LICENSE` is appropriate (MIT is present — verify it covers all code)
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

---

*End of Repository Stabilization & Open Source Readiness Roadmap*
