// Check drawings for print (DRW1): node tools/diagrams/check_print.js <file.svg>...
// For each drawing, at the print version's text width (175.9 mm, or 200 mm tall at most), reports
// the smallest text and the thinnest line in points, text that overlaps other text, and text that runs off the drawing.
// A drawing passes when its text is at least 7 pt, its lines at least 0.75 pt, and nothing overlaps or runs off.
// Exit code 1 if any drawing fails.
const { chromium } = require('playwright');
const path = require('path');
const PT_MM = 25.4 / 72;
(async () => {
  const files = process.argv.slice(2);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage();
  let failed = 0;
  for (const f of files) {
    await p.goto('file://' + path.resolve(f));
    const r = await p.evaluate(() => {
      const svg = document.querySelector('svg');
      const vb = svg.viewBox.baseVal;
      const k = Math.min(175.9 / vb.width, 200 / vb.height);   // mm per drawing unit in print
      const toUser = (el) => {                                   // an element's box in the svg's own units
        const bb = el.getBBox(), m = el.getCTM(), root = svg.getCTM().inverse();
        const mm = root.multiply(m);
        const pts = [[bb.x, bb.y], [bb.x + bb.width, bb.y], [bb.x, bb.y + bb.height], [bb.x + bb.width, bb.y + bb.height]]
          .map(([x, y]) => { const q = new DOMPoint(x, y).matrixTransform(mm); return [q.x, q.y]; });
        const xs = pts.map(q => q[0]), ys = pts.map(q => q[1]);
        return { x0: Math.min(...xs), y0: Math.min(...ys), x1: Math.max(...xs), y1: Math.max(...ys), s: Math.sqrt(Math.abs(mm.a * mm.d - mm.b * mm.c)),
                 rot: Math.abs(mm.b) > Math.abs(mm.a) };   // turned on its side: the font's empty space is left and right
      };
      const texts = [...svg.querySelectorAll('text')].filter(t => t.textContent.trim() && !t.closest('clipPath, defs'));
      const boxes = texts.map(t => {
        const u = toUser(t);
        const fs = parseFloat(getComputedStyle(t).fontSize);
        return { t: t.textContent.trim(), ...u, pt: fs * u.s * k / (25.4 / 72) };
      });
      let minText = Math.min(...boxes.map(x => x.pt));
      const small = boxes.filter(x => x.pt < 7 - 1e-6).map(x => `"${x.t}" ${x.pt.toFixed(2)} pt`);
      let minLine = Infinity, thin = [];
      for (const el of svg.querySelectorAll('line, path, rect, circle, polyline, polygon, ellipse')) {
        if (el.closest('clipPath, defs')) continue;
        const cs = getComputedStyle(el);
        if (cs.stroke === 'none' || cs.visibility === 'hidden' || cs.display === 'none') continue;
        const w = parseFloat(cs.strokeWidth);
        if (!(w > 0)) continue;
        const m = svg.getCTM().inverse().multiply(el.getCTM());
        const pt = w * Math.sqrt(Math.abs(m.a * m.d - m.b * m.c)) * k / (25.4 / 72);
        if (pt < minLine) minLine = pt;
        if (pt < 0.75 - 1e-6) thin.push(`${el.tagName}.${el.getAttribute('class') || ''} ${pt.toFixed(2)} pt`);
      }
      const pad = 0.15;  // let text boxes touch a little: a font's box includes empty space above and below the letters
      const over = [];
      for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
        const a = boxes[i], c = boxes[j];
        if (a.t === c.t && Math.abs(a.x0 - c.x0) < 3 && Math.abs(a.y0 - c.y0) < 3) continue;   // a label drawn twice on purpose
        const trim = (q) => q.rot ? [(q.x1 - q.x0) * pad, 0] : [0, (q.y1 - q.y0) * pad];
        const [wa, ha] = trim(a), [wc, hc] = trim(c);
        if (a.x0 + wa < c.x1 - wc && c.x0 + wc < a.x1 - wa && a.y0 + ha < c.y1 - hc && c.y0 + hc < a.y1 - ha) over.push(`"${a.t}" / "${c.t}"`);
      }
      const off = boxes.filter(x => x.x0 < vb.x - 0.5 || x.x1 > vb.x + vb.width + 0.5 || x.y0 < vb.y - 0.5 || x.y1 > vb.y + vb.height + 0.5)
        .map(x => `"${x.t}"`);
      return { w: vb.width * k, h: vb.height * k, minText, minLine, small, thin: [...new Set(thin)], over, off };
    });
    const bad = r.small.length || r.thin.length || r.over.length || r.off.length;
    if (bad) failed++;
    console.log(`${bad ? 'FAIL' : 'ok  '} ${path.basename(f)}: ${r.w.toFixed(0)} x ${r.h.toFixed(0)} mm, text from ${r.minText.toFixed(1)} pt, lines from ${r.minLine.toFixed(2)} pt`);
    for (const [name, list] of [['small text', r.small], ['thin lines', r.thin], ['overlapping text', r.over], ['text off the drawing', r.off]])
      if (list.length) console.log(`     ${name}: ${list.slice(0, 8).join('; ')}${list.length > 8 ? ` (+${list.length - 8} more)` : ''}`);
  }
  await b.close();
  process.exit(failed ? 1 : 0);
})();
