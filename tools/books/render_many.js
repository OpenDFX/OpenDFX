// Render many SVGs to opaque PNGs in one browser session, for the print PDF (M13).
// node tools/books/render_many.js jobs.json   where jobs.json is [{"svg": path, "png": path, "width": cssPx, "height": cssPx, "scale": n}, ...]
// Uses Chromium, the same engine that draws the website, so the PNGs match what readers see online.
// In Claude's cloud sessions Chromium is at /opt/pw-browsers/chromium; elsewhere Playwright's own browser is used.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const pinned = '/opt/pw-browsers/chromium';
  const browser = await chromium.launch(fs.existsSync(pinned) ? { executablePath: pinned } : {});
  for (const j of jobs) {
    const page = await browser.newPage({ viewport: { width: j.width, height: j.height }, deviceScaleFactor: j.scale, colorScheme: 'light' });
    const html = `<html><body style="margin:0;background:#fff"><img src="file://${path.resolve(j.svg)}" style="display:block;width:${j.width}px;height:${j.height}px"></body></html>`;
    // Load the page from a file next to the PNG: a page made with setContent may not read file:// images.
    const holder = `${j.png}.html`;
    fs.writeFileSync(holder, html);
    await page.goto('file://' + path.resolve(holder), { waitUntil: 'load' });
    const ok = await page.evaluate(() => { const i = document.images[0]; return i.complete && i.naturalWidth > 0; });
    if (!ok) throw new Error(`could not load ${j.svg}`);
    // Each drawing carries its own font (FONT1). Wait until the image is fully decoded, with its text drawn in that
    // font, before capturing, so no strip is taken while the drawing is still being painted.
    await page.evaluate(async () => { await document.images[0].decode(); await document.fonts.ready; });
    await page.waitForTimeout(50);
    fs.unlinkSync(holder);
    // A 600 dpi drawing can be larger than some Chromium builds will capture in one screenshot, so it is captured
    // in strips (j.png.0, j.png.1, ...) that build_books.py stitches together.
    const strip = j.strip || 256;
    let n = 0;
    for (let y = 0; y < j.height; y += strip, n++) {
      const h = Math.min(strip, j.height - y);
      // Chromium can refuse a capture while it is still compositing ("Unable to capture screenshot"); try again.
      for (let attempt = 1; ; attempt++) {
        try {
          await page.screenshot({ path: `${j.png}.${n}`, type: 'png', clip: { x: 0, y, width: j.width, height: h } });
          break;
        } catch (e) {
          if (attempt >= 3 || !String(e).includes('Unable to capture screenshot')) throw e;
          await page.waitForTimeout(500);
        }
      }
    }
    fs.writeFileSync(`${j.png}.strips`, String(n));
    await page.close();
  }
  await browser.close();
})();
