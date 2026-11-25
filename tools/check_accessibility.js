// Accessibility checks for the website and the drawings (M13a). WCAG 2.2 AA.
//
//   node tools/check_accessibility.js [site/dist]
//
// 1. Runs axe-core on every page of the built website, in light and dark mode
//    (the WCAG 2.0 to 2.2 A and AA rules and axe's best practices).
//    The permanent-address pages (/PCB-DFA-006/) only forward, so they're skipped.
// 2. Checks every page reflows at 320 CSS pixels wide without scrolling sideways (WCAG 1.4.10).
// 3. Checks the contrast of every piece of text in the book's drawings, in light and dark mode,
//    because axe can't see inside an image. Small text needs 4.5 to 1 and large text 3 to 1 (WCAG 1.4.3).
//
// Needs Playwright with Chromium, and axe-core (npm install --no-save axe-core@4.10.3).
// Exits 1 on any failure.
const { chromium } = require('playwright');
const fs = require('fs');
const http = require('http');
const path = require('path');

const repo = path.resolve(__dirname, '..');
const dist = path.resolve(process.argv[2] || path.join(repo, 'site', 'dist'));
const axeSource = fs.readFileSync(require.resolve('axe-core/axe.min.js', { paths: [repo, process.cwd()] }), 'utf8');
const AXE_TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'];

function sitePages() {
  const pages = [];
  (function walk(dir) {
    for (const name of fs.readdirSync(dir)) {
      const p = path.join(dir, name);
      if (fs.statSync(p).isDirectory()) {
        if (dir === dist && (/^PCB-/.test(name) || name === '_astro')) continue;
        walk(p);
      } else if (name === 'index.html') {
        pages.push('/' + path.relative(dist, p).replace(/index\.html$/, '').split(path.sep).join('/'));
      }
    }
  })(dist);
  pages.push('/404.html');
  return pages.sort();
}

function drawings() {
  const out = [];
  (function walk(dir) {
    for (const name of fs.readdirSync(dir)) {
      const p = path.join(dir, name);
      if (fs.statSync(p).isDirectory()) walk(p);
      else if (name.endsWith('.svg') && path.basename(dir) === 'images') out.push(p);
    }
  })(path.join(repo, 'book'));
  return out.sort();
}

const TYPES = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.woff2': 'font/woff2', '.json': 'application/json', '.ico': 'image/x-icon' };

function serve() {
  const server = http.createServer((req, res) => {
    let p = decodeURIComponent(req.url.split('?')[0]);
    let file = path.join(dist, p);
    if (!file.startsWith(dist)) { res.writeHead(403); return res.end(); }
    if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    if (!fs.existsSync(file)) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream' });
    fs.createReadStream(file).pipe(res);
  });
  return new Promise(resolve => server.listen(0, '127.0.0.1', () => resolve(server)));
}

// Runs in the drawing's own page: every <text> whose contrast with what lies under it is too low.
function lowContrastText() {
  const lum = c => {
    const [r, g, b] = c.match(/[\d.]+/g).slice(0, 3).map(Number).map(v => {
      v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const texts = [...document.querySelectorAll('text')];
  texts.forEach(t => { t.style.pointerEvents = 'none'; });
  const shapes = ['rect', 'path', 'circle', 'ellipse', 'polygon'];
  const under = (x, y) => {
    for (const e of document.elementsFromPoint(x, y)) {
      if (!shapes.includes(e.tagName)) continue;
      const s = getComputedStyle(e);
      if (s.fill.startsWith('rgb') && !(parseFloat(s.fillOpacity) < 0.5)) return s.fill;
    }
    return 'rgb(255, 255, 255)';
  };
  const bad = [];
  for (const t of texts) {
    const s = getComputedStyle(t);
    if (!t.textContent.trim() || s.display === 'none' || !s.fill.startsWith('rgb')) continue;
    let worst = Infinity, bg = null;
    if (s.paintOrder.startsWith('stroke') && s.stroke.startsWith('rgb') && parseFloat(s.strokeWidth) >= 2) {
      bg = s.stroke; worst = ratio(s.fill, bg);          // a halo under the text is its background
    } else {
      const r = t.getBoundingClientRect(), y = r.top + r.height / 2;
      for (const x of [r.left + 2, r.left + r.width / 2, r.right - 2]) {
        const c = under(x, y), k = ratio(s.fill, c);
        if (k < worst) { worst = k; bg = c; }
      }
    }
    const size = parseFloat(s.fontSize), large = size >= 24 || (+s.fontWeight >= 700 && size >= 18.66);
    if (worst < (large ? 3 : 4.5)) bad.push(`"${t.textContent.trim().slice(0, 30)}" ${s.fill} on ${bg}: ${worst.toFixed(2)} to 1`);
  }
  return bad;
}

(async () => {
  const server = await serve();
  const base = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch();
  const failures = [];
  const pages = sitePages();

  for (const scheme of ['light', 'dark']) {
    const context = await browser.newContext({ colorScheme: scheme, viewport: { width: 1280, height: 900 } });
    await context.addInitScript(s => { try { localStorage.setItem('starlight-theme', s); } catch (e) {} }, scheme);
    const page = await context.newPage();
    for (const url of pages) {
      await page.setViewportSize({ width: 1280, height: 900 });
      await page.goto(base + url, { waitUntil: 'load' });
      // Expressive Code makes a wide code block focusable just after load; let it run first.
      await page.waitForTimeout(300);
      await page.addScriptTag({ content: axeSource });
      const result = await page.evaluate(tags => axe.run(document, { runOnly: { type: 'tag', values: tags } }), AXE_TAGS);
      for (const v of result.violations) {
        for (const n of v.nodes) failures.push(`${scheme} ${url}: ${v.id} (${v.impact}) at ${n.target.join(' ')}`);
      }
      if (scheme === 'light') {
        await page.setViewportSize({ width: 320, height: 640 });
        await page.waitForTimeout(100);
        const wide = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
        if (wide > 0) failures.push(`${url}: scrolls sideways by ${wide} px at 320 px wide (reflow)`);
      }
    }
    for (const file of drawings()) {
      await page.goto('file://' + file);
      // Text is hit-tested on screen, so the window must hold the whole drawing.
      const box = await page.evaluate(() => { const r = document.documentElement.getBoundingClientRect(); return [r.width, r.height]; });
      await page.setViewportSize({ width: Math.ceil(box[0]) + 20, height: Math.ceil(box[1]) + 20 });
      for (const line of await page.evaluate(lowContrastText)) {
        failures.push(`${scheme} ${path.relative(repo, file)}: ${line}`);
      }
    }
    await context.close();
  }
  await browser.close();
  server.close();

  console.log(`check_accessibility: ${pages.length} pages and ${drawings().length} drawings, in light and dark mode`);
  for (const f of failures) console.log('  ' + f);
  console.log(failures.length ? `${failures.length} problems` : 'no problems found');
  process.exit(failures.length ? 1 : 0);
})();
