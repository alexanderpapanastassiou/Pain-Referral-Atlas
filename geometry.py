# -*- coding: utf-8 -*-
"""Region geometry for the lower-quarter plates.

Bands are drawn generously wider than the silhouette (the clipPath trims them)
and are contiguous in y so the painted regions tile without white slivers.

GEO[region_id] = [(view, x, y, w, h, mirror, part), ...]
  view : "ant" | "post" | "plant"
  part : "torso" (clipped to the pelvis) | "limbs" (clipped to the legs/soles)
"""

def _r(view, x, y, x2, y2, mirror=False, part="torso"):
    return (view, x, y, x2 - x, y2 - y, mirror, part)


GEO = {
    # ================= ANTERIOR — pelvis =================
    "lower-abdomen": [_r("ant", 56, 0, 204, 70)],
    "groin":         [_r("ant", 84, 70, 116, 144, True)],
    "pubic":         [_r("ant", 116, 70, 144, 160)],
    "hip-ant":       [_r("ant", 50, 70, 84, 144, True)],

    # ================= ANTERIOR — limb =================
    "troch":      [_r("ant", 0, 104, 96, 172, True, "limbs")],
    "thigh-lat":  [_r("ant", 0, 172, 96, 276, True, "limbs"),
                   _r("post", 0, 142, 88, 276, True, "limbs")],
    "thigh-ant":  [_r("ant", 96, 140, 113, 276, True, "limbs")],
    "thigh-med":  [_r("ant", 113, 140, 140, 276, True, "limbs")],
    "knee-lat":   [_r("ant", 0, 276, 97, 314, True, "limbs")],
    "knee-ant":   [_r("ant", 97, 276, 111, 314, True, "limbs")],
    "knee-med":   [_r("ant", 111, 276, 140, 314, True, "limbs")],
    "leg-lat":    [_r("ant", 0, 314, 98, 438, True, "limbs")],
    "leg-ant":    [_r("ant", 98, 314, 108, 438, True, "limbs")],
    "leg-med":    [_r("ant", 108, 314, 140, 438, True, "limbs")],
    "ankle-lat":  [_r("ant", 0, 438, 97, 466, True, "limbs"),
                   _r("post", 0, 444, 97, 474, True, "limbs")],
    "ankle-ant":  [_r("ant", 97, 438, 109, 466, True, "limbs")],
    "ankle-med":  [_r("ant", 109, 438, 140, 466, True, "limbs"),
                   _r("post", 97, 444, 140, 474, True, "limbs")],
    "foot-dorsum":[_r("ant", 0, 466, 140, 494, True, "limbs")],
    "lat-toes":   [_r("ant", 0, 494, 100, 512, True, "limbs"),
                   _r("plant", 30, 0, 86, 46, True, "limbs")],
    "great-toe":  [_r("ant", 100, 494, 140, 512, True, "limbs"),
                   _r("plant", 86, 0, 120, 46, True, "limbs")],

    # ================= POSTERIOR — pelvis =================
    "tl-junction":   [_r("post", 96, 0, 164, 24)],
    "lumbar":        [_r("post", 96, 24, 118, 62, True)],
    "lumbar-midline":[_r("post", 118, 24, 142, 62)],
    "flank":         [_r("post", 40, 0, 96, 62, True)],
    "iliac-crest":   [_r("post", 40, 62, 220, 82)],
    "si-joint":      [_r("post", 102, 82, 120, 120, True)],
    "sacrum":        [_r("post", 120, 82, 140, 118)],
    "coccyx":        [_r("post", 120, 118, 140, 138)],
    "buttock-upper": [_r("post", 40, 82, 102, 120, True)],
    "buttock-lower": [_r("post", 40, 120, 120, 160, True)],
    "perineum":      [_r("post", 108, 138, 152, 160)],

    # ================= POSTERIOR — limb =================
    "thigh-post": [_r("post", 88, 142, 140, 276, True, "limbs")],
    "knee-post":  [_r("post", 0, 276, 140, 314, True, "limbs")],
    "calf":       [_r("post", 0, 314, 140, 406, True, "limbs")],
    "achilles":   [_r("post", 0, 406, 140, 444, True, "limbs")],

    # ================= PLANTAR =================
    "forefoot-plant": [_r("plant", 30, 46, 120, 92, True, "limbs")],
    "arch":           [_r("plant", 30, 92, 120, 148, True, "limbs")],
    "heel-plantar":   [_r("plant", 30, 148, 120, 210, True, "limbs"),
                       _r("post", 0, 474, 140, 512, True, "limbs")],
}
