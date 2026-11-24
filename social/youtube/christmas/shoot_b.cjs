// node shoot.cjs <outdir> <t1,t2,...> | node shoot.cjs <outdir> all <fps> <dur>
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const [out, times, fps = '30', dur = '39'] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  p.on('console', (m) => { if (m.type() === 'error' || m.type() === 'warning') console.log('console:', m.text()); }); p.on('pageerror', (e) => console.log('pageerror:', e.message));
  await p.goto('http://127.0.0.1:8767/batch.html?s='+process.env.S+(process.env.CTA?'&cta=1':'')); await p.waitForFunction('window.READY === true', null, { timeout: 120000 });
  const cdp = await p.context().newCDPSession(p);
  const list = times === 'all' ? Array.from({ length: Math.round(+dur * +fps) }, (_, i) => i / +fps) : times.split(',').map(Number);
  const t0 = Date.now();
  for (let i = 0; i < list.length; i++) {
    if (process.env.FROM && list[i] < +process.env.FROM) continue;
    await p.evaluate((t) => window.renderAt(t), list[i]);
    const { data } = await cdp.send('Page.captureScreenshot', { format: 'jpeg', quality: 93 });
    fs.writeFileSync(path.join(out, times === 'all' ? String(i).padStart(5, '0') + '.jpg' : `t${list[i].toFixed(1)}.jpg`), Buffer.from(data, 'base64'));
    if (i % 60 === 0) console.log('frame', i, '/', list.length, ((Date.now() - t0) / 1000).toFixed(0) + 's');
  }
  await b.close();
})();
