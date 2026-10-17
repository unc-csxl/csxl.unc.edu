# Dependabot remediation: implementation and validation

**Date:** October 16, 2026 (America/New_York)

**Branch:** `fix/dependabot-critical-high`

**Baseline:** `2a2c0a8dd8d36f9446acde09614adb81a912ec22`

**Status:** Implementation and local verification complete. CI image verification and deployment checks are tracked below.

The updated lockfiles have **zero critical and zero high findings** in the scans below. No application regressions were found in the completed tests. Two dependency compatibility failures were found and fixed during verification.

## Dependency changes

| Dependency | Before | Verified version / disposition |
| --- | --- | --- |
| PyJWT | 2.8.0 | 2.15.1 |
| AnyIO | 4.13.0 | 4.14.2 |
| cryptography | 46.0.7 | 50.0.2 |
| Starlette | 1.0.0 | 1.3.1; FastAPI remains 0.135.3 |
| python-multipart | 0.0.26 | 0.0.30 |
| urllib3 | 2.6.3 | 2.8.0 |
| Mako | 1.3.10 | 1.3.12 |
| Soup Sieve | 2.8.3 | 2.8.4 |
| PyGithub | 2.3.0 | 2.7.0 for JWT compatibility |
| Honcho | 1.1.0 | 2.0.0; removes need for setuptools |
| setuptools | 70.0.0 | Removed from the development dependency graph |
| Angular framework / compiler | 21.2.8 | 21.2.25 |
| Angular CLI / build | 21.2.7 | 21.2.27 |

Both pnpm lockfiles were regenerated, including the vulnerable transitive packages. Parent updates resolve the critical Piscina, proxy-addr, and tar findings. Updating express-rate-limit within its parent's allowed range removes its exact pin to vulnerable ip-address 10.1.0. No pnpm overrides, forced major upgrade, or audit exclusions were needed.

Python security floors are recorded in `pyproject.toml`. The unused legacy `backend/requirements.txt` was removed after confirming production, CI, and devcontainer consumers use uv; the development guide explains how to export requirements when needed. CI and the devcontainer now provision Python 3.11, matching the project requirement and production image.

### Compatibility issues fixed

1. **PyGithub 2.3 encoded an integer JWT issuer.** The upgraded PyJWT rejects it. PyGithub 2.7 normalizes the issuer to a string. Tests now cover RSA signing with the real libraries and CSXL's GitHub OAuth success/failure path using a fake HTTP transport. CSXL's normal session authentication continues to use HS256. [PyGithub release notes](https://pygithub.readthedocs.io/en/v2.8.0/changes.html)
2. **Honcho 1.1 failed to start without setuptools.** Its undeclared `pkg_resources` usage became visible when setuptools was removed. Honcho 2.0 starts the existing Procfile successfully without that dependency. [Honcho release](https://pypi.org/project/honcho/2.0.0/)

## Security scan results

| Scope | Critical | High | Moderate | Low |
| --- | ---: | ---: | ---: | ---: |
| Root pnpm audit | 0 | 0 | 0 | 0 |
| Frontend pnpm audit | 0 | 0 | 14 | 6 |
| Python OSV scan of all 69 locked registry packages | 0 | 0 | 8 | 1 |

Python counts are GitHub advisory matches, excluding duplicate PYSEC aliases. These are independent scan results, not live Dependabot alert counts. Lower-severity findings remain outside this critical/high remediation. Container OS packages and installed global tools are not included in these lockfile audits.

`http-cache-semantics` 4.3.0 is outside the reported affected range of GHSA-ch52-4w7c-c8xp, so it no longer appears in the npm audit. The advisory has no published patch designation and is disputed by the maintainer; no claim of a confirmed upstream security fix or risk acceptance is made. [Upstream discussion](https://github.com/kornelski/http-cache-semantics/issues/56)

## Verification completed

| Check | Result |
| --- | --- |
| Original backend suite | 572 passed |
| Updated backend suite | **582 passed**, including 10 new regression cases |
| Existing PyJWT 2.8 session token | Accepted by the updated authentication endpoint |
| Authentication protections | Existing delegation, expiry, audience, origin, signature, and development-mode tests pass |
| API contract comparison | All 104 OpenAPI paths unchanged after normalizing two startup timestamp defaults |
| Frontend lint | Passed before and after updates |
| Production Angular build | Passed before and after updates; artifacts written outside `docs/` |
| Locked installs | Root/frontend frozen installs, backend development install, and clean production-only Python install passed |
| Backend formatting | Ruff check passed |
| Root tooling | Commitlint accepts a valid message and rejects an invalid message |
| Process manager | `honcho check` and startup of Caddy, Uvicorn, and Angular passed |
| Live browser flows | Development login/profile, article Markdown, Material course dialog/input, reservation date picker, room draft/confirm/reload/cancel, and office-hours history passed |
| Browser error checks | No uncaught page exceptions or failed application API requests in the completed smoke flow |
| Markdown injection check | Synthetic article response retained Markdown formatting, escaped raw HTML, and removed executable link URLs |
| Development hot reload | Template update appeared in the browser; original content restored and observed without browser exceptions |
| Production runtime | Clean `--no-dev` environment, three Uvicorn workers, compiled SPA deep links, and authenticated API access passed |
| Production static delivery | Byte ranges, ETag/304 responses, GZip, and uncached SPA deep links passed |
| Production authentication restriction | Development impersonation route rejected in production mode |
| Alembic / Mako | Temporary revision generation and Python compilation passed |

The servers used synthetic credentials and the separate `csxl_dependabot` database. Backend tests used `csxl_dependabot_test`. Room-test operating hours were normalized to daytime windows in the synthetic database because the default fixtures crossed midnight during this late-evening run. No production data or external OAuth account was used.

The final backend run reports eight warnings: existing SQLAlchemy relationship warnings, Starlette's HTTPX test-client deprecation, short synthetic keys in existing tests, and PyGithub's deprecated positional token argument. They did not cause failures; signing and verification checks were not disabled.

### Existing migration limitation

`alembic upgrade head` on an entirely empty disposable database fails because the first migration alters an existing `user` table. The same missing-table failure was reproduced with the original locked dependencies. This repository uses its database initialization/reset scripts to create the schema. No migrations were changed by this work; the full migration history was not validated against a production schema snapshot.

## CI and follow-up

- Added weekly Dependabot updates for uv, both npm projects, and GitHub Actions; Angular patch/minor updates are grouped.
- Added critical/high npm audit gates and pull-request dependency review. The review gate checks newly introduced findings; it is not a replacement for a full Python audit.
- Added a production image build/import job and a Honcho CLI check. Fixed the backend test invocation and moved CI frontend build output outside the documentation directory.
- The production Docker image and devcontainer image **could not be built locally** because Docker is unavailable. The new production-image CI job still needs to run after the branch is published.
- Real UNC SSO and GitHub authorization were not exercised against external accounts. Their local and mocked regression tests passed; retain a staging login check before production rollout.
- After merge and deployment, confirm the image commit, health checks, authentication, and critical/high Dependabot alert closure. The GitHub connector could not export the complete alert dashboard, so closure has not been verified.

## Local evidence and reproduction

The live development stack is at `http://localhost:1560`; the separate production-mode smoke server is at `http://localhost:1563`. Both use synthetic data.

Evidence from this workspace is under `/tmp/csxl-dependabot-*`, including `backend-final-tests.log`, `frontend-final-lint.log`, `frontend-final-build.log`, the three final audit JSON files, `browser-smoke.mjs`, `browser-results.json`, `hmr.log`, and browser screenshots. These temporary files are not committed artifacts.

With development PostgreSQL configured, use a disposable database name for backend checks:

```bash
uv sync --project backend --locked --group dev
POSTGRES_DATABASE=csxl_dependabot uv run --project backend --locked pytest backend/test
uv run --project backend ruff format --check backend
uv run --project backend honcho check
pnpm install --frozen-lockfile
pnpm audit --audit-level high
pnpm --dir frontend install --frozen-lockfile
pnpm --dir frontend audit --audit-level high
pnpm --dir frontend lint
pnpm --dir frontend exec ng build --configuration production --output-path /tmp/csxl-security-build
```

For the current synthetic stack, replay the browser checks with:

```bash
PLAYWRIGHT_BROWSERS_PATH=/tmp/csxl-playwright node /tmp/csxl-dependabot-browser-smoke.mjs
```
