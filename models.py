# -*- coding: utf-8 -*-
"""3-D figure specifications for the two referred-pain atlases.

Every body part is a lofted tube described by stations along an axis. All
coordinates are the PLATE coordinates of the matching 2-D atlas (x across,
y down, midline x = 130) with a third axis z pointing anteriorly, so the
figure's front view lines up with the anterior plate and each face can be
labelled by looking up the plate rectangle its centroid falls in.
"""
import sys

def _y(y, cx, cz, rx, rz):
    return {"y": y, "cx": cx, "cz": cz, "rx": rx, "rz": rz}

def _z(z, cx, cy, rx, ry):
    return {"z": z, "cx": cx, "cy": cy, "rx": rx, "ry": ry}


# ============================================================ upper quarter
# plate 260 x 440 — head to mid-thigh
UE_PARTS = [
    {"name": "head", "tag": "torso", "sectors": 32, "step": 6, "capStart": True,
     "stations": [
         _y(10, 130, -3, 4, 5), _y(14, 130, -3, 17, 20), _y(26, 130, -3, 31, 37),
         _y(40, 130, -3, 38, 45), _y(52, 130, -3, 40, 46), _y(64, 130, -2, 38, 44),
         _y(76, 130, -1, 34, 39), _y(88, 130, -1, 26, 29), _y(96, 130, -1, 17, 20),
         _y(101, 130, -2, 13, 15),
     ]},
    {"name": "neck", "tag": "torso", "sectors": 20, "step": 6,
     "stations": [
         _y(88, 130, -4, 15, 14), _y(100, 130, -4, 15, 14), _y(112, 130, -3, 17, 15),
         _y(122, 130, -2, 21, 17),
     ]},
    {"name": "torso", "tag": "torso", "sectors": 44, "step": 9, "capEnd": True,
     "stations": [
         _y(106, 130, -2, 17, 15), _y(118, 130, -1, 31, 19), _y(132, 130, 0, 49, 24),
         _y(142, 130, 0, 55, 26), _y(158, 130, 0, 50, 28), _y(182, 130, 0, 46, 28),
         _y(212, 130, 0, 43, 26), _y(240, 130, 0, 40, 24), _y(286, 130, 0, 39, 23),
         _y(330, 130, 0, 44, 26), _y(352, 130, 0, 43, 27), _y(370, 130, 0, 41, 26),
         _y(380, 130, 0, 38, 24),
     ]},
    {"name": "thigh", "tag": "torso", "mirror": True, "sectors": 18, "step": 8, "capEnd": True,
     "stations": [
         _y(350, 108, 0, 16, 19), _y(372, 106, 0, 20, 21), _y(400, 105, 0, 20, 21),
         _y(418, 105, 0, 19, 20),
     ]},
    {"name": "arm", "tag": "arms", "mirror": True, "sectors": 26, "step": 8,
     "capStart": True, "capEnd": True,
     "stations": [
         _y(124, 86, -1, 8, 10), _y(132, 84, -1, 14, 17), _y(146, 78, -1, 17, 19),
         _y(160, 72, -1, 16, 18), _y(182, 65.5, -1, 13, 15), _y(232, 60.5, -1, 12, 14),
         _y(254, 57, -1, 12, 14), _y(282, 54.5, 0, 11.5, 12.5), _y(330, 49, 1, 12, 11),
         _y(354, 45.5, 2, 11, 8.5), _y(368, 42, 2, 16, 7), _y(382, 40, 2, 22, 6.5),
         _y(398, 40, 2, 21, 6), _y(412, 43, 2, 15, 5), _y(424, 46, 2, 7, 4),
     ]},
]

UE_SPEC = {
    "mid": 130, "snap": 10,
    "yaw0": 24, "pitch0": 6, "zoom0": 1,
    "views": [["Front", 0, 0], ["Back", 180, 0], ["Left", -90, 0], ["Right", 90, 0], ["Hands", 20, 20, 2.0, 385]],
    "parts": UE_PARTS,
}

# ============================================================ lower quarter
# plate 260 x 520 — lower trunk to toes, plus plantar plate 260 x 210
LQ_PARTS = [
    {"name": "trunk", "tag": "torso", "sectors": 44, "step": 9, "capStart": True, "capEnd": True,
     "stations": [
         _y(0, 130, 0, 48, 26), _y(20, 130, 0, 50, 26), _y(44, 130, 0, 55, 28),
         _y(86, 130, 0, 63, 32), _y(120, 130, 0, 62, 32), _y(144, 130, 0, 58, 30),
         _y(152, 130, 0, 52, 28), _y(162, 130, 0, 38, 24),
     ]},
    {"name": "leg", "tag": "limbs", "mirror": True, "sectors": 26, "step": 9,
     "stations": [
         _y(92, 100, 0, 23, 25), _y(104, 98.5, 0, 26, 27), _y(152, 99, 0, 25, 26),
         _y(206, 99.5, 0, 20.5, 22), _y(258, 100.5, 0, 16.5, 18), _y(286, 101, 0, 14, 15.5),
         _y(316, 100.5, 0, 12.5, 15), _y(362, 99, -1, 12, 14), _y(406, 98, -1, 11, 12),
         _y(440, 98, 0, 12, 12), _y(478, 98, 3, 11, 12),
     ]},
    {"name": "foot", "tag": "foot", "mirror": True, "axis": "z", "sectors": 20, "step": 4,
     "capStart": True, "capEnd": True,
     "stations": [
         _z(-20, 98, 491, 0.6, 0.6), _z(-18, 98, 490, 8, 8), _z(-12, 98, 489, 13, 12), _z(0, 98, 488, 15, 13),
         _z(14, 98, 490, 17, 11), _z(26, 98, 494, 17, 8), _z(36, 98, 497, 14, 5),
         _z(40, 98, 499, 6, 2.5),
     ]},
]

LQ_SPEC = {
    "mid": 130, "snap": 10,
    "yaw0": 24, "pitch0": 6, "zoom0": 1,
    "views": [["Front", 0, 0], ["Back", 180, 0], ["Left", -90, 0], ["Right", 90, 0], ["Feet", 30, 28, 2.2, 470], ["Soles", 180, -74, 1.9, 505]],
    "foot": {"tags": ["foot"], "as": "limbs", "zHeel": -20, "zToe": 40,
             "plantY": [197, 8], "antY": [466, 512]},
    "parts": LQ_PARTS,
}


# ============================================================ whole body
# One figure for every atlas. World frame = the UE plate frame (head at y≈10,
# crotch at y≈372). Lower-quarter parts are authored in LE plate coordinates and
# placed with a frame; plate lookups run back through the same frames, so each
# face still takes its label from the 2-D atlas that owns that part of the body.
LQ_LEG_FRAME   = {"sx": 0.8,  "sy": 1.0,   "oy": 215}    # LE y 157 (crotch) → 372
LQ_TRUNK_FRAME = {"sx": 0.74, "sy": 0.713, "oy": 260}    # LE y 0 (T-L jn) → 260, 157 → 372
UE_LQ_SPLIT = 260                                         # world y where trunk labels switch to the LE plates

def _face_features():
    """Schematic facial features on the UE head (centre y 52, rx 40, rz 46)."""
    return [
        {"name": "eye", "tag": "torso", "mirror": True, "sectors": 12, "step": 3, "tint": "ink",
         "region": "frontal", "bind": [], "capStart": True, "capEnd": True,
         "stations": [_y(51, 116, 40, 2, 1.4), _y(54, 116, 41, 4.6, 2.4), _y(57, 116, 40, 2, 1.4)]},
        {"name": "brow", "tag": "torso", "mirror": True, "sectors": 10, "step": 3, "tint": "ink",
         "region": "frontal", "bind": [], "capStart": True, "capEnd": True,
         "stations": [_y(45.5, 116, 39.5, 5, 0.8), _y(47, 116, 40.5, 7, 1.1), _y(48.5, 116, 39.5, 5, 0.8)]},
        {"name": "nose", "tag": "torso", "axis": "z", "sectors": 12, "step": 4, "region": "face", "bind": [],
         "capEnd": True,
         "stations": [_z(36, 130, 63, 5.5, 6.5), _z(44, 130, 66, 5, 6), _z(50, 130, 69.5, 3.4, 3.6), _z(53, 130, 71, 1, 1)]},
        {"name": "mouth", "tag": "torso", "sectors": 12, "step": 2, "tint": "ink", "region": "face", "bind": [],
         "capStart": True, "capEnd": True,
         "stations": [_y(80.5, 130, 32.5, 7, 1.0), _y(82, 130, 34.5, 10.5, 1.5), _y(83.5, 130, 32.5, 7, 1.0)]},
        {"name": "ear", "tag": "torso", "mirror": True, "sectors": 12, "step": 4, "region": "ear", "bind": [],
         "capStart": True, "capEnd": True,
         "stations": [_y(51, 89.5, -4, 2.2, 4), _y(56, 87.5, -4, 4.4, 7), _y(66, 87.5, -3, 4.4, 7), _y(72, 89.5, -3, 2.2, 4)]},
    ]


def full_parts(upper_bind, trunk_bind, lower_bind, face_regions=True):
    """Whole-body parts. *_bind are binding lists for the UE-authored upper
    parts, the trunk, and the LE-authored legs and feet."""
    P = []
    def part(src, **over):
        p = dict(src); p.update(over); return p
    head, neck, torso, thigh, arm = UE_PARTS
    P.append(part(head, bind=upper_bind))
    P.extend(_face_features() if face_regions else [dict(f, region=None) for f in _face_features()])
    P.append(part(neck, bind=upper_bind))
    # pelvis deepened a little so the leg tops sit inside it
    torso_st = list(torso["stations"][:9]) + [
        _y(330, 130, 0, 44, 29), _y(352, 130, 0, 44, 30), _y(370, 130, 0, 42, 29), _y(380, 130, 0, 39, 27)]
    P.append(part(torso, stations=torso_st, bind=trunk_bind))
    P.append(part(arm, bind=upper_bind))
    trunk, leg, foot = LQ_PARTS
    P.append(part(leg, frame=LQ_LEG_FRAME, bind=lower_bind))
    P.append(part(foot, frame=LQ_LEG_FRAME, bind=lower_bind))
    return P


FULL_VIEWS = [["Front", 0, 0], ["Back", 180, 0], ["Left", -90, 0], ["Right", 90, 0],
              ["Head", 25, 8, 2.6, 60], ["Hands", 20, 20, 2.2, 385],
              ["Feet", 30, 28, 2.2, 690], ["Soles", 180, -74, 2.0, 725]]

LQ_FOOT = {"tags": ["foot"], "as": "limbs", "zHeel": -20, "zToe": 40, "plantY": [197, 8], "antY": [466, 512]}


def plates_from_ue(geo, arm_regions, mid_w=260):
    """UE GEO: {rid: [(view,x,y,w,h,mirror),...]} -> {view: [[rid,x,y,w,h,part],...]}"""
    out = {"ant": [], "post": []}
    for rid, shapes in geo.items():
        part = "arms" if rid in arm_regions else "torso"
        for (v, x, y, w, h, mirror) in shapes:
            out[v].append([rid, x, y, w, h, part])
            if mirror:
                out[v].append([rid, mid_w - x - w, y, w, h, part])
    return out


def plates_from_lq(geo, mid_w=260):
    """LQ GEO: {rid: [(view,x,y,w,h,mirror,part),...]} -> {view: [[rid,x,y,w,h,part],...]}"""
    out = {"ant": [], "post": [], "plant": []}
    for rid, shapes in geo.items():
        for (v, x, y, w, h, mirror, part) in shapes:
            out[v].append([rid, x, y, w, h, part])
            if mirror:
                out[v].append([rid, mid_w - x - w, y, w, h, part])
    return out


ARM_REGIONS = {
    "deltoid-lat", "deltoid-ant", "deltoid-post", "arm-ant", "arm-med", "arm-post",
    "elbow-lat", "elbow-ant", "elbow-med", "elbow-post",
    "forearm-rad", "forearm-volar", "forearm-uln", "forearm-dors",
    "wrist", "thenar", "palm", "digits-rad", "digits-uln", "hand-dors", "web-space",
}


import pathlib as _pathlib
SRC = _pathlib.Path(__file__).resolve().parent.parent


def _load(path, name):
    import importlib.util
    s = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m


def _ue_plates():
    G = _load(SRC / "upper" / "geometry.py", "ue_geometry")
    return plates_from_ue(G.GEO, ARM_REGIONS)


def _lq_plates():
    G = _load(SRC / "lower" / "geometry.py", "lq_geometry")
    p = plates_from_lq(G.GEO)
    # the 2-D plates draw the pelvis block over the top of each thigh; the 3-D
    # thigh surface there needs a label of its own
    for rid, v, x, y, x2, y2 in [
        ("buttock-lower", "post", 88, 100, 140, 142),
        ("troch", "post", 0, 100, 88, 142),
        ("thigh-ant", "ant", 96, 104, 113, 140),
        ("thigh-med", "ant", 113, 104, 140, 140),
    ]:
        p[v].append([rid, x, y, x2 - x, y2 - y, "limbs"])
        p[v].append([rid, 260 - x2, y, x2 - x, y2 - y, "limbs"])
    p["foot"] = LQ_FOOT
    return p


def _full_spec(upper_bind, trunk_bind, lower_bind, plate_sets, views=None, face_regions=True):
    return {"mid": 130, "snap": 10, "yaw0": 24, "pitch0": 6, "zoom0": 1,
            "views": views or FULL_VIEWS, "plateSets": plate_sets,
            "parts": full_parts(upper_bind, trunk_bind, lower_bind, face_regions)}


def ue_spec():
    """UE atlas: whole figure, upper-quarter zones live, legs neutral."""
    ue = [{"set": "ue"}]
    return _full_spec(ue, ue, [], {"ue": _ue_plates()}, [v for v in FULL_VIEWS if v[0] not in ("Feet", "Soles")])


def lq_spec():
    """LE atlas: whole figure, lower-quarter zones live, head/arms neutral."""
    lq = [{"set": "lq", "frame": LQ_LEG_FRAME}]
    trunk = [{"set": "lq", "frame": LQ_TRUNK_FRAME}]
    return _full_spec([], trunk, lq, {"lq": _lq_plates()}, [v for v in FULL_VIEWS if v[0] not in ("Head", "Hands")], face_regions=False)


def whole_spec():
    """Combined atlas: UE plates above the thoracolumbar junction, LE plates below."""
    ue = [{"set": "ue"}]
    lq = [{"set": "lq", "frame": LQ_LEG_FRAME}]
    trunk = [{"set": "ue", "yMax": UE_LQ_SPLIT}, {"set": "lq", "frame": LQ_TRUNK_FRAME}]
    return _full_spec(ue, trunk, lq, {"ue": _ue_plates(), "lq": _lq_plates()})


if __name__ == "__main__":
    import json
    json.dump({"ue": ue_spec(), "lq": lq_spec(), "whole": whole_spec()}, open(_pathlib.Path(__file__).resolve().parent / "specs.json", "w"))
    print("wrote specs.json")
