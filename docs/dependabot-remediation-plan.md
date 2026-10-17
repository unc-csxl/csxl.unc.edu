# Critical and high dependency vulnerability remediation plan

**Repository:** [unc-csxl/csxl.unc.edu](https://github.com/unc-csxl/csxl.unc.edu)

**Reviewed:** October 16, 2026 (America/New_York)

**Baseline:** `main` at `2a2c0a8dd8d36f9446acde09614adb81a912ec22`

**Status:** Dependency fixes implemented and tested locally on `fix/dependabot-critical-high`; deployment is pending. See [implementation and validation results](dependabot-validation.md).

The inventory and proposed PR breakdown below preserve the original review baseline. The validation report records the actual resolved versions, compatibility fixes, remaining lower-severity findings, and release checks still outstanding.

Start with the critical Python dependencies and Angular build tools, then clear the remaining high findings in focused PRs. Fix the installed dependency graph and deploy the resulting artifacts; closing an alert alone is not completion.

## 1. Evidence and scope

The supplied screenshot confirms five critical Dependabot alerts covering four distinct advisories:

| Alert | Package / manifest | Locked version | Minimum fix for this advisory | Planned work |
| --- | --- | --- | --- | --- |
| [#357](https://github.com/unc-csxl/csxl.unc.edu/security/dependabot/357) | AnyIO; `backend/uv.lock` | `4.13.0` | `4.14.2` | PR 1 |
| [#378](https://github.com/unc-csxl/csxl.unc.edu/security/dependabot/378) | PyJWT; `backend/uv.lock` | `2.8.0` | `2.14.0` | PR 1 |
| [#382](https://github.com/unc-csxl/csxl.unc.edu/security/dependabot/382) | PyJWT; `backend/requirements.txt` | Constraint `>=2.8.0,<2.9.0` | `2.14.0`; current constraint prevents it | PR 1, including legacy manifest cleanup |
| [#395](https://github.com/unc-csxl/csxl.unc.edu/security/dependabot/395) | Piscina; `frontend/pnpm-lock.yaml`; development | `5.1.4` | `5.3.2` | PR 2 |
| [#399](https://github.com/unc-csxl/csxl.unc.edu/security/dependabot/399) | proxy-addr; `frontend/pnpm-lock.yaml`; development | `2.0.7` | `2.0.8` | PR 2 |

The GitHub connector could read the repository but did not support its Dependabot-alert endpoint. The complete dashboard, high-alert IDs, dismissal state, and deployed image were therefore not inspected. This plan supplements the screenshot with fresh dependency scans, rather than treating the screenshot as a complete alert export.

Read-only checks performed:

- Ran `pnpm audit --json` independently at the repository root and in `frontend`.
- Queried OSV for all 72 registry packages in `backend/uv.lock`, then retrieved the matching GitHub-reviewed advisories. Counted GHSA records once rather than counting their PYSEC aliases again.
- Inspected manifests, dependency paths, authentication and static-file code, Docker builds, devcontainer configuration, and CI.
- Verified the proposed Python patch floors on PyPI and the available Angular 21 releases in the npm registry. Dependency resolution and application compatibility remain implementation checks.

| Scan scope | Critical matches | High matches | Interpretation |
| --- | ---: | ---: | --- |
| Root `pnpm-lock.yaml` | 0 | 11 | Commitlint tooling; these GHSAs also appear in the frontend scan |
| `frontend/pnpm-lock.yaml` | 3 | 56 | Includes repeated advisories for different package/version records |
| `backend/uv.lock` | 2 | 20 | Distinct GitHub-reviewed advisories |

After deduplicating GHSA IDs across these scans, there are **5 critical and 70 high advisories**. These are independent scan counts, **not Dependabot alert counts**. The additional critical scan finding is [node-tar GHSA-23hp-3jrh-7fpw](https://github.com/advisories/GHSA-23hp-3jrh-7fpw), through `@angular/cli → pacote → tar`; its dashboard alert ID is unverified. The appendix lists the complete critical/high scan inventory.

`backend/requirements.txt` was inspected as a legacy manifest but was not separately resolved and audited. It may account for additional dashboard alerts. Container OS packages and installed global tools are outside this lockfile inventory.

## 2. Priority and ownership

Assign named owners at kickoff. The following are proposed delivery targets, measured from kickoff, not existing project policy.

| Work | Suggested owner | Target | Completion evidence |
| --- | --- | --- | --- |
| Reconcile dashboard and establish reproducible baseline | Maintainer | First half-day | Every critical/high alert mapped to a manifest, dependency path, owner, and PR |
| PR 1: Python critical fixes | Backend owner | Within 48 hours | Both PyJWT manifests addressed; AnyIO patched; auth tests and staged image pass |
| PR 2: Angular runtime and build-tool fixes | Frontend/build owner | Within 48 hours for critical fixes | Piscina, proxy-addr, and tar absent at vulnerable versions; production build passes |
| PR 3: Remaining Python high fixes | Backend owner | Within 7 days | Patched runtime graph, targeted tests, and rebuilt image |
| PR 4: Remaining JavaScript/tooling high fixes | Frontend/build owner | Within 7 days | Both pnpm locks audited; unpatched advisory explicitly tracked |
| PR 5: Prevent recurrence | Maintainer | Within 7 days | Dependency update configuration and CI security checks working |

If triage establishes an exposed exploitable path, prioritize its containment and release immediately. Run backend and frontend work concurrently where staffing allows, with one owner coordinating each lockfile. Split a slow high-severity upgrade out of a PR if it delays a ready critical fix.

### Exposure findings that affect sequencing

- **PyJWT is on the authentication path.** However, the inspected code passes only `HS256` with `_JWT_SECRET`; it does not mix HMAC and asymmetric algorithms. The critical advisory requires mixed algorithm families and a specially formatted asymmetric verification key. Those prerequisites were not found in these calls. Upgrade promptly and preserve the single-algorithm policy; this review does not establish that production tokens can be forged. [Advisory](https://github.com/advisories/GHSA-ffc3-869f-jxw9)
- **AnyIO ships in the backend dependency graph.** Its critical issue concerns TLS hostname handling for internationalized domains. Trace actual outbound use, including HTTPX and library clients; package presence alone does not establish that the affected TLS path executes. [Advisory](https://github.com/advisories/GHSA-82r6-8w77-94w6)
- **Piscina, proxy-addr, and tar are build/development dependencies here.** The production Dockerfile copies compiled browser assets into a Python image, not frontend `node_modules`. They still affect developer and CI environments. Piscina exploitation requires an existing prototype-pollution primitive; proxy-addr requires the affected proxy-trust configuration. Do not characterize either as a demonstrated CSXL production exploit. [Piscina advisory](https://github.com/advisories/GHSA-67c8-pqhq-4rmx), [proxy-addr advisory](https://github.com/advisories/GHSA-jqcg-44mw-7w3h)
- **The inspected frontend is a browser application.** No SSR/hydration configuration was found. Record that evidence for Angular transfer-cache/SSR findings while still upgrading the affected framework packages.

## 3. Establish the baseline

- [ ] Export all open critical/high alerts with an account that can read Dependabot alerts. Include every page and retain the raw export with the review evidence. [GitHub API documentation](https://docs.github.com/en/rest/dependabot/alerts)

  ```bash
  gh api --method GET --paginate --slurp \
    'repos/unc-csxl/csxl.unc.edu/dependabot/alerts?state=open&severity=critical,high&per_page=100' \
    | jq 'add' > /tmp/csxl-dependabot-critical-high.json
  ```

- [ ] Track alert number, GHSA/CVE, severity, manifest, locked version, direct/transitive path, runtime/build scope, fix version, owner, PR, and deployment. Deduplicate implementation work by dependency family while retaining every alert number, including both PyJWT alerts.
- [ ] Compare the deployed image's package versions and commit with this baseline. The repository lockfiles do not prove what is running.
- [ ] Establish a clean install/build/test result before upgrading. Record pre-existing failures separately.
- [ ] Resolve Python-version drift: `pyproject.toml` and `uv.lock` require Python 3.11, while CI and the devcontainer provision 3.12. For this remediation, explicitly use 3.11 for verification and provision it in CI/dev; keep any broader Python migration separate. Confirm which interpreter `uv` actually runs.
- [ ] Confirm consumers of `backend/requirements.txt`. Production, CI, and the devcontainer currently use uv. Remove the legacy file if unused; otherwise generate it from the canonical lock and verify its consumer. Its old FastAPI and PyJWT constraints must not remain an alternative vulnerable install path.

## 4. Implementation PRs

### PR 1 — Patch Python authentication and critical TLS dependencies

**Primary files:** `backend/pyproject.toml`, `backend/uv.lock`, `backend/requirements.txt`, and authentication regression tests if changes are needed.

- [ ] Replace the PyJWT `<2.9.0` cap with a tested range allowing **2.14.0 or newer**, below the next major. Regenerate the lock; editing a manifest alone leaves production's frozen install unchanged.
- [ ] Upgrade AnyIO to **4.14.2 or newer** within its compatible major, using uv's resolver. Verify the requirements of Starlette, HTTPX, and watchfiles.
- [ ] Address `requirements.txt` in the same PR: remove it after confirming it has no consumers, or regenerate it with the patched versions. Verify alerts **#378 and #382** independently after merge.
- [ ] Preserve the recent authentication protections: fixed algorithm selection, delegated-token audience and expiry, origin checks, development-login restrictions, and bootstrap response headers.
- [ ] Exercise valid sessions, expired/invalid signatures, delegated handoffs, wrong audience/origin, and rejection of handoff tokens as ordinary API tokens. Verify that existing issued session tokens remain compatible with the upgraded decoder.
- [ ] Validate GitHub OAuth/delegated login with mocked outbound services and a staging smoke test. Check PyGithub's use of PyJWT as well as direct application calls.

**Exit:** Patched PyJWT and AnyIO are in the rebuilt runtime image; relevant tests pass; #357, #378, and #382 resolve or have a specific, investigated reason for remaining open.

### PR 2 — Update Angular 21 and remove critical build-tool versions

**Primary files:** `frontend/package.json`, `frontend/pnpm-lock.yaml`.

Use the existing Angular 21 line first. Published candidates verified during this review are **Angular framework 21.2.25** and **CLI/build 21.2.27**. Framework packages must remain mutually aligned; CLI/build have their own patch numbering. These are candidates to resolve and test, not an already validated upgrade.

- [ ] Update the framework group, including compiler/compiler-cli, core, common, router, forms, animations, and browser packages. The highest observed framework fix floor is **21.2.24**; 21.2.25 is the candidate target.
- [ ] Update `@angular/cli` and `@angular/build` together to 21.2.27. Published build metadata pins Piscina 5.3.2, Undici 7.29.1, and Vite 7.3.6; CLI metadata pins Pacote 21.5.1 and MCP SDK 1.31.0. [CLI metadata](https://registry.npmjs.org/@angular%2fcli/21.2.27), [build metadata](https://registry.npmjs.org/@angular%2fbuild/21.2.27)
- [ ] Keep Material/CDK mutually compatible and verify angular-eslint peers. Material/CDK 21.2.14 are available if an update is needed; do not force their patch numbers to match Angular core.
- [ ] Confirm all resolved copies of **Piscina >=5.3.2**, **proxy-addr >=2.0.8**, and **tar >=7.5.21**. Tar 7.5.19 fixes the critical advisory, but 7.5.21 also clears the observed high advisory in the same package.
- [ ] Prefer updates to the owning dependency. If a parent still pins an affected child, use a narrow, documented override only after checking compatibility, with an owner and removal condition.
- [ ] Ensure the Node 22 patch satisfies package engines; the inspected Angular 21 candidates require Node **22.12.0 or newer** on that major. Keep the repository's pinned pnpm version consistent during the update.
- [ ] Verify production build, lint, development server startup/HMR, login, routing, Markdown/article rendering, Material dialogs, and a reservation/office-hours workflow. Preserve DOMPurify in the Markdown rendering path.

**Exit:** #395 and #399 resolve; the independently detected tar critical finding is cleared; no vulnerable framework/build versions remain in the reviewed paths. A passing build alone is insufficient—rerun the audit.

### PR 3 — Clear remaining Python high findings

The following floors cover the high advisories found in this scan. Select versions that satisfy **all** current advisories and parent constraints, then verify the resolved graph again.

| Package | Locked | Observed high-fix floor | Dependency context / validation |
| --- | --- | --- | --- |
| `cryptography` | 46.0.7 | **50.0.0** | PyJWT crypto extra; verify wheels/OpenSSL in the built image and signing integrations |
| `starlette` | 1.0.0 | **1.3.1** | FastAPI; test static files, SPA fallback, errors, and form handling where used |
| `python-multipart` | 0.0.26 | **0.0.30** | FastAPI extras; bound form/header parsing and exercise affected endpoints if present |
| `urllib3` | 2.6.3 | **2.8.0** | Requests, PyGithub, Sentry; test outbound redirects, TLS/proxy behavior, and response handling |
| `mako` | 1.3.10 | **1.3.12** | Alembic; verify migration tooling on a disposable database |
| `soupsieve` | 2.8.3 | **2.8.4** | BeautifulSoup; test academic-section scraping with fixtures |
| `setuptools` | 70.0.0 | **78.1.1** | Explicit dev dependency; current `<70.1.0` cap blocks the fix; remove if unnecessary or update and test |

PyJWT's four high advisories are covered by PR 1's 2.14.0 floor. All package-specific GHSA links are in the appendix.

- [ ] Refresh these packages with targeted uv updates. Upgrade FastAPI if necessary to permit the patched Starlette release; do not bypass an incompatible parent requirement. FastAPI 0.143.3 is a published candidate whose metadata permits Starlette 1.3.1, but prefer the smallest compatible change established by resolution and tests. [PyPI metadata](https://pypi.org/pypi/fastapi/0.143.3/json)
- [ ] Assess actual reachability: the repository uses a custom Starlette `StaticFiles` subclass; the Windows-specific advisory needs separate platform assessment. No direct multipart/form API use was found in the initial search. The BeautifulSoup selector inspected is a constant, not user-provided. Record these limits without treating them as fixes.
- [ ] Consider replacing `fastapi[all]` with only required extras after enumerating actual imports and runtime needs. Keep this optional cleanup separate if it delays security updates.
- [ ] Keep development-only dependencies out of `uv sync --no-dev` production installs. Check image build dependencies separately from the application runtime environment.

### PR 4 — Finish JavaScript transitive and tooling updates

PR 2 should resolve many of these. Re-audit first, then work on the remainder. Update **both** root and frontend locks for shared advisories; they are independent pnpm projects.

| Package | Locked version(s) | Observed fix floor | Main parent/context |
| --- | --- | --- | --- |
| `@modelcontextprotocol/sdk` | 1.26.0 | 1.31.0 | Angular CLI |
| `pacote` | 21.3.1 | 21.5.1 | Angular CLI |
| `sigstore` | 4.1.0 | 4.1.1 | Pacote |
| `hono` | 4.12.12 | 4.12.25 | MCP SDK |
| `ip-address` | 10.1.0 | 10.3.1 | MCP SDK / express-rate-limit |
| `undici` | 7.24.4 | 7.29.1 | Angular build |
| `vite` | 7.3.2 | 7.3.5 | Angular build; proposed parent update selects 7.3.6 |
| `browserslist` | 4.28.2 | 4.28.7 | Angular build |
| `immutable` | 5.1.5 | 5.1.8 | Sass |
| `source-map-js` | 1.2.1 | 1.2.2 | Sass/PostCSS dependency graph |
| `postcss` | 8.5.9 | 8.5.18 | Direct frontend build dependency; check transitive copies too |
| `nanoid` | 3.3.11 | 3.3.18 | PostCSS |
| `brace-expansion` | 1.1.14; 5.0.5 | 1.1.20 on 1.x; 5.0.11 on 5.x | ESLint / minimatch; preserve each parent's compatible major |
| `js-yaml` | 4.1.1 | 4.3.2 | ESLint and root commitlint |
| `fast-uri` | 3.1.0 | 3.1.7 | Ajv in frontend tooling and root commitlint |
| `http-cache-semantics` | 4.2.0 | **No published patch in the advisory** | Pacote / node-gyp / make-fetch-happen |

**Implementation update:** The resolved graph now uses `http-cache-semantics` 4.3.0, outside this advisory's affected range (`<=4.2.0`), and the fresh npm audit no longer reports it. Upstream disputes the advisory; this is not a claim that 4.3.0 contains a confirmed security patch. No audit suppression or exception was added. [Upstream discussion](https://github.com/kornelski/http-cache-semantics/issues/56)

- [ ] Update parent packages and regenerate locks; inspect remaining paths with `pnpm why <package>` in each project. Do not run a blanket forced audit fix or hand-edit resolved versions/hashes.
- [ ] Validate root commitlint/Husky behavior after root-tooling changes, alongside frontend lint/build checks.
- [ ] Handle [GHSA-ch52-4w7c-c8xp](https://github.com/advisories/GHSA-ch52-4w7c-c8xp) explicitly: check whether an updated parent removes `http-cache-semantics`. If it remains, assess whether this build path ever shares credentialed cached responses across users. Prefer removing/replacing the affected path or a reviewed upstream fix when available. Use isolated build caches and credentials as applicable, and document why the advisory's conditions are or are not reachable.
- [ ] If that advisory cannot yet be removed, record an owner, evidence, compensating controls, and a short expiry/review date for a maintainer-approved exception. Keep it visible as unresolved; do not invent a patched version or silently suppress it.

### PR 5 — Prevent recurrence

- [ ] Add `.github/dependabot.yml` updates for npm at `/` and `/frontend`, uv at `/backend`, and GitHub Actions, using the currently supported ecosystem configuration. Enable security updates and group compatible package families; keep framework migrations separate from routine patches. [Supported ecosystems](https://docs.github.com/en/code-security/dependabot/ecosystems-supported-by-dependabot/supported-ecosystems-and-repositories)
- [ ] Add CI audits for both pnpm projects and Python runtime/dev dependencies. Fail on newly introduced critical/high findings; explicitly track any temporary baseline exception by GHSA, owner, reason, and expiry.
- [ ] Add dependency review on PRs and retain audit reports as CI artifacts. Keep frozen/locked installs and manifest consistency checks.
- [ ] Make an explicit Python 3.11 test job and production container build part of verification. Ensure a documented frontend smoke-test path exists; this repository has no general frontend test script.
- [ ] Assign weekly vulnerability triage and a named backup reviewer. Review the unpatched cache advisory at least weekly until removed or fixed.

## 5. Validation and release gates

Run these from a clean checkout of each remediation PR, with the agreed Python runtime and a **disposable test PostgreSQL database** configured as in CI. Backend fixtures create/drop the test database.

```bash
# Root tooling and frontend: both dependency trees matter.
pnpm install --frozen-lockfile
pnpm audit --audit-level high
pnpm --dir frontend install --frozen-lockfile
pnpm --dir frontend lint
pnpm --dir frontend exec ng build --configuration production --output-path /tmp/csxl-security-build
pnpm --dir frontend audit --audit-level high

# Explicit interpreter and test path avoid the existing version/path ambiguity.
uv sync --project backend --python 3.11 --locked --group dev
uv run --project backend --python 3.11 --locked ruff format --check backend
uv run --project backend --python 3.11 --locked pytest backend/test

# Export the exact locked Python graphs for auditing.
uv export --project backend --locked --no-dev --no-hashes --no-emit-project \
  -o /tmp/csxl-runtime-requirements.txt
uv export --project backend --locked --all-groups --no-hashes --no-emit-project \
  -o /tmp/csxl-all-requirements.txt
uvx pip-audit --no-deps --disable-pip -r /tmp/csxl-runtime-requirements.txt
uvx pip-audit --no-deps --disable-pip -r /tmp/csxl-all-requirements.txt

# Reproduce the deployed build, including the no-dev Python install.
docker build --pull -t csxl:security-review .
```

Pin the audit tool version in CI. `pip-audit` also reports lower-severity findings; preserve its report and map advisory IDs to severity for a critical/high gate. A scanner error is not a clean result. [pip-audit documentation](https://github.com/pypa/pip-audit), [pnpm audit documentation](https://pnpm.io/cli/audit)

The frontend build uses `/tmp` above because the current Angular configuration defaults to `../docs`. This avoids overwriting repository documentation during validation.

For each release:

1. Attach the before/after audit delta, resolved versions, covered alert IDs, test results, and any remaining exception to the PR.
2. Build a new immutable image and verify its actual Python package versions; test login/delegation, representative APIs, static assets/SPA fallback, and application workflows in staging.
3. Deploy through the normal release process. Monitor authentication failures, HTTP errors, resource use, and outbound integration failures through an agreed observation window.
4. Retain the previous image digest for operational rollback. If rollback restores vulnerable packages, reopen the remediation work and apply containment while preparing a corrected release.
5. After merge and GitHub's dependency refresh, reconcile every alert with the export. Confirm deployment separately from Dependabot closure. Investigate persistent alerts for duplicate manifests, stale constraints, or remaining transitive copies.

## 6. Definition of done

- [ ] Every open critical/high Dependabot alert is mapped to an owner and disposition, including alerts absent from the screenshot and this independent scan.
- [ ] All five screenshot alerts are fixed in their respective manifests; no critical findings remain in the reviewed dependency graphs.
- [ ] All fixable high findings are removed. Any unpatched finding has an explicitly approved, expiring exception and remains reported as outstanding.
- [ ] Root pnpm, frontend pnpm, Python runtime, and Python development graphs have been rescanned without hiding tool failures.
- [ ] Tests, clean production build, staging smoke checks, and release observation pass.
- [ ] The patched artifacts are deployed; obsolete dependency manifests cannot reinstall the vulnerable versions.
- [ ] Automated updates and security checks are operating.

## Appendix: critical/high advisory inventory

This inventory is generated from the review's independent scans. **Alert IDs are unknown except those mapped above.** One row represents one GHSA/package combination; a GHSA can affect more than one package, so row totals need not equal distinct-advisory totals. `root` means the root pnpm lock; `frontend` means the frontend pnpm lock; `backend` means the uv lock. Patch floors in the implementation tables account for the combined findings for each package.

| Severity | Package | Baseline version(s) | Lock scope | Advisory |
| --- | --- | --- | --- | --- |
| Critical | `anyio` | 4.13.0 | backend | [GHSA-82r6-8w77-94w6](https://github.com/advisories/GHSA-82r6-8w77-94w6) |
| Critical | `piscina` | 5.1.4 | frontend | [GHSA-67c8-pqhq-4rmx](https://github.com/advisories/GHSA-67c8-pqhq-4rmx) |
| Critical | `proxy-addr` | 2.0.7 | frontend | [GHSA-jqcg-44mw-7w3h](https://github.com/advisories/GHSA-jqcg-44mw-7w3h) |
| Critical | `pyjwt` | 2.8.0 | backend | [GHSA-ffc3-869f-jxw9](https://github.com/advisories/GHSA-ffc3-869f-jxw9) |
| Critical | `tar` | 7.5.13 | frontend | [GHSA-23hp-3jrh-7fpw](https://github.com/advisories/GHSA-23hp-3jrh-7fpw) |
| High | `@angular/common` | 21.2.8 | frontend | [GHSA-39pv-4j6c-2g6v](https://github.com/advisories/GHSA-39pv-4j6c-2g6v) |
| High | `@angular/common` | 21.2.8 | frontend | [GHSA-48r7-hpm6-gfxm](https://github.com/advisories/GHSA-48r7-hpm6-gfxm) |
| High | `@angular/common` | 21.2.8 | frontend | [GHSA-jhpw-976m-542j](https://github.com/advisories/GHSA-jhpw-976m-542j) |
| High | `@angular/common` | 21.2.8 | frontend | [GHSA-p3vc-36g9-x9gr](https://github.com/advisories/GHSA-p3vc-36g9-x9gr) |
| High | `@angular/common` | 21.2.8 | frontend | [GHSA-q6f4-qqrg-jv6x](https://github.com/advisories/GHSA-q6f4-qqrg-jv6x) |
| High | `@angular/compiler` | 21.2.8 | frontend | [GHSA-jj27-h5hq-8x99](https://github.com/advisories/GHSA-jj27-h5hq-8x99) |
| High | `@angular/core` | 21.2.8 | frontend | [GHSA-jj27-h5hq-8x99](https://github.com/advisories/GHSA-jj27-h5hq-8x99) |
| High | `@angular/core` | 21.2.8 | frontend | [GHSA-rgjc-h3x7-9mwg](https://github.com/advisories/GHSA-rgjc-h3x7-9mwg) |
| High | `@angular/router` | 21.2.8 | frontend | [GHSA-ff3f-86qr-9cv3](https://github.com/advisories/GHSA-ff3f-86qr-9cv3) |
| High | `@modelcontextprotocol/sdk` | 1.26.0 | frontend | [GHSA-6qxp-vccf-f47h](https://github.com/advisories/GHSA-6qxp-vccf-f47h) |
| High | `brace-expansion` | 1.1.14, 5.0.5 | frontend | [GHSA-3jxr-9vmj-r5cp](https://github.com/advisories/GHSA-3jxr-9vmj-r5cp) |
| High | `brace-expansion` | 1.1.14, 5.0.5 | frontend | [GHSA-6j4f-fj2g-mc7p](https://github.com/advisories/GHSA-6j4f-fj2g-mc7p) |
| High | `brace-expansion` | 1.1.14, 5.0.5 | frontend | [GHSA-mh99-v99m-4gvg](https://github.com/advisories/GHSA-mh99-v99m-4gvg) |
| High | `brace-expansion` | 1.1.14, 5.0.5 | frontend | [GHSA-qhr7-859c-m2p7](https://github.com/advisories/GHSA-qhr7-859c-m2p7) |
| High | `brace-expansion` | 1.1.14, 5.0.5 | frontend | [GHSA-rgw5-rvv9-x895](https://github.com/advisories/GHSA-rgw5-rvv9-x895) |
| High | `browserslist` | 4.28.2 | frontend | [GHSA-73wf-gq98-2v4g](https://github.com/advisories/GHSA-73wf-gq98-2v4g) |
| High | `browserslist` | 4.28.2 | frontend | [GHSA-c83g-rgw3-j3cx](https://github.com/advisories/GHSA-c83g-rgw3-j3cx) |
| High | `cryptography` | 46.0.7 | backend | [GHSA-537c-gmf6-5ccf](https://github.com/advisories/GHSA-537c-gmf6-5ccf) |
| High | `cryptography` | 46.0.7 | backend | [GHSA-g6cj-pr64-35w5](https://github.com/advisories/GHSA-g6cj-pr64-35w5) |
| High | `cryptography` | 46.0.7 | backend | [GHSA-jwv3-5hgf-82ww](https://github.com/advisories/GHSA-jwv3-5hgf-82ww) |
| High | `fast-uri` | 3.1.0 | frontend, root | [GHSA-4c8g-83qw-93j6](https://github.com/advisories/GHSA-4c8g-83qw-93j6) |
| High | `fast-uri` | 3.1.0 | frontend, root | [GHSA-7p8r-x3mc-p8w7](https://github.com/advisories/GHSA-7p8r-x3mc-p8w7) |
| High | `fast-uri` | 3.1.0 | frontend, root | [GHSA-f65p-4m7j-42xc](https://github.com/advisories/GHSA-f65p-4m7j-42xc) |
| High | `fast-uri` | 3.1.0 | frontend, root | [GHSA-jqff-g426-hqxp](https://github.com/advisories/GHSA-jqff-g426-hqxp) |
| High | `fast-uri` | 3.1.0 | frontend, root | [GHSA-q3j6-qgpj-74h6](https://github.com/advisories/GHSA-q3j6-qgpj-74h6) |
| High | `fast-uri` | 3.1.0 | frontend, root | [GHSA-qw65-cvwx-89v3](https://github.com/advisories/GHSA-qw65-cvwx-89v3) |
| High | `fast-uri` | 3.1.0 | frontend, root | [GHSA-v2hh-gcrm-f6hx](https://github.com/advisories/GHSA-v2hh-gcrm-f6hx) |
| High | `fast-uri` | 3.1.0 | frontend, root | [GHSA-v39h-62p7-jpjc](https://github.com/advisories/GHSA-v39h-62p7-jpjc) |
| High | `hono` | 4.12.12 | frontend | [GHSA-88fw-hqm2-52qc](https://github.com/advisories/GHSA-88fw-hqm2-52qc) |
| High | `http-cache-semantics` | 4.2.0 | frontend | [GHSA-ch52-4w7c-c8xp](https://github.com/advisories/GHSA-ch52-4w7c-c8xp) |
| High | `immutable` | 5.1.5 | frontend | [GHSA-v56q-mh7h-f735](https://github.com/advisories/GHSA-v56q-mh7h-f735) |
| High | `immutable` | 5.1.5 | frontend | [GHSA-xvcm-6775-5m9r](https://github.com/advisories/GHSA-xvcm-6775-5m9r) |
| High | `ip-address` | 10.1.0 | frontend | [GHSA-mwp4-54f8-5fhr](https://github.com/advisories/GHSA-mwp4-54f8-5fhr) |
| High | `js-yaml` | 4.1.1 | frontend, root | [GHSA-2883-xcg3-v3hh](https://github.com/advisories/GHSA-2883-xcg3-v3hh) |
| High | `js-yaml` | 4.1.1 | frontend, root | [GHSA-52cp-r559-cp3m](https://github.com/advisories/GHSA-52cp-r559-cp3m) |
| High | `js-yaml` | 4.1.1 | frontend, root | [GHSA-5p4m-2wfm-xmqj](https://github.com/advisories/GHSA-5p4m-2wfm-xmqj) |
| High | `mako` | 1.3.10 | backend | [GHSA-2h4p-vjrc-8xpq](https://github.com/advisories/GHSA-2h4p-vjrc-8xpq) |
| High | `mako` | 1.3.10 | backend | [GHSA-v92g-xgxw-vvmm](https://github.com/advisories/GHSA-v92g-xgxw-vvmm) |
| High | `nanoid` | 3.3.11 | frontend | [GHSA-28wg-ghj8-5hjv](https://github.com/advisories/GHSA-28wg-ghj8-5hjv) |
| High | `nanoid` | 3.3.11 | frontend | [GHSA-2v37-7h3g-55p8](https://github.com/advisories/GHSA-2v37-7h3g-55p8) |
| High | `nanoid` | 3.3.11 | frontend | [GHSA-xwg4-73v4-xw9w](https://github.com/advisories/GHSA-xwg4-73v4-xw9w) |
| High | `pacote` | 21.3.1 | frontend | [GHSA-w4pp-8pjf-rmxw](https://github.com/advisories/GHSA-w4pp-8pjf-rmxw) |
| High | `piscina` | 5.1.4 | frontend | [GHSA-x9g3-xrwr-cwfg](https://github.com/advisories/GHSA-x9g3-xrwr-cwfg) |
| High | `postcss` | 8.5.9 | frontend | [GHSA-6g55-p6wh-862q](https://github.com/advisories/GHSA-6g55-p6wh-862q) |
| High | `postcss` | 8.5.9 | frontend | [GHSA-r28c-9q8g-f849](https://github.com/advisories/GHSA-r28c-9q8g-f849) |
| High | `pyjwt` | 2.8.0 | backend | [GHSA-752w-5fwx-jx9f](https://github.com/advisories/GHSA-752w-5fwx-jx9f) |
| High | `pyjwt` | 2.8.0 | backend | [GHSA-9v7f-9g4p-ffgj](https://github.com/advisories/GHSA-9v7f-9g4p-ffgj) |
| High | `pyjwt` | 2.8.0 | backend | [GHSA-p4g4-x82p-q773](https://github.com/advisories/GHSA-p4g4-x82p-q773) |
| High | `pyjwt` | 2.8.0 | backend | [GHSA-xgmm-8j9v-c9wx](https://github.com/advisories/GHSA-xgmm-8j9v-c9wx) |
| High | `python-multipart` | 0.0.26 | backend | [GHSA-5rvq-cxj2-64vf](https://github.com/advisories/GHSA-5rvq-cxj2-64vf) |
| High | `python-multipart` | 0.0.26 | backend | [GHSA-pp6c-gr5w-3c5g](https://github.com/advisories/GHSA-pp6c-gr5w-3c5g) |
| High | `setuptools` | 70.0.0 | backend | [GHSA-5rjg-fvgr-3xxf](https://github.com/advisories/GHSA-5rjg-fvgr-3xxf) |
| High | `sigstore` | 4.1.0 | frontend | [GHSA-52v5-jr5w-gjxr](https://github.com/advisories/GHSA-52v5-jr5w-gjxr) |
| High | `soupsieve` | 2.8.3 | backend | [GHSA-2wc2-fm75-p42x](https://github.com/advisories/GHSA-2wc2-fm75-p42x) |
| High | `soupsieve` | 2.8.3 | backend | [GHSA-836r-79rf-4m37](https://github.com/advisories/GHSA-836r-79rf-4m37) |
| High | `source-map-js` | 1.2.1 | frontend | [GHSA-68fv-2mgg-jv7q](https://github.com/advisories/GHSA-68fv-2mgg-jv7q) |
| High | `starlette` | 1.0.0 | backend | [GHSA-82w8-qh3p-5jfq](https://github.com/advisories/GHSA-82w8-qh3p-5jfq) |
| High | `starlette` | 1.0.0 | backend | [GHSA-wqp7-x3pw-xc5r](https://github.com/advisories/GHSA-wqp7-x3pw-xc5r) |
| High | `tar` | 7.5.13 | frontend | [GHSA-8x88-c5mf-7j5w](https://github.com/advisories/GHSA-8x88-c5mf-7j5w) |
| High | `tar` | 7.5.13 | frontend | [GHSA-r292-9mhp-454m](https://github.com/advisories/GHSA-r292-9mhp-454m) |
| High | `undici` | 7.24.4 | frontend | [GHSA-4cwx-7wf7-3272](https://github.com/advisories/GHSA-4cwx-7wf7-3272) |
| High | `undici` | 7.24.4 | frontend | [GHSA-hm92-r4w5-c3mj](https://github.com/advisories/GHSA-hm92-r4w5-c3mj) |
| High | `undici` | 7.24.4 | frontend | [GHSA-rfgv-xxqx-mfg5](https://github.com/advisories/GHSA-rfgv-xxqx-mfg5) |
| High | `undici` | 7.24.4 | frontend | [GHSA-vmh5-mc38-953g](https://github.com/advisories/GHSA-vmh5-mc38-953g) |
| High | `undici` | 7.24.4 | frontend | [GHSA-vxpw-j846-p89q](https://github.com/advisories/GHSA-vxpw-j846-p89q) |
| High | `undici` | 7.24.4 | frontend | [GHSA-w293-vg96-wgc3](https://github.com/advisories/GHSA-w293-vg96-wgc3) |
| High | `urllib3` | 2.6.3 | backend | [GHSA-8988-9cw3-xx77](https://github.com/advisories/GHSA-8988-9cw3-xx77) |
| High | `urllib3` | 2.6.3 | backend | [GHSA-mf9v-mfxr-j63j](https://github.com/advisories/GHSA-mf9v-mfxr-j63j) |
| High | `urllib3` | 2.6.3 | backend | [GHSA-qccp-gfcp-xxvc](https://github.com/advisories/GHSA-qccp-gfcp-xxvc) |
| High | `urllib3` | 2.6.3 | backend | [GHSA-vxq7-64xx-v4gw](https://github.com/advisories/GHSA-vxq7-64xx-v4gw) |
| High | `vite` | 7.3.2 | frontend | [GHSA-fx2h-pf6j-xcff](https://github.com/advisories/GHSA-fx2h-pf6j-xcff) |
