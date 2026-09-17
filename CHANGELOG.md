# Changelog

## 2026-09-17 — Whole-body atlas

- Upper- and lower-quarter referred-pain atlases merged into one page: 117 structures
  across 79 zones, with an Upper/Lower quarter filter.
- Zones describing the same skin in both datasets (low back, buttock, groin, lower
  abdomen, thoracolumbar junction) unified under one label, so a click there lists
  structures from both quarters. Duplicate sacroiliac joint and quadratus lumborum
  entries collapsed to the lower-quarter versions.
- Rotatable 3-D figure is the default view; it covers the whole body and carries
  schematic facial features. Flat plates remain as a secondary view, now showing both
  quarters plus the plantar map.
- Dataset exported to `data/` as JSON and CSV.

### Corrections made during this work

- McCall, Park & O'Brien 1979 was cited as *J Bone Joint Surg Br*; it was published in
  *Spine* 1979;4(5):441-6. Fixed.
- The lower-quarter atlas had inherited the cervical Sources list and caveat cards
  verbatim. Replaced with the lumbar, pelvic and hip literature it actually draws on.
- Sacroiliac joint regraded A → B: only the zone *shape* comes from asymptomatic
  volunteers (Fortin 1994 Part I); every quoted percentage comes from a symptomatic
  patient series (Slipman 2000, 50 patients / 68 joints).
- Lower thoracic facets regraded A → B: volunteer provocation data reach only to T10–11,
  so T11–12 rests on symptomatic-patient data alone.
- Infraspinatus and upper trapezius regraded B → C (Travell & Simons clinical
  observation, not controlled provocation).
- Laslett sacroiliac cluster corrected to 2 of 4 tests — distraction, compression, thigh
  thrust, sacral thrust — with Gaenslen's dropped from the validated rule.
