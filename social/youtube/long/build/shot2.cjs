// node shot2.cjs <page> <w> <h> <out.png> <json>
const { chromium } = require('playwright');
(async () => { const [page, w, h, out, json] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +w, height: +h } });
  await p.goto('file://' + process.cwd() + '/' + page + '#' + encodeURIComponent(json)); await p.waitForFunction('window.READY===true'); await p.waitForTimeout(400);
  await p.screenshot({ path: out, omitBackground: page.startsWith('panels') }); await b.close(); })();
