// Render an SVG to PNG to check a diagram: node tools/render_svg.js <in.svg> <out.png> <width> <height> [light|dark]
const { chromium } = require('playwright');
(async () => {
  const [,, inp, out, w, h, scheme] = process.argv;
  const b = await chromium.launch({executablePath: '/opt/pw-browsers/chromium'});
  const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: 2, colorScheme: scheme||'light' });
  await p.goto('file://' + require('path').resolve(inp));
  await p.screenshot({ path: out });
  await b.close();
})();
