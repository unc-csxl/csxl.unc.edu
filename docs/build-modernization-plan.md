# Build Stack Modernization Plan

**Goal:** Migrate to pnpm (frontend), uv (backend), and adopt Angular build speed improvements. Changes must work in both devcontainer (dev) and production (Dockerfile).

---

## Current State

| Layer | Current Tool | Version/Notes |
|-------|-------------|---------------|
| Frontend package manager (dev) | npm | `npm install` in devcontainer `postCreateCommand` |
| Frontend package manager (prod) | yarn | Dockerfile installs yarn, uses `yarn install` |
| Frontend framework | Angular 21 | Already on `@angular/build:application` (esbuild) |
| Frontend lock file | `package-lock.json` | Root + frontend |
| Backend package manager | pip | `pip install -r requirements.txt` |
| Backend Python | 3.12 | Installed via deadsnakes PPA in devcontainer |
| Process manager | honcho | `Procfile` with caddy, uvicorn, ng serve |
| Root monorepo | npm | husky + commitlint |

## Target State

| Layer | Target Tool | Why |
|-------|------------|-----|
| Frontend package manager | **pnpm** | Faster installs, disk-efficient, strict dependency resolution |
| Angular build | **@angular/build:application** (already esbuild) + incremental build cache | Already on esbuild; add persistent build cache and `hmr` for dev |
| Backend package manager | **uv** | 10-100x faster than pip, drop-in replacement, lockfile support |
| Backend Python | 3.12 (unchanged) | uv manages deps, not Python version here |

---

## Migration Milestones

Each milestone is a discrete, merge-ready commit on the `refactor/build-modernization` branch. Every milestone should pass `uv run --project backend honcho start` (dev) and `docker build .` (prod) before moving on.

---

### Milestone 1: Create branch and add this plan

**Branch:** `refactor/build-modernization`

- [ ] Create branch from `main`
- [ ] Commit this plan document

**Validation:** Branch exists, plan is checked in.

---

### Milestone 2: Migrate root monorepo from npm to pnpm

**Files changed:**
- `.devcontainer/Dockerfile` — install pnpm globally (`corepack enable && corepack prepare pnpm@latest --activate`)
- `.devcontainer/devcontainer.json` — change `postCreateCommand` from `npm install` to `pnpm install`
- `package.json` (root) — add `"packageManager": "pnpm@10.x.x"` field
- Delete `package-lock.json` (root) → generate `pnpm-lock.yaml`
- Add `pnpm-workspace.yaml` if needed (optional; the root is not a monorepo workspace in pnpm terms unless we want to link frontend)

**Steps:**
1. Install pnpm locally: `corepack enable && corepack prepare pnpm@latest --activate`
2. Delete `/workspace/node_modules` and `/workspace/package-lock.json`
3. Run `pnpm install` at root — generates `pnpm-lock.yaml`
4. Verify `pnpm run prepare` works (husky)
5. Commit: `build: migrate root to pnpm`

**Validation:** `pnpm install && pnpm run prepare` succeeds.

---

### Milestone 3: Migrate frontend from npm to pnpm

**Files changed:**
- `.devcontainer/devcontainer.json` — update `postCreateCommand`
- `.devcontainer/Dockerfile` — pnpm is already installed from Milestone 2
- `.devcontainer/docker-compose.yml` — rename volume `csxl.unc.edu-node_modules` (pnpm uses a content-addressable store, but `node_modules` still exists; volume stays)
- `frontend/package.json` — add `"packageManager"` field
- Delete `frontend/package-lock.json` → generate `frontend/pnpm-lock.yaml`
- `Procfile` — change `npm run start:dynamic` → `pnpm run start:dynamic`
- `Dockerfile` (production) — replace yarn install with pnpm install

**Steps:**
1. `cd frontend && rm -rf node_modules package-lock.json`
2. `pnpm install` — generates `pnpm-lock.yaml`
3. `pnpm run build` — verify Angular production build works
4. `pnpm run start` — verify Angular dev server works
5. Update `Procfile` frontend command
6. Update `devcontainer.json` `postCreateCommand`:
   ```
   pnpm install && pnpm run prepare && cd frontend && pnpm install
   ```
7. Update `Dockerfile`:
   - Remove yarn installation
   - Add `RUN corepack enable && corepack prepare pnpm@latest --activate`
   - Use `pnpm install --frozen-lockfile` instead of `yarn install`
   - Copy `pnpm-lock.yaml` into image
   - Use `pnpm exec ng build` or `npx ng build`
8. Update `.devcontainer/Dockerfile` to install pnpm via corepack instead of leaving npm as primary
9. Commit: `build: migrate frontend to pnpm`

**Validation:**
- `cd frontend && pnpm run build` succeeds
- `uv run --project backend honcho start` launches all 3 processes
- `docker build -t csxl-test .` succeeds

---

### Milestone 4: Angular build speed improvements

Angular 21 with `@angular/build:application` already uses esbuild (not webpack). Additional improvements:

**Files changed:**
- `frontend/angular.json`

**Changes:**
1. **Enable HMR for dev** — Already the default in Angular 21's dev-server, but confirm it's active. Add to dev configuration if needed:
   ```json
   "development": {
     "optimization": false,
     "extractLicenses": false,
     "sourceMap": true,
     "namedChunks": true,
     "hmr": true
   }
   ```
2. **Enable persistent build cache** — Angular 21 has persistent disk cache by default with `@angular/build`. Verify by checking for `.angular/cache` directory. Ensure `.angular/` is in `.gitignore` and `.dockerignore`.
3. **Add `.dockerignore`** — Prevent sending `node_modules`, `.angular/cache`, `.git` to Docker build context (major speed improvement for `docker build`):
   ```
   node_modules
   .angular
   .git
   .devcontainer
   docs
   ```
4. **Evaluate zoneless** — Angular 21 supports experimental zoneless change detection. This is optional and outside the scope of this migration but noted for future consideration.

**Steps:**
1. Add `.dockerignore` if not present
2. Add `.angular/` to `.gitignore`
3. Confirm HMR and build cache are active
4. Commit: `build: angular build speed improvements`

**Validation:**
- `cd frontend && pnpm run build` completes faster on second run (cache hit)
- `pnpm run start` has HMR working (edit a template → browser refreshes instantly without full reload)
- `docker build .` sends smaller context

---

### Milestone 5: Migrate backend from pip to uv

**Files changed:**
- `.devcontainer/Dockerfile` — install uv, replace pip commands
- `Dockerfile` (production) — install uv, replace pip commands
- Add `backend/pyproject.toml` — uv uses `pyproject.toml` as the source of truth
- Add `backend/uv.lock` — uv lockfile for reproducible installs
- `backend/requirements.txt` — keep as fallback / for reference, or delete after migration
- `Procfile` — no change needed (still `uvicorn`)

**Steps:**
1. Install uv in devcontainer:
   ```dockerfile
   # Install uv
   COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
   ```
2. Create `backend/pyproject.toml` from `requirements.txt`:
   ```toml
   [project]
   name = "csxl-backend"
   version = "0.1.0"
   requires-python = ">=3.12"
   dependencies = [
       "fastapi[all]>=0.111.0,<0.112.0",
       "honcho>=1.1.0,<1.2.0",
       "psycopg2>=2.9.9,<2.10.0",
       "pyjwt>=2.8.0,<2.9.0",
       "pytest>=8.2.2,<8.3.0",
       "pytest-cov>=5.0.0,<5.1.0",
       "python-dotenv>=1.0.1,<1.1.0",
       "requests>=2.32.0,<2.33.0",
       "sqlalchemy>=2.0.30,<2.1.0",
       "alembic>=1.13.1,<1.14.0",
       "pygithub>=2.3.0,<2.4.0",
       "black>=24.4.2,<24.5.0",
       "setuptools>=70.0.0,<70.1.0",
       "bs4>=0.0.2",
   ]

   [tool.pytest.ini_options]
   testpaths = ["test"]
   ```
3. Generate lockfile: `cd backend && uv lock`
4. Install deps: `uv sync`
5. Update `.devcontainer/Dockerfile`:
   ```dockerfile
   # Replace:
   #   RUN python3 -m ensurepip
   #   RUN python3 -m pip install -r requirements.txt
   # With:
   COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
   COPY backend/pyproject.toml backend/uv.lock /workspace/backend/
   WORKDIR /workspace/backend
   RUN uv sync
   ```
6. Update production `Dockerfile`:
   ```dockerfile
   # Replace:
   #   RUN python3 -m pip install --upgrade pip
   #   COPY ./backend/requirements.txt /workspace/backend/requirements.txt
   #   RUN pip install --no-cache-dir --upgrade -r /workspace/backend/requirements.txt
   # With:
   COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
   COPY ./backend/pyproject.toml ./backend/uv.lock /workspace/backend/
   WORKDIR /workspace/backend
   RUN uv sync --frozen --no-dev
   ```
7. Update `devcontainer.json` `postCreateCommand` if backend install is needed post-create
8. Verify `uv run --project backend honcho start` — uvicorn still starts backend
9. Verify `pytest` still runs
10. Commit: `build: migrate backend to uv`

**Validation:**
- `cd /workspace/backend && uv sync` succeeds
- `uv run --project backend uvicorn --port=1561 --reload backend.main:app` starts
- `uv run --project backend pytest` passes
- `docker build -t csxl-test .` succeeds

---

### Milestone 6: Update documentation and clean up

**Files changed:**
- `docs/get_started.md` — update setup instructions
- `CONTRIBUTING.md` — update contributor setup
- `README.md` — update build/run instructions
- Remove stale files: `backend/requirements.txt` (if fully replaced), root `package-lock.json`, `frontend/package-lock.json`

**Steps:**
1. Update all docs referencing `npm`, `pip`, `yarn` to use `pnpm` and `uv`
2. Remove orphaned lockfiles
3. Final smoke test of full dev workflow:
   - Rebuild devcontainer from scratch
   - `uv run --project backend honcho start` — all services run
   - Run `uv run --project backend pytest`
   - Run `pnpm run build` in frontend
4. Final smoke test of production:
   - `docker build -t csxl-test .`
   - `docker run -p 8080:8080 csxl-test` — app serves
5. Commit: `docs: update for pnpm and uv migration`

**Validation:** Full dev and prod workflows pass from a clean state.

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| pnpm strict mode breaks phantom dependencies | Run `pnpm install` and `pnpm run build` before committing; fix any missing explicit dependencies |
| uv lockfile resolution differs from pip | Pin versions tightly in `pyproject.toml` (already pin-ranged in requirements.txt); run full test suite |
| Docker layer cache invalidation | Order COPY commands to maximize cache hits (lockfiles before source code) |
| devcontainer rebuild breaks for other developers | Test full rebuild from scratch at each milestone |
| Volume mounts for node_modules conflict with pnpm | pnpm's default `node_modules` layout (hoisted) is compatible with volume mounts; if issues arise, use `node-linker=hoisted` in `.npmrc` |

## Branching Strategy

```
main
 └── refactor/build-modernization
      ├── Milestone 1: plan document
      ├── Milestone 2: root → pnpm
      ├── Milestone 3: frontend → pnpm
      ├── Milestone 4: angular speed improvements
      ├── Milestone 5: backend → uv
      └── Milestone 6: docs + cleanup
```

Each milestone is a separate commit. The branch can be merged to `main` after all milestones pass validation, or individual milestones can be cherry-picked if needed.

## Commands Cheat Sheet

```bash
# Dev setup (after migration)
pnpm install                          # Root (husky/commitlint)
cd frontend && pnpm install           # Frontend deps
cd backend && uv sync                 # Backend deps
uv run --project backend honcho start # Start all dev services

# Production build
docker build -t csxl .                # Full prod image

# Tests
cd backend && uv run pytest           # Backend tests
cd frontend && pnpm run lint          # Frontend lint
cd frontend && pnpm run build         # Frontend prod build check
```
