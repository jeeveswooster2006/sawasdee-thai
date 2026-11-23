const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('http://127.0.0.1:8767/rain_ov.html'); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: 'ov-title.png', omitBackground: true });
  await p.evaluate(() => { document.getElementById('cap').style.display = 'block'; });
  await p.screenshot({ path: 'ov-cap.png', omitBackground: true }); await b.close(); })();
