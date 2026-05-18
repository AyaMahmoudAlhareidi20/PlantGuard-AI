import streamlit as st
import numpy as np
import json
import os
import pickle
import io
from PIL import Image

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PlantGuard AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --green-dark:   #0a2e1a;
    --green-mid:    #145c30;
    --green-bright: #22c55e;
    --green-glow:   #4ade80;
    --gold:         #d4a843;
    --gold-light:   #f0c96a;
    --cream:        #f9f5ec;
    --white:        #ffffff;
    --text-dim:     #94a3b8;
}


html, body, [data-testid="stAppViewContainer"] {
    background: var(--green-dark) !important;
    font-family: 'DM Sans', sans-serif;
}

data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(34,197,94,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 40% 30% at 90% 80%, rgba(212,168,67,0.08) 0%, transparent 50%),
        var(--green-dark) !important;
}

[data-testid="stHeader"] { background: transparent !important; }

/* ─── HIDE STREAMLIT CHROME ─── */
#MainMenu, footer, header { visibility: hidden; }

/* ─── UNIVERSITY BANNER ─── */
.uni-banner {
    background: linear-gradient(135deg, var(--green-mid) 0%, #0f3d20 100%);
    border: 1px solid rgba(34,197,94,0.25);
    border-radius: 16px;
    padding: 18px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}
.uni-left { display: flex; align-items: center; gap: 16px; }
.uni-icon {
    width: 54px; height: 54px;
    background: linear-gradient(135deg, var(--gold), var(--gold-light));
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 26px;
}
.uni-name {
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 15px;
    color: var(--gold-light);
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.uni-dept {
    font-size: 12px;
    color: rgba(255,255,255,0.55);
    margin-top: 2px;
    letter-spacing: 0.08em;
}
.uni-badge {
    background: rgba(34,197,94,0.15);
    border: 1px solid rgba(34,197,94,0.3);
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 12px;
    color: var(--green-glow);
    font-weight: 500;
    letter-spacing: 0.06em;
}

/* ─── HERO HEADER ─── */
.hero {
    text-align: center;
    padding: 48px 0 36px;
}
.hero-tag {
    display: inline-block;
    background: rgba(34,197,94,0.12);
    border: 1px solid rgba(34,197,94,0.3);
    border-radius: 30px;
    padding: 6px 20px;
    font-size: 12px;
    color: var(--green-glow);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 20px;
    font-weight: 600;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(38px, 6vw, 72px);
    font-weight: 900;
    color: var(--white);
    line-height: 1.05;
    margin: 0 0 16px;
    letter-spacing: -1px;
}
.hero-title span {
    background: linear-gradient(90deg, var(--green-bright), var(--gold-light));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 17px;
    color: rgba(255,255,255,0.55);
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.6;
    font-weight: 300;
}

/* ─── STAT CARDS ─── */
.stat-row {
    display: flex;
    gap: 16px;
    margin-bottom: 36px;
}
.stat-card {
    flex: 1;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
}
.stat-val {
    font-family: 'Playfair Display', serif;
    font-size: 30px;
    font-weight: 700;
    color: var(--green-glow);
}
.stat-lbl {
    font-size: 12px;
    color: rgba(255,255,255,0.4);
    margin-top: 4px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ─── UPLOAD CARD ─── */
.upload-card {
    background: rgba(255,255,255,0.03);
    border: 1.5px dashed rgba(34,197,94,0.3);
    border-radius: 24px;
    padding: 36px;
    transition: all 0.3s;
}
.upload-card:hover {
    border-color: rgba(34,197,94,0.6);
    background: rgba(34,197,94,0.04);
}

/* ─── FILE UPLOADER OVERRIDE ─── */
[data-testid="stFileUploader"] {
    background: transparent !important;
}
[data-testid="stFileUploader"] label {
    color: rgba(255,255,255,0.7) !important;
    font-size: 15px !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: rgba(34,197,94,0.05) !important;
    border: 1.5px dashed rgba(34,197,94,0.4) !important;
    border-radius: 16px !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] span {
    color: rgba(255,255,255,0.6) !important;
}
[data-testid="stFileUploaderDropzone"] button {
    background: linear-gradient(135deg, var(--green-mid), #1a7a40) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* ─── SELECTBOX ─── */
[data-testid="stSelectbox"] label {
    color: rgba(255,255,255,0.7) !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}
[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: white !important;
}

/* ─── BUTTON ─── */
[data-testid="stButton"] button {
    background: linear-gradient(135deg, #16803c, var(--green-bright)) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    padding: 14px 32px !important;
    width: 100% !important;
    letter-spacing: 0.04em !important;
    box-shadow: 0 4px 24px rgba(34,197,94,0.35) !important;
    transition: all 0.3s !important;
}
[data-testid="stButton"] button:hover {
    box-shadow: 0 6px 32px rgba(34,197,94,0.55) !important;
    transform: translateY(-1px) !important;
}

/* ─── IMAGE ─── */
[data-testid="stImage"] img {
    border-radius: 18px !important;
    border: 1px solid rgba(34,197,94,0.2) !important;
}

/* ─── RESULT CARDS ─── */
.result-box {
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 16px;
}
.result-healthy {
    background: linear-gradient(135deg, rgba(34,197,94,0.12), rgba(34,197,94,0.06));
    border: 1.5px solid rgba(34,197,94,0.4);
}
.result-diseased {
    background: linear-gradient(135deg, rgba(239,68,68,0.12), rgba(239,68,68,0.05));
    border: 1.5px solid rgba(239,68,68,0.35);
}
.result-status {
    font-size: 13px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 8px;
}
.result-status.healthy { color: var(--green-glow); }
.result-status.diseased { color: #f87171; }
.result-plant {
    font-family: 'Playfair Display', serif;
    font-size: 26px;
    font-weight: 700;
    color: white;
    margin-bottom: 4px;
}
.result-disease {
    font-size: 16px;
    color: rgba(255,255,255,0.6);
    margin-bottom: 16px;
}
.conf-bar-bg {
    background: rgba(255,255,255,0.1);
    border-radius: 8px;
    height: 8px;
    overflow: hidden;
    margin: 8px 0 4px;
}
.conf-bar-fill {
    height: 100%;
    border-radius: 8px;
    transition: width 0.8s ease;
}
.conf-pct {
    font-size: 13px;
    color: rgba(255,255,255,0.5);
}

/* ─── INFO SECTION ─── */
.info-section {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 24px 28px;
    margin-bottom: 14px;
}
.info-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
}
.info-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.info-icon.green { background: rgba(34,197,94,0.15); }
.info-icon.gold  { background: rgba(212,168,67,0.15); }
.info-icon.red   { background: rgba(239,68,68,0.12); }
.info-title {
    font-size: 14px;
    font-weight: 700;
    color: white;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.info-body {
    font-size: 14px;
    color: rgba(255,255,255,0.65);
    line-height: 1.7;
}
.info-body ul { margin: 8px 0; padding-left: 18px; }
.info-body li { margin-bottom: 6px; }

/* ─── MODEL PILLS ─── */
.model-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.25);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 12px;
    color: var(--green-glow);
    font-weight: 600;
    margin: 2px;
}

/* ─── DIVIDER ─── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(34,197,94,0.2), transparent);
    margin: 32px 0;
}

/* ─── SECTION LABEL ─── */
.section-lbl {
    font-size: 11px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.3);
    margin-bottom: 12px;
    font-weight: 600;
}

/* ─── SPINNER ─── */
[data-testid="stSpinner"] { color: var(--green-glow) !important; }

/* ─── COLUMNS GAP ─── */
[data-testid="column"] { padding: 0 10px !important; }
</style>
""", unsafe_allow_html=True)


# ─── DISEASE DATABASE ────────────────────────────────────────────────────────────
DISEASE_DB = {
    # Apple
    "Apple___Apple_scab": {
        "plant": "Apple", "disease": "Apple Scab",
        "description": "Fungal disease causing dark, scabby lesions on leaves and fruit caused by Venturia inaequalis.",
        "treatment": ["Apply fungicides (myclobutanil, captan) at green tip stage", "Remove and destroy infected leaves", "Ensure good air circulation by pruning", "Use scab-resistant apple varieties"],
        "severity": "Medium"
    },
    "Apple___Black_rot": {
        "plant": "Apple", "disease": "Black Rot",
        "description": "Fungal disease (Botryosphaeria obtusa) causing brown leaf spots and fruit rot.",
        "treatment": ["Prune out dead or diseased wood", "Apply copper-based fungicides", "Remove mummified fruit from trees", "Improve air circulation"],
        "severity": "High"
    },
    "Apple___Cedar_apple_rust": {
        "plant": "Apple", "disease": "Cedar Apple Rust",
        "description": "Fungal disease caused by Gymnosporangium juniperi-virginianae requiring two hosts.",
        "treatment": ["Apply protective fungicides in spring", "Remove nearby cedar/juniper trees if possible", "Use resistant apple varieties", "Apply myclobutanil or mancozeb"],
        "severity": "Medium"
    },
    "Apple___healthy": {
        "plant": "Apple", "disease": "Healthy",
        "description": "Plant appears healthy with no signs of disease or infection.",
        "treatment": ["Maintain regular watering schedule", "Continue current care routine", "Monitor for early signs of pests"],
        "severity": "None"
    },
    # Blueberry
    "Blueberry___healthy": {
        "plant": "Blueberry", "disease": "Healthy",
        "description": "Plant appears healthy with no signs of disease.",
        "treatment": ["Maintain soil pH between 4.5–5.5", "Ensure proper irrigation", "Monitor for pests regularly"],
        "severity": "None"
    },
    # Cherry
    "Cherry_(including_sour)___Powdery_mildew": {
        "plant": "Cherry", "disease": "Powdery Mildew",
        "description": "Fungal disease creating white powdery coating on leaves and shoots.",
        "treatment": ["Apply sulfur-based or potassium bicarbonate fungicides", "Improve air circulation", "Avoid overhead irrigation", "Remove heavily infected shoots"],
        "severity": "Medium"
    },
    "Cherry_(including_sour)___healthy": {
        "plant": "Cherry", "disease": "Healthy",
        "description": "Plant appears healthy with no visible disease.",
        "treatment": ["Continue good cultural practices", "Prune for air circulation", "Regular pest monitoring"],
        "severity": "None"
    },
    # Corn
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "plant": "Corn (Maize)", "disease": "Gray Leaf Spot",
        "description": "Fungal disease (Cercospora zeae-maydis) causing rectangular gray-tan lesions.",
        "treatment": ["Use resistant hybrids", "Apply strobilurin or triazole fungicides", "Practice crop rotation", "Improve field drainage"],
        "severity": "High"
    },
    "Corn_(maize)___Common_rust_": {
        "plant": "Corn (Maize)", "disease": "Common Rust",
        "description": "Caused by Puccinia sorghi, producing cinnamon-brown pustules on leaves.",
        "treatment": ["Plant resistant varieties", "Apply fungicides (propiconazole) if severe", "Early planting to avoid peak spore periods", "Monitor regularly"],
        "severity": "Medium"
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "plant": "Corn (Maize)", "disease": "Northern Leaf Blight",
        "description": "Fungal disease (Exserohilum turcicum) causing long cigar-shaped gray-green lesions.",
        "treatment": ["Use resistant hybrids", "Apply fungicides at early stages", "Crop rotation with non-host crops", "Bury or remove crop debris"],
        "severity": "High"
    },
    "Corn_(maize)___healthy": {
        "plant": "Corn (Maize)", "disease": "Healthy",
        "description": "Plant appears healthy.",
        "treatment": ["Continue balanced fertilization", "Monitor for pests", "Ensure adequate drainage"],
        "severity": "None"
    },
    # Grape
    "Grape___Black_rot": {
        "plant": "Grape", "disease": "Black Rot",
        "description": "Fungal disease (Guignardia bidwellii) causing brown leaf lesions and shriveled black fruit.",
        "treatment": ["Apply mancozeb or myclobutanil fungicides", "Remove mummified berries", "Prune for good air circulation", "Apply protective sprays from budbreak"],
        "severity": "High"
    },
    "Grape___Esca_(Black_Measles)": {
        "plant": "Grape", "disease": "Esca (Black Measles)",
        "description": "Complex trunk disease caused by multiple fungi leading to tiger-stripe leaf pattern.",
        "treatment": ["Protect pruning wounds with fungicide paste", "Remove and destroy infected wood", "Avoid large pruning cuts", "No complete cure — manage with cultural practices"],
        "severity": "Severe"
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "plant": "Grape", "disease": "Leaf Blight",
        "description": "Caused by Pseudocercospora vitis, producing dark angular spots on leaves.",
        "treatment": ["Apply copper or mancozeb fungicides", "Improve canopy aeration", "Remove infected leaves", "Reduce humidity around vines"],
        "severity": "Medium"
    },
    "Grape___healthy": {
        "plant": "Grape", "disease": "Healthy",
        "description": "Plant appears healthy.",
        "treatment": ["Maintain trellis system", "Regular canopy management", "Soil nutrition monitoring"],
        "severity": "None"
    },
    # Orange
    "Orange___Haunglongbing_(Citrus_greening)": {
        "plant": "Orange", "disease": "Citrus Greening (HLB)",
        "description": "Bacterial disease (Candidatus Liberibacter) spread by psyllid insects — no cure.",
        "treatment": ["Remove and destroy infected trees immediately", "Control Asian citrus psyllid with insecticides", "Use certified disease-free planting material", "Maintain tree nutrition to slow decline"],
        "severity": "Severe"
    },
    # Peach
    "Peach___Bacterial_spot": {
        "plant": "Peach", "disease": "Bacterial Spot",
        "description": "Caused by Xanthomonas arboricola, creating water-soaked spots on leaves and fruit.",
        "treatment": ["Apply copper-based bactericides from budbreak", "Use resistant peach varieties", "Avoid overhead irrigation", "Prune for air circulation"],
        "severity": "High"
    },
    "Peach___healthy": {
        "plant": "Peach", "disease": "Healthy",
        "description": "Plant appears healthy.",
        "treatment": ["Continue regular pruning", "Proper irrigation", "Fertilize in early spring"],
        "severity": "None"
    },
    # Pepper
    "Pepper,_bell___Bacterial_spot": {
        "plant": "Bell Pepper", "disease": "Bacterial Spot",
        "description": "Caused by Xanthomonas campestris, producing dark water-soaked leaf spots.",
        "treatment": ["Apply copper hydroxide sprays", "Use disease-free certified seeds", "Avoid working in fields when wet", "Rotate crops every 2–3 years"],
        "severity": "High"
    },
    "Pepper,_bell___healthy": {
        "plant": "Bell Pepper", "disease": "Healthy",
        "description": "Plant appears healthy.",
        "treatment": ["Maintain consistent watering", "Fertilize with balanced NPK", "Monitor for aphids"],
        "severity": "None"
    },
    # Potato
    "Potato___Early_blight": {
        "plant": "Potato", "disease": "Early Blight",
        "description": "Fungal disease (Alternaria solani) causing dark brown target-ring lesions.",
        "treatment": ["Apply chlorothalonil or mancozeb fungicides", "Remove infected lower leaves", "Ensure adequate potassium nutrition", "Avoid overhead irrigation"],
        "severity": "Medium"
    },
    "Potato___Late_blight": {
        "plant": "Potato", "disease": "Late Blight",
        "description": "Caused by Phytophthora infestans — the pathogen behind the Irish Famine.",
        "treatment": ["Apply metalaxyl or chlorothalonil preventively", "Destroy infected plant material immediately", "Plant certified disease-free tubers", "Monitor weather for high-risk conditions"],
        "severity": "Severe"
    },
    "Potato___healthy": {
        "plant": "Potato", "disease": "Healthy",
        "description": "Plant appears healthy.",
        "treatment": ["Hill soil regularly", "Monitor for Colorado beetle", "Adequate irrigation"],
        "severity": "None"
    },
    # Raspberry
    "Raspberry___healthy": {
        "plant": "Raspberry", "disease": "Healthy",
        "description": "Plant appears healthy.",
        "treatment": ["Prune old canes annually", "Mulch around base", "Monitor for spider mites"],
        "severity": "None"
    },
    # Soybean
    "Soybean___healthy": {
        "plant": "Soybean", "disease": "Healthy",
        "description": "Plant appears healthy.",
        "treatment": ["Maintain crop rotation", "Monitor for aphids and spider mites", "Balanced fertilization"],
        "severity": "None"
    },
    # Squash
    "Squash___Powdery_mildew": {
        "plant": "Squash", "disease": "Powdery Mildew",
        "description": "Fungal disease causing white powdery growth on leaf surfaces.",
        "treatment": ["Apply potassium bicarbonate or neem oil", "Plant resistant varieties", "Space plants for air circulation", "Remove heavily infected leaves"],
        "severity": "Medium"
    },
    # Strawberry
    "Strawberry___Leaf_scorch": {
        "plant": "Strawberry", "disease": "Leaf Scorch",
        "description": "Caused by Diplocarpon earlianum, producing purple-red irregular spots.",
        "treatment": ["Apply captan or myclobutanil fungicides", "Remove infected leaves", "Avoid overhead watering", "Renovate beds after harvest"],
        "severity": "Medium"
    },
    "Strawberry___healthy": {
        "plant": "Strawberry", "disease": "Healthy",
        "description": "Plant appears healthy.",
        "treatment": ["Mulch around plants", "Regular irrigation", "Remove old leaves after harvest"],
        "severity": "None"
    },
    # Tomato
    "Tomato___Bacterial_spot": {
        "plant": "Tomato", "disease": "Bacterial Spot",
        "description": "Caused by Xanthomonas species, producing dark water-soaked lesions on all plant parts.",
        "treatment": ["Apply copper-based bactericides", "Use disease-free seeds/transplants", "Avoid overhead irrigation", "Rotate crops annually"],
        "severity": "High"
    },
    "Tomato___Early_blight": {
        "plant": "Tomato", "disease": "Early Blight",
        "description": "Fungal disease (Alternaria solani) causing concentric ring lesions — bull's-eye pattern.",
        "treatment": ["Apply chlorothalonil or mancozeb every 7–10 days", "Remove lower infected leaves", "Stake plants to improve air circulation", "Mulch to prevent soil splash"],
        "severity": "Medium"
    },
    "Tomato___Late_blight": {
        "plant": "Tomato", "disease": "Late Blight",
        "description": "Caused by Phytophthora infestans — rapidly destructive in cool wet weather.",
        "treatment": ["Apply metalaxyl-based fungicides preventively", "Remove and destroy all infected tissue", "Avoid overhead watering", "Destroy all crop debris after season"],
        "severity": "Severe"
    },
    "Tomato___Leaf_Mold": {
        "plant": "Tomato", "disease": "Leaf Mold",
        "description": "Caused by Passalora fulva in high humidity greenhouse conditions.",
        "treatment": ["Improve greenhouse ventilation", "Apply mancozeb or copper fungicides", "Reduce relative humidity below 85%", "Use resistant varieties"],
        "severity": "Medium"
    },
    "Tomato___Septoria_leaf_spot": {
        "plant": "Tomato", "disease": "Septoria Leaf Spot",
        "description": "Fungal disease (Septoria lycopersici) causing small circular spots with dark borders.",
        "treatment": ["Apply chlorothalonil or mancozeb preventively", "Remove infected lower leaves", "Mulch soil surface", "Stake for better air flow"],
        "severity": "Medium"
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "plant": "Tomato", "disease": "Spider Mites",
        "description": "Tiny arachnids causing stippled, bronzed leaves and fine webbing.",
        "treatment": ["Apply miticides (abamectin, bifenazate)", "Use insecticidal soap or neem oil", "Increase humidity around plants", "Introduce predatory mites (Phytoseiidae)"],
        "severity": "Medium"
    },
    "Tomato___Target_Spot": {
        "plant": "Tomato", "disease": "Target Spot",
        "description": "Caused by Corynespora cassiicola, producing brown circular spots with concentric rings.",
        "treatment": ["Apply azoxystrobin or chlorothalonil fungicides", "Improve air circulation", "Remove infected leaves", "Avoid excessive nitrogen fertilization"],
        "severity": "Medium"
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "plant": "Tomato", "disease": "Yellow Leaf Curl Virus",
        "description": "Viral disease transmitted by whiteflies, causing leaf curling and yellowing.",
        "treatment": ["Control whitefly populations with imidacloprid or neem", "Use reflective mulches to deter whiteflies", "Plant resistant tomato varieties", "Remove and destroy infected plants early"],
        "severity": "Severe"
    },
    "Tomato___Tomato_mosaic_virus": {
        "plant": "Tomato", "disease": "Mosaic Virus",
        "description": "Viral disease causing mottled light-dark green mosaic pattern on leaves.",
        "treatment": ["No chemical cure — remove infected plants", "Sanitize tools with bleach solution", "Control aphid vectors", "Use virus-free certified seeds"],
        "severity": "High"
    },
    "Tomato___healthy": {
        "plant": "Tomato", "disease": "Healthy",
        "description": "Plant appears healthy.",
        "treatment": ["Maintain consistent watering", "Stake or cage plants", "Fertilize with calcium to prevent blossom end rot"],
        "severity": "None"
    },
}

SEVERITY_COLOR = {
    "None":   ("#22c55e", "rgba(34,197,94,0.12)"),
    "Medium": ("#f59e0b", "rgba(245,158,11,0.12)"),
    "High":   ("#ef4444", "rgba(239,68,68,0.10)"),
    "Severe": ("#dc2626", "rgba(220,38,38,0.15)"),
}


# ─── MODEL LOADING ───────────────────────────────────────────────────────────────
@st.cache_resource
def load_models():
    models = {}
    errors = []

    # EfficientNet
    try:
        import tensorflow as tf
        eff_path = "/kaggle/input/datasets/ayamahmoudalhareidi/dmprojectds/final_model.keras"
        if not os.path.exists(eff_path):
            eff_path = "/kaggle/working/final_model.keras"
        if os.path.exists(eff_path):
            models["efficientnet"] = tf.keras.models.load_model(eff_path)
    except Exception as e:
        errors.append(f"EfficientNet: {e}")

    # Class names
    try:
        for p in ["/kaggle/input/datasets/ayamahmoudalhareidi/dmprojectds/class_names.json",
                  "/kaggle/working/class_names.json"]:
            if os.path.exists(p):
                with open(p) as f:
                    models["class_names"] = json.load(f)
                break
    except Exception as e:
        errors.append(f"Class names: {e}")

    # Ensemble
    try:
        for p in ["/kaggle/input/datasets/ayamahmoudalhareidi/ml-models/ensemble.pkl",
                  "/kaggle/working/ensemble.pkl"]:
            if os.path.exists(p):
                with open(p, "rb") as f:
                    ens = pickle.load(f)
                models["ensemble"]  = ens.get("ensemble")
                models["scaler"]    = ens.get("scaler")
                models["pca"]       = ens.get("pca")
                models["le"]        = ens.get("le")
                break
    except Exception as e:
        errors.append(f"Ensemble: {e}")

    return models, errors


def get_db_info(raw_class: str) -> dict:
    if raw_class in DISEASE_DB:
        return DISEASE_DB[raw_class]
    for key, val in DISEASE_DB.items():
        if key.lower() == raw_class.lower():
            return val
    # Fallback: parse name
    parts = raw_class.replace("___", " — ").replace("_", " ").split(" — ")
    plant   = parts[0].strip() if len(parts) > 0 else raw_class
    disease = parts[1].strip() if len(parts) > 1 else "Unknown"
    is_healthy = "healthy" in raw_class.lower()
    return {
        "plant": plant,
        "disease": "Healthy" if is_healthy else disease,
        "description": "This plant appears healthy." if is_healthy else f"Detected condition: {disease}.",
        "treatment": ["Continue current care practices."] if is_healthy else ["Consult a local agronomist.", "Monitor the plant closely."],
        "severity": "None" if is_healthy else "Medium"
    }


def predict_efficientnet(img: Image.Image, model, class_names):
    import tensorflow as tf
    img_r = img.convert("RGB").resize((224, 224))
    arr = np.array(img_r, dtype=np.float32)
    arr = np.expand_dims(arr, 0)
    from tensorflow.keras.applications.efficientnet_v2 import preprocess_input
    arr = preprocess_input(arr)
    preds = model.predict(arr, verbose=0)[0]
    idx = int(np.argmax(preds))
    return class_names[idx], float(preds[idx])


def predict_ensemble(img: Image.Image, models_dict):
    import tensorflow as tf
    from tensorflow.keras.applications import ResNet50
    from tensorflow.keras.applications.resnet50 import preprocess_input as resnet_pre
    from tensorflow.keras.preprocessing import image as keras_image

    resnet = ResNet50(weights="imagenet", include_top=False, pooling="avg")
    img_r = img.convert("RGB").resize((224, 224))
    arr = keras_image.img_to_array(img_r)
    arr = np.expand_dims(arr, 0)
    arr = resnet_pre(arr)
    feat = resnet.predict(arr, verbose=0).flatten()
    feat_scaled = models_dict["scaler"].transform([feat])
    feat_pca = models_dict["pca"].transform(feat_scaled)
    pred_label = models_dict["ensemble"].predict(feat_pca)[0]
    proba = models_dict["ensemble"].predict_proba(feat_pca)[0]
    class_name = models_dict["le"].inverse_transform([pred_label])[0]
    confidence = float(np.max(proba))
    return class_name, confidence


# ─── RENDER RESULT ───────────────────────────────────────────────────────────────
def render_result(class_name: str, confidence: float, model_label: str):
    info = get_db_info(class_name)
    is_healthy = info["disease"].lower() == "healthy"
    sev_color, sev_bg = SEVERITY_COLOR.get(info["severity"], ("#94a3b8", "rgba(148,163,184,0.1)"))
    box_cls = "result-healthy" if is_healthy else "result-diseased"
    status_cls = "healthy" if is_healthy else "diseased"
    status_icon = "✅" if is_healthy else "⚠️"
    bar_color = "#22c55e" if is_healthy else "#ef4444"
    conf_pct = int(confidence * 100)

    st.markdown(f"""
    <div class="result-box {box_cls}">
        <div class="result-status {status_cls}">{status_icon} &nbsp; {info['severity'].upper() if not is_healthy else 'HEALTHY PLANT'}</div>
        <div class="result-plant">{info['plant']}</div>
        <div class="result-disease">{info['disease']}</div>
        <div style="font-size:12px;color:rgba(255,255,255,0.35);margin-bottom:6px;letter-spacing:0.08em;">CONFIDENCE — {model_label}</div>
        <div class="conf-bar-bg">
            <div class="conf-bar-fill" style="width:{conf_pct}%; background: linear-gradient(90deg, {bar_color}, {bar_color}cc);"></div>
        </div>
        <div class="conf-pct">{conf_pct}% confidence</div>
    </div>
    """, unsafe_allow_html=True)

    # Description
    st.markdown(f"""
    <div class="info-section">
        <div class="info-header">
            <div class="info-icon green">🔬</div>
            <div class="info-title">About This Condition</div>
        </div>
        <div class="info-body">{info['description']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Treatment
    if info.get("treatment"):
        items = "".join(f"<li>{t}</li>" for t in info["treatment"])
        icon_cls = "green" if is_healthy else "gold"
        icon = "💚" if is_healthy else "💊"
        title = "Care Recommendations" if is_healthy else "Treatment Protocol"
        st.markdown(f"""
        <div class="info-section">
            <div class="info-header">
                <div class="info-icon {icon_cls}">{icon}</div>
                <div class="info-title">{title}</div>
            </div>
            <div class="info-body"><ul>{items}</ul></div>
        </div>
        """, unsafe_allow_html=True)

    # Severity badge
    if not is_healthy:
        st.markdown(f"""
        <div class="info-section">
            <div class="info-header">
                <div class="info-icon red">⚡</div>
                <div class="info-title">Severity Level</div>
            </div>
            <div class="info-body">
                <span style="
                    display:inline-block;
                    background:{sev_bg};
                    border:1px solid {sev_color}55;
                    color:{sev_color};
                    border-radius:20px;
                    padding:4px 16px;
                    font-size:13px;
                    font-weight:700;
                    letter-spacing:0.1em;
                ">{info['severity'].upper()}</span>
                <p style="margin-top:10px;">
                    {"Immediate action recommended — this disease can cause significant crop loss." if info['severity'] in ("Severe","High") else "Monitor closely and apply recommended treatments promptly."}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_fused(results):
    (cls_a, conf_a, lbl_a), (cls_b, conf_b, lbl_b) = results

    # لو نفس النتيجة → متوسط بسيط
    if cls_a == cls_b:
        render_result(
            cls_a,
            (conf_a + conf_b) / 2,
            f"Fused ({lbl_a} + {lbl_b})"
        )
        return

    # اختيار الأعلى ثقة
    if conf_a >= conf_b:
        final_cls, final_conf, final_lbl = cls_a, conf_a, lbl_a
    else:
        final_cls, final_conf, final_lbl = cls_b, conf_b, lbl_b

    st.markdown("""
    <div style="
        background: rgba(56,189,248,0.08);
        border: 1px solid rgba(56,189,248,0.25);
        border-radius: 12px;
        padding: 10px 14px;
        margin-bottom: 10px;
        color: #38bdf8;
        font-size: 13px;">
        🧠 Fused Decision (Best Confidence Selected)
    </div>
    """, unsafe_allow_html=True)

    render_result(final_cls, final_conf, f"Fused ({final_lbl})")

# ─── MAIN APP ────────────────────────────────────────────────────────────────────
def main():
    # University Banner
    st.markdown("""
    <div class="uni-banner">
        <div class="uni-left">
            <div class="uni-icon">🎓</div>
            <div>
                <div class="uni-name">AL RYADA UNIVERSITY</div>
                <div class="uni-dept">Faculty of Computers &amp; Artificial Intelligence</div>
            </div>
        </div>
        <div class="uni-badge">🌿 AI Project</div>
    </div>
    """, unsafe_allow_html=True)

    # Hero
    st.markdown("""
    <div class="hero">
        <div class="hero-tag"> AI-Powered Precision Agriculture</div>
        <h1 class="hero-title">Plant<span>Guard</span> AI</h1>
        <p class="hero-sub">Upload a leaf image and our dual-model AI instantly diagnoses diseases with treatment recommendations.</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    st.markdown("""
    <div class="stat-row">
        <div class="stat-card">
            <div class="stat-val">38</div>
            <div class="stat-lbl">Disease Classes</div>
        </div>
        <div class="stat-card">
            <div class="stat-val">14</div>
            <div class="stat-lbl">Plant Species</div>
        </div>
        <div class="stat-card">
            <div class="stat-val">2</div>
            <div class="stat-lbl">AI Models</div>
        </div>
        <div class="stat-card">
            <div class="stat-val">95%+</div>
            <div class="stat-lbl">Accuracy</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Load models
    models, load_errors = load_models()

    # Two columns
    left_col, right_col = st.columns([1, 1.1], gap="large")

    with left_col:
        st.markdown('<div class="section-lbl">Upload Your Image</div>', unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Choose a plant leaf image",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed"
        )

        st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-lbl">Select AI Model</div>', unsafe_allow_html=True)

        model_choice = st.selectbox(
            "Model",
            options=["EfficientNetV2B0 (Deep Learning)", "Ensemble (LR + SVM + RF)", "Both Models"],
            label_visibility="collapsed"
        )

        st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)

        analyze_btn = st.button("🔍  Analyze Plant", use_container_width=True)

        if uploaded:
            img = Image.open(uploaded).convert("RGB")
            st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-lbl">Uploaded Image</div>', unsafe_allow_html=True)
            st.image(img, use_container_width=True)

        # Model info pills
        st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div>
            <div class="section-lbl">Active Models</div>
            <span class="model-pill">⚡ EfficientNetV2B0</span>
            <span class="model-pill">🧠 LR + SVM + RF Ensemble</span>
            <span class="model-pill">🔗 ResNet50 Features</span>
        </div>
        """, unsafe_allow_html=True)

    with right_col:
        if analyze_btn and uploaded:
            img = Image.open(uploaded).convert("RGB")

            with st.spinner("Analyzing..."):
                results = []

                # EfficientNet
                if model_choice in ("EfficientNetV2B0 (Deep Learning)", "Both Models"):
                    if "efficientnet" in models and "class_names" in models:
                        cls, conf = predict_efficientnet(img, models["efficientnet"], models["class_names"])
                        results.append((cls, conf, "EfficientNetV2B0"))
                    else:
                        st.warning("⚠️ EfficientNet model not loaded.")

                # Ensemble
                if model_choice in ("Ensemble (LR + SVM + RF)", "Both Models"):
                    if "ensemble" in models:
                        cls, conf = predict_ensemble(img, models)
                        results.append((cls, conf, "Ensemble"))
                    else:
                        st.warning("⚠️ Ensemble model not loaded.")

            if results:
                
                
                 st.markdown('<div class="section-lbl">Diagnosis Results</div>', unsafe_allow_html=True)

    
                 if len(results) == 2:
                    render_fused(results)
                 else:
                    cls, conf, lbl = results[0]
                    render_result(cls, conf, lbl)
            else:
                st.error("No results. Check model files are accessible.")

        elif not uploaded:
            # Placeholder state
            st.markdown("""
            <div style="
                height: 480px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                background: rgba(255,255,255,0.02);
                border: 1.5px dashed rgba(34,197,94,0.2);
                border-radius: 24px;
                text-align: center;
            ">
                <div style="font-size: 64px; margin-bottom: 20px; opacity: 0.6;">🌿</div>
                <div style="font-size: 18px; color: rgba(255,255,255,0.5); font-family: 'Playfair Display', serif; margin-bottom: 8px;">
                    Ready to Diagnose
                </div>
                <div style="font-size: 13px; color: rgba(255,255,255,0.25); max-width: 260px; line-height: 1.6;">
                    Upload a plant leaf image on the left and click Analyze
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="divider"></div>
    <div style="text-align:center; padding: 16px 0 32px;">
        <div style="font-size:13px; color:rgba(255,255,255,0.2); letter-spacing:0.08em;">
            PlantGuard AI &nbsp;·&nbsp; AL RYADA UNIVERSITY &nbsp;·&nbsp; Faculty of Computers & AI &nbsp;·&nbsp; 2026
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
