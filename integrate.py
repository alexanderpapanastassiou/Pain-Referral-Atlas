# -*- coding: utf-8 -*-
"""Inject the rotatable 3-D body view into a referred-pain atlas page.

Both atlases share the same plate panel and paint()/tooltip code, so one set of
string patches serves both. The 3-D view is a second rendering of the same
region/heat state — paint() feeds it the same map it paints the SVG plates with.
"""
import json
import pathlib

RENDERER = (pathlib.Path(__file__).parent / "body3d.js").read_text()

CSS = """
/* ---------- 3-D model view ---------- */
.seg{display:inline-flex;background:var(--surface-2);border-radius:8px;padding:3px;gap:2px}
.seg button{font-size:12px;font-weight:500;color:var(--ink-soft);padding:4px 10px;border-radius:6px;white-space:nowrap}
.seg button:hover{color:var(--ink)}
.seg button[aria-pressed="true"]{background:var(--surface);color:var(--accent-ink);font-weight:600;box-shadow:0 1px 2px rgba(20,30,24,.12)}
.bothlink{font-size:12px;font-weight:500;color:var(--accent-ink);text-decoration:none;padding:4px 10px;border-radius:6px;border:1px solid var(--line);white-space:nowrap}
.bothlink:hover{background:var(--accent-soft)}
#model3d{display:none;padding:8px 8px 4px}
.plate-wrap.model #model3d{display:block}
.plate-wrap.model .figs{display:none}
.b3d-canvas{display:block;width:100%;height:min(64vh,600px);border-radius:8px;background:var(--paper);cursor:grab;touch-action:none;outline:none}
.b3d-canvas:focus-visible{box-shadow:0 0 0 2px var(--accent)}
.b3d-canvas.grabbing{cursor:grabbing}
.b3d-bar{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:9px 4px 4px}
.b3d-views{display:flex;gap:4px;flex-wrap:wrap}
.b3d-btn{font-size:11.5px;font-weight:500;color:var(--ink-soft);border:1px solid var(--line);border-radius:6px;padding:4px 9px;background:var(--surface)}
.b3d-btn:hover{background:var(--surface-2);color:var(--ink)}
.b3d-hint{font-family:"IBM Plex Mono";font-size:10px;letter-spacing:.04em;color:var(--ink-faint);margin-left:auto}
@media (max-width:520px){.b3d-hint{display:none}}
</style>"""

TOGGLE = """<h2>Body plate</h2>
          <div class="seg" role="group" aria-label="Plate style">
            <button type="button" id="viewPlates" aria-pressed="true">Plates</button>
            <button type="button" id="viewModel" aria-pressed="false">3-D model</button>
          </div>
          <a class="bothlink" href="https://claude.ai/artifact/7H1MEtjaCd6geyoixzjZN3" target="_blank" rel="noopener" title="Whole-body atlas: upper and lower quarter on one 3-D figure">Both quarters ↗</a>"""

MODEL_DIV = """        <div id="model3d"></div>
        <div class="legend" id="legend"></div>"""

# after the SVG rects are painted, feed the same map to the model
PAINT_HOOK = """  rects.forEach(el => {
    const v = map[el.dataset.r] || 0;
    el.classList.remove('h1','h2','h3','picked');
    if (v) el.classList.add('h' + v);
    if (mode === 'region' && el.dataset.r === activeRegion) el.classList.add('picked');
  });
  if (B3D) B3D.setHeat(map, mode === 'region' ? activeRegion : null);"""

PAINT_ORIG = """  rects.forEach(el => {
    const v = map[el.dataset.r] || 0;
    el.classList.remove('h1','h2','h3','picked');
    if (v) el.classList.add('h' + v);
    if (mode === 'region' && el.dataset.r === activeRegion) el.classList.add('picked');
  });"""

# tooltip: factor the per-rect handlers into showTip()/hideTip() so the model can share them
TIP_ORIG_START = "/* tooltip */\nconst tip = $('tip');\nrects.forEach(el => {"
TIP_NEW = """/* tooltip — shared by the SVG plates and the 3-D model */
const tip = $('tip');
function tipText(rid){
  let extra;
  if (mode === 'structure' && activeStruct){
    const i = activeStruct.zones[rid];
    extra = i ? {3:'Primary zone',2:'Common referral',1:'Spillover'}[i] : 'Not a referral zone';
  } else {
    extra = DENSITY[rid] + ' structure' + (DENSITY[rid]===1?'':'s') + ' refer here';
  }
  return '<span class="tt">' + esc(extra) + '</span>' + esc(R[rid]);
}
function placeTip(cx, cy){
  const pad = 14;
  let x = cx + pad, y = cy + pad;
  if (x + 250 > window.innerWidth) x = cx - 250 - pad;
  if (y + 60 > window.innerHeight) y = cy - 60;
  tip.style.left = x + 'px'; tip.style.top = y + 'px';
}
function hideTip(){ tip.classList.remove('on'); rects.forEach(x => x.classList.remove('hovered')); }
rects.forEach(el => {"""

MODEL_JS = """
/* ---------------- 3-D model ---------------- */
const plateWrap = document.querySelector('.plate-wrap');
function setPlateView(model, persist){
  plateWrap.classList.toggle('model', model);
  $('viewPlates').setAttribute('aria-pressed', String(!model));
  $('viewModel').setAttribute('aria-pressed', String(model));
  if (model){
    if (!B3D && window.Body3D){
      B3D = new Body3D($('model3d'), DATA.model3d, {
        label: 'Rotatable 3-D body heat map — drag to rotate, scroll to zoom, click a zone to select it',
        onHover: (rid, x, y) => {
          if (!rid){ hideTip(); return; }
          tip.innerHTML = tipText(rid); placeTip(x, y); tip.classList.add('on');
        },
        onPick: (rid) => {
          if (!rid) return;
          if (mode==='region' && activeRegion===rid){ mode='density'; activeRegion=null; }
          else { activeRegion = rid; activeStruct=null; mode='region'; }
          paint(); renderRail(); tip.innerHTML = tipText(rid);
        }
      });
      paint();
    } else if (B3D) B3D.redraw();
  } else hideTip();
  if (persist){ try { localStorage.setItem('atlas-plate-view', model ? 'model' : 'plates'); } catch (e) {} }
}
$('viewPlates').addEventListener('click', () => setPlateView(false, true));
$('viewModel').addEventListener('click', () => setPlateView(true, true));
(function(){
  let saved = null;
  try { saved = localStorage.getItem('atlas-plate-view'); } catch (e) {}
  if (saved === 'model') setPlateView(true, false);
})();
</script>"""


def inject(html: str, spec: dict) -> str:
    """Return the page with the 3-D view wired in. Raises if an anchor is missing."""
    def sub(old, new, count=1):
        nonlocal html
        assert html.count(old) == count, (old[:60], html.count(old))
        html = html.replace(old, new)

    # CSS — before the closing </style> of the page's single stylesheet
    sub("</style>", CSS)
    # toggle in the plate panel head
    sub("<h2>Body plate</h2>", TOGGLE)
    # model container just above the legend
    sub('        <div class="legend" id="legend"></div>', MODEL_DIV)
    # renderer + spec, before the page script
    sub("<script>\nconst DATA = __PAYLOAD__;",
        "<script>\n" + RENDERER + "\n</script>\n<script>\nconst DATA = __PAYLOAD__;\nDATA.model3d = __MODEL3D__;")
    # paint() hook — B3D must be declared before the first paint() runs
    sub("let query = '';", "let query = '';\nlet B3D = null;   // 3-D model, created on first use")
    sub(PAINT_ORIG, PAINT_HOOK)
    # tooltip refactor
    sub(TIP_ORIG_START, TIP_NEW)
    # model wiring before the closing script tag (the last one in the page)
    idx = html.rindex("</script>")
    html = html[:idx] + MODEL_JS + html[idx + len("</script>"):]
    html = html.replace("__MODEL3D__", json.dumps(spec, separators=(",", ":")))
    return html
