import fs from "node:fs/promises";
import path from "node:path";

process.env.PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS ??= "1";

const { chromium } =
  await import("/workspace/frontend/node_modules/playwright/index.mjs");

const flowPath = process.argv[2];

if (!flowPath) {
  console.error("Usage: node run-flow.mjs /path/to/flow.json");
  process.exit(1);
}

const rawFlow = await fs.readFile(flowPath, "utf8");
const flow = JSON.parse(rawFlow);

const browser = await chromium.launch({ headless: flow.headless ?? true });
const context = await browser.newContext({
  viewport: flow.viewport ?? { width: 1440, height: 1200 },
});
const page = await context.newPage();

const resolveUrl = (value) => {
  if (!value) {
    return value;
  }

  if (/^https?:\/\//.test(value)) {
    return value;
  }

  return new URL(value, flow.baseUrl ?? "http://localhost:1560").toString();
};

try {
  for (const step of flow.steps ?? []) {
    switch (step.action) {
      case "goto":
        await page.goto(resolveUrl(step.url), {
          waitUntil: step.waitUntil ?? "domcontentloaded",
        });
        break;
      case "waitForLoadState":
        await page.waitForLoadState(step.state ?? "networkidle");
        break;
      case "waitForTimeout":
        await page.waitForTimeout(step.timeout ?? 1000);
        break;
      case "waitForSelector":
        await page.waitForSelector(step.selector, step.options ?? {});
        break;
      case "click":
        await page.click(step.selector, step.options ?? {});
        break;
      case "fill":
        await page.fill(step.selector, step.value ?? "");
        break;
      case "assertText": {
        const locator = page.locator(step.selector);
        await locator.waitFor(step.options ?? {});
        const text = await locator.textContent();
        if (!text || !text.includes(step.text)) {
          throw new Error(
            `Expected selector ${step.selector} to include text ${JSON.stringify(step.text)} but found ${JSON.stringify(text)}`,
          );
        }
        break;
      }
      case "screenshot": {
        const screenshotPath = path.resolve(step.path);
        await fs.mkdir(path.dirname(screenshotPath), { recursive: true });
        await page.screenshot({
          path: screenshotPath,
          fullPage: step.fullPage ?? true,
        });
        console.log(`screenshot:${screenshotPath}`);
        break;
      }
      default:
        throw new Error(`Unsupported action: ${step.action}`);
    }
  }
} finally {
  await browser.close();
}
