# -*- coding: utf-8 -*-
"""Shared dataset for the referred-pain library: regions, structures, referral maps."""

# ---------------------------------------------------------------------------
# EVIDENCE TIERS
# ---------------------------------------------------------------------------
TIERS = {
    "A": {
        "label": "A — Experimental map, asymptomatic volunteers",
        "short": "A",
        "desc": "Referral zone produced by controlled provocation (intra-articular distension or "
                "injection) in asymptomatic volunteers, then charted. The strongest design available "
                "for referred-pain mapping: the zone is caused, not merely observed.",
    },
    "B": {
        "label": "B — Provocation mapping in symptomatic patients",
        "short": "B",
        "desc": "Referral zone produced by provocation (discography, intra-articular stimulation, "
                "nerve root stimulation) in patients who already have pain. Real experimental data, "
                "but the population is sensitised and no asymptomatic control arm exists.",
    },
    "C": {
        "label": "C — Clinical observation / expert synthesis",
        "short": "C",
        "desc": "Zone compiled from unblinded clinical case observation rather than controlled "
                "provocation. Useful for generating hypotheses; not validated diagnostic anatomy. "
                "Most myofascial referral maps sit here.",
    },
}

# ---------------------------------------------------------------------------
# BODY REGIONS
# geometry: list of (view, kind, coords, mirror)
#   view  : "ant" | "post"
#   kind  : "rect"  coords = (x, y, w, h)
#   mirror: True -> also emit the shape reflected about x = 120
# ---------------------------------------------------------------------------
REGIONS = [
    # ---- head -------------------------------------------------------------
    ("vertex",        "Vertex / top of head",            [("ant","rect",(60,12,120,26),False),
                                                          ("post","rect",(60,12,120,26),False)]),
    ("frontal",       "Frontal / supraorbital / retro-orbital", [("ant","rect",(96,38,48,28),False)]),
    ("temporal",      "Temporal / side of head",         [("ant","rect",(60,38,36,20),True),
                                                          ("post","rect",(60,38,36,20),True)]),
    ("ear",           "Ear / retromastoid",              [("ant","rect",(60,58,36,24),True)]),
    ("face",          "Face / cheek / jaw",              [("ant","rect",(96,66,48,34),False)]),
    ("occiput",       "Occiput",                         [("post","rect",(90,38,60,32),False)]),
    ("suboccipital",  "Suboccipital",                    [("post","rect",(92,70,56,22),False)]),

    # ---- neck -------------------------------------------------------------
    ("neck-ant",      "Anterior neck / throat",          [("ant","rect",(100,100,40,20),False)]),
    ("neck-upper",    "Upper posterior neck",            [("post","rect",(96,92,48,16),False)]),
    ("neck-mid",      "Mid posterior neck",              [("post","rect",(96,108,48,14),False)]),
    ("neck-lower",    "Lower posterior neck",            [("post","rect",(94,122,52,20),False)]),

    # ---- shoulder girdle --------------------------------------------------
    ("shoulder-top",  "Top of shoulder / suprascapular", [("ant","rect",(56,112,48,26),True),
                                                          ("post","rect",(56,112,48,28),True)]),
    ("scap-sup",      "Superior angle of scapula",       [("post","rect",(76,142,28,24),True)]),
    ("interscap",     "Interscapular / upper thoracic paraspinal", [("post","rect",(104,142,32,64),False)]),
    ("scap-border",   "Vertebral border of scapula",     [("post","rect",(76,166,28,50),True)]),
    ("scap-inf",      "Inferior angle of scapula",       [("post","rect",(80,216,24,24),True)]),

    # ---- chest / trunk ----------------------------------------------------
    ("chest-ant",     "Anterior chest / precordial / breast", [("ant","rect",(92,138,56,62),False)]),
    ("chest-lat",     "Lateral chest wall / axillary line",   [("ant","rect",(66,138,26,62),True)]),
    ("epigastric",    "Epigastric / upper abdomen",      [("ant","rect",(78,200,84,50),False)]),
    ("abd-lower",     "Lower abdomen",                   [("ant","rect",(78,250,84,62),False)]),
    ("groin",         "Groin / inguinal",                [("ant","rect",(74,312,38,70),True)]),
    ("thoracic-mid",  "Mid thoracic paraspinal (T5–T8)", [("post","rect",(96,206,48,44),False)]),
    ("thoracolumbar", "Thoracolumbar junction (T9–T12)", [("post","rect",(94,250,52,42),False)]),
    ("flank",         "Flank / lateral trunk",           [("post","rect",(72,206,24,86),True)]),
    ("lumbar",        "Lumbar / low back",               [("post","rect",(92,292,56,48),False)]),
    ("si-buttock",    "Sacroiliac / buttock",            [("post","rect",(74,340,44,60),True)]),

    # ---- shoulder / arm ---------------------------------------------------
    ("deltoid-ant",   "Anterior deltoid / anterior shoulder", [("ant","rect",(52,128,28,52),True)]),
    ("deltoid-lat",   "Lateral deltoid / lateral shoulder",   [("ant","rect",(24,128,28,52),True)]),
    ("deltoid-post",  "Posterior deltoid / posterior shoulder",[("post","rect",(26,128,52,52),True)]),
    ("arm-ant",       "Anterior / lateral upper arm",    [("ant","rect",(28,180,30,62),True)]),
    ("arm-med",       "Medial upper arm",                [("ant","rect",(58,180,24,62),True)]),
    ("arm-post",      "Posterior upper arm",             [("post","rect",(28,180,54,62),True)]),

    # ---- elbow ------------------------------------------------------------
    ("elbow-lat",     "Lateral epicondyle / lateral elbow", [("ant","rect",(22,242,22,26),True),
                                                             ("post","rect",(20,242,18,26),True)]),
    ("elbow-ant",     "Antecubital / anterior elbow",    [("ant","rect",(44,242,20,26),True)]),
    ("elbow-med",     "Medial epicondyle / medial elbow",[("ant","rect",(64,242,20,26),True)]),
    ("elbow-post",    "Olecranon / posterior elbow",     [("post","rect",(38,242,40,26),True)]),

    # ---- forearm ----------------------------------------------------------
    ("forearm-rad",   "Dorsoradial forearm",             [("ant","rect",(16,268,22,70),True)]),
    ("forearm-volar", "Volar forearm",                   [("ant","rect",(38,268,20,70),True)]),
    ("forearm-uln",   "Ulnar forearm",                   [("ant","rect",(58,268,24,70),True)]),
    ("forearm-dors",  "Dorsal forearm",                  [("post","rect",(16,268,66,70),True)]),

    # ---- wrist / hand -----------------------------------------------------
    ("wrist",         "Wrist",                           [("ant","rect",(10,338,72,16),True),
                                                          ("post","rect",(10,338,72,16),True)]),
    ("thenar",        "Thumb / thenar eminence",         [("ant","rect",(4,354,26,40),True)]),
    ("palm",          "Palm",                            [("ant","rect",(30,354,32,28),True)]),
    ("digits-rad",    "Radial digits (index, middle)",   [("ant","rect",(26,382,22,32),True)]),
    ("digits-uln",    "Ulnar digits (ring, little)",     [("ant","rect",(48,382,22,32),True)]),
    ("hand-dors",     "Dorsum of hand",                  [("post","rect",(26,354,44,60),True)]),
    ("web-space",     "Thumb–index web space",           [("post","rect",(2,354,24,40),True)]),
]

REGION_LABEL = {r[0]: r[1] for r in REGIONS}

# ---------------------------------------------------------------------------
# STRUCTURES
# Each: id, name, category, tier, source, note (differentiating clinical note),
#       zones = {region_id: intensity}   intensity 3=primary 2=common 1=spillover
# ---------------------------------------------------------------------------

CATEGORIES = [
    ("facet",    "Zygapophysial (facet) joint"),
    ("disc",     "Intervertebral disc"),
    ("root",     "Nerve root (dynatome)"),
    ("ligament", "Spinal ligament"),
    ("joint",    "Peripheral joint / bursa"),
    ("muscle",   "Muscle (myofascial)"),
]

S = []  # structures

def add(sid, name, cat, tier, source, note, zones, lookalikes=""):
    S.append(dict(id=sid, name=name, cat=cat, tier=tier, source=source,
                  note=note, zones=zones, lookalikes=lookalikes))

# ===========================================================================
# FACET JOINTS
# ===========================================================================
add("facet-c0c1", "C0–C1 atlanto-occipital joint", "facet", "A",
    "Dreyfuss, Michaelsen & Fletcher, Spine 1994 — provocative intra-articular injection, "
    "5 asymptomatic volunteers.",
    "Consistently suboccipital; may extend cephalad toward the vertex and occasionally the frontal region. "
    "Very small volunteer sample (N=5) — treat the zone as indicative, not precise.",
    {"suboccipital": 3, "occiput": 2, "vertex": 1, "frontal": 1, "neck-upper": 2})

add("facet-c1c2", "C1–C2 lateral atlanto-axial joint", "facet", "A",
    "Dreyfuss et al., Spine 1994 (N=5 volunteers); clinical validation by controlled blocks — "
    "Aprill, Axinn & Bogduk, Cephalalgia 2002 (21/34 patients confirmed).",
    "Discrete unilateral pain at the occipito-cervical junction, retromastoid area and upper cervical region. "
    "Aprill's clinical criteria (occipital pain + focal C1 transverse process tenderness + restricted rotation) "
    "had only 60% positive predictive value — distribution alone cannot substitute for a diagnostic block.",
    {"occiput": 3, "suboccipital": 3, "ear": 2, "neck-upper": 2})

add("facet-c2c3", "C2–C3 facet joint (third occipital nerve)", "facet", "A",
    "Dwyer, Aprill & Bogduk, Spine 1990 — volunteer distension; validated clinically in Aprill et al. 1990; "
    "Lord et al., JNNP 1994 — controlled double-blind blocks.",
    "Upper neck pain extending into the head — toward the ear, vertex, forehead or eye. The most common "
    "source of headache after whiplash: third occipital nerve headache found in 27% of whiplash patients "
    "overall and 53% of those whose dominant complaint was headache.",
    {"neck-upper": 3, "occiput": 3, "suboccipital": 2, "ear": 2, "vertex": 2, "frontal": 1, "temporal": 1},
    "Cervicogenic headache from C1–2; occipital neuralgia; migraine")

add("facet-c3c4", "C3–C4 facet joint", "facet", "A",
    "Dwyer, Aprill & Bogduk, Spine 1990 — volunteer distension; corroborated in symptomatic patients by "
    "Fukui et al., Pain 1996.",
    "Neck pain from the suboccipital region down to the lower neck — characteristically WITHOUT shoulder "
    "involvement. That absence is the useful discriminator from C4–5 and below.",
    {"neck-upper": 3, "neck-mid": 3, "neck-lower": 2, "occiput": 2, "suboccipital": 1})

add("facet-c4c5", "C4–C5 facet joint", "facet", "A",
    "Dwyer, Aprill & Bogduk, Spine 1990 — volunteer distension; Fukui et al., Pain 1996.",
    "More caudally located than C3–4: top of the shoulder and the lower part of the neck. Fukui found "
    "lower posterior cervical in 76% and suprascapular in 43% of symptomatic patients.",
    {"neck-lower": 3, "neck-mid": 2, "shoulder-top": 3, "scap-sup": 1})

add("facet-c5c6", "C5–C6 facet joint", "facet", "A",
    "Dwyer, Aprill & Bogduk, Spine 1990 — volunteer distension; Fukui et al., Pain 1996; prevalence "
    "data from Cooper, Bailey & Bogduk, Pain Medicine 2007.",
    "Lower neck, top of the scapula and the shoulder region above the level of the scapular spine. "
    "Together with C2–3, one of the two most frequently implicated levels in chronic neck pain "
    "(~35% of cases).",
    {"neck-lower": 3, "shoulder-top": 3, "scap-sup": 2, "deltoid-post": 1, "interscap": 1})

add("facet-c6c7", "C6–C7 facet joint", "facet", "A",
    "Dwyer, Aprill & Bogduk, Spine 1990 — volunteer distension; Fukui et al., Pain 1996.",
    "Extends caudally as far as the scapular spine. Fukui: superior scapular angle 48%, mid-scapular 41%, "
    "lower posterior cervical 33%.",
    {"scap-sup": 3, "interscap": 3, "neck-lower": 2, "shoulder-top": 2, "scap-border": 1})

add("facet-c7t1", "C7–T1 facet joint", "facet", "B",
    "Fukui et al., Pain 1996 — intra-articular contrast/dorsal ramus stimulation in 61 SYMPTOMATIC "
    "patients. Not covered by the Dwyer volunteer study.",
    "Mid-scapular region in 86% of patients; superior angle of scapula in 28%. Note this level rests on "
    "patient-provocation data only — a tier below the C2–3 to C6–7 volunteer maps.",
    {"interscap": 3, "scap-border": 2, "scap-sup": 2, "neck-lower": 1})

add("facet-tupper", "Upper thoracic facet joints (T1–T4)", "facet", "B",
    "Fukui et al., Reg Anesth 1997 (symptomatic patients, T1–2/T2–3); Dreyfuss, Tibiletti & Dreyer, "
    "Spine 1994 (volunteers, from T3–4 down).",
    "Local paraspinal pain lateral to the joint, from about half a segment above to a full segment below "
    "the joint of origin. Does not cross the midline and does not reliably distinguish adjacent levels.",
    {"interscap": 3, "scap-border": 2, "scap-sup": 1, "neck-lower": 1})

add("facet-tmid", "Mid thoracic facet joints (T5–T8)", "facet", "A",
    "Dreyfuss, Tibiletti & Dreyer, Spine 1994 — distension in asymptomatic volunteers (T3–4 to T10–11).",
    "Local paraspinal zone lateral to the joint, half a segment above to one segment below. IMPORTANT: "
    "27% of injected joints produced no pain at all, and the resulting patterns overlap heavily with "
    "costotransverse joint and soft-tissue patterns — thoracic maps are far less segment-discriminating "
    "than the cervical ones.",
    {"thoracic-mid": 3, "interscap": 2, "flank": 1})

add("facet-tlower", "Lower thoracic facet joints (T9–T12)", "facet", "B",
    "Dreyfuss et al., Spine 1994 — volunteers, but only as far down as T10–11; Fukui et al., "
    "Reg Anesth 1997 — T11–12, symptomatic patients only.",
    "Paraspinal pain at and just below the segment, with modest lateral spread into the flank. "
    "Graded B rather than A because the range is split: T9–10 and T10–11 have volunteer-provocation "
    "evidence, but T11–12 rests on symptomatic-patient data alone. Same caveat as the rest of the "
    "thoracic spine: granular per-segment diagrams circulating in handouts are illustrative "
    "composites, not something either primary study reports.",
    {"thoracolumbar": 3, "thoracic-mid": 2, "flank": 2, "lumbar": 1})

# ===========================================================================
# DISCS
# ===========================================================================
add("disc-c2c3", "C2–C3 intervertebral disc", "disc", "B",
    "Schellhas et al., AJNR 2000 — provocation discography, 40 chronic head/neck pain patients; "
    "Slipman et al., Spine J 2005 (41 subjects, 101 maps).",
    "Head pain is disproportionately a C2–3 phenomenon: 19/40 reported head pain (occipital most common, "
    "then temporal, then parietal) and 4 patients had EXCLUSIVELY head pain with no neck component. "
    "80% of painful C2–3 discs looked normal on MRI.",
    {"occiput": 3, "neck-upper": 3, "suboccipital": 2, "temporal": 2, "vertex": 2, "face": 1})

add("disc-c3c4", "C3–C4 intervertebral disc", "disc", "B",
    "Slipman et al., Spine J 2005 (19 maps); Grubb & Kelly, Spine 2000.",
    "Neck, subocciput, trapezius, anterior neck, face, shoulder, interscapular and limb — one of the "
    "broadest referral fields of any cervical disc.",
    {"neck-mid": 3, "neck-upper": 2, "shoulder-top": 2, "interscap": 2, "suboccipital": 1,
     "neck-ant": 1, "face": 1, "deltoid-ant": 1})

add("disc-c4c5", "C4–C5 intervertebral disc", "disc", "B",
    "Slipman et al., Spine J 2005 (27 maps); Grubb & Kelly, Spine 2000.",
    "Neck, shoulder, interscapular, trapezius, extremity, face, chest, subocciput. Grubb & Kelly found "
    "anterior chest wall referral begins at this level.",
    {"neck-lower": 3, "shoulder-top": 3, "interscap": 2, "scap-sup": 2, "chest-ant": 1,
     "deltoid-ant": 1, "arm-ant": 1})

add("disc-c5c6", "C5–C6 intervertebral disc", "disc", "B",
    "Slipman et al., Spine J 2005 (27 maps); Grubb & Kelly, Spine 2000.",
    "Neck, trapezius, interscapular, subocciput, anterior neck, chest, face. Bilateral pain occurred in "
    "30–62% of discs at every level — laterality of pain does NOT indicate laterality of pathology.",
    {"neck-lower": 3, "shoulder-top": 3, "interscap": 2, "chest-ant": 2, "scap-sup": 2,
     "deltoid-ant": 1, "arm-ant": 1})

add("disc-c6c7", "C6–C7 intervertebral disc", "disc", "B",
    "Slipman et al., Spine J 2005 (16 maps); Grubb & Kelly, Spine 2000.",
    "Neck, interscapular, trapezius, shoulder, extremity, subocciput. Arm referral is most consistent "
    "at this level and C5–6.",
    {"interscap": 3, "neck-lower": 2, "shoulder-top": 2, "scap-border": 2, "arm-ant": 1,
     "forearm-rad": 1, "chest-ant": 1})

add("disc-c7t1", "C7–T1 intervertebral disc", "disc", "B",
    "Grubb & Kelly, Spine 2000; Slipman et al., Spine J 2005 (only 2 maps at this level).",
    "Mid-posterior neck through to the mid-thoracic spine, and the interscapular region. Very few mapped "
    "cases — the weakest-supported of the cervical disc levels.",
    {"interscap": 3, "neck-lower": 2, "thoracic-mid": 2})

# ===========================================================================
# NERVE ROOTS (DYNATOMES)
# ===========================================================================
add("root-c4", "C4 nerve root (dynatome)", "root", "B",
    "Slipman et al., Spine 1998 — fluoroscopically guided cervical nerve root stimulation, "
    "134 stimulations in 87 subjects (only 4 at C4).",
    "Base of neck and top of shoulder. Only 4 stimulations at this level — the least-supported root map.",
    {"neck-lower": 3, "shoulder-top": 3, "scap-sup": 1})

add("root-c5", "C5 nerve root (dynatome)", "root", "B",
    "Slipman et al., Spine 1998 (14 stimulations at C5).",
    "Lateral shoulder and lateral arm. NOTE: dynatomal (symptom) maps are measurably broader than "
    "textbook dermatomes — the expected pattern held in as little as 54% of stimulations.",
    {"deltoid-lat": 3, "shoulder-top": 2, "arm-ant": 2, "neck-lower": 2, "deltoid-ant": 1})

add("root-c6", "C6 nerve root (dynatome)", "root", "B",
    "Slipman et al., Spine 1998 (43 stimulations at C6).",
    "Lateral arm, dorsoradial forearm, thumb and index finger — but ~30% of C6 stimulations also produced "
    "LITTLE FINGER symptoms, classically a C8 finding. Intrathecal anastomoses between adjacent dorsal "
    "roots (up to ~61%) blur segment-specific territories.",
    {"forearm-rad": 3, "thenar": 3, "digits-rad": 2, "arm-ant": 2, "deltoid-lat": 2,
     "neck-lower": 2, "digits-uln": 1, "scap-sup": 1},
    "C7 root; radial tunnel; de Quervain's; carpal tunnel")

add("root-c7", "C7 nerve root (dynatome)", "root", "B",
    "Slipman et al., Spine 1998 (52 stimulations at C7 — the largest subgroup).",
    "Posterior arm, dorsal forearm, middle finger, and prominent interscapular/scapular referral. "
    "Proximal (scapular) referral is far more common in dynatomal maps than dermatome charts suggest.",
    {"forearm-dors": 3, "digits-rad": 3, "arm-post": 2, "interscap": 2, "scap-border": 2,
     "hand-dors": 2, "elbow-post": 1})

add("root-c8", "C8 nerve root (dynatome)", "root", "B",
    "Slipman et al., Spine 1998 (21 stimulations at C8).",
    "Ulnar forearm, ring and little fingers — but ~24% of C8 stimulations produced INDEX FINGER symptoms, "
    "classically a C6/C7 finding. Symptom location does not reliably localise the root.",
    {"digits-uln": 3, "forearm-uln": 3, "arm-med": 2, "elbow-med": 2, "interscap": 1, "digits-rad": 1},
    "Cubital tunnel; Guyon's canal; neurogenic thoracic outlet syndrome")

# ===========================================================================
# LIGAMENTS
# ===========================================================================
add("lig-cerv-isl", "Cervical interspinous ligaments", "ligament", "C",
    "Kellgren, Clin Sci 1939 — hypertonic saline injection in volunteers; replicated in principle by "
    "Feinstein et al. 1954.",
    "Deep, diffuse, segmentally-organised ache in the neck and shoulder girdle that does NOT follow "
    "dermatomes. Foundational but small-N, non-blinded 1930s–50s work; Inman & Saunders noted the "
    "resulting maps 'could not be given with any great precision'.",
    {"neck-mid": 3, "neck-lower": 3, "shoulder-top": 2, "interscap": 2, "occiput": 1})

add("lig-thor-isl", "Thoracic interspinous ligaments", "ligament", "C",
    "Kellgren, Clin Sci 1939; Feinstein et al. 1954.",
    "Segmental paraspinal ache with lateral spread around the chest wall. Superficial structures "
    "(supraspinous ligament, spinous process) give sharply localised pain instead — the depth of the "
    "structure, not its level, determines whether pain refers.",
    {"interscap": 2, "thoracic-mid": 3, "thoracolumbar": 2, "flank": 2, "chest-lat": 1})

# ===========================================================================
# PERIPHERAL JOINTS
# ===========================================================================
add("joint-acj", "Acromioclavicular joint", "joint", "A",
    "Gerber, Galantay & Hersche, JSES 1998 — hypertonic saline injection mapping in asymptomatic "
    "volunteers. (Sample size not verifiable from open sources.)",
    "Burning pain over the joint itself, deep in the supraspinatus fossa and upper trapezius, sometimes "
    "extending to the anterolateral deltoid and anterolateral neck. Can convincingly mimic cervical or "
    "trapezius myofascial pain.",
    {"shoulder-top": 3, "scap-sup": 2, "deltoid-ant": 2, "neck-lower": 1, "deltoid-lat": 1},
    "Upper trapezius myofascial pain; C4–5/C5–6 facet; cervical radiculopathy")

add("joint-subacromial", "Subacromial space / bursa", "joint", "A",
    "Gerber, Galantay & Hersche, JSES 1998 — hypertonic saline injection in asymptomatic volunteers.",
    "Intense pain at the lateral border of the acromion and over the lateral deltoid — a more focal and "
    "more distal pattern than AC joint referral. This is the classic 'impingement' distribution.",
    {"deltoid-lat": 3, "shoulder-top": 2, "arm-ant": 1},
    "C5 radiculopathy; supraspinatus/infraspinatus myofascial referral; axillary nerve entrapment")

add("joint-sij", "Sacroiliac joint", "joint", "A",
    "Fortin, Dwyer, West & Pier, Spine 1994 — two-part injection/arthrography study, asymptomatic "
    "volunteers (Part I) and clinical evaluation (Part II).",
    "A consistent buttock zone approximately 10 cm inferior and 3 cm lateral to the PSIS. (Not to be "
    "confused with the Fortin finger test, a separate clinical manoeuvre in which the patient points to a "
    "spot within about 1 cm of the PSIS.) In symptomatic patients the pattern was far more variable, "
    "ranging to frank radicular leg pain. The zone is NOT specific — it overlaps lumbar-referred pain.",
    {"si-buttock": 3, "lumbar": 2})

# ===========================================================================
# MUSCLES — neck / shoulder girdle
# ===========================================================================
add("m-upper-trap", "Upper trapezius", "muscle", "C",
    "Zone map: Travell & Simons Vol. 1 (clinical observation). Referral DIRECTION separately corroborated "
    "by controlled hypertonic saline injection in healthy volunteers (Graven-Nielsen, Arendt-Nielsen et al.).",
    "Posterolateral neck up to the temple — the classic unilateral 'tension headache' pattern — and the "
    "angle of the jaw. Spillover to occiput and mastoid. One of only two muscles here whose referral "
    "DIRECTION has independent experimental support; the grade stays C because the mapped zone borders "
    "still come from clinical observation, and the saline work corroborates direction, not extent.",
    {"neck-lower": 3, "neck-mid": 2, "temporal": 3, "face": 2, "occiput": 2, "shoulder-top": 2, "ear": 1},
    "C2–3 facet; cervicogenic headache; migraine")

add("m-mid-trap", "Middle trapezius", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Superficial burning ache between the vertebral border of the scapula and the spine, locally over C7–T3.",
    {"interscap": 3, "scap-border": 2, "shoulder-top": 1, "neck-lower": 1})

add("m-low-trap", "Lower trapezius", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Local ache at the T6–T9 paraspinal origin and over the top of the shoulder, with spillover to the "
    "base of the neck and mastoid — Travell & Simons specifically flag this 'far' referral as atypical.",
    {"thoracic-mid": 3, "shoulder-top": 2, "interscap": 2, "neck-lower": 2, "occiput": 1})

add("m-levator-scap", "Levator scapulae", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Angle of the neck (the neck–shoulder junction) and along the vertebral border of the scapula to its "
    "inferior angle. Classically limits cervical rotation toward the painful side.",
    {"neck-lower": 3, "shoulder-top": 2, "scap-border": 3, "scap-sup": 2, "deltoid-post": 1})

add("m-scm", "Sternocleidomastoid (both heads)", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Sternal head: vertex, cheek/malar region, supraorbital ridge, deep in the ear, pharynx (sore-throat "
    "sensation), sternum. Clavicular head: bilateral frontal headache, deep ear pain, plus autonomic "
    "phenomena (postural dizziness, disequilibrium, tinnitus, lacrimation) that are a hallmark feature.",
    {"vertex": 3, "face": 3, "frontal": 3, "ear": 3, "temporal": 2, "neck-ant": 2, "chest-ant": 1},
    "Trigeminal neuralgia; TMD; cervicogenic dizziness; sinus headache")

add("m-scalenes", "Scalenes (anterior / middle / posterior)", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Anterior/pectoral chest wall, vertebral border of scapula, and down the radial forearm to thumb and "
    "index finger — closely mimics C6 radiculopathy. Posterior scalene skews more interscapular.",
    {"chest-ant": 3, "scap-border": 3, "forearm-rad": 3, "thenar": 2, "digits-rad": 2,
     "deltoid-ant": 2, "arm-ant": 2, "interscap": 2},
    "C6 radiculopathy; neurogenic thoracic outlet syndrome; carpal tunnel")

add("m-splenius-cap", "Splenius capitis", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "A 'boring' pain focused at the very top of the head. Classically no frontal or ocular involvement — "
    "that absence distinguishes it from sternocleidomastoid.",
    {"vertex": 3, "neck-upper": 1})

add("m-splenius-cerv", "Splenius cervicis", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Retro-orbital pain (behind the eye) and the angle of the neck/occiput, with reported ipsilateral "
    "blurred vision as a concomitant.",
    {"frontal": 3, "occiput": 3, "neck-upper": 2, "neck-lower": 2, "shoulder-top": 1})

add("m-suboccipitals", "Suboccipital group", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Diffuse, deep, band- or 'halo'-like pain from the occiput over the top of the head toward the temple "
    "and eye. Travell & Simons note this pattern does not map to a crisp cutaneous zone.",
    {"suboccipital": 3, "occiput": 3, "temporal": 2, "vertex": 2, "frontal": 2})

add("m-rhomboids", "Rhomboid major / minor", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Superficial, localised ache along the vertebral border of the scapula. One of the few patterns with "
    "essentially NO spillover and no projection into the arm — that confinement is the diagnostic clue.",
    {"scap-border": 3, "interscap": 2})

# ===========================================================================
# MUSCLES — shoulder
# ===========================================================================
add("m-supraspinatus", "Supraspinatus", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Deep, boring ache centred over the mid-deltoid, spilling down the arm and forearm, occasionally to "
    "the wrist.",
    {"deltoid-lat": 3, "shoulder-top": 2, "arm-ant": 2, "elbow-lat": 2, "forearm-rad": 1, "wrist": 1},
    "Subacromial impingement; C5 radiculopathy")

add("m-infraspinatus", "Infraspinatus", "muscle", "C",
    "Zone map: Travell & Simons Vol. 1. Referral direction separately corroborated by hypertonic saline "
    "injection in healthy volunteers producing referred pain in the ipsilateral upper arm "
    "(Leffler et al., Eur J Pain 2000).",
    "Deep ache in the ANTERIOR shoulder/deltoid — the single most classic 'shoulder pain' myofascial "
    "pattern. Spillover down the lateral arm and radial forearm, plus local pain at the vertebral border "
    "of the scapula. Characteristically painful at rest and prevents sleeping on the affected side. "
    "The experimental corroboration covers only the arm component, not the anterior-deltoid, forearm or "
    "scapular zones, so the grade stays C with the rest of the myofascial maps.",
    {"deltoid-ant": 3, "deltoid-lat": 2, "arm-ant": 2, "forearm-rad": 2, "scap-border": 2,
     "digits-rad": 1, "shoulder-top": 1},
    "C5 radiculopathy (has weakness/reflex change); subacromial bursitis (painful arc); AC joint")

add("m-teres-minor", "Teres minor", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "A small, circumscribed patch of deep ache over the posterior deltoid near the axillary scapular "
    "border. Notably does NOT radiate — the confinement is the clue.",
    {"deltoid-post": 3})

add("m-teres-major", "Teres major", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Posterior deltoid and the inferior angle of the scapula, spilling down the back of the arm toward "
    "the elbow.",
    {"deltoid-post": 3, "scap-inf": 2, "arm-post": 2, "elbow-post": 1})

add("m-subscapularis", "Subscapularis", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Severe deep pain over the posterior shoulder and scapula — the 'shoulder holster' pattern — with a "
    "distinctive circumferential band around the wrist in severe cases. Strongly associated with "
    "frozen-shoulder-type restriction.",
    {"deltoid-post": 3, "scap-inf": 2, "scap-border": 2, "arm-post": 2, "wrist": 2},
    "Adhesive capsulitis; posterior labral pathology")

add("m-deltoid", "Deltoid (anterior / posterior)", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Localised to the involved third of the muscle itself, spreading only into the adjacent upper arm. "
    "Unusual among shoulder muscles for NOT projecting distal to the elbow.",
    {"deltoid-ant": 3, "deltoid-post": 3, "deltoid-lat": 2, "arm-ant": 1, "arm-post": 1})

add("m-lats", "Latissimus dorsi", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Constant ache over the inferior angle of the scapula and mid-back (the 'cape' of pain), spilling "
    "down the medial/posterior arm to the medial epicondyle and into the ring and little fingers.",
    {"scap-inf": 3, "thoracic-mid": 2, "arm-med": 2, "arm-post": 2, "elbow-med": 2,
     "forearm-uln": 1, "digits-uln": 2},
    "C8 radiculopathy; cubital tunnel")

add("m-pec-major", "Pectoralis major", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Anterior chest wall and breast. Clinically important: sternal-head trigger points near the 5th–6th "
    "costal cartilage can produce precordial pain and arrhythmia-like sensations that mimic cardiac "
    "disease — a well-documented diagnostic pitfall. Spillover down the medial arm to the ulnar digits.",
    {"chest-ant": 3, "deltoid-ant": 2, "arm-med": 2, "elbow-med": 2, "forearm-uln": 1, "digits-uln": 2},
    "Angina / cardiac pain (EXCLUDE FIRST); costochondritis; C8–T1 radiculopathy")

add("m-pec-minor", "Pectoralis minor", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Anterior chest and shoulder below the clavicle, referring down the medial arm and forearm to the "
    "ulnar three digits — overlapping the ulnar/thoracic outlet pattern.",
    {"chest-ant": 3, "deltoid-ant": 2, "arm-med": 2, "forearm-uln": 2, "digits-uln": 2},
    "Neurogenic thoracic outlet syndrome (subcoracoid space); C8 radiculopathy")

add("m-serratus-ant", "Serratus anterior", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Lateral chest wall in the mid-axillary line — the classic 'stitch in the side' — wrapping to the "
    "inferior scapular angle and down the medial arm to the ulnar forearm and digits. Often accompanied "
    "by air hunger / difficulty taking a deep breath.",
    {"chest-lat": 3, "scap-inf": 2, "arm-med": 2, "forearm-uln": 1, "digits-uln": 1, "chest-ant": 1})

add("m-serratus-post-sup", "Serratus posterior superior", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Deep, poorly localised ache UNDER the scapula, referring down the posterior arm to the ulnar forearm, "
    "hand and little finger, with occasional numbness in a C8–T1 distribution. The 'ache I can't reach'.",
    {"scap-border": 3, "scap-inf": 2, "deltoid-post": 2, "arm-post": 2, "forearm-uln": 2,
     "digits-uln": 2, "hand-dors": 1},
    "C8 radiculopathy; neurogenic thoracic outlet syndrome")

add("m-coracobrachialis", "Coracobrachialis", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Anterior deltoid and front of the upper arm, with an unusually long reach for a small muscle — down "
    "the entire posterior arm to the dorsal forearm and hand.",
    {"deltoid-ant": 3, "arm-ant": 2, "arm-post": 2, "forearm-dors": 2, "hand-dors": 2})

# ===========================================================================
# MUSCLES — arm / forearm / hand
# ===========================================================================
add("m-biceps", "Biceps brachii", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Anterior shoulder (front of deltoid) and down the front of the arm to the antecubital crease.",
    {"deltoid-ant": 3, "arm-ant": 3, "elbow-ant": 2, "forearm-volar": 1})

add("m-triceps", "Triceps brachii", "muscle", "C",
    "Travell & Simons Vol. 1 (multiple distinct trigger point sites).",
    "Posterior shoulder, posterior upper arm and the olecranon/posterior elbow, spilling down the "
    "posterior forearm to the dorsum of the hand.",
    {"arm-post": 3, "elbow-post": 3, "deltoid-post": 2, "forearm-dors": 2, "hand-dors": 1,
     "elbow-lat": 1, "digits-uln": 1})

add("m-brachialis", "Brachialis", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Front of the elbow over the muscle belly, with a distinctive projection to the base and dorsal web "
    "space of the THUMB — that thumb referral is the signature.",
    {"elbow-ant": 3, "thenar": 3, "web-space": 3, "arm-ant": 2},
    "C6 radiculopathy; de Quervain's; CMC arthritis")

add("m-brachioradialis", "Brachioradialis", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Lateral epicondyle ('tennis elbow' mimic) and down the dorsoradial forearm to the web space between "
    "thumb and index finger.",
    {"elbow-lat": 3, "forearm-rad": 3, "web-space": 3, "thenar": 2, "wrist": 1},
    "Lateral epicondylalgia; radial tunnel syndrome; C6 radiculopathy")

add("m-supinator", "Supinator", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Lateral epicondyle and proximal dorsal forearm — mimics resistant lateral epicondylalgia and radial "
    "tunnel syndrome — with spillover to the dorsal thumb web space.",
    {"elbow-lat": 3, "forearm-rad": 2, "web-space": 2, "thenar": 1},
    "Lateral epicondylalgia (resistant); PIN/radial tunnel entrapment")

add("m-pronator-teres", "Pronator teres", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Volar proximal forearm and radial wrist, spilling to the radial three digits and thenar region. Can "
    "accompany true median nerve paresthesia (pronator teres syndrome).",
    {"forearm-volar": 3, "wrist": 3, "thenar": 2, "digits-rad": 2, "elbow-ant": 2, "palm": 1},
    "Carpal tunnel syndrome; pronator syndrome; C6 radiculopathy")

add("m-wrist-ext", "Wrist extensors (ECRL / ECRB / ECU)", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "ECRL/ECRB: lateral epicondyle spilling to the dorsum of the hand and wrist (ECRB into the dorsal "
    "middle finger). ECU stays fairly localised to the dorsal-ulnar wrist.",
    {"elbow-lat": 3, "forearm-dors": 2, "wrist": 3, "hand-dors": 2, "digits-rad": 1},
    "Lateral epicondylalgia; C6–C7 radiculopathy")

add("m-finger-ext", "Finger extensors (EDC / EIP)", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Dorsal forearm and wrist referring into the dorsum of the corresponding finger(s) — a roughly "
    "segmental, one-slip-per-finger pattern.",
    {"forearm-dors": 3, "hand-dors": 3, "wrist": 2, "digits-rad": 2, "digits-uln": 2})

add("m-wrist-flex", "Wrist / finger flexors (FCR, FCU, FDS, FDP)", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Volar forearm referring to the palm, volar wrist and corresponding fingers — FCU skews ulnar/little "
    "finger, FCR skews radial palm. Palmaris longus is distinct: a superficial, hypersensitive "
    "'pins-and-needles' patch in the centre of the palm rather than a deep ache.",
    {"forearm-volar": 3, "forearm-uln": 2, "palm": 3, "wrist": 2, "digits-uln": 2, "digits-rad": 1},
    "Carpal tunnel syndrome; Guyon's canal; C8 radiculopathy")

add("m-adductor-pollicis", "Adductor pollicis", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Base of the thumb, thumb–index web space, centre of the palm and the wrist. Confined to the hand — "
    "can convincingly mimic carpal tunnel syndrome.",
    {"thenar": 3, "web-space": 3, "palm": 2, "wrist": 2},
    "Carpal tunnel syndrome; CMC arthritis")

add("m-opponens-pollicis", "Opponens pollicis", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Runs the length of the palmar/radial thumb itself, occasionally to the dorsal thumb and volar wrist.",
    {"thenar": 3, "wrist": 2, "web-space": 1})

add("m-first-dorsal-io", "First dorsal interosseous", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Radial side of the index finger, running its full length to the fingertip, plus the dorsal web space. "
    "Frequently mistaken for digital nerve entrapment.",
    {"digits-rad": 3, "web-space": 3, "hand-dors": 2},
    "Digital nerve entrapment; C6/C7 radiculopathy")

# ===========================================================================
# MUSCLES — trunk
# ===========================================================================
add("m-rectus-abd", "Rectus abdominis", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Hallmark feature: upper trigger points refer BILATERALLY across the mid and low back and can mimic "
    "epigastric or cardiac pain; lower trigger points refer bilaterally to the low back and sacral region "
    "and can produce colicky abdominal pain with GI symptoms.",
    {"epigastric": 3, "abd-lower": 3, "thoracolumbar": 2, "lumbar": 2, "thoracic-mid": 2, "chest-ant": 1},
    "Visceral pathology (EXCLUDE FIRST); lumbar facet; discogenic low back pain")

add("m-obliques", "External / internal obliques", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Upper fibres refer to the epigastrium and mimic heartburn; lower fibres refer to the groin and, in "
    "men, the testicle/scrotum. A well-known McBurney's-point mimic on the right — sometimes mistaken "
    "for appendicitis.",
    {"epigastric": 3, "abd-lower": 2, "groin": 3, "flank": 2, "chest-lat": 1},
    "Appendicitis (EXCLUDE FIRST); inguinal hernia; hip pathology")

add("m-quadratus-lumborum", "Quadratus lumborum", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Deep ache in the flank, iliac crest and sacroiliac region, spilling to the buttock, groin and greater "
    "trochanter. Superficial-layer points skew toward the iliac crest and lower buttock; deep-layer points "
    "concentrate over the SI joint.",
    {"flank": 3, "lumbar": 3, "si-buttock": 3, "groin": 2, "thoracolumbar": 2},
    "SI joint dysfunction; lumbar facet; hip pathology")

add("m-iliocostalis-thor", "Iliocostalis thoracis", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Segmental paraspinal band at the level of the trigger point that WRAPS AROUND THE CHEST WALL "
    "following the rib contours — can mimic cardiac or pleuritic pain.",
    {"thoracic-mid": 3, "flank": 2, "chest-lat": 2, "chest-ant": 2, "interscap": 2},
    "Cardiac / pleuritic pain (EXCLUDE FIRST); thoracic facet; costotransverse joint")

add("m-iliocostalis-lumb", "Iliocostalis lumborum", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Local low back extending into the buttock; sits more lateral than the longissimus pattern.",
    {"lumbar": 3, "si-buttock": 2, "flank": 2, "thoracolumbar": 2})

add("m-longissimus", "Longissimus thoracis", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Paraspinal band at the trigger point level — upper points stay local with some radiation toward the "
    "scapula; lower points extend into the buttock, generally more MEDIAL than the iliocostalis lumborum "
    "pattern.",
    {"thoracic-mid": 3, "thoracolumbar": 3, "lumbar": 2, "si-buttock": 2, "interscap": 1})

add("m-multifidi", "Multifidi", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Very localised deep segmental pain directly over or adjacent to the spinous process at the level "
    "involved. Cervical level refers to the occiput; lumbosacral level refers to the buttock and "
    "occasionally the posterior thigh, mimicking sciatica.",
    {"neck-mid": 2, "occiput": 2, "thoracic-mid": 2, "lumbar": 3, "si-buttock": 3, "thoracolumbar": 2},
    "Lumbar radiculopathy; facet joint pain")

add("m-serratus-post-inf", "Serratus posterior inferior", "muscle", "C",
    "Travell & Simons Vol. 1.",
    "Localised, persistent ache at the thoracolumbar junction over the muscle itself. One of the more "
    "confined trunk patterns — in sharp contrast to serratus posterior superior's long reach into the hand.",
    {"thoracolumbar": 3, "flank": 1})
