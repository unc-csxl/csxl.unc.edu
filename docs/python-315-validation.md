# Python 3.15 migration and validation

**Date:** October 16, 2026 (America/New_York)

**Branch:** `chore/python-3.15`

**Baseline:** `67e7cf6a9f049835316742a7ae022060fb122f85` from `origin/main`

This branch moves development, CI, and production configuration from Python 3.11
to Python 3.15.0. It preserves the preceding Dependabot remediation. Application
code, database migrations, and frontend dependencies are unchanged.

## Runtime and dependencies

- Added `.python-version`, updated the project requirement and Ruff target, and
  regenerated `backend/uv.lock` for Python 3.15.
- Updated the production base image to `python:3.15` and pinned uv to 0.13.1 in
  both Dockerfiles and CI. The project requires uv 0.13.1 or newer.
- The devcontainer installs a shared uv-managed Python under `/opt/python` with
  commands in `/usr/local/bin`. Ubuntu's system interpreter stays available for
  system tooling. Rebuild existing devcontainers before using this branch.
- CI tests Python 3.15 and checks its version and native dependency imports in
  the production image.

| Dependency | Baseline | Migration |
| --- | --- | --- |
| psycopg2 | 2.9.11 | 2.9.13 |
| SQLAlchemy | 2.0.49 | 2.0.55 |
| Pydantic / pydantic-core | 2.13.0 / 2.46.0 | 2.14.1 / 2.50.1 |
| CFFI / greenlet | 2.0.0 / 3.4.0 | 2.1.1 / 3.5.6 |
| uvloop / httptools | 0.22.1 / 0.7.1 | 0.23.0 / 0.9.0 |
| watchfiles / websockets | 1.1.1 / 16.0 | 1.3.0 / 17.2 |
| fastar / rignore | 0.11.0 / 0.7.6 | 0.12.0 / 0.8.1 |
| MarkupSafe | 3.0.3 | 3.0.4 |
| pytest / pytest-cov | 8.2.2 / 5.0.0 | 9.1.1 / 7.1.0 |
| coverage / Ruff | 7.13.5 / 0.11.13 | 7.16.2 / 0.17.1 |

Typing support packages also update; the obsolete conditional `tomli` dependency
disappears. FastAPI 0.135.3, Starlette 1.3.1, and Uvicorn 0.44.0 stay unchanged.
SQLAlchemy remains on its 2.0 series. Existing security floors remain in place.

The older locked CFFI, Pydantic core, and Rust-based tools lacked suitable Python
3.15 wheels for this environment. The updated versions install successfully.
psycopg2 2.9.13 and PyYAML 6.0.3 built successfully from source using the local
compiler and PostgreSQL headers. Verify builds on the deployment architecture
through the production-image CI job.

## Completed verification

Local checks use CPython 3.15.0 on Linux ARM64, isolated development and production
virtual environments, synthetic credentials, and the `csxl_python315` database.
Tests use `csxl_python315_test`; production data was not used.

| Check | Result |
| --- | --- |
| Locked development and clean production-only installs | Passed; production excludes pytest |
| Lockfile consistency | Passed: 69 packages, including the local project |
| Complete backend suite | **582 passed**, 8 warnings; 85% coverage |
| Backend formatting | Passed: 281 files |
| Honcho and development stack | Caddy, Uvicorn, and Angular started successfully |
| Backend reload | watchfiles restarted the worker and health recovered |
| API contract | All 104 paths and schemas match baseline after normalizing two startup timestamp defaults |
| Browser flows | Login/profile, formatted article Markdown, course dialog, room availability/calendar, reservation confirmation/reload/cancellation, office-hours history |
| Browser errors | No uncaught exceptions or failed application API requests in the completed flow |
| Production-mode server | Three Uvicorn workers, compiled frontend, authenticated API, and database health passed |
| Static delivery | SPA deep links, cache policy, byte ranges, ETag/304, and GZip passed |
| Production authentication restriction | Development impersonation endpoint rejected |
| Native runtime imports | Database driver, Pydantic core, greenlet, uvloop, httptools, CFFI, watchfiles, and other updated packages passed |
| Alembic / Mako | Temporary revision generation and Python compilation passed |
| CI configuration | YAML and embedded Python command parse successfully |
| Python security scan | 68 registry packages: **0 critical, 0 high, 7 moderate, 1 low** |

Security counts are distinct GitHub advisory matches returned by OSV, not live
Dependabot alert counts. Frontend/root lockfiles are unchanged from the preceding
security fix. Container OS packages are outside this scan.

### Existing time-sensitive test

The first run produced 581 passes and one reservation-map failure. The same test
failed on the baseline Python 3.11 environment: its current-time-based fixture
crossed midnight and overlapped the following day's hours. The test now sets an
explicit daytime opening and reservation and removes unrelated opening periods
within its isolated test transaction. Its assertions cover the complete room map
and another user's view. The corrected case passes on both interpreters; all 12
tests in its module pass on Python 3.15. Application reservation behavior was not
changed.

The complete rerun passed all 582 tests. Its eight warnings are the same categories
as the baseline: SQLAlchemy relationship overlap, Starlette's HTTPX test-client
deprecation, short synthetic test keys, and PyGithub's positional token argument.

Synthetic operating hours used by browser checks were likewise normalized to
daytime windows. No production operating hours were modified.

## Exploratory performance comparison

The local comparison does **not establish an overall speed improvement**. Both
servers used three Uvicorn workers, the same application code and compiled
frontend, and separate synthetic databases on the same PostgreSQL instance.
The Python 3.15 managed build had its GIL enabled and JIT disabled.

Each sample made 240 requests after 15 warm-up requests. Three rounds alternated
the order of Python 3.11 and 3.15. The table reports median throughput across
those rounds; all requests succeeded.

| Endpoint | Concurrent requests | Python 3.11 requests/s | Python 3.15 requests/s | Change |
| --- | ---: | ---: | ---: | ---: |
| Health | 1 | 1,038 | 982 | -5.4% |
| Authenticated profile | 1 | 539 | 542 | +0.7% |
| Article | 1 | 625 | 686 | +9.7% |
| Health | 8 | 1,794 | 1,592 | -11.3% |
| Authenticated profile | 8 | 1,125 | 1,051 | -6.5% |
| Article | 8 | 1,158 | 1,219 | +5.3% |

These are short, local samples affected by the client, database, scheduling, and
the dependency updates as well as the interpreter. They compare the migration
as a whole and do not isolate Python's performance. Use longer staging load tests
on the deployment architecture before claiming a speed benefit or regression.
The runner and raw latency/throughput samples are saved as
`/tmp/csxl-python315-benchmark.py` and `/tmp/csxl-python315-benchmark.json`.

## Remaining validation before rollout

- Build the production image in CI and rebuild the devcontainer. Docker is not
  available in this workspace, so neither image has been built locally. The
  running production-mode smoke server uses a clean `--no-dev` virtual
  environment rather than the Docker image.
- Exercise real UNC SSO and GitHub authorization in staging. Their local and
  mocked regression checks do not replace external account integration checks.
- Run the normal staging deployment checks against the real deployment
  architecture and database schema. No database migrations are introduced.
  The pre-existing empty-database Alembic limitation is documented in
  [the security validation report](dependabot-validation.md#existing-migration-limitation).

## Reproduction and local evidence

After rebuilding the devcontainer, or installing uv 0.13.1+ and Python 3.15:

```bash
uv python install 3.15
uv sync --project backend --locked --group dev
uv run --project backend --locked python --version
uv run --project backend --locked ruff format --check backend
uv run --project backend --locked honcho check
# Configure development PostgreSQL and use a disposable database name.
POSTGRES_DATABASE=csxl_python315 uv run --project backend --locked pytest backend/test --cov=backend
docker build --tag csxl:python315 .
```

The isolated local development stack uses `http://localhost:1570`; the separate
production-mode server uses `http://localhost:1573`. Evidence is under
`/tmp/csxl-python315-*`, including install/test logs, coverage JSON, the OSV scan,
OpenAPI comparison, browser runner/results/screenshots, and server logs. These
temporary artifacts are not committed.
