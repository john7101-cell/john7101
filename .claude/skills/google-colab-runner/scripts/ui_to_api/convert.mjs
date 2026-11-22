import { chromium } from 'playwright';
import fs from 'node:fs';
const files = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const browser = await chromium.launch();
const page = await browser.newPage();
page.on('pageerror', e => console.error('pageerror', String(e).slice(0, 200)));
await page.goto(process.env.COMFY_URL || 'http://127.0.0.1:8188/', { waitUntil: 'networkidle' });
await page.waitForFunction(() => window.app && window.app.graph && window.app.graphToPrompt, null, { timeout: 120000 });
const results = {};
for (const f of files) {
  const wf = JSON.parse(fs.readFileSync(f, 'utf8'));
  try {
    const r = await page.evaluate(async (wf) => {
      const missing = [];
      await window.app.loadGraphData(wf, true, true, null, { showMissingNodesDialog: false, showMissingModelsDialog: false });
      const p = await window.app.graphToPrompt();
      return { output: p.output };
    }, wf);
    results[f] = r;
  } catch (e) { results[f] = { error: String(e).slice(0, 500) }; }
}
fs.writeFileSync(process.argv[3], JSON.stringify(results));
await browser.close();
