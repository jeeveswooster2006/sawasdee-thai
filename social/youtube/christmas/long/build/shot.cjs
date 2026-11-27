const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + process.cwd() + '/panels.html'); await p.waitForFunction('window.READY===true'); await p.waitForTimeout(300);
  await p.screenshot({ path: 'panels.png', omitBackground: true }); await b.close(); })();
