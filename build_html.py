# -*- coding: utf-8 -*-
import json, html
import referral_data as D
import silhouette as SIL
from geometry import GEO

MID_W = 260

def shapes_for(view, part):
    out = []
    for rid, shapes in GEO.items():
        for (v, x, y, w, h, mirror, p) in shapes:
            if v != view or p != part:
                continue
            out.append((rid, x, y, w, h))
            if mirror:
                out.append((rid, MID_W - x - w, y, w, h))
    return out

def region_svg(view, part):
    return "\n        ".join(
        f'<rect class="rg" data-r="{rid}" x="{x}" y="{y}" width="{w}" height="{h}"/>'
        for rid, x, y, w, h in shapes_for(view, part))

def clip_svg(view, part):
    return "\n        ".join(f'<path d="{p}"/>' for p in SIL.SILHOUETTE[view][part])

def outline_svg(view):
    parts = SIL.SILHOUETTE[view]["torso"] + SIL.SILHOUETTE[view]["limbs"]
    return "\n        ".join(f'<path class="outline" d="{p}"/>' for p in parts)

# ---------------------------------------------------------------- payload ----
regions_payload = {rid: label for rid, label in D.REGIONS}
structures_payload = D.S
cats_payload = dict(D.CATEGORIES)
tiers_payload = D.TIERS

PAYLOAD = json.dumps({
    "regions": regions_payload,
    "structures": structures_payload,
    "cats": cats_payload,
    "tiers": tiers_payload,
}, ensure_ascii=False, separators=(",", ":"))

# ---------------------------------------------------------------- page -------
PAGE = """<title>LE Referred Pain Atlas</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600;8..60,700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">

<style>
:root{
  --paper:#F1F3EF;
  --surface:#FFFFFF;
  --surface-2:#E9ECE5;
  --surface-3:#DFE4DA;
  --ink:#1B231F;
  --ink-soft:#4B564F;
  --ink-faint:#7C877E;
  --line:#D8DDD3;
  --line-strong:#BCC4B7;
  --accent:#1F6F63;
  --accent-ink:#0E3F38;
  --accent-soft:#DCEAE5;

  /* heat ramp — single warm hue, ordinal, validated light-mode */
  --heat-1:#E89272;
  --heat-2:#D85B3F;
  --heat-3:#A31C14;
  --heat-0:#E4E8E0;      /* no referral */
  --heat-1-ink:#5E2B18;
  --heat-3-ink:#FFFFFF;

  --shadow:0 1px 2px rgba(20,30,24,.07),0 8px 24px -10px rgba(20,30,24,.22);
  --radius:10px;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --paper:#121915; --surface:#1A2420; --surface-2:#212C27; --surface-3:#293530;
    --ink:#E7ECE6; --ink-soft:#AAB6AC; --ink-faint:#79877D;
    --line:#2B3630; --line-strong:#3C4A43;
    --accent:#57C4AC; --accent-ink:#BEEBE0; --accent-soft:#1E3833;
    --heat-1:#93412C; --heat-2:#CB5D40; --heat-3:#F49877;
    --heat-0:#232E29;
    --heat-1-ink:#F3D6CA; --heat-3-ink:#2A1008;
    --shadow:0 1px 2px rgba(0,0,0,.35),0 8px 24px -10px rgba(0,0,0,.5);
  }
}
:root[data-theme="dark"]{
  --paper:#121915; --surface:#1A2420; --surface-2:#212C27; --surface-3:#293530;
  --ink:#E7ECE6; --ink-soft:#AAB6AC; --ink-faint:#79877D;
  --line:#2B3630; --line-strong:#3C4A43;
  --accent:#57C4AC; --accent-ink:#BEEBE0; --accent-soft:#1E3833;
  --heat-1:#93412C; --heat-2:#CB5D40; --heat-3:#F49877;
  --heat-0:#232E29;
  --heat-1-ink:#F3D6CA; --heat-3-ink:#2A1008;
  --shadow:0 1px 2px rgba(0,0,0,.35),0 8px 24px -10px rgba(0,0,0,.5);
}

*{box-sizing:border-box}
body{
  margin:0;background:var(--paper);color:var(--ink);
  font-family:"IBM Plex Sans",ui-sans-serif,system-ui,sans-serif;
  font-size:15px;line-height:1.55;
}
h1,h2,h3{font-family:"Source Serif 4",ui-serif,Georgia,serif;font-weight:600;margin:0;text-wrap:balance}
.mono{font-family:"IBM Plex Mono",ui-monospace,monospace;font-variant-numeric:tabular-nums}
::selection{background:var(--accent-soft);color:var(--accent-ink)}
:is(a,button,input,select,summary,[tabindex]):focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:4px}
button{font:inherit;color:inherit;background:none;border:none;cursor:pointer}

/* ---------- header ---------- */
header.top{position:sticky;top:0;z-index:60;background:color-mix(in srgb,var(--paper) 93%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.top-in{max-width:1400px;margin:0 auto;padding:13px 22px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.brand{display:flex;align-items:baseline;gap:10px;margin-right:auto}
.brand .mark{font-family:"IBM Plex Mono";font-weight:600;font-size:11px;letter-spacing:.08em;color:var(--accent-ink);background:var(--accent-soft);border-radius:5px;padding:2px 7px}
.brand h1{font-size:18px}
.top-actions{display:flex;gap:6px;align-items:center}
.btn{font-size:12.5px;font-weight:500;padding:7px 13px;border-radius:8px;border:1px solid var(--line);background:var(--surface);color:var(--ink-soft)}
.btn:hover{background:var(--surface-2);color:var(--ink)}
.btn.on{background:var(--accent-soft);border-color:var(--accent);color:var(--accent-ink);font-weight:600}

/* ---------- layout ---------- */
main{max-width:1400px;margin:0 auto;padding:22px 22px 70px}
.lede{max-width:70ch;color:var(--ink-soft);font-size:14.5px;margin:0 0 20px}
.lede strong{color:var(--ink);font-weight:600}
.siblings{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 20px}
.siblings a{font-size:12px;padding:5px 11px;border-radius:100px;border:1px solid var(--line);background:var(--surface);color:var(--ink-soft);text-decoration:none}
.siblings a:hover{background:var(--surface-2);color:var(--ink)}

.workspace{display:grid;grid-template-columns:minmax(430px,1.05fr) minmax(360px,1fr);gap:20px;align-items:start}
@media (max-width:1000px){.workspace{grid-template-columns:1fr}}

.panel{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow)}
.panel-head{display:flex;align-items:center;gap:10px;padding:13px 16px;border-bottom:1px solid var(--line);flex-wrap:wrap}
.panel-head h2{font-size:15.5px}
.panel-head .sub{font-size:11.5px;color:var(--ink-faint);font-family:"IBM Plex Mono";letter-spacing:.04em;margin-left:auto}

/* ---------- plate ---------- */
.plate-wrap{position:sticky;top:74px}
.plate-mode{padding:11px 16px;border-bottom:1px solid var(--line);background:var(--surface-2);font-size:12.5px;color:var(--ink-soft);display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}
.plate-mode b{color:var(--ink);font-weight:600}
.figs{display:grid;grid-template-columns:1fr 1fr;gap:4px;padding:10px 8px 4px}
.figs.plantar{grid-template-columns:1fr;padding:0 8px 6px}
.figs.plantar .fig svg{max-height:20vh}
.fig{display:flex;flex-direction:column;align-items:center;gap:5px}
.fig svg{width:100%;height:auto;max-height:52vh;display:block}
.fig figcaption{font-family:"IBM Plex Mono";font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-faint)}

.rg{fill:var(--heat-0);stroke:var(--paper);stroke-width:.5;stroke-opacity:.5;transition:fill .18s ease;cursor:pointer}
.rg.h1{fill:var(--heat-1)} .rg.h2{fill:var(--heat-2)} .rg.h3{fill:var(--heat-3)}
.rg.hovered{stroke:var(--ink);stroke-width:1.6;paint-order:stroke}
.rg.picked{stroke:var(--accent);stroke-width:2.4;paint-order:stroke}
@media (prefers-reduced-motion:reduce){.rg{transition:none}}
.outline{fill:none;stroke:var(--line-strong);stroke-width:2.8;pointer-events:none}
.divider{stroke:var(--paper);stroke-width:.9;fill:none;pointer-events:none;opacity:.55}

.legend{display:flex;align-items:center;gap:14px;padding:10px 16px 13px;border-top:1px solid var(--line);flex-wrap:wrap}
.legend .swatches{display:flex;align-items:center;gap:2px}
.legend .sw{width:34px;height:13px;border-radius:2px}
.legend .lbl{font-family:"IBM Plex Mono";font-size:10.5px;color:var(--ink-faint);letter-spacing:.04em}
.legend .cap{font-size:11.5px;color:var(--ink-soft)}

/* ---------- rail ---------- */
.controls{padding:12px 16px;border-bottom:1px solid var(--line);display:flex;flex-direction:column;gap:9px}
.search-wrap{position:relative}
.search-wrap input{width:100%;font:inherit;font-size:13.5px;padding:8px 12px 8px 31px;border-radius:8px;border:1px solid var(--line);background:var(--paper);color:var(--ink)}
.search-wrap svg{position:absolute;left:9px;top:50%;transform:translateY(-50%);opacity:.5}
.chips{display:flex;gap:5px;flex-wrap:wrap}
.chip{font-size:11.5px;font-weight:500;padding:4px 10px;border-radius:100px;border:1px solid var(--line);color:var(--ink-soft);background:var(--surface)}
.chip:hover{background:var(--surface-2)}
.chip.on{background:var(--accent-soft);border-color:var(--accent);color:var(--accent-ink);font-weight:600}

.rail-body{max-height:min(1000px,74vh);overflow-y:auto}
.slist{list-style:none;margin:0;padding:0}
.slist li{border-bottom:1px solid var(--line)}
.slist li:last-child{border-bottom:none}
.srow{width:100%;text-align:left;padding:11px 16px;display:flex;gap:10px;align-items:flex-start}
.srow:hover{background:var(--surface-2)}
.srow.on{background:var(--accent-soft)}
.srow .nm{font-size:13.6px;font-weight:500;flex:1;line-height:1.4}
.srow .meta{display:flex;gap:6px;align-items:center;flex-shrink:0;padding-top:1px}
.intens{font-family:"IBM Plex Mono";font-size:10px;font-weight:600;padding:2px 6px;border-radius:4px;white-space:nowrap}
.intens.i3{background:var(--heat-3);color:var(--heat-3-ink)}
.intens.i2{background:var(--heat-2);color:#fff}
.intens.i1{background:var(--heat-1);color:var(--heat-1-ink)}
.tier{font-family:"IBM Plex Mono";font-size:10px;font-weight:600;width:17px;height:17px;display:inline-flex;align-items:center;justify-content:center;border-radius:4px;flex-shrink:0}
.tier.tA{background:var(--ink);color:var(--paper)}
.tier.tB{background:var(--surface-3);color:var(--ink);border:1px solid var(--line-strong)}
.tier.tC{background:transparent;color:var(--ink-faint);border:1px dashed var(--line-strong)}
.catdot{font-family:"IBM Plex Mono";font-size:9.5px;color:var(--ink-faint);letter-spacing:.05em;text-transform:uppercase}

.empty{padding:26px 16px;color:var(--ink-faint);font-size:13px;text-align:center}

/* ---------- detail ---------- */
.detail{padding:15px 16px 18px;display:flex;flex-direction:column;gap:12px}
.detail h3{font-size:18px}
.detail .dmeta{display:flex;gap:7px;align-items:center;flex-wrap:wrap}
.detail .badge{font-size:11px;font-weight:600;padding:3px 9px;border-radius:100px;background:var(--surface-2);color:var(--ink-soft);border:1px solid var(--line)}
.dblock{display:flex;flex-direction:column;gap:4px}
.dblock .k{font-family:"IBM Plex Mono";font-size:10px;text-transform:uppercase;letter-spacing:.07em;color:var(--ink-faint)}
.dblock .v{font-size:13.4px;color:var(--ink);line-height:1.6}
.dblock .v.soft{color:var(--ink-soft)}
.zlist{display:flex;flex-direction:column;gap:4px;margin:0;padding:0;list-style:none}
.zlist li{display:flex;gap:9px;align-items:center;font-size:13px}
.zbar{width:6px;height:16px;border-radius:2px;flex-shrink:0}
.zbar.i3{background:var(--heat-3)} .zbar.i2{background:var(--heat-2)} .zbar.i1{background:var(--heat-1)}
.backbtn{align-self:flex-start;font-size:12.5px;color:var(--accent-ink);font-weight:600;padding:5px 11px;border-radius:7px;background:var(--accent-soft)}
.warnbox{background:var(--surface-2);border:1px solid var(--line);border-left:3px solid var(--heat-2);border-radius:7px;padding:10px 12px;font-size:12.6px;color:var(--ink-soft);line-height:1.55}

/* ---------- tooltip ---------- */
#tip{position:fixed;z-index:200;pointer-events:none;background:var(--ink);color:var(--paper);font-size:12px;padding:6px 10px;border-radius:6px;opacity:0;transition:opacity .12s;max-width:250px;line-height:1.45}
#tip.on{opacity:1}
#tip .tt{font-family:"IBM Plex Mono";font-size:10px;opacity:.75;letter-spacing:.05em;display:block}

/* ---------- table view ---------- */
#tableView{display:none;margin-top:22px}
#tableView.on{display:block}
.table-scroll{overflow-x:auto}
table{border-collapse:collapse;width:100%;min-width:900px}
thead th{position:sticky;top:0;text-align:left;font-family:"IBM Plex Mono";font-weight:600;font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-faint);background:var(--surface-2);padding:10px 13px;border-bottom:1px solid var(--line);white-space:nowrap}
tbody td{padding:11px 13px;border-bottom:1px solid var(--line);vertical-align:top;font-size:13px}
tbody tr:hover{background:var(--surface-2)}
tbody td.soft{color:var(--ink-soft)}

/* ---------- sections ---------- */
section.doc{margin-top:52px;scroll-margin-top:80px}
section.doc h2{font-size:23px;margin-bottom:5px}
section.doc .note{color:var(--ink-soft);font-size:14px;max-width:74ch;margin-bottom:16px}
.tiergrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:13px}
.tiercard{background:var(--surface);border:1px solid var(--line);border-radius:9px;padding:14px 15px;display:flex;flex-direction:column;gap:7px}
.tiercard .th{display:flex;align-items:center;gap:8px}
.tiercard h3{font-size:14.5px}
.tiercard p{margin:0;font-size:12.8px;color:var(--ink-soft);line-height:1.55}
.refs{columns:2;column-gap:38px;font-size:12.8px;color:var(--ink-soft);list-style:none;padding:0}
@media (max-width:700px){.refs{columns:1}}
.refs li{break-inside:avoid;margin-bottom:9px;padding-left:13px;text-indent:-13px}
.refs a{color:var(--ink-soft);text-decoration-color:var(--line-strong)}
.refs a:hover{color:var(--accent-ink)}
footer{border-top:1px solid var(--line);margin-top:58px;padding:24px 22px 56px;color:var(--ink-faint);font-size:12px}
footer .fi{max-width:1400px;margin:0 auto;max-width:80ch}
</style>

<header class="top">
  <div class="top-in">
    <div class="brand"><span class="mark">SOMATIC · LQ</span><h1>LE Referred Pain Atlas</h1></div>
    <div class="top-actions">
      <button class="btn" id="resetBtn">Reset</button>
      <button class="btn" id="tableBtn">Table view</button>
    </div>
  </div>
</header>

<main>
  <p class="lede">Where <strong>somatic structures of the lumbar spine, pelvis and lower limb</strong> send their pain. Click a structure to light its referral zones, or click anywhere on the body to see every structure that refers there, ranked. Every entry carries an <strong>evidence grade</strong> — the maps are not all built on equal ground, and the difference matters more than the pictures suggest.</p>

  <div class="siblings">
    <a href="https://claude.ai/code/artifact/084e13e2-762d-4459-b104-51f72a49ea22" target="_blank" rel="noopener">↗ Lumbosacral Root Atlas</a>
    <a href="https://claude.ai/code/artifact/adc45a60-1e27-4dfe-949d-410510ba9da2" target="_blank" rel="noopener">↗ Lower Quarter Differential</a>
    <a href="https://claude.ai/artifact/7H1MEtjaCd6geyoixzjZN3" target="_blank" rel="noopener">↗ Whole-Body 3-D Atlas</a>
  </div>

  <div class="workspace">

    <!-- ============ PLATE ============ -->
    <div class="plate-wrap">
      <div class="panel">
        <div class="panel-head">
          <h2>Body plate</h2>
          <span class="sub" id="plateSub">bilateral display</span>
        </div>
        <div class="plate-mode" id="plateMode"></div>
        <div class="figs">
          <figure class="fig">
            <svg viewBox="0 0 260 520" role="img" aria-label="Anterior lower-quarter heat map">
              <defs>
                <clipPath id="c-ant-t">__CLIP_ANT_TORSO__</clipPath>
                <clipPath id="c-ant-l">__CLIP_ANT_LIMBS__</clipPath>
              </defs>
              __OUT_ANT__
              <g clip-path="url(#c-ant-t)">__REG_ANT_TORSO__</g>
              <g clip-path="url(#c-ant-l)">__REG_ANT_LIMBS__</g>
            </svg>
            <figcaption>Anterior</figcaption>
          </figure>
          <figure class="fig">
            <svg viewBox="0 0 260 520" role="img" aria-label="Posterior lower-quarter heat map">
              <defs>
                <clipPath id="c-post-t">__CLIP_POST_TORSO__</clipPath>
                <clipPath id="c-post-l">__CLIP_POST_LIMBS__</clipPath>
              </defs>
              __OUT_POST__
              <g clip-path="url(#c-post-t)">__REG_POST_TORSO__</g>
              <g clip-path="url(#c-post-l)">__REG_POST_LIMBS__</g>
            </svg>
            <figcaption>Posterior</figcaption>
          </figure>
        </div>
        <div class="figs plantar">
          <figure class="fig">
            <svg viewBox="0 0 260 210" role="img" aria-label="Plantar heat map">
              <defs><clipPath id="c-plant-l">__CLIP_PLANT_LIMBS__</clipPath></defs>
              __OUT_PLANT__
              <g clip-path="url(#c-plant-l)">__REG_PLANT_LIMBS__</g>
            </svg>
            <figcaption>Plantar — soles, toes up</figcaption>
          </figure>
        </div>
        <div class="legend" id="legend"></div>
      </div>
    </div>

    <!-- ============ RAIL ============ -->
    <div class="panel">
      <div class="panel-head">
        <h2 id="railTitle">Structures</h2>
        <span class="sub" id="railCount"></span>
      </div>
      <div class="controls" id="controls">
        <div class="search-wrap">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input id="q" type="text" placeholder="Search structures, zones, clinical notes…" autocomplete="off">
        </div>
        <div class="chips" id="catChips"></div>
        <div class="chips" id="tierChips"></div>
      </div>
      <div class="rail-body" id="railBody"></div>
    </div>
  </div>

  <!-- ============ TABLE VIEW ============ -->
  <div id="tableView">
    <div class="panel">
      <div class="panel-head"><h2>Full data table</h2><span class="sub">every structure &amp; zone</span></div>
      <div class="table-scroll">
        <table>
          <thead><tr><th>Structure</th><th>Category</th><th>Grade</th><th>Referral zones (3 = primary, 2 = common, 1 = spillover)</th><th>Clinical note</th></tr></thead>
          <tbody id="tbody"></tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- ============ EVIDENCE ============ -->
  <section class="doc" id="evidence">
    <h2>How to read the evidence grades</h2>
    <p class="note">Referred-pain maps circulate as if they were all the same kind of fact. They are not. These three grades separate zones that were <em>caused</em> under controlled conditions from zones that were <em>observed</em> in clinic — a distinction that governs how much weight any single map should carry.</p>
    <div class="tiergrid" id="tierGrid"></div>
  </section>

  <!-- ============ CAVEATS ============ -->
  <section class="doc" id="caveats">
    <h2>Four things this atlas cannot do</h2>
    <p class="note">These limitations are documented in the source literature itself, not imported criticism. Reading the maps without them produces false confidence.</p>
    <div class="tiergrid">
      <div class="tiercard">
        <h3>Localise a segment</h3>
        <p>McCall's volunteer maps showed "considerable overlap" between adjacent lumbar facet levels, and provocation discography shows the same: adjacent discs produce overlapping patterns, and pain extending below the knee tracks the grade of annular disruption rather than the level. A pain map narrows a differential; it does not name a level. Controlled diagnostic blocks do.</p>
      </div>
      <div class="tiercard">
        <h3>Name the source from location alone</h3>
        <p>DePalma 2011: paramidline low back pain cannot separate a facet joint from the sacroiliac joint. The one location finding with real discriminating value is midline pain — present in 95.8% of confirmed discogenic cases against 15.4% of facet and 12.9% of SI joint cases. Everything else on these maps overlaps.</p>
      </div>
      <div class="tiercard">
        <h3>Tell you how far down the leg it goes</h3>
        <p>Whether facet pain reaches below the knee is contested — where it did (Mooney &amp; Robertson, 3 of 20), large-volume injectate is now blamed. The sacroiliac joint DOES reach below the knee in roughly a quarter to a half of confirmed cases (Slipman 2000), and the hip refers distal to the knee in 22% (Lesher 2008). "It stays above the knee" is not a safe rule for any of them.</p>
      </div>
      <div class="tiercard">
        <h3>Prove a trigger point exists</h3>
        <p>Meta-analysis of trigger-point palpation found interrater κ = 0.45 overall, with taut-band and twitch-response agreement at or near chance in some studies (Rathbone 2017; Lucas 2009). The construct itself is contested (Quintner 2015 vs. Dommerholt 2015). Muscle-referred pain is a real, reproducible phenomenon — Kellgren established that in 1938 — but the crisp borders drawn in myofascial atlases outrun their evidence.</p>
      </div>
    </div>
  </section>

  <!-- ============ SOURCES ============ -->
  <section class="doc" id="sources">
    <h2>Sources</h2>
    <p class="note">Primary mapping studies and the systematic reviews that qualify them.</p>
    <ul class="refs">
      <li>Mooney V, Robertson J. The facet syndrome. <em>Clin Orthop Relat Res</em> 1976;(115):149-56.</li>
      <li>McCall IW, Park WM, O'Brien JP. Induced pain referral from posterior lumbar elements in normal subjects. <em>Spine</em> 1979;4(5):441-6.</li>
      <li><a href="https://pubmed.ncbi.nlm.nih.gov/9430810/" target="_blank" rel="noopener">Fukui S, Ohseto K, Shiotani M, et al. Distribution of referred pain from the lumbar zygapophyseal joints and dorsal rami. <em>Clin J Pain</em> 1997;13(4):303-7.</a></li>
      <li>Marks R. Distribution of pain provoked from lumbar facet joints and related structures during diagnostic spinal infiltration. <em>Pain</em> 1989;39(1):37-40.</li>
      <li>Fortin JD, Dwyer AP, West S, Pier J. Sacroiliac joint: pain referral maps upon applying a new injection/arthrography technique. Part I: asymptomatic volunteers. <em>Spine</em> 1994;19(13):1475-82.</li>
      <li>Fortin JD, Aprill CN, Ponthieux B, Pier J. Sacroiliac joint: pain referral maps upon applying a new injection/arthrography technique. Part II: clinical evaluation. <em>Spine</em> 1994;19(13):1483-9.</li>
      <li>Slipman CW, Jackson HB, Lipetz JS, et al. Sacroiliac joint pain referral zones. <em>Arch Phys Med Rehabil</em> 2000;81(3):334-8.</li>
      <li>Laslett M, Aprill CN, McDonald B, Young SB. Diagnosis of sacroiliac joint pain: validity of individual provocation tests and composites of tests. <em>Man Ther</em> 2005;10(3):207-18.</li>
      <li>Lesher JM, Dreyfuss P, Hager N, Kaplan M, Furman M. Hip joint pain referral patterns: a descriptive study. <em>Pain Med</em> 2008;9(1):22-5.</li>
      <li>DePalma MJ, Ketchum JM, Trussell BS, Saullo TR, Slipman CW. Does the location of low back pain predict its source? <em>PM&amp;R</em> 2011;3(1):33-9.</li>
      <li>Ohnmeiss DD, Vanharanta H, Ekholm J. Degree of disc disruption and lower extremity pain. <em>Spine</em> 1997;22(14):1600-5.</li>
      <li>Ohnmeiss DD, Vanharanta H, Ekholm J. Relation between pain location and disc pathology: a study of pain drawings and CT/discography. <em>Clin J Pain</em> 1999;15(3):210-7.</li>
      <li>Carragee EJ, Tanner CM, Khurana S, et al. The rates of false-positive lumbar discography in select patients without low back symptoms. <em>Spine</em> 2000;25(11):1373-80.</li>
      <li>Suri P, Rainville J, Katz JN, et al. The accuracy of the physical examination for the diagnosis of midlumbar and low lumbar nerve root impingement. <em>Spine</em> 2011;36(1):63-73.</li>
      <li>Kellgren JH. Observations on referred pain arising from muscle. <em>Clin Sci</em> 1938;3:175-90.</li>
      <li>Kellgren JH. On the distribution of pain arising from deep somatic structures. <em>Clin Sci</em> 1939;4:35-46.</li>
      <li>Feinstein B, Langton JNK, Jameson RM, Schiller F. Experiments on pain referred from deep somatic tissues. <em>J Bone Joint Surg</em> 1954;36-A:981-97.</li>
      <li>Travell JG, Simons DG. <em>Myofascial Pain and Dysfunction: The Trigger Point Manual, Vol. 2 — The Lower Extremities.</em> Williams &amp; Wilkins, 1992.</li>
      <li><a href="https://pubmed.ncbi.nlm.nih.gov/19158550/" target="_blank" rel="noopener">Lucas N, et al. Reliability of physical examination for diagnosis of myofascial trigger points. <em>Clin J Pain</em> 2009.</a></li>
      <li><a href="https://pubmed.ncbi.nlm.nih.gov/28098584/" target="_blank" rel="noopener">Rathbone ATL, Grosman-Rimon L, Kumbhare DA. Interrater agreement of manual palpation for identification of myofascial trigger points. <em>Clin J Pain</em> 2017.</a></li>
      <li><a href="https://academic.oup.com/rheumatology/article-abstract/54/3/392/1796114" target="_blank" rel="noopener">Quintner JL, Bove GM, Cohen ML. A critical evaluation of the trigger point phenomenon. <em>Rheumatology</em> 2015;54(3):392-9.</a></li>
    </ul>
  </section>
</main>

<div id="tip" role="status" aria-live="polite"></div>

<footer><div class="fi">An educational anatomy and clinical-reasoning reference. Referred-pain maps narrow a differential; they do not establish a diagnosis. Where the literature disagrees or the evidence is thin, this atlas says so rather than smoothing it over — check the grade before you lean on a pattern.</div></footer>

<script>
const DATA = __PAYLOAD__;
const R = DATA.regions, ST = DATA.structures, CATS = DATA.cats, TIERS = DATA.tiers;

// density: how many structures refer to each region (weighted by intensity)
const DENSITY = {};
Object.keys(R).forEach(k => DENSITY[k] = 0);
ST.forEach(s => Object.keys(s.zones).forEach(z => DENSITY[z] += 1));
const DMAX = Math.max(...Object.values(DENSITY));
// rank-band the density so the default plate actually discriminates:
// hottest third = 3, middle third = 2, remainder with any referral = 1
const DENSITY_BAND = (() => {
  const live = Object.keys(DENSITY).filter(k => DENSITY[k] > 0)
                     .sort((a,b) => DENSITY[b] - DENSITY[a]);
  const band = {};
  Object.keys(DENSITY).forEach(k => band[k] = 0);
  live.forEach((k,i) => { band[k] = i < live.length/3 ? 3 : i < 2*live.length/3 ? 2 : 1; });
  return band;
})();

let mode = 'density';        // 'density' | 'structure' | 'region'
let activeStruct = null;
let activeRegion = null;
let filterCats = new Set();
let filterTiers = new Set();
let query = '';

const $ = id => document.getElementById(id);
const rects = Array.from(document.querySelectorAll('.rg'));
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

/* ---------------- painting ---------------- */
function paint(){
  let map = {}, capt = '';
  if (mode === 'structure' && activeStruct){
    map = activeStruct.zones;
    capt = 'Referral intensity';
  } else if (mode === 'region' && activeRegion){
    map = {};
    matching().forEach(s => { if (s.zones[activeRegion]) map[activeRegion] = 3; });
    capt = 'Selected zone';
  } else {
    map = DENSITY_BAND;
    capt = 'Referral density';
  }
  rects.forEach(el => {
    const v = map[el.dataset.r] || 0;
    el.classList.remove('h1','h2','h3','picked');
    if (v) el.classList.add('h' + v);
    if (mode === 'region' && el.dataset.r === activeRegion) el.classList.add('picked');
  });
  renderLegend(capt);
  renderPlateMode();
}

function renderLegend(capt){
  if (mode === 'region'){
    // the plate is showing one picked zone, not a ramp — the ramp lives in the list
    $('legend').innerHTML =
      '<span class="cap"><b>Zone selected</b></span>' +
      '<span class="lbl">structures at right, ranked by referral intensity then evidence grade</span>';
    return;
  }
  const labels = mode === 'density' ? ['few','several','many'] : ['spillover','common','primary'];
  $('legend').innerHTML =
    '<span class="cap"><b>' + esc(capt) + '</b></span>' +
    '<span class="swatches">' +
      '<span class="sw" style="background:var(--heat-1)"></span>' +
      '<span class="sw" style="background:var(--heat-2)"></span>' +
      '<span class="sw" style="background:var(--heat-3)"></span>' +
    '</span>' +
    '<span class="lbl">' + labels.join(' &nbsp;·&nbsp; ') + '</span>';
}

function renderPlateMode(){
  const el = $('plateMode');
  if (mode === 'structure' && activeStruct){
    el.innerHTML = 'Showing <b>' + esc(activeStruct.name) + '</b> — darkest zones are its primary referral area.';
  } else if (mode === 'region' && activeRegion){
    el.innerHTML = 'Showing every structure that refers to <b>' + esc(R[activeRegion]) + '</b>.';
  } else {
    el.innerHTML = '<b>Referral crossroads.</b> Colour shows how many of the ' + ST.length +
      ' structures refer pain into each zone — the hottest areas are where a differential is widest.';
  }
}

/* ---------------- filtering ---------------- */
function matching(){
  const q = query.trim().toLowerCase();
  return ST.filter(s => {
    if (filterCats.size && !filterCats.has(s.cat)) return false;
    if (filterTiers.size && !filterTiers.has(s.tier)) return false;
    if (!q) return true;
    const hay = (s.name + ' ' + s.note + ' ' + s.source + ' ' + s.lookalikes + ' ' +
      Object.keys(s.zones).map(z => R[z]).join(' ')).toLowerCase();
    return hay.includes(q);
  });
}

/* ---------------- rail ---------------- */
function renderRail(){
  const body = $('railBody');
  if (mode === 'structure' && activeStruct){ renderDetail(activeStruct); return; }

  let list, title, sub;
  if (mode === 'region' && activeRegion){
    list = matching().filter(s => s.zones[activeRegion])
      .sort((a,b) => (b.zones[activeRegion] - a.zones[activeRegion]) ||
                     (a.tier < b.tier ? -1 : a.tier > b.tier ? 1 : 0) ||
                     a.name.localeCompare(b.name));
    title = R[activeRegion];
    sub = list.length + ' structure' + (list.length===1?'':'s') + ' refer here';
  } else {
    list = matching().sort((a,b) => a.cat.localeCompare(b.cat) || a.name.localeCompare(b.name));
    title = 'Structures';
    sub = list.length + ' of ' + ST.length;
  }
  $('railTitle').textContent = title;
  $('railCount').textContent = sub;

  if (!list.length){ body.innerHTML = '<div class="empty">Nothing matches those filters.</div>'; return; }

  const back = (mode === 'region')
    ? '<div style="padding:11px 16px 0"><button class="backbtn" data-back="1">← All structures</button></div>' : '';

  body.innerHTML = back + '<ul class="slist">' + list.map(s => {
    const i = activeRegion && mode==='region' ? s.zones[activeRegion] : null;
    const iLbl = {3:'primary',2:'common',1:'spillover'}[i];
    return '<li><button class="srow" data-s="' + s.id + '">' +
      '<span class="nm">' + esc(s.name) +
        '<br><span class="catdot">' + esc(CATS[s.cat]) + '</span></span>' +
      '<span class="meta">' +
        (i ? '<span class="intens i' + i + '">' + iLbl + '</span>' : '') +
        '<span class="tier t' + s.tier + '" title="Evidence grade ' + s.tier + '">' + s.tier + '</span>' +
      '</span></button></li>';
  }).join('') + '</ul>';
}

function renderDetail(s){
  const zones = Object.entries(s.zones).sort((a,b) => b[1]-a[1]);
  const zl = zones.map(([z,i]) =>
    '<li><span class="zbar i' + i + '"></span><span>' + esc(R[z]) +
    ' <span class="catdot">' + {3:'primary',2:'common',1:'spillover'}[i] + '</span></span></li>').join('');
  $('railTitle').textContent = 'Structure detail';
  $('railCount').textContent = TIERS[s.tier].short + ' grade';
  $('railBody').innerHTML =
    '<div class="detail">' +
      '<button class="backbtn" data-back="1">← All structures</button>' +
      '<h3>' + esc(s.name) + '</h3>' +
      '<div class="dmeta">' +
        '<span class="badge">' + esc(CATS[s.cat]) + '</span>' +
        '<span class="tier t' + s.tier + '">' + s.tier + '</span>' +
        '<span class="badge">' + esc(TIERS[s.tier].label) + '</span>' +
      '</div>' +
      '<div class="dblock"><span class="k">Referral zones</span><ul class="zlist">' + zl + '</ul></div>' +
      '<div class="dblock"><span class="k">Clinical note</span><span class="v">' + esc(s.note) + '</span></div>' +
      (s.lookalikes ? '<div class="warnbox"><b>Differentiate from:</b> ' + esc(s.lookalikes) + '</div>' : '') +
      '<div class="dblock"><span class="k">Source</span><span class="v soft">' + esc(s.source) + '</span></div>' +
    '</div>';
}

/* ---------------- chips ---------------- */
function renderChips(){
  $('catChips').innerHTML = Object.entries(CATS).map(([k,v]) =>
    '<button class="chip' + (filterCats.has(k)?' on':'') + '" data-cat="' + k + '">' + esc(v) + '</button>').join('');
  $('tierChips').innerHTML = ['A','B','C'].map(t =>
    '<button class="chip' + (filterTiers.has(t)?' on':'') + '" data-tier="' + t + '">Grade ' + t + '</button>').join('');
}

/* ---------------- static sections ---------------- */
function renderTierGrid(){
  $('tierGrid').innerHTML = ['A','B','C'].map(t =>
    '<div class="tiercard"><div class="th"><span class="tier t' + t + '">' + t + '</span>' +
    '<h3>' + esc(TIERS[t].label.split('—')[1].trim()) + '</h3></div>' +
    '<p>' + esc(TIERS[t].desc) + '</p></div>').join('');
}

function renderTable(){
  $('tbody').innerHTML = ST.map(s => {
    const z = Object.entries(s.zones).sort((a,b)=>b[1]-a[1])
      .map(([k,v]) => esc(R[k]) + ' (' + v + ')').join('; ');
    return '<tr><td><b>' + esc(s.name) + '</b></td><td class="soft">' + esc(CATS[s.cat]) +
      '</td><td><span class="tier t' + s.tier + '">' + s.tier + '</span></td><td class="soft">' + z +
      '</td><td class="soft">' + esc(s.note) + '</td></tr>';
  }).join('');
}

/* ---------------- events ---------------- */
document.addEventListener('click', e => {
  const back = e.target.closest('[data-back]');
  if (back){ mode='density'; activeStruct=null; activeRegion=null; paint(); renderRail(); return; }
  const srow = e.target.closest('[data-s]');
  if (srow){
    activeStruct = ST.find(x => x.id === srow.dataset.s);
    activeRegion = null; mode = 'structure'; paint(); renderRail();
    document.querySelector('.plate-wrap').scrollIntoView({block:'nearest', behavior:'smooth'});
    return;
  }
  const rg = e.target.closest('.rg');
  if (rg){
    if (mode==='region' && activeRegion===rg.dataset.r){ mode='density'; activeRegion=null; }
    else { activeRegion = rg.dataset.r; activeStruct=null; mode='region'; }
    paint(); renderRail(); return;
  }
  const cat = e.target.closest('[data-cat]');
  if (cat){
    const k = cat.dataset.cat;
    filterCats.has(k) ? filterCats.delete(k) : filterCats.add(k);
    renderChips(); renderRail(); if(mode==='region') paint(); return;
  }
  const tier = e.target.closest('[data-tier]');
  if (tier){
    const k = tier.dataset.tier;
    filterTiers.has(k) ? filterTiers.delete(k) : filterTiers.add(k);
    renderChips(); renderRail(); if(mode==='region') paint(); return;
  }
});

$('q').addEventListener('input', e => { query = e.target.value; renderRail(); });
$('resetBtn').addEventListener('click', () => {
  mode='density'; activeStruct=null; activeRegion=null;
  filterCats.clear(); filterTiers.clear(); query=''; $('q').value='';
  renderChips(); paint(); renderRail();
});
$('tableBtn').addEventListener('click', e => {
  const tv = $('tableView'); tv.classList.toggle('on');
  e.currentTarget.classList.toggle('on', tv.classList.contains('on'));
  if (tv.classList.contains('on')) tv.scrollIntoView({behavior:'smooth', block:'start'});
});

/* tooltip */
const tip = $('tip');
rects.forEach(el => {
  el.addEventListener('mouseenter', () => {
    document.querySelectorAll('.rg.hovered').forEach(x => x.classList.remove('hovered'));
    rects.filter(x => x.dataset.r === el.dataset.r).forEach(x => x.classList.add('hovered'));
    const rid = el.dataset.r;
    let extra;
    if (mode === 'structure' && activeStruct){
      const i = activeStruct.zones[rid];
      extra = i ? {3:'Primary zone',2:'Common referral',1:'Spillover'}[i] : 'Not a referral zone';
    } else {
      extra = DENSITY[rid] + ' structure' + (DENSITY[rid]===1?'':'s') + ' refer here';
    }
    tip.innerHTML = '<span class="tt">' + esc(extra) + '</span>' + esc(R[rid]);
    tip.classList.add('on');
  });
  el.addEventListener('mousemove', ev => {
    const pad = 14;
    let x = ev.clientX + pad, y = ev.clientY + pad;
    if (x + 250 > window.innerWidth) x = ev.clientX - 250 - pad;
    if (y + 60 > window.innerHeight) y = ev.clientY - 60;
    tip.style.left = x + 'px'; tip.style.top = y + 'px';
  });
  el.addEventListener('mouseleave', () => {
    tip.classList.remove('on');
    rects.forEach(x => x.classList.remove('hovered'));
  });
});

renderChips(); renderTierGrid(); renderTable(); paint(); renderRail();
</script>
"""

# This module is a TEMPLATE, not an entry point. ../../build.py reads the PAGE
# string above as text: the page shell (header, rail, detail, table, evidence,
# caveats, sources) plus the lower-quarter plate blocks, and rewrites it into the
# whole-body atlas. Run `python build.py` from the repository root instead.
