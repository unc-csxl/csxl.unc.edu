---
name: playwright-localhost-screenshots
description: "Use when reproducing frontend bugs on the local dev proxy, logging in through localhost:1560, navigating CSXL pages with Playwright, and capturing screenshots. Triggers: Playwright, screenshot, localhost:1560, dev proxy, browser repro, auth/as, UI verification."
argument-hint: "Describe the localhost flow to run and the screenshot path to capture."
user-invocable: true
---

# Playwright Localhost Screenshots

Use this skill to drive the local CSXL site through the `http://localhost:1560` Caddy proxy with Playwright, especially for login flows, UI repro steps, and screenshot capture.

## When To Use

- Reproducing frontend bugs that require navigating real pages in the devcontainer
- Logging in through a development auth route like `/auth/as/rhonda/999999999`
- Capturing screenshots of the current UI state for debugging or verification
- Verifying that a page shows the form, assignment card, or another view after data loads

## Preconditions

1. The local stack is running and reachable at `http://localhost:1560`.
2. Frontend dependencies are installed in `/workspace/frontend`.
3. Playwright is available from `/workspace/frontend/node_modules/.bin/playwright`.

## Runner

Use the JSON-driven runner at [run-flow.mjs](./scripts/run-flow.mjs).

The runner accepts a flow file with steps such as:

- `goto`
- `waitForLoadState`
- `waitForSelector`
- `click`
- `fill`
- `screenshot`
- `assertText`

## Usage

1. Create a JSON flow file, typically under `/tmp`, describing the browser actions.
2. Run:

```bash
node /workspace/.github/skills/playwright-localhost-screenshots/scripts/run-flow.mjs \
  /tmp/your-flow.json
```

3. Review the generated screenshot path from the flow file.

## Example Flow

See [localhost-flow.example.json](./assets/localhost-flow.example.json) for the expected structure.

## Notes

- Prefer `waitForLoadState` plus a stable `waitForSelector` before asserting text or capturing screenshots.
- For this repo, authenticate first through `/auth/as/...` before opening protected pages.
- Use full-page screenshots for page-level verification.
