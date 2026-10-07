# Aura Skincare — GitHub vs Working Tree Mismatch Audit

**Date:** 2026-10-04
**Branch:** `release/v1.1` | **HEAD:** `81d4df0` ("merge: integrate 1-5 features into v1.1", by navil, 2026-09-20)
**Remote:** `HEAD == origin/release/v1.1` — branch is in sync with GitHub; the mismatch is between the **index (staging area)** and the **working tree**, not with the remote.
**Scope:** read-only audit — no files modified.

---

## 1. Git State Audit

### Current state
| Item | Value |
|---|---|
| Branch | `release/v1.1` |
| HEAD | `81d4df0` merge "integrate 1-5 features into v1.1" |
| vs remote | HEAD == `origin/release/v1.1` (synced) |
| **Staged (index) vs HEAD** | **90 changes** (68 added, 21 modified, 1 deleted) |
| **Unstaged (working tree) vs HEAD** | **282 changes** (68 deleted, 214 modified) |
| **Untracked** | **153 files** |

### Classification: intentional vs accidental

**Staged (90) — INTENTIONAL, review-ready:**
- 68 additions: RAG docs (6) + RAG README, prompt_builder.py, RAG runtime (9), Product metadata models/repos/schemas/services (49), 2 RAG tests.
- 21 modifications: AI core (`customer_agent`, `router_agent`, `langgraph_service`, `routes/ai`, `search_products` = 4) + Product core (17 files).
- 1 deletion: `prompt_manager.py` → replaced by `prompt_builder.py`.

**Unstaged deletions (68) — MIXED:**
- *Intentional cleanup:* all root `*-STATUS.md` / `*-REPORT.md` files (relocated verbatim into `Aura-Skincare-Docs/12-Project-Brain/reports/`), `98-Governance/*.md` (replaced by `01-Governance/*.md`), old graphify skill docs (12), `.env.example`, `.pre-commit-config.yaml` (placeholder), `database/README.md`, `infrastructure/README.md`, `shared/README.md`, `tests/README.md`, `tools/README.md`, root `AGENTS.md`, `AI-STATUS.md`, `AUTH-STATUS.md`, `pyproject.toml`/`uv.lock`/`package.json` (consolidated into backend/frontend), `d/AURA-DEV-001.md`.
- *Accidental/incomplete:* these 68 deletions were performed in the working tree **without staging** — they will NOT be included if `git commit` is run now.

**Unstaged modifications (193) — INTENTIONAL but unstaged:**
- Full backend module updates (auth, analytics, cart, customer, inventory, order, notification, admin, payment, marketing_ai, order_automation), Alembic migrations, config (`settings.py`, `main.py`, `auth.py`, `router.py`, `Makefile`, `docker-compose.yml`, `pyproject.toml`), and all frontend API route refactors. Legitimate work, just not staged.

**Untracked (153) — MIXED:**
- *Intentional, uncommitted code:* AI submodules (`providers/`, `customer_memory/`, `memory/`, `knowledge/`, `tool_manager.py`, `session_state.py`), integrations (email/n8n/payment/redis/storage), payment module, notification/routes/services, marketing_ai generation, new Alembic migrations, frontend components/lib/store/utils.
- *Accidental artifacts:* `certs/` (16 CA/client/server keys — NOT gitignored), `.kilo/*` (Kilo tooling incl. `node_modules`), `staged_files.txt`, `pycache_warning.txt`, `test_checkout.json`, `frontend/public/*.jpg` (test images), `.env` (root).

---

## 2. Project Structure Audit

**Structure is clean:** three sources of truth — `backend/` (backend), `frontend/` (Next.js), `Aura-Skincare-Docs/` (single source of truth for docs). No duplicate top-level folders.

| Folder | Verdict |
|---|---|
| `backend/` | ✅ Source of truth — keep |
| `frontend/` | ✅ Source of truth — keep |
| `Aura-Skincare-Docs/` | ✅ SSoT for documentation — keep |
| `.kilo/` | Kilo tooling (agents, plans, skills, node_modules); previously `Aura-Skincare-Docs/.config/kilo/skills/graphify` was committed — keep tooling but ensure `node_modules/` is gitignored |
| `.github/` | CI — keep |
| `certs/` | ⚠️ **DO NOT push.** Contains CA private keys (`ca.key`), client/server keys; contains n8n sandbox TLS. Not gitignored. |
| `docker-compose.yml`, `Makefile`, `kilo.json`, `LICENSE`, `README.md` | keep; `Makefile`/`docker-compose.yml`/`pyproject.toml` were modified to move backend to monorepo layout (`cd backend`) |

**Duplicates found:**
1. Report files at **root** (deleted in WT) AND identical copies in `Aura-Skincare-Docs/12-Project-Brain/reports/` (untracked) → consolidate to the docs folder.
2. `Aura-Skincare-Docs/98-Governance/*.md` (staged-delete) replaced by same-named files in `01-Governance/` (untracked) → keep `01-Governance`, remove `98-Governance`.

**Source of truth:** `Aura-Skincare-Docs/` for docs; `backend/app/` and `frontend/src/` for code.

---

## 3. Code Change Classification

### A. Production-ready
- **Product module:** `ProductSearchFilter` DTO (primary contract), `ProductRepository.get_list()` — single query builder, fail-fast slug lookup (`[], 0` when `brand_slug`/`category_slug` not found — per `product.repository.slug_validation_fail_fast` decision), subquery joins for junction tables, pagination/sorting. `ProductService` CRUD with slug/sku uniqueness. New metadata models (benefit, ingredient, routine, skin_type/concern/benefit/tag + all junctions).
- **RAG:** `rag_service.py` + `vector_store.py`, `embedding_service.py`, `retriever.py`, `chunk_builder.py`, `knowledge_repository.py`, `exceptions.py`, schemas — complete pipeline.
- **PromptBuilder:** loads `prompts/*.md`, builds context-aware prompts with RAG context, tool results, customer profile, purchase history, cart, wishlist.
- `routes/ai.py`, `config/settings.py`, `main.py` (audit-log middleware, `/health` + `/health/ready` readiness checks).

### B. Experimental
- `RouterAgent` returns `agent|confidence|reasoning` but `LangGraphAIService` hardcodes `next_agent="customer"` — router exists but is bypassed (useless until wired or removed).
- `CustomerAIAgent` Bengali fallback responses (localized marketing copy).
- RAG keyword-based query detection (heuristic; functional).
- n8n sandbox service in `docker-compose.yml`.

### C. Incomplete
- AI module pieces referenced by staged files but **NOT staged**: `providers/base.py`, `tool_manager.py`, `memory/memory_manager.py`, `memory/redis_session_store.py`, `customer_memory/` (5 files), `knowledge/`, `session_state.py`, all integrations, payment module, notification routes/services. If pushed now, `routes/ai.py` imports will fail.
- `prompt_manager.py` deleted; verify every caller was migrated to `PromptBuilder` (staged files suggest yes — verify).
- Alembic: multiple heads (`5f5a2ed5fc92_merge_multiple_heads`); dummy migration `ee4283811b61` (empty `pass`) deleted — verify no other migration depends on it (38240b68e837 has `down_revision: None` — safe).
- `.env.example` deleted → no onboarding boilerplate remains.

### D. Accidental
- `.env.example`, `.pre-commit-config.yaml` (placeholder-only) deleted unnecessarily.
- Root report files deleted while identical copies sit untracked under `12-Project-Brain/reports/` (duplicated state).
- 68 deletions + 193 modifications left unstaged — **the core mismatch**.
- `staged_files.txt`, `pycache_warning.txt`, `test_checkout.json`, pycache entries listed inside them — debug dumps.
- `certs/` (16 keys) untracked & not gitignored — would be caught by `git add -A`.
- `frontend/public/skincare_*.jpg` — test asset images.

---

## 4. Security Audit

| Asset | Location | Status | Risk |
|---|---|---|---|
| Supabase pooler URL + password | `.env`, `backend/.env` | Untracked | ⚠️ currently safe, but `backend/.env` is NOT gitignored |
| Supabase anon + service_role_key | `.env`, `backend/.env` | Untracked | ⚠️ same |
| GEMINI_API_KEY | `.env` | Untracked, gitignored | ✅ safe |
| SECRET_KEY / JWT_SECRET_KEY | `.env` | Untracked | ⚠️ same |
| `certs/ca.key` / client key / server key | `certs/` | Untracked, **NOT gitignored** | 🔴 **HIGH — would be pushed by `git add -A`** |
| Secrets committed in HEAD | checked | none found (no `.pem`/`.key`/`.crt` in HEAD) | ✅ safe |

**Critical findings:**
1. `backend/.env` contains real production credentials (Supabase pooler with embedded password, anon + service-role keys, secret keys) and is **untracked AND NOT gitignored**. Add `backend/.env` to `.gitignore`.
2. `certs/` is untracked and **not** in `.gitignore`. Add `certs/` to `.gitignore`.
3. docker-compose n8n sandbox uses hardcoded (identical) tokens for API key + registration token — n8n sandbox artifact, not Aura secrets; still should use `${VAR}` interpolation.
4. `test_checkout.json` contains PII-like test payload (email, full name, address) — delete.

---

## 5. Documentation Audit

**Structure is solid** (numbered folders, SSoT). Issues:

| Issue | Location | Action |
|---|---|---|
| Duplicate status reports | root + `12-Project-Brain/reports/` (identical copies) | Keep only `12-Project-Brain/reports/`; commit them, delete root copies |
| Obsolete governance docs | `98-Governance/*.md` | Replace with same-named `01-Governance/*.md` (content updated) |
| Graphify skill docs | `Aura-Skincare-Docs/.config/kilo/skills/graphify/` | Deleted intentionally (12 files) |
| RAG docs | `13-AI-Execution/RAG/` | ✅ new, complete (RAG-001..005 + README) |
| Root `AGENTS.md`, `*-STATUS.md`, `*-REPORT.md` | root | Relocate to `12-Project-Brain/reports/` |

**Recommended final structure:**
```
Aura-Skincare-Docs/
├── 00-Foundation/       (vision, mvp-scope, non-goals, glossary)
├── 01-Governance/       (change-management, document-lifecycle, documentation-policy,
│                        ownership-matrix, repository-standards, review-process, versioning-policy)
├── 02-SSoT/
├── 03-Agent-Contracts/
├── 04-Schemas/
├── 05-PRD/
├── 06-SAD/
├── 07-Database/
├── 08-API/
├── 09-Validation/
├── 10-Implementation/
├── 11-Decisions/
├── 12-Project-Brain/    (INDEX, backlog, milestones, project-status,
│                        reports/ <- ALL status/done reports move here)
├── 13-AI-Execution/     (RAG-001..005 + Memory/Prompt docs)
├── 14-Operations/
├── 15-Security/
├── 16-Integrations/
├── 17-Automation/
├── 18-Analytics/
├── 19-Testing/
├── 98-Archive/
└── 99-Templates/
```

---

## 6. Git Commit Strategy (5 commits)

**Step 0 — Safety first (no commit):**
```
git add .gitignore        # stage .gitignore hygiene
```

**Commit 1 — `Foundation cleanup: remove obsolete & duplicate documents`** (unstaged deletions)
- Delete: root `AGENTS.md`, `AI-STATUS.md`, `AUTH-STATUS.md`, `DATABASE-STATUS.md`, `MARKETING-STATUS.md`, `PRODUCT-STATUS.md`, `ORDER-AUTOMATION-STATUS.md`, `MILESTONE-V1.1-RC1-001.md`, all `CUSTOMER-*.md` (7), all `EPIC-*.md` (7), all `FOUNDATION-CORE-001-*.md` (6), `BUG-REPORT.md`, `ORDER-CLOSE-001-REPORT.md`, `PROJECT-BOOT-001.md`, `PROJECT-BOOT-002.md`, `.env.example`, `.pre-commit-config.yaml`, `database/README.md`, `infrastructure/README.md`, `shared/README.md`, `tests/README.md`, `tools/README.md`, `Aura-Skincare-Docs/98-Governance/*.md` (7), `Aura-Skincare-Docs/.config/kilo/skills/graphify/*` (12), `Aura-Skincare-Docs/d/AURA-DEV-001.md`, root `pyproject.toml`, `uv.lock`, `package.json`.
- **NOT in commit:** nothing — these are pure deletions, all content is preserved in `12-Project-Brain/reports/`.

**Commit 2 — `Product: metadata models, repositories, schemas, services + ProductSearchFilter`** (staged 68 adds + staged product mods + unstaged product test mods)
- Staged adds: `backend/app/modules/product/models/*.{benefit,ingredient,product_benefit,product_ingredient,product_routine,product_skin_concern,product_skin_type,product_tag,routine_type,skin_concern,skin_type,tag}.py` (12); `repositories/*` (12); `schemas/*` (13 incl. `product_search_filter.py`); `services/*` (12).
- Staged mods: `models/{__init__,brand,category,product,product_image,product_variant}`, `repositories/{__init__,category,product}`, `schemas/{__init__,brand,category,product_image,product_variant}`, `services/{__init__,product,product_variant}`.
- Add to this commit (unstaged): `backend/tests/test_product_*.py` (3 test files).
- NOT in commit: none of the above should be excluded.

**Commit 3 — `AI: core agents, LangGraph router, providers, memory, tool_manager, customer_memory`** (staged AI + unstaged AI submodules)
- Staged: `customer_agent.py`, `router_agent.py`, `langgraph_service.py`, `routes/ai.py`, `search_products.py`, `schemas/ai.py`, `repositories/base.py`, `services/{__init__,langgraph_service}`, `prompts/{customer,guardrails,router,system}.md`, `prompt_builder.py`, `rag/{__init__,chunk_builder,embedding_service,exceptions,knowledge_repository,rag_service,retriever,schemas,vector_store}.py`.
- Add (unstaged): `providers/{__init__,base}.py`, `tool_manager.py`, `session_state.py`, `memory/{memory_manager.py,redis_session_store.py}`, `customer_memory/{__init__,conversation_memory,preference_memory,profile_memory,purchase_memory,shopping_memory}.py`, `knowledge/*`, `integrations/*`, `modules/{payment,notification,marketing_ai}/*` backend files, `app/api/dependencies/rbac.py`, `app/api/middleware/audit_log.py`, `app/api/public/*`, `app/config/supabase_client.py`, `app/integrations/*`, all new Alembic migrations.
- ⚠️ Note `RouterAgent` bypass — leave code as-is (reviewer decision), just ship it.

**Commit 4 — `RAG: business-knowledge layer, embeddings, vector store, chunking + RAG docs + tests`** (already in staged set — keep separate for traceability)
- From staged adds: `Aura-Skincare-Docs/13-AI-Execution/RAG/{RAG-001..005,README}.md`, `backend/app/modules/ai/services/rag/*`, `backend/app/modules/ai/services/prompt_builder.py`.
- From staged adds: `backend/tests/test_rag_service.py`, `backend/tests/test_ai_rag_integration.py`.
- NOT in commit: nothing.

**Commit 5 — `Docs consolidation, config hygiene & security prep`** (unstaged docs + gitignore + misc)
- Stage & commit (unstaged): `Aura-Skincare-Docs/01-Governance/*.md` (7 new-governance files), `Aura-Skincare-Docs/12-Project-Brain/reports/*.md` (32 relocated reports), `Aura-Skincare-Docs/open.md` (review before commit), `Aura-Skincare-Docs/05-PRD/features/FEAT-005.yaml`, `Aura-Skincare-Docs/15-Security/Sec-005-Supabase-Auth-Storage-Integration.md`.
- `.gitignore` update: add `certs/`, `backend/.env`, `backend/venv`, `backend/.venv`, `*.pyc`, `__pycache__/`, `.verify_index/`, `staged_files.txt`, `pycache_warning.txt`, `test_checkout.json`, `frontend/public/skincare_*.jpg`, `.kilo/node_modules/`.
- ⚠️ Do NOT commit: `certs/*`, `.env`, `backend/.env`, `staged_files.txt`, `pycache_warning.txt`, `test_checkout.json`, `.kilo/*` (tooling), `frontend/public/*.jpg` (unless they are real assets — decide).

---

## 7. Final Professional Checklist

**Before push:**
- [ ] `git status` clean (every change committed in one of the 5 commits above; nothing left in working tree)
- [ ] `git diff --cached` reviewed commit-by-commit (no accidental files)
- [ ] tests pass (`cd backend && uv run pytest`)
- [ ] lint + typecheck pass (`cd backend && uv run ruff check .` && `mypy .`)
- [ ] secrets removed: `.gitignore` covers `certs/`, `backend/.env`; verify with `git ls-remote`/`git check-ignore certs/ca.key backend/.env`
- [ ] `staged_files.txt`, `pycache_warning.txt`, `test_checkout.json`, `.env`, pycache deleted
- [ ] docs organized: root reports deleted, `01-Governance` present, `98-Governance` gone, `12-Project-Brain/reports/` committed
- [ ] git clean: `git clean -n` shows only ignored artifacts (`node_modules`, `__pycache__`, `.venv`, `.next`)
- [ ] commit history clean: 5 logical commits, no merge conflicts anticipated (HEAD == origin)
- [ ] `git push origin release/v1.1` only after all above pass

**Important warnings:**
- The index currently holds 90 staged changes while 282 unstaged changes sit in the working tree. A plain `git commit` would ship ONLY the 90 staged — the 68 deletions would vanish from history (content preserved in untracked copies, but that's fragile).
- Do NOT run `git add -A` blindly: it would also stage `certs/`, `staged_files.txt`, `test_checkout.json`, `.env` before the `.gitignore` update is committed.
- No code was modified in this audit; every action above is a review recommendation.
