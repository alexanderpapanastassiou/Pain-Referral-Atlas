/* Body3D — a dependency-free schematic body renderer for the referred-pain atlases.
 *
 * Why not a 3D library: the page must stay self-contained and work offline, and
 * a schematic figure of ~3,500 quads needs nothing a Canvas2D painter's
 * algorithm cannot do. Everything here is plain JavaScript.
 *
 * Geometry: each body part is a lofted tube — a list of "stations" giving the
 * centre and elliptical radii at points along an axis — sampled into rings and
 * stitched into quads. Every quad is assigned the SAME region id the 2-D plates
 * use, by projecting its centroid onto the anterior / posterior (/ plantar)
 * plate and looking up the rectangle it lands in. The 3-D model therefore paints
 * exactly what the plates paint; it is a different view of one dataset.
 *
 * Rendering: rotate → perspective-project → cull back faces → depth-sort →
 * flat-shade. Region boundaries and highlights are stroked per face in painter
 * order so they are occluded correctly for free.
 */
(function (global) {
  'use strict';

  const TAU = Math.PI * 2;
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const deg = d => d * Math.PI / 180;

  /* ---------------------------------------------------------------- spline */
  // cubic Hermite through non-uniformly spaced stations (finite-difference tangents)
  function hermite(st, axis, keys, u) {
    let i = 0;
    while (i < st.length - 2 && u > st[i + 1][axis]) i++;
    const a = st[i], b = st[i + 1];
    const h = b[axis] - a[axis];
    const t = clamp((u - a[axis]) / h, 0, 1);
    const t2 = t * t, t3 = t2 * t;
    const h00 = 2 * t3 - 3 * t2 + 1, h10 = t3 - 2 * t2 + t, h01 = -2 * t3 + 3 * t2, h11 = t3 - t2;
    const prev = st[Math.max(0, i - 1)], next = st[Math.min(st.length - 1, i + 2)];
    const out = {};
    keys.forEach(k => {
      const m0 = (i === 0) ? (b[k] - a[k]) / h : (b[k] - prev[k]) / (b[axis] - prev[axis]);
      const m1 = (i === st.length - 2) ? (b[k] - a[k]) / h : (next[k] - a[k]) / (next[axis] - a[axis]);
      out[k] = h00 * a[k] + h10 * h * m0 + h01 * b[k] + h11 * h * m1;
    });
    return out;
  }

  /* ---------------------------------------------------------------- mesh */
  // A frame maps a plate set's own coordinates into the model's world frame:
  // world.x = mid + (x - mid) * sx ;  world.y = y * sy + oy ;  z is untouched.
  const ID = { sx: 1, sy: 1, oy: 0 };
  const toWorld = (fr, mid, x, y) => [mid + (x - mid) * fr.sx, y * fr.sy + fr.oy];
  const toNative = (fr, mid, x, y) => [mid + (x - mid) / fr.sx, (y - fr.oy) / fr.sy];

  // Accept the older single-plate-set shape as well as the multi-set shape:
  //   spec.plates + spec.foot                     → one set, every part bound to it
  //   spec.plateSets {name:{ant,post,plant,foot}} + part.bind [{set, frame, yMin, yMax}]
  function normalise(spec) {
    if (!spec.plateSets) {
      spec.plateSets = { default: { ant: spec.plates.ant, post: spec.plates.post, plant: spec.plates.plant, foot: spec.foot } };
    }
    spec.parts.forEach(p => {
      p.frame = Object.assign({}, ID, p.frame || {});
      if (!p.bind) p.bind = p.bind === null ? [] : [{ set: 'default' }];
      p.bind.forEach(b => { b.frame = Object.assign({}, ID, b.frame || {}); });
    });
    return spec;
  }

  function buildMesh(spec) {
    normalise(spec);
    const V = [];      // vertices  [X, Y, Z] in world coordinates (Y down, Z anterior)
    const F = [];      // faces     {v:[...], n:[..], c:[..], part, rid, nb:[...]}
    const lookup = makeLookup(spec);

    spec.parts.forEach(part => {
      (part.mirror ? [false, true] : [false]).forEach(mir => loft(part, mir));
    });

    function loft(part, mir) {
      const axis = part.axis || 'y';                 // 'y' (vertical) or 'z' (feet)
      const st = part.stations;
      const isY = axis === 'y';
      const keys = isY ? ['cx', 'cz', 'rx', 'rz'] : ['cx', 'cy', 'rx', 'ry'];
      const u0 = st[0][axis], u1 = st[st.length - 1][axis];
      const M = part.sectors || 20;
      const step = part.step || 8;
      const us = ringPositions(spec, part, u0, u1, step);
      const nRings = us.length;
      const samples = us.map(u => hermite(st, axis, keys, u));
      const angles = isY ? sectorAngles(spec, part, samples, M) : null;
      const MM = angles ? angles[0].length : M;
      const ringIdx = [], centres = [];
      for (let i = 0; i < nRings; i++) {
        const u = us[i];
        const s = samples[i];
        const idx = [];
        const fr = part.frame;
        let C, cw;
        if (isY) { cw = toWorld(fr, spec.mid, s.cx, u); C = [mir ? 2 * spec.mid - cw[0] : cw[0], cw[1], s.cz]; }
        else { cw = toWorld(fr, spec.mid, s.cx, s.cy); C = [mir ? 2 * spec.mid - cw[0] : cw[0], cw[1], u]; }
        for (let j = 0; j < MM; j++) {
          const th = angles ? angles[i][j] : TAU * j / MM;
          let X, Y, Z;
          if (isY) {
            const rx = Math.max(0.4, s.rx), rz = Math.max(0.4, s.rz);
            X = s.cx + rx * Math.cos(th); Y = u; Z = s.cz + rz * Math.sin(th);
          } else {
            const rx = Math.max(0.4, s.rx), ry = Math.max(0.4, s.ry);
            X = s.cx + rx * Math.cos(th); Y = s.cy + ry * Math.sin(th); Z = u;
          }
          const w = toWorld(fr, spec.mid, X, Y); X = w[0]; Y = w[1];
          if (mir) X = 2 * spec.mid - X;
          idx.push(V.push([X, Y, Z]) - 1);
        }
        ringIdx.push(idx); centres.push(C);
      }
      const base = F.length;
      const fid = (i, j) => base + i * MM + ((j + MM) % MM);
      for (let i = 0; i < nRings - 1; i++) {
        const c0 = centres[i], c1 = centres[i + 1];
        const axisMid = [(c0[0] + c1[0]) / 2, (c0[1] + c1[1]) / 2, (c0[2] + c1[2]) / 2];
        for (let j = 0; j < MM; j++) {
          const a = ringIdx[i][j], b = ringIdx[i][(j + 1) % MM],
                c = ringIdx[i + 1][(j + 1) % MM], d = ringIdx[i + 1][j];
          const f = makeFace([a, b, c, d], part, axisMid);
          // neighbours by edge: 0 = a-b (previous ring row), 1 = b-c (next sector),
          // 2 = c-d (next row), 3 = d-a (previous sector)
          f.nb = [i > 0 ? fid(i - 1, j) : -1, fid(i, j + 1),
                  i < nRings - 2 ? fid(i + 1, j) : -1, fid(i, j - 1)];
          F.push(f);
        }
      }
      // flat, region-less caps so a cut end never shows the hollow inside
      const cap = (ring, row, slot, dir) => {
        const f = makeFace(ring.slice(), part, null);
        f.cap = true; f.n = dir; f.rid = null; f.nb = ring.map(() => -1);
        const ci = F.push(f) - 1;
        row.forEach(rf => { F[rf].nb[slot] = ci; });
      };
      if (part.capStart) {
        const row = []; for (let j = 0; j < MM; j++) row.push(fid(0, j));
        cap(ringIdx[0], row, 0, isY ? [0, -1, 0] : [0, 0, -1]);
      }
      if (part.capEnd) {
        const row = []; for (let j = 0; j < MM; j++) row.push(fid(nRings - 2, j));
        cap(ringIdx[nRings - 1], row, 2, isY ? [0, 1, 0] : [0, 0, 1]);
      }
    }

    function makeFace(idx, part, axisMid) {
      const pts = idx.map(i => V[i]);
      const c = [0, 0, 0];
      pts.forEach(p => { c[0] += p[0]; c[1] += p[1]; c[2] += p[2]; });
      c[0] /= pts.length; c[1] /= pts.length; c[2] /= pts.length;
      const f = { v: idx, n: [0, 0, 1], c: c, part: part.tag, rid: null, tint: part.tint || null };
      if (!axisMid) return f;
      // Newell normal — robust for slightly non-planar quads
      let n = [0, 0, 0];
      for (let i = 0; i < pts.length; i++) {
        const p = pts[i], q = pts[(i + 1) % pts.length];
        n[0] += (p[1] - q[1]) * (p[2] + q[2]);
        n[1] += (p[2] - q[2]) * (p[0] + q[0]);
        n[2] += (p[0] - q[0]) * (p[1] + q[1]);
      }
      const L = Math.hypot(n[0], n[1], n[2]) || 1;
      n = [n[0] / L, n[1] / L, n[2] / L];
      // outward = away from the loft axis
      const d = [c[0] - axisMid[0], c[1] - axisMid[1], c[2] - axisMid[2]];
      if (n[0] * d[0] + n[1] * d[1] + n[2] * d[2] < 0) n = [-n[0], -n[1], -n[2]];
      f.n = n;
      f.rid = part.region !== undefined ? part.region : lookup(part, c, n);
      return f;
    }

    return { V, F };
  }

  // ring positions: a regular step, plus a ring at every plate-rectangle edge
  // that crosses this part, so horizontal region boundaries fall exactly on a
  // ring instead of the nearest one
  // every plate rectangle that binds to this part, expressed in the part's
  // native frame: [rid, x, y, w, h, view]
  function boundRects(spec, part) {
    const out = [];
    part.bind.forEach(b => {
      const set = spec.plateSets[b.set]; if (!set) return;
      ['ant', 'post'].forEach(v => (set[v] || []).forEach(r => {
        if (r[5] !== part.tag) return;
        // set-native → world → part-native
        const p0 = toWorld(b.frame, spec.mid, r[1], r[2]), p1 = toWorld(b.frame, spec.mid, r[1] + r[3], r[2] + r[4]);
        if (b.yMin != null && p1[1] < b.yMin) return;
        if (b.yMax != null && p0[1] > b.yMax) return;
        const y0w = b.yMin != null ? Math.max(p0[1], b.yMin) : p0[1];
        const y1w = b.yMax != null ? Math.min(p1[1], b.yMax) : p1[1];
        const q0 = toNative(part.frame, spec.mid, p0[0], y0w), q1 = toNative(part.frame, spec.mid, p1[0], y1w);
        out.push([r[0], q0[0], q0[1], q1[0] - q0[0], q1[1] - q0[1], v]);
      }));
      // binding limits are boundaries too
      [b.yMin, b.yMax].forEach(y => { if (y != null) { const q = toNative(part.frame, spec.mid, spec.mid, y); out.push([null, 0, q[1], 0, 0, 'lim']); } });
    });
    return out;
  }

  // ring positions: a regular step, plus a ring at every plate-rectangle edge
  // that crosses this part, so horizontal region boundaries fall exactly on a
  // ring instead of the nearest one
  function ringPositions(spec, part, u0, u1, step) {
    const set = [u0, u1];
    if ((part.axis || 'y') === 'y') {
      boundRects(spec, part).forEach(r => {
        [r[2], r[2] + r[4]].forEach(y => { if (y > u0 + 1.5 && y < u1 - 1.5) set.push(Math.round(y * 4) / 4); });
      });
    }
    const edges = Array.from(new Set(set)).sort((a, b) => a - b);
    const out = [];
    for (let i = 0; i < edges.length - 1; i++) {
      const a = edges[i], b = edges[i + 1];
      const n = Math.max(1, Math.round((b - a) / step));
      for (let k = 0; k < n; k++) out.push(a + (b - a) * k / n);
    }
    out.push(u1);
    // merge rings closer than 1.5 units (keeps quads from degenerating)
    const merged = [out[0]];
    for (let i = 1; i < out.length; i++) {
      if (out[i] - merged[merged.length - 1] >= 1.5) merged.push(out[i]);
      else if (i === out.length - 1) merged[merged.length - 1] = out[i];
    }
    return merged;
  }

  // sector angles per ring: uniform, but warped so that a sector boundary sits
  // exactly where each plate-rectangle X-edge crosses the tube. Anchor ORDER is
  // the same on every ring (acos is monotone), so the rings still stitch as a grid.
  function sectorAngles(spec, part, samples, M) {
    let xmin = Infinity, xmax = -Infinity;
    samples.forEach(s => { xmin = Math.min(xmin, s.cx - s.rx); xmax = Math.max(xmax, s.cx + s.rx); });
    const ys = part.stations.map(s => s.y);
    const y0 = Math.min(...ys), y1 = Math.max(...ys);
    const xs = new Set();
    boundRects(spec, part).forEach(r => {
      if (r[5] === 'lim') return;
      if (r[2] > y1 || r[2] + r[4] < y0) return;
      [r[1], r[1] + r[3]].forEach(x => {
        const X = r[5] === 'post' ? 2 * spec.mid - x : x;
        if (X > xmin + 1 && X < xmax - 1) xs.add(Math.round(X * 2) / 2);
      });
    });
    const edges = Array.from(xs).sort((a, b) => b - a);       // descending x → ascending front angle
    if (!edges.length) return samples.map(() => Array.from({ length: M }, (_, j) => TAU * j / M));
    // anchors per ring, in a fixed order: front (x desc), then back (x asc)
    const anchors = samples.map(s => {
      const front = edges.map(x => Math.acos(clamp((x - s.cx) / s.rx, -1, 1)));
      const back = front.slice().reverse().map(a => TAU - a);
      return front.concat(back);
    });
    const K = anchors[0].length;
    // mean interval sizes → integer sector counts per interval (same on every ring)
    const mean = new Array(K).fill(0);
    anchors.forEach(a => { for (let k = 0; k < K; k++) { const nx = a[(k + 1) % K]; mean[k] += ((nx - a[k]) % TAU + TAU) % TAU; } });
    const counts = mean.map(m => Math.max(1, Math.round(M * (m / anchors.length) / TAU)));
    return anchors.map(a => {
      const out = [];
      for (let k = 0; k < K; k++) {
        const a0 = a[k], span = ((a[(k + 1) % K] - a0) % TAU + TAU) % TAU;
        for (let q = 0; q < counts[k]; q++) out.push((a0 + span * q / counts[k]) % TAU);
      }
      return out;
    });
  }

  /* ------------------------------------------------- 2-D plate lookup */
  function makeLookup(spec) {
    const snap = spec.snap == null ? 10 : spec.snap;
    function find(set, view, tag, x, y) {
      const rs = set[view];
      if (!rs) return null;
      let best = null, bestD = Infinity;
      for (let i = 0; i < rs.length; i++) {
        const r = rs[i];
        if (r[5] !== tag) continue;
        const dx = x < r[1] ? r[1] - x : x > r[1] + r[3] ? x - r[1] - r[3] : 0;
        const dy = y < r[2] ? r[2] - y : y > r[2] + r[4] ? y - r[2] - r[4] : 0;
        if (dx === 0 && dy === 0) return r[0];
        const d = Math.hypot(dx, dy);
        if (d < bestD) { bestD = d; best = r[0]; }
      }
      return bestD <= snap ? best : null;
    }
    // world centroid + normal → region id, via the first binding whose Y range holds it
    return function (part, c, n) {
      for (let k = 0; k < part.bind.length; k++) {
        const b = part.bind[k];
        if (b.yMin != null && c[1] < b.yMin) continue;
        if (b.yMax != null && c[1] >= b.yMax) continue;
        const set = spec.plateSets[b.set]; if (!set) continue;
        const q = toNative(b.frame, spec.mid, c[0], c[1]);
        const X = q[0], Y = q[1], Z = c[2];
        const tag = part.tag;
        const foot = set.foot && set.foot.tags.indexOf(tag) >= 0 ? set.foot : null;
        const tagBase = foot ? foot.as : tag;
        if (foot) {
          // Y is "down" in plate coordinates, so a sole faces +Y
          const t = (Z - foot.zHeel) / (foot.zToe - foot.zHeel);           // 0 heel → 1 toe
          if (n[1] > 0.5 && set.plant) {
            const y2 = foot.plantY[0] + (foot.plantY[1] - foot.plantY[0]) * t; // [heel y, toe y]
            return find(set, 'plant', tagBase, X, y2);
          }
          if (n[2] >= 0) {
            const y2 = foot.antY[0] + (foot.antY[1] - foot.antY[0]) * t;
            return find(set, 'ant', tagBase, X, y2);
          }
          return find(set, 'post', tagBase, 2 * spec.mid - X, Y);
        }
        if (n[2] >= 0) return find(set, 'ant', tagBase, X, Y);
        return find(set, 'post', tagBase, 2 * spec.mid - X, Y);
      }
      return null;
    };
  }

  /* ---------------------------------------------------------------- colour */
  function hexToRgb(h) {
    h = (h || '').trim();
    if (h[0] === '#') h = h.slice(1);
    if (h.length === 3) h = h.split('').map(c => c + c).join('');
    const n = parseInt(h, 16);
    if (isNaN(n)) return [128, 128, 128];
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }
  function cssVar(name, fallback) {
    const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    return v || fallback;
  }

  /* ---------------------------------------------------------------- viewer */
  function Body3D(host, spec, opts) {
    opts = opts || {};
    const self = this;
    const mesh = buildMesh(spec);
    const V = mesh.V, F = mesh.F;


    // bounds
    let minY = Infinity, maxY = -Infinity, maxR = 0;
    V.forEach(p => { minY = Math.min(minY, p[1]); maxY = Math.max(maxY, p[1]); });
    const cy = (minY + maxY) / 2;
    V.forEach(p => { maxR = Math.max(maxR, Math.hypot(p[0] - spec.mid, p[1] - cy, p[2])); });
    const halfH = (maxY - minY) / 2;

    // DOM
    host.classList.add('b3d');
    host.innerHTML =
      '<canvas class="b3d-canvas" tabindex="0" role="img" aria-label="' + (opts.label || 'Rotatable 3-D body heat map') + '"></canvas>' +
      '<div class="b3d-bar">' +
        '<div class="b3d-views" role="group" aria-label="Preset views">' +
          (spec.views || [['Front', 0, 0], ['Back', 180, 0], ['Left', -90, 0], ['Right', 90, 0]])
            .map(v => '<button type="button" class="b3d-btn" data-yaw="' + v[1] + '" data-pitch="' + v[2] + '" data-zoom="' + (v[3] || 1) + '" data-focus="' + (v[4] == null ? '' : v[4]) + '">' + v[0] + '</button>').join('') +
        '</div>' +
        '<span class="b3d-hint">drag to rotate · scroll or pinch to zoom · click a zone</span>' +
      '</div>';
    const canvas = host.querySelector('canvas');
    const ctx = canvas.getContext('2d');

    // state
    let yaw = deg(spec.yaw0 || 0), pitch = deg(spec.pitch0 || 0), zoom = spec.zoom0 || 1;
    let focusY = null;        // plate-Y to centre on (null = figure centre)
    let heat = {}, picked = null, hovered = null;
    let colors = null, W = 0, H = 0, dpr = 1;
    let frameReq = 0;
    let frontSorted = [];     // faces drawn last frame, painter order (far → near)
    let proj = null;          // projected 2-D points per vertex
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

    function readColors() {
      shadeTable = null;
      colors = {
        heat: [cssVar('--heat-0', '#E4E8E0'), cssVar('--heat-1', '#E89272'),
               cssVar('--heat-2', '#D85B3F'), cssVar('--heat-3', '#A31C14')].map(hexToRgb),
        paper: cssVar('--paper', '#F1F3EF'),
        surface: cssVar('--surface', '#FFFFFF'),
        line: cssVar('--line-strong', '#BCC4B7'),
        ink: cssVar('--ink', '#1B231F'),
        accent: cssVar('--accent', '#1F6F63'),
        dark: matchMedia('(prefers-color-scheme: dark)').matches
      };
      const t = document.documentElement.getAttribute('data-theme');
      if (t === 'dark') colors.dark = true; else if (t === 'light') colors.dark = false;
    }

    function resize() {
      const r = canvas.getBoundingClientRect();
      dpr = Math.min(2, window.devicePixelRatio || 1);
      W = Math.max(1, Math.round(r.width)); H = Math.max(1, Math.round(r.height));
      canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    /* ---- projection ---- */
    function project() {
      const cyaw = Math.cos(yaw), syaw = Math.sin(yaw), cp = Math.cos(pitch), sp = Math.sin(pitch);
      const D = maxR * 3.2;                       // camera distance
      const cyv = focusY == null ? cy : cy + (focusY - cy) * Math.min(1, Math.max(0, (zoom - 1) / 0.8));
      const fit = Math.min(W / (maxR * 2.05), H / (halfH * 2.12));
      const s = fit * zoom;
      const ox = W / 2, oy = H / 2;
      proj = new Array(V.length);
      const depth = new Float64Array(V.length);
      for (let i = 0; i < V.length; i++) {
        const p = V[i];
        const x = p[0] - spec.mid, y = -(p[1] - cyv), z = p[2];
        const x1 = x * cyaw + z * syaw, z1 = -x * syaw + z * cyaw;
        const y2 = y * cp - z1 * sp, z2 = y * sp + z1 * cp;
        const f = D / (D - z2);
        proj[i] = [ox + s * x1 * f, oy - s * y2 * f];
        depth[i] = z2;
      }
      // rotate normals, cull, sort
      const camz = D;
      const front = [];
      for (let i = 0; i < F.length; i++) {
        const f = F[i], n = f.n, c = f.c;
        const nx = n[0], ny = -n[1], nz = n[2];
        const nx1 = nx * cyaw + nz * syaw, nz1 = -nx * syaw + nz * cyaw;
        const ny2 = ny * cp - nz1 * sp, nz2 = ny * sp + nz1 * cp;
        const x = c[0] - spec.mid, y = -(c[1] - cyv), z = c[2];
        const x1 = x * cyaw + z * syaw, z1 = -x * syaw + z * cyaw;
        const y2 = y * cp - z1 * sp, z2 = y * sp + z1 * cp;
        // view vector from face to camera
        const vx = -x1, vy = -y2, vz = camz - z2;
        const dot = nx1 * vx + ny2 * vy + nz2 * vz;
        f._front = dot > 0;
        f._z = z2;
        f._nv = [nx1, ny2, nz2];
        if (f._front) front.push(f);
      }
      front.sort((a, b) => a._z - b._z);
      frontSorted = front;
    }

    /* ---- draw ---- */
    // light from the viewer's upper-left, fixed to the camera; shading is
    // quantised to 24 steps so colour strings come from a small cached table
    const LIGHT = [-0.42, 0.62, 0.66], STEPS = 24;
    let shadeTable = null;
    function buildShadeTable() {
      shadeTable = colors.heat.concat([hexToRgb(colors.ink)]).map(rgb => {
        const row = [];
        for (let i = 0; i <= STEPS; i++) {
          const d = i / STEPS;
          const k = colors.dark ? 0.66 + 0.5 * d : 0.74 + 0.36 * d;
          row.push('rgb(' + Math.min(255, rgb[0] * k | 0) + ',' + Math.min(255, rgb[1] * k | 0) + ',' + Math.min(255, rgb[2] * k | 0) + ')');
        }
        return row;
      });
    }
    function shade(level, nv) {
      if (!shadeTable) buildShadeTable();
      const d = Math.max(0, nv[0] * LIGHT[0] + nv[1] * LIGHT[1] + nv[2] * LIGHT[2]);
      return shadeTable[level][Math.round(d * STEPS)];
    }

    function draw() {
      frameReq = 0;
      if (!colors) readColors();
      if (!W) resize();
      project();
      ctx.clearRect(0, 0, W, H);

      // pass 1 — silhouette: edges whose neighbour is back-facing (or absent),
      // stroked wide; pass 2 covers the inner half, leaving a clean outline
      ctx.lineJoin = 'round'; ctx.lineCap = 'round';
      ctx.strokeStyle = colors.line; ctx.lineWidth = 3.2;
      ctx.beginPath();
      for (let i = 0; i < frontSorted.length; i++) {
        const f = frontSorted[i], idx = f.v, nb = f.nb;
        for (let k = 0; k < idx.length; k++) {
          const g = nb[k] >= 0 ? F[nb[k]] : null;
          if (g && g._front) continue;
          const a = proj[idx[k]], b = proj[idx[(k + 1) % idx.length]];
          ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]);
        }
      }
      ctx.stroke();

      // pass 2 — faces in painter order, then that face's boundary edges
      for (let i = 0; i < frontSorted.length; i++) {
        const f = frontSorted[i];
        const lvl = f.rid ? (heat[f.rid] | 0) : 0;
        ctx.fillStyle = f.tint ? shade(4, f._nv) : shade(clamp(lvl, 0, 3), f._nv);
        pathOf(f, 0.45); ctx.fill();
        const idx = f.v, nb = f.nb;
        for (let k = 0; k < idx.length; k++) {
          const g = nb[k] >= 0 ? F[nb[k]] : null;
          const gr = g ? g.rid : null;
          const gFront = !!(g && g._front);
          let style = null, w = 0;
          if (picked && ((f.rid === picked) !== (gFront && gr === picked))) { style = colors.accent; w = 2.2; }
          else if (hovered && ((f.rid === hovered) !== (gFront && gr === hovered))) { style = colors.ink; w = 1.5; }
          else if (gFront && gr !== f.rid) { style = colors.paper; w = 0.9; }
          if (!style) continue;
          const a = proj[idx[k]], b = proj[idx[(k + 1) % idx.length]];
          ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]);
          ctx.strokeStyle = style; ctx.lineWidth = w; ctx.stroke();
        }
      }
    }

    // polygon path, optionally grown by `grow` px away from its centre so
    // neighbouring fills overlap and anti-aliasing leaves no hairline seams
    function pathOf(f, grow) {
      const idx = f.v;
      let cx = 0, cy = 0;
      if (grow) { for (let k = 0; k < idx.length; k++) { cx += proj[idx[k]][0]; cy += proj[idx[k]][1]; } cx /= idx.length; cy /= idx.length; }
      ctx.beginPath();
      for (let k = 0; k < idx.length; k++) {
        let p = proj[idx[k]], x = p[0], y = p[1];
        if (grow) { const dx = x - cx, dy = y - cy, d = Math.hypot(dx, dy) || 1; x += dx / d * grow; y += dy / d * grow; }
        if (k === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.closePath();
    }

    function request() { if (!frameReq) frameReq = requestAnimationFrame(draw); }

    /* ---- picking ---- */
    function pick(px, py) {
      if (!proj) return null;
      for (let i = frontSorted.length - 1; i >= 0; i--) {
        const f = frontSorted[i];
        if (inPoly(f.v, px, py)) return f;
      }
      return null;
    }
    function inPoly(idx, px, py) {
      let inside = false;
      for (let i = 0, j = idx.length - 1; i < idx.length; j = i++) {
        const a = proj[idx[i]], b = proj[idx[j]];
        if (((a[1] > py) !== (b[1] > py)) && (px < (b[0] - a[0]) * (py - a[1]) / (b[1] - a[1]) + a[0])) inside = !inside;
      }
      return inside;
    }

    /* ---- interaction ---- */
    let dragging = false, moved = 0, lx = 0, ly = 0, pinch = null;
    const pointers = new Map();
    canvas.style.touchAction = 'none';

    canvas.addEventListener('pointerdown', e => {
      canvas.setPointerCapture(e.pointerId);
      pointers.set(e.pointerId, [e.clientX, e.clientY]);
      if (pointers.size === 2) {
        const p = Array.from(pointers.values());
        pinch = { d: Math.hypot(p[0][0] - p[1][0], p[0][1] - p[1][1]), z: zoom };
        dragging = false; return;
      }
      dragging = true; moved = 0; lx = e.clientX; ly = e.clientY;
      canvas.classList.add('grabbing');
    });
    canvas.addEventListener('pointermove', e => {
      if (pointers.has(e.pointerId)) pointers.set(e.pointerId, [e.clientX, e.clientY]);
      if (pinch && pointers.size === 2) {
        const p = Array.from(pointers.values());
        const d = Math.hypot(p[0][0] - p[1][0], p[0][1] - p[1][1]);
        zoom = clamp(pinch.z * d / pinch.d, 0.6, 3.2); request(); return;
      }
      if (dragging) {
        const dx = e.clientX - lx, dy = e.clientY - ly;
        moved += Math.abs(dx) + Math.abs(dy);
        lx = e.clientX; ly = e.clientY;
        yaw += dx * 0.011; pitch = clamp(pitch + dy * 0.008, -deg(88), deg(88));
        request(); return;
      }
      hoverAt(e);
    });
    function endPointer(e) {
      pointers.delete(e.pointerId);
      if (pointers.size < 2) pinch = null;
      if (!dragging) return;
      dragging = false; canvas.classList.remove('grabbing');
      if (moved < 5 && e.type === 'pointerup') {
        const f = pick(...local(e));
        if (opts.onPick) opts.onPick(f ? f.rid : null);
      }
    }
    canvas.addEventListener('pointerup', endPointer);
    canvas.addEventListener('pointercancel', endPointer);
    canvas.addEventListener('pointerleave', e => {
      if (hovered) { hovered = null; request(); if (opts.onHover) opts.onHover(null); }
    });
    canvas.addEventListener('wheel', e => {
      e.preventDefault();
      zoom = clamp(zoom * (e.deltaY < 0 ? 1.1 : 0.9), 0.6, 3.2);
      request();
    }, { passive: false });
    canvas.addEventListener('keydown', e => {
      const k = e.key;
      let used = true;
      if (k === 'ArrowLeft') yaw -= deg(15);
      else if (k === 'ArrowRight') yaw += deg(15);
      else if (k === 'ArrowUp') pitch = clamp(pitch - deg(10), -deg(88), deg(88));
      else if (k === 'ArrowDown') pitch = clamp(pitch + deg(10), -deg(88), deg(88));
      else if (k === '+' || k === '=') zoom = clamp(zoom * 1.1, 0.6, 3.2);
      else if (k === '-') zoom = clamp(zoom * 0.9, 0.6, 3.2);
      else used = false;
      if (used) { e.preventDefault(); request(); }
    });
    function local(e) {
      const r = canvas.getBoundingClientRect();
      return [e.clientX - r.left, e.clientY - r.top];
    }
    let hoverPending = null, hoverQueued = false;
    function hoverAt(e) {
      hoverPending = e;
      if (hoverQueued) return;
      hoverQueued = true;
      requestAnimationFrame(() => {
        const ev = hoverPending; hoverQueued = false;
        const f = pick(...local(ev));
        const rid = f ? f.rid : null;
        canvas.style.cursor = rid ? 'pointer' : 'grab';
        if (rid !== hovered) { hovered = rid; request(); }
        if (opts.onHover) opts.onHover(rid, ev.clientX, ev.clientY);
      });
    }

    // preset views
    host.querySelectorAll('.b3d-btn').forEach(b => {
      b.addEventListener('click', () => {
        focusY = b.dataset.focus === '' ? null : +b.dataset.focus;
        animateTo(deg(+b.dataset.yaw), deg(+b.dataset.pitch), +b.dataset.zoom || 1);
      });
    });
    function animateTo(ty, tp, tz) {
      // shortest way round
      const dy0 = ((ty - yaw) % TAU + TAU * 1.5) % TAU - Math.PI;
      const y0 = yaw, p0 = pitch, dp = tp - pitch, z0 = zoom, dz = tz - zoom;
      if (reduced) { yaw = ty; pitch = tp; zoom = tz; request(); return; }
      const t0 = performance.now(), dur = 340;
      (function step(now) {
        const t = clamp((now - t0) / dur, 0, 1), e = 1 - Math.pow(1 - t, 3);
        yaw = y0 + dy0 * e; pitch = p0 + dp * e; zoom = z0 + dz * e;
        draw();
        if (t < 1) requestAnimationFrame(step);
      })(t0);
    }

    // theme + size changes
    const ro = 'ResizeObserver' in window ? new ResizeObserver(() => { resize(); request(); }) : null;
    if (ro) ro.observe(canvas); else window.addEventListener('resize', () => { resize(); request(); });
    const mo = new MutationObserver(() => { colors = null; request(); });
    mo.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
    matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => { colors = null; request(); });

    /* ---- public API ---- */
    this.setHeat = function (map, pickedRegion) {
      heat = map || {}; picked = pickedRegion || null; request();
    };
    this.setHover = function (rid) { if (rid !== hovered) { hovered = rid; request(); } };
    this.redraw = function () { colors = null; resize(); request(); };
    this.regions = function () { const s = new Set(); F.forEach(f => f.rid && s.add(f.rid)); return s; };
    this.faceCount = F.length;
    this.view = function (y, p, z, fy) { yaw = deg(y); pitch = deg(p || 0); if (z) zoom = z; focusY = fy == null ? null : fy; request(); };
    this.stats = function () {
      const per = {}; F.forEach(f => { const k = f.rid || '(none)'; per[k] = (per[k] || 0) + 1; }); return per;
    };
    this._mesh = mesh; this._draw = draw;

    resize(); request();
  }

  global.Body3D = Body3D;
  global.Body3D.buildMesh = buildMesh;
})(typeof window !== 'undefined' ? window : globalThis);
