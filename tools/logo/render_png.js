// Draw the press kit's PNG files from its SVG files, with transparent backgrounds (tools/logo/build_brand.py).
// node tools/logo/render_png.js jobs.json, where each job is {svg, png, height}; the width follows the SVG's shape.
const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const job of jobs) {
    const text = fs.readFileSync(job.svg, 'utf8');
    const [, , vw, vh] = text.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);
    const height = job.height;
    const width = Math.round((vw / vh) * height);
    await page.setViewportSize({ width, height });
    const sized = text.replace(/width="[^"]+" height="[^"]+"/, `width="${width}" height="${height}"`);
    await page.setContent(`<html><body style="margin:0;background:transparent">${sized}</body></html>`);
    await page.locator('body > svg').screenshot({ path: job.png, omitBackground: true });
  }
  await browser.close();
})();
