# Referred Pain Atlas

An interactive whole-body atlas of somatic referred pain, built for clinical reasoning
in physical therapy. It maps **117 structures** — cervical and lumbar facet joints,
intervertebral discs, nerve roots, spinal ligaments, peripheral joints and myofascial
sources — onto **79 body zones**, and every entry carries an evidence grade so you can
see which patterns were *caused* under controlled conditions and which were merely
*observed* in clinic.

The whole thing is a single static HTML file. No build step is needed to use it, no
server, no dependencies, and no network requests except the webfont stylesheet.

## Using it

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000     # then visit http://localhost:8000
```

The page opens on a rotatable 3-D figure. Drag to turn it, scroll or pinch to zoom,
arrow keys to nudge it, and the preset buttons jump to Front, Back, Left, Right, Head,
Hands, Feet and Soles. Click a zone to list every structure that refers there, ranked by
referral intensity then evidence grade; click a structure to light up its referral
zones. The **Plates** toggle swaps the figure for the flat anterior, posterior and
plantar maps, and Table view shows the whole dataset at once.

The 3-D figure is a procedurally generated schematic — lofted limbs and an ellipsoid
trunk — not a scanned anatomical mesh. Every one of its ~8,900 faces takes its region
label by projecting onto the same 2-D plate rectangles the flat maps use, so the two
views can never disagree about where a zone is.

### Hosting it

Any static host works. For GitHub Pages: push this repository, then in
**Settings → Pages** set the source to the `main` branch, root folder. The atlas will be
served at `https://<user>.github.io/<repo>/`.

## The data

`data/` carries the merged dataset as plain files so it can be reused without scraping
the HTML:

| file | contents |
|---|---|
| `data/atlas.json` | full dataset — structures, zones, categories, evidence tiers |
| `data/structures.csv` | one row per structure, with its referral zones and source |
| `data/zones.csv` | one row per zone, with how many structures refer there |

Evidence grades are the point of the whole thing, and they are not interchangeable:

- **A** — referral zone produced by controlled provocation in *asymptomatic volunteers*.
  The strongest design available: the zone was caused, not merely observed.
- **B** — provocation (injection, discography, diagnostic block) in *symptomatic
  patients*. Real experimental data, but the population is already in pain.
- **C** — clinical observation or expert synthesis, unblinded. Useful for generating
  hypotheses; not validated diagnostic anatomy.

Upper- and lower-quarter data were compiled separately and merged here. Where the two
described the same skin — low back, buttock, groin, lower abdomen, thoracolumbar
junction — the zones share one label, so a click there lists structures from both. The
sacroiliac joint and quadratus lumborum appeared in both sets; the lower-quarter entries
were kept.

## Rebuilding

Only needed if you change the underlying data. Requires Python 3.8+ and nothing else:

```bash
python3 build.py        # regenerates index.html and everything in data/
```

The build is deterministic — the same inputs produce a byte-identical `index.html`.

```
build.py              merges both datasets, assembles the page, writes data exports
src/upper/            cervical / upper-quarter data, plate geometry, page template
src/lower/            lumbosacral / lower-quarter data, plate geometry, page shell
src/render/
  body3d.js           dependency-free Canvas2D renderer (geometry, picking, controls)
  models.py           the figure: lofted body parts and their plate bindings
  integrate.py        injects the renderer and its wiring into the page
data/                 generated — do not edit by hand
index.html            generated — do not edit by hand
```

`src/upper/data.py` and `src/lower/referral_data.py` are where the structures live. Each
entry is a name, category, evidence tier, source citation, clinical note, lookalikes, and
a dict of referral zones weighted 3 (primary) / 2 (common) / 1 (spillover). Adding a
structure means adding one entry there and rebuilding.

### Why a hand-written renderer

The 3-D view uses no WebGL and no third-party library — it is a software renderer in
about 600 lines of plain JavaScript: perspective projection, back-face culling, a
depth-sorted painter's algorithm, flat shading, and polygon-hit picking. That keeps the
page self-contained and offline-capable, and it costs roughly 4 ms per frame. The
trade-off is that the figure is schematic rather than anatomically modelled.

## Scope and limits

This is an educational reference, not a diagnostic instrument, and the source literature
is explicit about what these maps cannot do. They cannot localise a segment: adjacent
facet levels and adjacent discs produce overlapping patterns, and pain location cannot
separate a lumbar facet joint from the sacroiliac joint at all. They cannot tell you the
side: 30–62% of cervical discs produced bilateral pain at every level tested. Midline
versus paramidline low back pain is the one location finding with real discriminating
value. And trigger-point palpation, which underwrites every grade-C myofascial entry, has
interrater κ ≈ 0.45 — the crisp borders drawn in myofascial atlases outrun their
evidence.

A pain map narrows a differential. It does not establish a diagnosis.

Full citations are listed in the Sources section of the page itself and in the `source`
column of `data/structures.csv`.

## A note on the companion links

The row of pills under the lede points at four private artifacts that only their owner
can open — anyone else visiting a published copy gets a dead link. Repoint them at your
own hosted copies, or set `COMPANION_LINKS = []` near the top of `build.py` to drop the
row entirely, then rebuild.

## Typography

The page loads Source Serif 4, IBM Plex Sans and IBM Plex Mono from Google Fonts. That is
its only outbound request. If the stylesheet is blocked or unavailable the page falls back
to system serif, sans and mono faces and remains fully usable — nothing but the lettering
changes. To make it entirely self-contained, drop the webfont `<link>` from the page
template in `src/lower/build_html.py` and either accept the system stack or inline the
fonts as base64 in the stylesheet.

## License

No license has been chosen yet, which means default copyright applies and nobody can
reuse this. Two things need deciding separately: the **code** (build scripts and
renderer), where MIT or Apache-2.0 are the usual picks, and the **compiled dataset**,
where CC BY 4.0 is common for factual compilations. The underlying findings are facts
from the published literature and are not themselves copyrightable, but this particular
compilation, its zone scheme and its clinical notes are original work.
