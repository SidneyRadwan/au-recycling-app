const { chromium } = require('playwright');

const PAGES = [
  { url: 'http://localhost:3000/',                          name: 'Homepage',         lightId: '22e72583-1c11-471a-bdf7-67313fd0dc92', darkId: '8a43e56c-1c46-4479-a73a-85fbf5c092a7' },
  { url: 'http://localhost:3000/councils',                  name: 'Councils list',    lightId: 'f2b5f0e8-c7c6-4b8f-98eb-ced843d1a7b4', darkId: '5cf2427f-3866-42a1-bf31-ffe79ad558ce' },
  { url: 'http://localhost:3000/materials',                 name: 'Materials list',   lightId: 'e6c8f6a8-14d1-472e-9454-5f1995355418', darkId: '991208cd-884d-4e08-a759-ee0e643ed7bc' },
  { url: 'http://localhost:3000/councils/city-of-sydney',   name: 'City of Sydney',   lightId: 'a6024b57-ee7a-487a-b801-a4d8644284f9', darkId: 'a72e9343-ea3e-4d14-81bf-d9f453a8c0f7' },
  { url: 'http://localhost:3000/materials/batteries',       name: 'Batteries detail', lightId: '20ea3f8a-93b4-4f12-944f-dd455618cf7a', darkId: '6aa11b30-2825-4f39-9fc9-1d9a1f498233' },
  { url: 'http://localhost:3000/ai-preview',                name: 'AI Preview',       lightId: 'ba60d2e8-1678-4131-99e8-c21b16615708', darkId: 'b11d3747-b942-448c-bc57-f9259fafb6bf' },
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
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(1000);

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
  console.log('All captures submitted.');
})();
