// node shoot_png.cjs <outdir> <m> <times|all> [fps] [dur]  — transparent PNG overlay frames
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const [out, m, times, fps = '30', dur = '20.6'] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', (e) => console.log('pageerror:', e.message));
  await p.goto('http://127.0.0.1:8767/x5.html?m=' + m + (process.env.CTA ? '&cta=1' : '')); await p.waitForFunction('window.READY === true', null, { timeout: 120000 });
  const list = times === 'all' ? Array.from({ length: Math.round(+dur * +fps) }, (_, i) => i / +fps) : times.split(',').map(Number);
  for (let i = 0; i < list.length; i++) {
    if (process.env.FROM && list[i] < +process.env.FROM) continue;
    await p.evaluate((t) => window.renderAt(t), list[i]);
    await p.screenshot({ path: path.join(out, times === 'all' ? String(i).padStart(5, '0') + '.png' : `t${list[i].toFixed(1)}.png`), omitBackground: true });
    if (i % 100 === 0) console.log('frame', i, '/', list.length);
  }
  await b.close();
})();
