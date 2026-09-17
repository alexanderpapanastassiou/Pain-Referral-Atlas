# -*- coding: utf-8 -*-
"""SVG silhouettes for the lower-quarter plates.

Anterior / posterior: viewBox 0 0 260 520, midline x = 130. Drawn as a pelvic
block plus two legs; the legs overlap the pelvis at the hip so the join reads
continuous, then diverge below the crotch.

Plantar: viewBox 0 0 260 210, two soles, toes up. Plantar regions matter far
more in the lower quarter than they do in the upper, so they get their own view
rather than being crammed onto the posterior foot.
"""

PELVIS = (
    "M 82,0 L 178,0 "
    "L 185,44 "
    "L 190,86 "
    "C 189,114 184,132 176,144 "
    "L 150,157 "
    "C 140,151 136,141 130,141 "
    "C 124,141 120,151 110,157 "
    "L 84,144 "
    "C 76,132 71,114 70,86 "
    "L 75,44 Z"
)

# leg — patient's right (viewer-left). Down the medial edge, round the foot,
# back up the lateral edge.
LEG = (
    "M 127,104 "
    "L 124,152 "
    "L 120,206 "
    "L 117,258 "
    "L 115,286 "
    "L 113,316 "
    "L 111,362 "
    "L 110,406 "
    "L 111,440 "
    "C 113,454 113,472 110,486 "
    "C 105,500 90,502 84,495 "
    "C 80,488 80,470 82,456 "
    "L 85,440 "
    "L 86,406 "
    "L 87,362 "
    "L 88,316 "
    "L 87,286 "
    "L 84,258 "
    "L 79,206 "
    "L 74,152 "
    "L 70,104 Z"
)

# one sole, toes up — patient's right foot, drawn on the viewer's left
SOLE = (
    "M 75,8 "
    "C 95,8 110,20 111,40 "
    "L 108,70 "
    "C 104,86 100,100 100,120 "
    "L 101,150 "
    "C 103,176 92,197 75,197 "
    "C 58,197 47,176 49,150 "
    "L 50,120 "
    "C 50,100 46,86 42,70 "
    "L 39,40 "
    "C 40,20 55,8 75,8 Z"
)


def mirror_path(d: str, axis: float) -> str:
    """Reflect an absolute-coordinate path about x = axis."""
    out, i, n = [], 0, len(d)
    while i < n:
        ch = d[i]
        if ch.isalpha() or ch in " ,":
            out.append(ch)
            i += 1
            continue
        j = i
        if d[j] in "+-":
            j += 1
        while j < n and (d[j].isdigit() or d[j] == "."):
            j += 1
        num = float(d[i:j])
        if j < n and d[j] == ",":          # x coordinates are followed by a comma
            num = 2 * axis - num
        out.append("%g" % num)
        i = j
    return "".join(out)


SILHOUETTE = {
    "ant":  {"torso": [PELVIS], "limbs": [LEG, mirror_path(LEG, 130)]},
    "post": {"torso": [PELVIS], "limbs": [LEG, mirror_path(LEG, 130)]},
    "plant": {"torso": [], "limbs": [SOLE, mirror_path(SOLE, 130)]},
}
