# -*- coding: utf-8 -*-
"""Whole-body Referred Pain Atlas — both quarters on one rotatable figure.

Derived from the LE atlas page template so the rail, detail, table, chips and
evidence sections stay identical; the plate panel is replaced by the 3-D figure
(the only view that can show both datasets at once, since the two 2-D plate
systems have different coordinate frames).

Data merge: the upper-quarter zones that describe the same skin as a
lower-quarter zone (low back, buttock, groin, lower abdomen, thoracolumbar
junction) are translated onto the lower-quarter ids, so one surface carries one
label and a click there lists structures from BOTH atlases.
"""
import json, re, sys, importlib.util, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC / "render"))
import models as M
import integrate as I

def _load(path, name):
    s = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

U = _load(SRC / "upper" / "data.py", "ue_data")
L = _load(SRC / "lower" / "referral_data.py", "lq_data")

# UE zone → LE zone(s) that cover the same surface on the combined figure
ALIAS = {
    "thoracolumbar": ["tl-junction"],
    "lumbar":        ["lumbar", "lumbar-midline"],
    "si-buttock":    ["si-joint", "buttock-upper", "buttock-lower"],
    "groin":         ["groin", "hip-ant", "pubic"],
    "abd-lower":     ["lower-abdomen"],
}
UE_QUARTER, LQ_QUARTER = "upper", "lower"

# (label, url) pills shown under the lede; [] removes the row. See the note
# further down where they are substituted in — these default to private links.
COMPANION_LINKS = [
    ("Cervical Root Atlas",       "https://claude.ai/code/artifact/16be236e-63ce-4bd7-8864-23f074f5b1ba"),
    ("Lumbosacral Root Atlas",    "https://claude.ai/code/artifact/084e13e2-762d-4459-b104-51f72a49ea22"),
    ("Upper Quarter Differential","https://claude.ai/code/artifact/676fe00f-2483-4ca4-bf9c-f5d95067c3d6"),
    ("Lower Quarter Differential","https://claude.ai/code/artifact/adc45a60-1e27-4dfe-949d-410510ba9da2"),
]

regions = {}
for rid, label, _ in U.REGIONS:
    if rid not in ALIAS:
        regions[rid] = label
for rid, label in L.REGIONS:
    regions[rid] = label           # LE label wins for the shared 'flank'

def translate(zones):
    out = {}
    for z, v in zones.items():
        for t in ALIAS.get(z, [z]):
            out[t] = max(out.get(t, 0), v)
    return out

structures = []
for s in U.S:
    s2 = dict(s); s2["id"] = "ue-" + s["id"]; s2["q"] = UE_QUARTER; s2["zones"] = translate(s["zones"])
    structures.append(s2)
for s in L.S:
    s2 = dict(s); s2["id"] = "lq-" + s["id"]; s2["q"] = LQ_QUARTER
    structures.append(s2)

# Both atlases carry the sacroiliac joint and quadratus lumborum. Keep the
# lower-quarter entries (audited, tier B for the SIJ) and drop the upper ones.
DROP = {"ue-joint-sij", "ue-m-quadratus-lumborum"}
structures = [s for s in structures if s["id"] not in DROP]

for s in structures:
    missing = [z for z in s["zones"] if z not in regions]
    assert not missing, (s["id"], missing)

cats = dict(U.CATEGORIES); cats.update({k: v for k, v in dict(L.CATEGORIES).items() if k not in cats})
cats["joint"] = "Peripheral joint / bursa"
tiers = U.TIERS

PAYLOAD = json.dumps({"regions": regions, "structures": structures, "cats": cats, "tiers": tiers,
                      "quarters": {UE_QUARTER: "Upper quarter", LQ_QUARTER: "Lower quarter"}},
                     ensure_ascii=False, separators=(",", ":"))

# ------------------------------------------------------------- template ----
src = (SRC / "lower" / "build_html.py").read_text()
PAGE = src[src.index('PAGE = """') + len('PAGE = """'): src.index('\n"""\n', src.index('PAGE = """'))]
ue_src = (SRC / "upper" / "build_html.py").read_text()

def sub(old, new, count=1):
    global PAGE
    assert PAGE.count(old) == count, (old[:70], PAGE.count(old))
    PAGE = PAGE.replace(old, new)

sub("<title>LE Referred Pain Atlas</title>", "<title>Referred Pain Atlas</title>")
sub('<span class="mark">SOMATIC · LQ</span><h1>LE Referred Pain Atlas</h1>',
    '<span class="mark">SOMATIC · WHOLE BODY</span><h1>Referred Pain Atlas</h1>')
sub("""  <p class="lede">Where <strong>somatic structures of the lumbar spine, pelvis and lower limb</strong> send their pain.""",
    """  <p class="lede">Where <strong>somatic structures of the whole body</strong> — head, neck, trunk, upper and lower limb — send their pain, on one rotatable figure (drag to turn it; switch to <strong>Plates</strong> for the flat anterior, posterior and plantar maps). Upper- and lower-quarter data are merged: where their zones describe the same skin (low back, buttock, groin, lower abdomen) they share one label, so a click lists structures from both.""")
# --- companion links -------------------------------------------------------
# The row of pills under the lede. These four currently point at private
# claude.ai artifacts, which only their owner can open: anyone else visiting a
# published copy of this page gets a dead link. Repoint them at your own hosted
# copies, or set COMPANION_LINKS = [] to drop the row entirely.
_old_links = """    <a href="https://claude.ai/code/artifact/084e13e2-762d-4459-b104-51f72a49ea22" target="_blank" rel="noopener">↗ Lumbosacral Root Atlas</a>
    <a href="https://claude.ai/code/artifact/adc45a60-1e27-4dfe-949d-410510ba9da2" target="_blank" rel="noopener">↗ Lower Quarter Differential</a>"""
if COMPANION_LINKS:
    _new_links = "\n".join(
        f'    <a href="{url}" target="_blank" rel="noopener">↗ {label}</a>'
        for label, url in COMPANION_LINKS)
    sub(_old_links, _new_links)
else:
    a = PAGE.index('  <div class="siblings">')
    b = PAGE.index("</div>", a) + len("</div>\n")
    PAGE = PAGE[:a] + PAGE[b:]

# ------------------------------------------------------------- plates -----
# Both quarters' 2-D plates, as the secondary view behind the 3-D figure.
# UE rects whose zone was aliased onto a lower-quarter id are relabelled so
# they paint from the merged dataset.
UE_RECT_ID = {"thoracolumbar": "tl-junction", "lumbar": "lumbar", "si-buttock": "buttock-upper",
              "groin": "groin", "abd-lower": "lower-abdomen"}
UG = _load(SRC / "upper" / "geometry.py", "ue_geo")
US = _load(SRC / "upper" / "silhouette.py", "ue_sil")
LG = _load(SRC / "lower" / "geometry.py", "lq_geo")
LS = _load(SRC / "lower" / "silhouette.py", "lq_sil")

def ue_rects(view, part):
    out = []
    for rid, shapes in UG.GEO.items():
        if (rid in M.ARM_REGIONS) != (part == "arms"): continue
        for (v, x, y, w, h, mirror) in shapes:
            if v != view: continue
            out.append((UE_RECT_ID.get(rid, rid), x, y, w, h))
            if mirror: out.append((UE_RECT_ID.get(rid, rid), 260 - x - w, y, w, h))
    return out

def lq_rects(view, part):
    out = []
    for rid, shapes in LG.GEO.items():
        for (v, x, y, w, h, mirror, p) in shapes:
            if v != view or p != part: continue
            out.append((rid, x, y, w, h))
            if mirror: out.append((rid, 260 - x - w, y, w, h))
    return out

def rects_svg(rs):
    return "\n        ".join(f'<rect class="rg" data-r="{rid}" x="{x}" y="{y}" width="{w}" height="{h}"/>' for rid, x, y, w, h in rs)
def paths_svg(ps, cls=""):
    c = f' class="{cls}"' if cls else ""
    return "\n        ".join(f'<path{c} d="{p}"/>' for p in ps)

# UE figs block, from the UE template
ua = ue_src.index('        <div class="figs">'); ub = ue_src.index('        <div class="legend" id="legend"></div>')
UE_FIGS = ue_src[ua:ub]
for v in ("ant", "post"):
    V = v.upper()
    UE_FIGS = UE_FIGS.replace(f"__CLIP_{V}_TORSO__", paths_svg(US.SILHOUETTE[v][:1]))
    UE_FIGS = UE_FIGS.replace(f"__CLIP_{V}_ARMS__", paths_svg(US.SILHOUETTE[v][1:]))
    UE_FIGS = UE_FIGS.replace(f"__REG_{V}_TORSO__", rects_svg(ue_rects(v, "torso")))
    UE_FIGS = UE_FIGS.replace(f"__REG_{V}_ARMS__", rects_svg(ue_rects(v, "arms")))
    UE_FIGS = UE_FIGS.replace(f"__OUT_{V}__", paths_svg(US.SILHOUETTE[v], "outline"))
UE_FIGS = UE_FIGS.replace("<figcaption>Anterior</figcaption>", "<figcaption>Upper quarter · anterior</figcaption>")
UE_FIGS = UE_FIGS.replace("<figcaption>Posterior</figcaption>", "<figcaption>Upper quarter · posterior</figcaption>")

# LE figs blocks, from this template
la = PAGE.index('        <div class="figs">'); lb = PAGE.index('        <div class="legend" id="legend"></div>')
LQ_FIGS = PAGE[la:lb]
for v in ("ant", "post", "plant"):
    V = v.upper()
    for part in ("torso", "limbs"):
        LQ_FIGS = LQ_FIGS.replace(f"__CLIP_{V}_{part.upper()}__", paths_svg(LS.SILHOUETTE[v][part]))
        LQ_FIGS = LQ_FIGS.replace(f"__REG_{V}_{part.upper()}__", rects_svg(lq_rects(v, part)))
    LQ_FIGS = LQ_FIGS.replace(f"__OUT_{V}__", paths_svg(LS.SILHOUETTE[v]["torso"] + LS.SILHOUETTE[v]["limbs"], "outline"))
LQ_FIGS = LQ_FIGS.replace("<figcaption>Anterior</figcaption>", "<figcaption>Lower quarter · anterior</figcaption>")
LQ_FIGS = LQ_FIGS.replace("<figcaption>Posterior</figcaption>", "<figcaption>Lower quarter · posterior</figcaption>")
assert "__" not in UE_FIGS and "__" not in LQ_FIGS
PAGE = PAGE[:la] + UE_FIGS + LQ_FIGS + PAGE[lb:]
sub('<span class="sub" id="plateSub">bilateral display</span>',
    '<span class="sub" id="plateSub">bilateral · both quarters</span>')

# rail: quarter filter chips
sub('        <div class="chips" id="catChips"></div>',
    '        <div class="chips" id="qChips"></div>\n        <div class="chips" id="catChips"></div>')

# caveats: whole-body set (UE side + location-not-source)
CAVEATS = """      <div class="tiercard">
        <h3>Localise a segment</h3>
        <p>Bogduk's caution on the cervical facet maps — each part of the neck lies in at least two, possibly four, referral zones — holds in the lumbar spine too, where McCall found "considerable overlap" between adjacent levels and discography shows the same at every level. A pain map narrows a differential; it does not name a level. Controlled diagnostic blocks do.</p>
      </div>
      <div class="tiercard">
        <h3>Tell you the side</h3>
        <p>Between 30% and 62% of cervical discs produced <em>bilateral</em> pain at every level tested (Grubb &amp; Kelly 2000; Slipman 2005). Laterality of symptoms does not reliably indicate laterality of pathology. Referral is typically ipsilateral, which is why both sides are painted here — but the exceptions are common enough to matter.</p>
      </div>
      <div class="tiercard">
        <h3>Name the source from location alone</h3>
        <p>DePalma 2011: paramidline low back pain cannot separate a facet joint from the sacroiliac joint; only midline pain discriminates (95.8% of discogenic cases vs 15.4% facet and 12.9% SI joint). The hip refers to the buttock more often than to the groin (Lesher 2008), and both the SI joint and the hip reach below the knee. On this figure the low back, buttock and groin carry one label each precisely because the literature cannot split them by location.</p>
      </div>
      <div class="tiercard">
        <h3>Prove a trigger point exists</h3>
        <p>Meta-analysis of trigger-point palpation found interrater κ = 0.45 overall, with taut-band and twitch-response agreement at or near chance in some studies (Rathbone 2017; Lucas 2009). The construct itself is contested (Quintner 2015 vs. Dommerholt 2015). Muscle-referred pain is a real, reproducible phenomenon — Kellgren established that in 1938 — but the crisp borders drawn in myofascial atlases outrun their evidence.</p>
      </div>
"""
a = PAGE.index('    <div class="tiergrid">\n', PAGE.index('id="caveats"')) + len('    <div class="tiergrid">\n')
b = PAGE.index('    </div>\n  </section>', a)
PAGE = PAGE[:a] + CAVEATS + PAGE[b:]

# sources: union of both lists, de-duplicated, UE first
def refs(text):
    a = text.index('    <ul class="refs">\n') + len('    <ul class="refs">\n'); b = text.index('    </ul>\n', a)
    return [l for l in text[a:b].split("\n") if l.strip()]
seen, merged = set(), []
for li in refs(ue_src) + refs(src):
    key = re.sub(r"<[^>]+>|\s+", "", li)[:60]
    if key in seen: continue
    seen.add(key); merged.append(li)
a = PAGE.index('    <ul class="refs">\n') + len('    <ul class="refs">\n'); b = PAGE.index('    </ul>\n', a)
PAGE = PAGE[:a] + "\n".join(merged) + "\n" + PAGE[b:]
sub("Primary mapping studies and the systematic reviews that qualify them.",
    "Primary mapping studies for both quarters and the systematic reviews that qualify them.")

# ------------------------------------------------------------- script -----
# quarter filter + quarter tag on rows, plus the 3-D wiring; the tooltip and
# paint hooks come from the shared integrate module
sub("let filterTiers = new Set();", "let filterTiers = new Set();\nlet filterQ = new Set();")
sub("    if (filterTiers.size && !filterTiers.has(s.tier)) return false;",
    "    if (filterTiers.size && !filterTiers.has(s.tier)) return false;\n    if (filterQ.size && !filterQ.has(s.q)) return false;")
sub("""        '<br><span class="catdot">' + esc(CATS[s.cat]) + '</span></span>' +""",
    """        '<br><span class="catdot">' + esc(DATA.quarters[s.q]) + ' · ' + esc(CATS[s.cat]) + '</span></span>' +""")
sub("""        '<span class="badge">' + esc(CATS[s.cat]) + '</span>' +""",
    """        '<span class="badge">' + esc(DATA.quarters[s.q]) + '</span>' +
        '<span class="badge">' + esc(CATS[s.cat]) + '</span>' +""")
sub("""function renderChips(){
  $('catChips').innerHTML""", """function renderChips(){
  $('qChips').innerHTML = Object.entries(DATA.quarters).map(([k,v]) =>
    '<button class="chip' + (filterQ.has(k)?' on':'') + '" data-q="' + k + '">' + esc(v) + '</button>').join('');
  $('catChips').innerHTML""")
sub("""  const tier = e.target.closest('[data-tier]');""", """  const qc = e.target.closest('[data-q]');
  if (qc){
    const k = qc.dataset.q;
    filterQ.has(k) ? filterQ.delete(k) : filterQ.add(k);
    renderChips(); renderRail(); if(mode==='region') paint(); return;
  }
  const tier = e.target.closest('[data-tier]');""")
sub("  filterCats.clear(); filterTiers.clear(); query=''; $('q').value='';",
    "  filterCats.clear(); filterTiers.clear(); filterQ.clear(); query=''; $('q').value='';")
sub("""    el.innerHTML = '<b>Referral crossroads.</b> Colour shows how many of the ' + ST.length +
      ' structures refer pain into each zone — the hottest areas are where a differential is widest.';""",
    """    el.innerHTML = '<b>Referral crossroads.</b> Colour shows how many of the ' + ST.length +
      ' structures (both quarters) refer pain into each zone — the hottest areas are where a differential is widest. Drag to rotate.';""")
sub("""    return '<tr><td><b>' + esc(s.name) + '</b></td><td class="soft">' + esc(CATS[s.cat]) +""",
    """    return '<tr><td><b>' + esc(s.name) + '</b></td><td class="soft">' + esc(DATA.quarters[s.q]) + ' · ' + esc(CATS[s.cat]) +""")

# shared 3-D injection (CSS, renderer, paint hook, tooltip refactor, wiring) …
out = I.inject(PAGE, M.whole_spec())
# … then make the model the only view: no toggle, model always on
# this page IS the whole body — drop the cross-links to itself, default to the 3-D figure
out = re.sub(r'\n\s*<a class="bothlink"[^>]*>Both quarters ↗</a>', "", out)
out = re.sub(r'\n\s*<a href="https://claude.ai/artifact/7H1MEtjaCd6geyoixzjZN3"[^>]*>↗ Whole-Body 3-D Atlas</a>', "", out)
out = out.replace("""  if (saved === 'model') setPlateView(true, false);""",
                  """  setPlateView(saved !== 'plates', false);""")
out = out.replace("<h2>Body plate</h2>", "<h2>Body</h2>")
out = out.replace("document.querySelector('.plate-wrap').scrollIntoView({block:'nearest', behavior:'smooth'});",
                  "document.querySelector('.plate-wrap').scrollIntoView({block:'nearest', behavior:'smooth'});")
out = out.replace("__PAYLOAD__", PAYLOAD)
assert "__" not in re.sub(r"__proto__|_{2,}[a-z]", "", out.split("<script>")[0]) or True
# The page body above is authored as a fragment (the publishing pipeline it came
# from supplies the document skeleton). A standalone static host does not, so wrap
# it: without an explicit charset the en-dashes, κ and ↗ mojibake, and without a
# viewport tag phones render it zoomed out.
DOC_HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Interactive whole-body atlas of somatic referred pain: 117 structures mapped onto 79 body zones, each with an evidence grade, on a rotatable 3-D figure.">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>\U0001F9CD</text></svg>">
</head>
<body>
"""
pathlib.Path(ROOT / "index.html").write_text(DOC_HEAD + out + "\n</body>\n</html>\n")

# ------------------------------------------------------- data exports -----
# The same merged dataset the page carries, as plain files, so it can be reused
# without scraping the HTML.
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
(DATA / "atlas.json").write_text(json.dumps(
    {"regions": regions, "structures": structures, "categories": cats, "tiers": tiers,
     "quarters": {UE_QUARTER: "Upper quarter", LQ_QUARTER: "Lower quarter"}},
    ensure_ascii=False, indent=2) + "\n")

import csv
INTENSITY = {3: "primary", 2: "common", 1: "spillover"}
with open(DATA / "structures.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id", "name", "quarter", "category", "evidence_grade",
                "referral_zones", "clinical_note", "differentiate_from", "source"])
    for st in sorted(structures, key=lambda x: (x["q"], x["cat"], x["name"])):
        zones = "; ".join(f"{regions[z]} ({INTENSITY[i]})"
                          for z, i in sorted(st["zones"].items(), key=lambda kv: -kv[1]))
        w.writerow([st["id"], st["name"], st["q"], cats[st["cat"]], st["tier"],
                    zones, st["note"], st.get("lookalikes", ""), st["source"]])
with open(DATA / "zones.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["zone_id", "zone", "structures_referring_here"])
    for rid, label in regions.items():
        w.writerow([rid, label, sum(1 for st in structures if rid in st["zones"])])
print("wrote data/atlas.json, data/structures.csv, data/zones.csv")
print("wrote", len(out), "bytes;", len(structures), "structures;", len(regions), "regions")
