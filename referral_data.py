# -*- coding: utf-8 -*-
"""Lower-quarter referred pain dataset: regions, structures, referral maps."""

TIERS = {
    "A": {"label": "A — Experimental map, asymptomatic volunteers", "short": "A",
          "desc": "Referral zone produced by controlled provocation in asymptomatic volunteers, then "
                  "charted. The strongest design available: the zone is caused, not merely observed."},
    "B": {"label": "B — Provocation mapping in symptomatic patients", "short": "B",
          "desc": "Referral zone produced by provocation (injection, discography, joint block) in "
                  "patients who already have pain. Real experimental data, but the population is "
                  "sensitised and there is no asymptomatic control arm."},
    "C": {"label": "C — Clinical observation / expert synthesis", "short": "C",
          "desc": "Zone compiled from unblinded clinical case observation rather than controlled "
                  "provocation. Useful for generating hypotheses; not validated diagnostic anatomy. "
                  "Every myofascial referral map sits here."},
}

# ---------------------------------------------------------------------------
# BODY REGIONS  (id, label)
# ---------------------------------------------------------------------------
REGIONS = [
    # trunk / pelvis
    ("tl-junction",   "Thoracolumbar junction"),
    ("lumbar",        "Lumbar paraspinal"),
    ("lumbar-midline","Lumbar midline"),
    ("flank",         "Flank / lateral trunk"),
    ("iliac-crest",   "Iliac crest"),
    ("si-joint",      "Sacroiliac joint region"),
    ("sacrum",        "Sacrum"),
    ("coccyx",        "Coccyx"),
    ("buttock-upper", "Upper buttock"),
    ("buttock-lower", "Lower buttock / gluteal fold"),
    ("perineum",      "Perineum / pelvic floor"),
    ("lower-abdomen", "Lower abdomen"),
    ("groin",         "Groin / inguinal"),
    ("pubic",         "Pubic / adductor origin"),
    ("troch",         "Greater trochanter / lateral hip"),
    ("hip-ant",       "Anterior hip"),
    # thigh
    ("thigh-ant",     "Anterior thigh"),
    ("thigh-med",     "Medial thigh"),
    ("thigh-lat",     "Lateral thigh"),
    ("thigh-post",    "Posterior thigh"),
    # knee
    ("knee-ant",      "Anterior knee / patella"),
    ("knee-med",      "Medial knee"),
    ("knee-lat",      "Lateral knee"),
    ("knee-post",     "Posterior knee / popliteal fossa"),
    # leg
    ("leg-ant",       "Anterior shin"),
    ("leg-lat",       "Lateral leg"),
    ("leg-med",       "Medial leg"),
    ("calf",          "Posterior calf"),
    ("achilles",      "Achilles region"),
    # ankle / foot
    ("ankle-ant",     "Anterior ankle"),
    ("ankle-med",     "Medial malleolus"),
    ("ankle-lat",     "Lateral malleolus"),
    ("heel-plantar",  "Plantar heel"),
    ("arch",          "Medial arch"),
    ("forefoot-plant","Plantar forefoot / metatarsal heads"),
    ("foot-dorsum",   "Dorsum of foot"),
    ("great-toe",     "Great toe / first web space"),
    ("lat-toes",      "Lateral toes"),
]
REGION_LABEL = {r[0]: r[1] for r in REGIONS}

CATEGORIES = [
    ("facet",    "Zygapophysial (facet) joint"),
    ("disc",     "Intervertebral disc"),
    ("root",     "Nerve root (dynatome)"),
    ("ligament", "Spinal ligament"),
    ("joint",    "Peripheral joint"),
    ("muscle",   "Muscle (myofascial)"),
]

S = []


def add(sid, name, cat, tier, source, note, zones, lookalikes=""):
    S.append(dict(id=sid, name=name, cat=cat, tier=tier, source=source,
                  note=note, zones=zones, lookalikes=lookalikes))


# ==========================================================================
# LUMBAR FACET JOINTS
# ==========================================================================
_FACET_SRC = ("Mooney & Robertson, Clin Orthop 1976 (N=20, 5 volunteers + 15 patients); "
              "McCall, Park & O'Brien, Spine 1979 (asymptomatic volunteers); "
              "Fukui et al., Clin J Pain 1997 (symptomatic); Marks, Pain 1989.")

add("facet-l12", "L1–L2 facet joint", "facet", "B", _FACET_SRC,
    "Upper lumbar facets refer laterally and proximally — flank, iliac crest and lateral hip — rather "
    "than down the leg. McCall's volunteer data put the upper levels in the flank and greater "
    "trochanter region.",
    {"lumbar": 3, "flank": 3, "iliac-crest": 2, "tl-junction": 2, "troch": 1})

add("facet-l23", "L2–L3 facet joint", "facet", "B", _FACET_SRC,
    "Lumbar paraspinal with lateral spread to the iliac crest and trochanter. Level-specific maps "
    "overlap heavily — McCall's own conclusion was 'considerable overlap' between levels.",
    {"lumbar": 3, "iliac-crest": 3, "flank": 2, "troch": 2, "buttock-upper": 1})

add("facet-l34", "L3–L4 facet joint", "facet", "B", _FACET_SRC,
    "Lumbar paraspinal, iliac crest, upper buttock and greater trochanter, beginning to reach the "
    "lateral thigh.",
    {"lumbar": 3, "buttock-upper": 3, "iliac-crest": 2, "troch": 2, "thigh-lat": 1, "groin": 1})

add("facet-l45", "L4–L5 facet joint", "facet", "B", _FACET_SRC,
    "One of the two most commonly implicated levels. Buttock and trochanteric referral dominate; "
    "Marks (1989) attributed most buttock and trochanteric pain to L4–L5.",
    {"buttock-upper": 3, "lumbar": 3, "troch": 3, "buttock-lower": 2, "thigh-post": 2,
     "thigh-lat": 2, "si-joint": 1})

add("facet-l5s1", "L5–S1 facet joint", "facet", "B", _FACET_SRC,
    "Buttock and posterior thigh. Whether facet pain can reach below the knee is genuinely contested: "
    "Mooney & Robertson saw whole-leg pain in 3 of 20, but that is now widely attributed to "
    "large-volume saline rupturing the capsule. Windsor's electrical stimulation — a more specific "
    "stimulus — produced smaller, more proximal zones.",
    {"buttock-upper": 3, "buttock-lower": 3, "thigh-post": 3, "lumbar": 2, "si-joint": 2,
     "troch": 2, "thigh-lat": 1},
    "SI joint (indistinguishable by pain location alone — DePalma 2011); L5/S1 radiculopathy")

# ==========================================================================
# LUMBAR DISCS
# ==========================================================================
_DISC_SRC = ("Vanharanta / Ohnmeiss provocation discography series; Carragee et al., Spine 2000 "
             "(false-positive rates); DePalma et al., PM&R 2011 (midline vs paramidline).")

add("disc-l34", "L3–L4 intervertebral disc", "disc", "B", _DISC_SRC,
    "Midline low back pain with anterior/lateral thigh referral. Discography localises the level "
    "poorly — overlap between adjacent levels is the norm.",
    {"lumbar-midline": 3, "lumbar": 2, "thigh-ant": 2, "thigh-lat": 1, "groin": 1})

add("disc-l45", "L4–L5 intervertebral disc", "disc", "B", _DISC_SRC,
    "Midline low back pain, buttock and posterolateral leg. DePalma 2011: midline pain was present "
    "in 95.8% of confirmed discogenic cases versus 15.4% of facet and 12.9% of SI joint cases — the "
    "one location finding with real discriminating value.",
    {"lumbar-midline": 3, "lumbar": 3, "buttock-upper": 2, "thigh-post": 2, "thigh-lat": 2,
     "leg-lat": 1},
    "L5 radiculopathy; lumbar facet (but midline location favours disc)")

add("disc-l5s1", "L5–S1 intervertebral disc", "disc", "B", _DISC_SRC,
    "Midline low back, buttock, posterior thigh and calf. Pain extending below the knee correlates "
    "with the grade of annular disruption, not with which level is symptomatic.",
    {"lumbar-midline": 3, "buttock-upper": 3, "thigh-post": 2, "calf": 2, "lumbar": 2,
     "leg-lat": 1, "si-joint": 1})

# ==========================================================================
# NERVE ROOTS (DYNATOMES)
# ==========================================================================
add("root-l3", "L3 nerve root", "root", "B",
    "Clinical radiculopathy series; ASIA sensory points; Suri et al. 2011 (femoral stretch test).",
    "Anterior and distal thigh to the medial knee. Prone knee bend is the loading test — 70% "
    "sensitive and 88% specific for L3 specifically.",
    {"thigh-ant": 3, "knee-med": 2, "groin": 2, "thigh-med": 2, "lumbar": 1})

add("root-l4", "L4 nerve root", "root", "B",
    "Clinical radiculopathy series; ASIA sensory points.",
    "Medial leg and medial malleolus, with anterior thigh involvement. The transitional root — it "
    "feeds both the femoral nerve and the lumbosacral trunk, so it can present like an upper or a "
    "lower lumbar lesion.",
    {"leg-med": 3, "ankle-med": 3, "knee-med": 2, "thigh-ant": 2, "lumbar": 1, "leg-ant": 1})

add("root-l5", "L5 nerve root", "root", "B",
    "Clinical radiculopathy series; ASIA sensory points; SLR/slump literature.",
    "Lateral leg, dorsum of foot, great toe and first web space, with buttock and posterolateral "
    "thigh referral proximally. The commonest lumbar radiculopathy alongside S1.",
    {"leg-lat": 3, "foot-dorsum": 3, "great-toe": 3, "thigh-post": 2, "buttock-upper": 2,
     "leg-ant": 2, "thigh-lat": 2, "lumbar": 1},
    "Common fibular n. at the fibular neck (spares hip abduction and inversion); gluteus minimus TrP")

add("root-s1", "S1 nerve root", "root", "B",
    "Clinical radiculopathy series; ASIA sensory points.",
    "Posterior thigh and calf into the lateral foot and lateral malleolus. Achilles reflex loss is "
    "the localising sign.",
    {"calf": 3, "ankle-lat": 3, "lat-toes": 2, "thigh-post": 3, "buttock-lower": 2,
     "heel-plantar": 2, "buttock-upper": 2},
    "Piriformis / deep gluteal syndrome; SI joint; hamstring pathology")

# ==========================================================================
# LIGAMENT
# ==========================================================================
add("lig-lumbar-isl", "Lumbar &amp; sacral interspinous ligaments", "ligament", "C",
    "Kellgren, Clin Sci 1939; Feinstein et al., JBJS 1954 (as conventionally reported — the "
    "level-specific zones could not be verified against the primary tables).",
    "Deep, diffuse, segmentally-organised ache that does NOT follow dermatomes. Upper lumbar levels "
    "refer to flank and hip; lower lumbar and sacral levels refer into buttock and posterior thigh, "
    "approaching the knee in a minority. Foundational but small-N, non-blinded work.",
    {"lumbar": 3, "buttock-upper": 2, "flank": 2, "si-joint": 2, "thigh-post": 2, "iliac-crest": 1})

# ==========================================================================
# PERIPHERAL JOINTS
# ==========================================================================
add("joint-sij", "Sacroiliac joint", "joint", "B",
    "Zone geometry: Fortin et al., Spine 1994 Part I — 10 ASYMPTOMATIC volunteers (grade-A design). "
    "All quoted percentages: Slipman et al., Arch Phys Med Rehabil 2000 — 50 SYMPTOMATIC patients "
    "(68 joints; 18 bilateral, 32 unilateral), selected by a single positive intra-articular block.",
    "Graded B, not A: only the zone SHAPE — a consistent 3 × 10 cm area immediately caudal to the "
    "PSIS — comes from asymptomatic volunteers. Every percentage below comes from a symptomatic "
    "patient series. Slipman: buttock 94%, lower lumbar 72%, lower extremity roughly a quarter to a "
    "half (secondary sources report 28% and 50% for the same dataset), groin 14%, upper lumbar 6%. "
    "So SI pain CAN go below the knee — 'it stays above the knee' is not a safe rule.",
    {"si-joint": 3, "buttock-upper": 3, "lumbar": 2, "buttock-lower": 2, "thigh-post": 2,
     "groin": 1, "calf": 1},
    "L5–S1 facet (DePalma 2011: paramidline location cannot separate the two); lumbar disc")

add("joint-hip", "Hip joint", "joint", "B",
    "Lesher et al., Pain Medicine 2008 — fluoroscopically-guided intra-articular injection with "
    "pre-injection pain mapping, N=51 symptomatic patients.",
    "Buttock 71% — more common than groin, which contradicts the classic teaching. Thigh 57%, groin "
    "55%, distal to knee 22%, foot 6%, isolated knee 2%, lower lumbar spine 0%. Fourteen distinct "
    "referral patterns were identified: there is no single dominant hip pattern.",
    {"buttock-upper": 3, "groin": 3, "thigh-ant": 3, "thigh-lat": 2, "knee-ant": 2, "troch": 2,
     "thigh-med": 2, "knee-med": 1, "leg-ant": 1},
    "L2–L4 radiculopathy; SI joint; greater trochanteric pain syndrome. In adolescents with knee "
    "pain, always examine the hip — SCFE presents as knee pain in ~15%.")

add("joint-knee", "Knee joint (intra-articular)", "joint", "C",
    "Clinical observation; no controlled volunteer referral-mapping study identified.",
    "Largely local, with referral into the anterior thigh and proximal calf. Graded C because — "
    "unlike the hip and SI joint — no controlled provocation mapping study was found for the knee.",
    {"knee-ant": 3, "knee-med": 2, "knee-lat": 2, "thigh-ant": 1, "calf": 1, "knee-post": 1})

# ==========================================================================
# MUSCLES — gluteals & pelvis
# ==========================================================================
_TS = "Travell & Simons, Myofascial Pain and Dysfunction Vol. 2 (Lower Half of Body)."

add("m-glut-max", "Gluteus maximus", "muscle", "C", _TS,
    "Diffuse ache over the buttock mass. The medial-fibre trigger point near the coccyx mimics "
    "coccydynia. Rarely crosses the knee.",
    {"buttock-upper": 3, "buttock-lower": 3, "coccyx": 2, "sacrum": 2, "thigh-post": 1},
    "Coccydynia; SI joint dysfunction")

add("m-glut-med", "Gluteus medius", "muscle", "C", _TS,
    "Posterior iliac crest, sacrum and the whole buttock — the classic 'low back pain' muscle. "
    "Spillover into the posterior thigh and upper calf.",
    {"iliac-crest": 3, "buttock-upper": 3, "sacrum": 2, "si-joint": 2, "buttock-lower": 2,
     "thigh-post": 2, "lumbar": 2},
    "SI joint dysfunction; lumbar facet; L5 radiculopathy")

add("m-glut-min", "Gluteus minimus", "muscle", "C", _TS,
    "THE pseudo-sciatica pattern, and the most convincing non-radicular mimic in the whole atlas. "
    "Anterior fibres refer from the lateral buttock down the OUTSIDE of the leg as far as the ankle; "
    "posterior fibres run down the back of the buttock and thigh, stopping at the calf. Leg pain to "
    "the ankle with no dermatomal, myotomal or reflex change should raise this immediately.",
    {"buttock-lower": 3, "thigh-lat": 3, "leg-lat": 3, "ankle-lat": 2, "buttock-upper": 2,
     "thigh-post": 2, "calf": 2, "knee-lat": 2},
    "L5 or S1 radiculopathy — the discriminator is the ABSENCE of reflex, myotome and dermatome findings")

add("m-piriformis", "Piriformis", "muscle", "C", _TS,
    "Over the SI joint, sacrum, buttock and posterior hip, extending into the proximal two-thirds of "
    "the posterior thigh. Distinguish the myofascial referral (rarely past the knee) from true "
    "piriformis syndrome — sciatic nerve entrapment — which does produce symptoms to the foot.",
    {"si-joint": 3, "buttock-upper": 3, "sacrum": 2, "buttock-lower": 2, "thigh-post": 2},
    "Deep gluteal syndrome (true nerve entrapment); SI joint; S1 radiculopathy")

add("m-tfl", "Tensor fasciae latae", "muscle", "C", _TS,
    "Anterolateral hip over the greater trochanter and down the lateral thigh along the IT band "
    "toward the lateral knee.",
    {"troch": 3, "thigh-lat": 3, "hip-ant": 2, "knee-lat": 1},
    "Greater trochanteric pain syndrome; IT band syndrome")

add("m-iliopsoas", "Iliopsoas", "muscle", "C", _TS,
    "A vertical band in the ipsilateral upper lumbar paraspinal region plus anterior groin, "
    "spilling into the anterior thigh to the knee. A frequently missed mimic of discogenic back pain.",
    {"lumbar": 3, "groin": 3, "thigh-ant": 2, "lumbar-midline": 1, "hip-ant": 2},
    "Discogenic low back pain; hip flexor strain; intra-articular hip pathology")

add("m-ql", "Quadratus lumborum", "muscle", "C", _TS,
    "Superficial layer refers along the iliac crest and into the lower buttock and greater "
    "trochanter; deep layer concentrates over the SI joint, with spillover to the groin and lower "
    "lateral abdomen. One of the most consistently missed sources of 'SI joint' pain.",
    {"iliac-crest": 3, "si-joint": 3, "buttock-lower": 2, "troch": 2, "groin": 2, "flank": 2,
     "lower-abdomen": 1, "lumbar": 2},
    "SI joint dysfunction; greater trochanteric pain syndrome; hip pathology")

add("m-rectus-abd-low", "Rectus abdominis (lower fibres)", "muscle", "C", _TS,
    "Refers as a band across the LOW BACK bilaterally, plus sacral and pelvic pain — easily missed "
    "because the examination focuses on posterior structures.",
    {"lumbar": 3, "sacrum": 2, "lower-abdomen": 3, "si-joint": 1},
    "Mechanical low back pain; visceral/gynaecological pathology (exclude first)")

add("m-add-longus", "Adductor longus / brevis", "muscle", "C", _TS,
    "Deep groin and anteromedial thigh, running down the medial leg to just below the knee.",
    {"groin": 3, "thigh-med": 3, "pubic": 2, "knee-med": 2, "leg-med": 1},
    "Adductor strain; osteitis pubis; hip labral pathology")

add("m-add-magnus", "Adductor magnus", "muscle", "C", _TS,
    "Ischiocondylar portion refers along the posteromedial thigh to the knee; the proximal/pubic "
    "portion produces a deep intrapelvic ache that may be perceived intravaginally or intrarectally.",
    {"thigh-med": 3, "pubic": 3, "perineum": 2, "knee-med": 1, "groin": 2},
    "Chronic pelvic pain syndromes; adductor strain")

add("m-pectineus", "Pectineus", "muscle", "C", _TS,
    "Sharply localised deep pain in the groin crease with minimal spillover.",
    {"groin": 3, "hip-ant": 2, "thigh-med": 1},
    "Hip labral tear; intra-articular hip pathology; femoroacetabular impingement")

add("m-gracilis", "Gracilis", "muscle", "C", _TS,
    "A diffuse, superficial ache with an itching quality along the medial thigh — distinctively "
    "surface-level rather than deep, which separates it from adductor longus.",
    {"thigh-med": 3, "knee-med": 1})

add("m-obturator-int", "Obturator internus", "muscle", "C", _TS,
    "Deep pelvic floor, coccyx and posterior vaginal or rectal wall, spilling into the perineum and "
    "posterior thigh.",
    {"perineum": 3, "coccyx": 3, "buttock-lower": 2, "thigh-post": 1, "sacrum": 1},
    "Pudendal neuralgia; levator ani syndrome")

add("m-levator-ani", "Levator ani / coccygeus", "muscle", "C", _TS,
    "Coccyx and lower sacrum — the coccydynia pattern — with buttock referral and a sensation of "
    "rectal fullness.",
    {"coccyx": 3, "sacrum": 3, "perineum": 2, "buttock-lower": 2},
    "Coccydynia; levator ani syndrome; proctalgia fugax")

# ==========================================================================
# MUSCLES — thigh
# ==========================================================================
add("m-rectus-fem", "Rectus femoris", "muscle", "C", _TS,
    "Deep anterior thigh and, characteristically, the ANTERIOR KNEE — the referral is felt distally "
    "even though the trigger point sits proximally near the ASIS.",
    {"knee-ant": 3, "thigh-ant": 3, "hip-ant": 1},
    "Patellofemoral pain syndrome")

add("m-vastus-lat", "Vastus lateralis", "muscle", "C", _TS,
    "The widest referral of the quadriceps group — the entire lateral thigh from hip to knee, with "
    "the most distal trigger point referring to the lateral knee and proximal ones to the lateral "
    "hip and buttock.",
    {"thigh-lat": 3, "knee-lat": 3, "troch": 2, "buttock-lower": 1},
    "IT band syndrome; lateral knee pain; greater trochanteric pain syndrome")

add("m-vastus-med", "Vastus medialis", "muscle", "C", _TS,
    "Medial knee, with the superior (VMO) trigger point referring deep into the knee joint. "
    "Classically associated with a reflex-inhibition 'buckling' or giving-way sensation in the "
    "ABSENCE of true ligamentous laxity.",
    {"knee-med": 3, "knee-ant": 2, "thigh-ant": 1},
    "Meniscal tear; ACL insufficiency (but ligament tests are negative); patellofemoral pain")

add("m-vastus-int", "Vastus intermedius", "muscle", "C", _TS,
    "Diffuse, poorly localised mid-anterior thigh spreading toward the anterior knee. Often "
    "underappreciated in 'unexplained' anterior thigh ache.",
    {"thigh-ant": 3, "knee-ant": 2})

add("m-sartorius", "Sartorius", "muscle", "C", _TS,
    "Superficial, TINGLING or paraesthetic in quality — atypical for myofascial pain — running "
    "along the muscle from the anterolateral thigh toward the medial knee. The proximal trigger "
    "point near the ASIS can mimic meralgia paraesthetica.",
    {"thigh-ant": 3, "thigh-lat": 2, "knee-med": 2, "hip-ant": 1},
    "Meralgia paraesthetica (lateral femoral cutaneous n.)")

add("m-biceps-fem", "Biceps femoris", "muscle", "C", _TS,
    "Posterior thigh into the posterior knee and lateral popliteal fossa.",
    {"thigh-post": 3, "knee-post": 3, "buttock-lower": 1, "calf": 1},
    "Hamstring strain; S1 radiculopathy")

add("m-medial-hams", "Semitendinosus / semimembranosus", "muscle", "C", _TS,
    "Lower buttock crease and posteromedial thigh down to the popliteal fossa — a distinct laterality "
    "from biceps femoris.",
    {"buttock-lower": 3, "thigh-post": 3, "knee-post": 2, "knee-med": 1},
    "Proximal hamstring tendinopathy; ischiogluteal bursitis")

# ==========================================================================
# MUSCLES — leg
# ==========================================================================
add("m-gastroc", "Gastrocnemius", "muscle", "C", _TS,
    "Medial head refers to the medial calf and the instep/arch; lateral head to the posterior knee "
    "and lateral calf. Implicated in nocturnal calf cramps.",
    {"calf": 3, "arch": 2, "knee-post": 2, "leg-med": 2, "leg-lat": 1},
    "DVT (EXCLUDE FIRST in an acutely swollen, warm calf); S1 radiculopathy")

add("m-soleus", "Soleus", "muscle", "C", _TS,
    "The LOWER trigger point near the Achilles refers to the HEEL and plantar surface — a textbook "
    "mimic of plantar fasciitis, reproducing weight-bearing heel pain. The upper/lateral trigger "
    "point refers, unexpectedly, to the SI JOINT region.",
    {"heel-plantar": 3, "achilles": 3, "calf": 2, "si-joint": 2, "knee-post": 1},
    "Plantar fasciitis; Achilles tendinopathy; Baxter's neuropathy; SI joint dysfunction")

add("m-popliteus", "Popliteus", "muscle", "C", _TS,
    "Localised posterior knee pain, worse descending stairs or hills and with squatting. Minimal "
    "spillover.",
    {"knee-post": 3, "calf": 1},
    "Popliteus tendinopathy; posterior horn meniscal tear; Baker's cyst")

add("m-tib-ant", "Tibialis anterior", "muscle", "C", _TS,
    "Anterior ankle and the dorsum of the great toe and first ray, with local anterior shin pain.",
    {"leg-ant": 3, "ankle-ant": 3, "great-toe": 3, "foot-dorsum": 2},
    "L5 radiculopathy; deep fibular n. entrapment; anterior compartment syndrome")

add("m-tib-post", "Tibialis posterior", "muscle", "C", _TS,
    "Diffuse — Achilles region, the ENTIRE plantar sole, and the posterior calf. The widest plantar "
    "distribution of any leg muscle.",
    {"achilles": 3, "forefoot-plant": 3, "arch": 3, "calf": 2, "heel-plantar": 2},
    "Tarsal tunnel syndrome; tibialis posterior tendinopathy; plantar fasciitis")

add("m-peroneals", "Fibularis (peroneus) longus / brevis", "muscle", "C", _TS,
    "Lateral malleolus and lateral ankle/foot; longus spills to the lateral foot dorsum, brevis to "
    "the lateral shin.",
    {"ankle-lat": 3, "leg-lat": 3, "foot-dorsum": 2, "lat-toes": 1},
    "Chronic lateral ankle instability; superficial fibular n. entrapment; L5/S1 radiculopathy")

add("m-edl", "Extensor digitorum longus", "muscle", "C", _TS,
    "Dorsum of the foot and anterolateral shin, referring into the dorsal aspect of the middle toes.",
    {"foot-dorsum": 3, "leg-ant": 2, "lat-toes": 2, "ankle-ant": 2})

add("m-fdl", "Flexor digitorum longus", "muscle", "C", _TS,
    "Plantar surface over metatarsal heads 2–5, with a deep calf ache.",
    {"forefoot-plant": 3, "calf": 2, "arch": 1})

# ==========================================================================
# MUSCLES — foot
# ==========================================================================
add("m-edb", "Extensor digitorum brevis", "muscle", "C", _TS,
    "Local dorsolateral midfoot pain.",
    {"foot-dorsum": 3, "ankle-ant": 1})

add("m-abd-hallucis", "Abductor hallucis", "muscle", "C", _TS,
    "Medial heel and medial plantar foot.",
    {"heel-plantar": 3, "arch": 3, "ankle-med": 1},
    "Tarsal tunnel syndrome; medial-band plantar fasciitis")

add("m-fdb", "Flexor digitorum brevis", "muscle", "C", _TS,
    "Plantar surface under metatarsal heads 2–4 and the central heel.",
    {"forefoot-plant": 3, "heel-plantar": 2, "arch": 1})

add("m-quad-plantae", "Quadratus plantae", "muscle", "C", _TS,
    "Central plantar heel pad. Distinctively, it mimics plantar fasciitis WITHOUT arch involvement — "
    "that absence is the discriminator.",
    {"heel-plantar": 3},
    "Plantar fasciitis (but without arch pain); Baxter's neuropathy")

add("m-interossei-foot", "Foot interossei", "muscle", "C", _TS,
    "Local pain in the corresponding toe and web space. Third and fourth web-space trigger points "
    "can mimic Morton's neuroma.",
    {"forefoot-plant": 3, "lat-toes": 3, "foot-dorsum": 2},
    "Morton's neuroma; metatarsalgia; stress fracture")
