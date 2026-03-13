const { chromium } = require('playwright');

// Subset of pages to retry — copy entries from figma-capture.js as needed
const PAGES = [
  { url: 'http://localhost:3000/councils/city-of-sydney',   name: 'City of Sydney',   lightId: '134d2645-2031-427b-a6b9-0fa333cd2345', darkId: '569d2686-2600-4c45-9c23-b35b1555d437' },
  { url: 'http://localhost:3000/materials/batteries',       name: 'Batteries detail', lightId: 'ffb92921-93cb-4982-9e72-9ca7783b1226', darkId: 'ffbc5c90-3ced-44d9-9cb6-4bafa8c27796' },
];

const CAPTURE_SCRIPT = 'https://mcp.figma.com/mcp/html-to-design/capture.js';

async function capturePage(browser, { url, id, name, theme }) {
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });

  if (theme === 'dark') {
    await context.addInitScript(() => window.localStorage.setItem('theme', 'dark'));
  }

  const page = await context.newPage();
  try {
    console.log(`[${name} / ${theme}] Navigating to ${url}`);
    await page.goto(url, { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(2000);

    const scriptResp = await page.context().request.get(CAPTURE_SCRIPT);
    const scriptText = await scriptResp.text();
    await page.evaluate((s) => {
      const el = document.createElement('script');
      el.textContent = s;
      document.head.appendChild(el);
    }, scriptText);
    await page.waitForTimeout(800);

    const endpoint = `https://mcp.figma.com/mcp/capture/${id}/submit`;
    page.evaluate(({ captureId, endpoint }) => {
      return window.figma.captureForDesign({ captureId, endpoint, selector: 'body' });
    }, { captureId: id, endpoint }).catch(() => {});

    await page.waitForTimeout(8000);
    console.log(`[${name} / ${theme}] Capture submitted ✓`);
  } catch (err) {
    console.error(`[${name} / ${theme}] Error: ${err.message}`);
  } finally {
    await context.close();
  }
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  for (const p of PAGES) {
    await capturePage(browser, { url: p.url, id: p.lightId, name: p.name, theme: 'light' });
    await capturePage(browser, { url: p.url, id: p.darkId,  name: p.name, theme: 'dark'  });
  }
  await browser.close();
  console.log('Done.');
})();
