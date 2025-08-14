# -*- coding: utf-8 -*-
"""
Streamlit — Introduction du projet
Offre culturelle en France
"""

import streamlit as st

# -------------------------
# Configuration de la page
# -------------------------
st.set_page_config(
    page_title="Offre culturelle en France",
    page_icon="⭐",
    layout="wide"
)

# -----------------------------------------
# Palette pastel
# -----------------------------------------
try:
    # Si vous avez déjà défini pastel_colors(ex: dans un module config.py)
    from config import pastel_colors  # type: ignore
except Exception:
    # Palette pastel par défaut (douce et lisible)
    pastel_colors = [
        "#312E60","#4D2A6C","#692678","#852284","#A01E90","#BC1A9C",
        "#D816A8","#F412B4","#FF1DA8","#FF339C","#FF4A90","#FF6084",
        "#FF7678","#FF8D6C","#FF0066"
    ]

# -------------------------
# Styles légers (CSS)
# -------------------------
st.markdown(
    f"""
    <style>
      :root {{
        --bg: #FFFFFF;
        --primary: {pastel_colors[1]};
        --secondary: {pastel_colors[3]};
        --accent: {pastel_colors[5]};
        --text: {pastel_colors[7]};
        --muted: {pastel_colors[9]};
      }}
      /* Confort visuel global + évite le titre "rogné" en haut */
      .stApp {{
        background: var(--bg);
      }}
      .block-container {{
        padding-top: 2.2rem;
        padding-bottom: 2rem;
      }}
      /* Cartes douces */
      .soft-card {{
        background: #FFFFFF;
        border: 1px solid rgba(0,0,0,0.04);
        border-radius: 16px;
        padding: 1.1rem 1.2rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
      }}
      /* Titre avec bandeau pastel */
      .hero {{
        background: #FFFFFF;
        border-radius: 18px;
        padding: 28px 28px;
        color: #0b1b2b;
        border: 1px solid rgba(0,0,0,0.05);
      }}
      .hero h1 {{
        margin: 0 0 0.3rem 0;
        font-size: 2.0rem;
      }}
      .hero p {{
        margin: 0.2rem 0 0 0;
        font-size: 1.05rem;
      }}
      /* Puces lisibles */
      ul li {{
        line-height: 1.5;
      }}
      /* Lien/bouton discret */
      .cta {{
        display: inline-block;
        padding: 10px 14px;
        border-radius: 12px;
        background: var(--accent);
        color: #2b1b2b;
        text-decoration: none;
        font-weight: 600;
      }}
      .caption {{
        color: var(--muted);
        font-size: 0.86rem;
        margin-top: 0.4rem;
      }}
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# En-tête (Hero)
# -------------------------
st.markdown(
  f"""
  <div class="hero">
    <h1 style="margin-bottom: 0.5rem;">
      ⭐ Offre culturelle en France
    </h1>
    <p>
      <strong>Problématique :</strong> Comment assurer une répartition 
      <em>équitable</em> de l’offre culturelle sur le territoire&nbsp;?
    </p>
  </div>
  """,
  unsafe_allow_html=True
)

st.markdown("")

# -------------------------
# Bande d’images depuis assets/
# -------------------------
from pathlib import Path

# Chemin vers le dossier assets (à la racine du projet)
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

# Liste des images et légendes
images = [
    ("library.jpg",  "📚 Bibliothèques"),
    ("museum.jpg",   "🏛️ Musées"),
    ("cinema.jpg",   "🎬 Cinémas"),
    ("festival.jpg", "🎉 Festivals"),
]

# Colonnes pour afficher les images
cols = st.columns(len(images))

for col, (filename, caption) in zip(cols, images):
    img_path = ASSETS_DIR / filename
    if img_path.exists():
        col.image(str(img_path), use_container_width=True, caption=caption)
    else:
        col.error(f"Image manquante : {filename}")

# -------------------------
# Objectifs & Périmètre
# -------------------------
st.markdown(
  f"""
  <h3>🎯 Objectifs de l’étude</h3>
  <div class="soft-card">
    <ul>
    <li><strong>Mesurer</strong> l’accessibilité et la couverture de l’offre.</li>
    <li><strong>Comparer</strong> les régions selon des indicateurs.</li>
    <li><strong>Identifier</strong> les axes d'amélioration.</li>
    </ul>
  </div>
  """,
  unsafe_allow_html=True
)

st.markdown(
    f"""
    <h3>📍 Périmètre</h3>
    <div class="soft-card">
      <ul>
        <li><strong>Offres étudiées :</strong> bibliothèques, musées, cinémas, festivals.</li>
        <li><strong>Échelle d’analyse :</strong> régionale.</li>
        <li><strong>Période :</strong> sur 2024 principalement, avec les données disponibles les plus récentes.</li>
      </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Méthode & Indicateurs (aperçu)
# -------------------------
left, right = st.columns([1, 1])
with left:
    st.markdown(
      f"""
      <h3>🛠️ Démarche</h3>
      <div class="soft-card">
        <ol>
        <li><strong>Collecter</strong> les données (fichiers du defi.data.gouv.fr, open data).</li>
        <li><strong>Préparer</strong> les données (nettoyage, géocodage, normalisation).</li>
        <li><strong>Analyser</strong> les données (analyse descriptive et spatiale).</li>
        <li><strong>Visualiser</strong> les données (cartes, barplots, tableaux de bord interactifs).</li>
        </ol>
      </div>
      """,
      unsafe_allow_html=True
    )

with right:
    st.markdown(
      f"""
      <h3>🔑 Indicateurs clés</h3>
      <div class="soft-card">
        <ul>
        <li><strong>Densité</strong> : nombre d'équipements par habitant.</li>
        <li><strong>Couverture</strong> : pourcentage de la population à moins de X km d’un équipement.</li>
        <li><strong>Équité</strong> : écarts inter-territoires, quintiles.</li>
        <li><strong>Fréquentation</strong> : si disponible.</li>
        </ul>
      </div>
      """,
      unsafe_allow_html=True
    )

# -------------------------
# Navigation (cards arrondies, HTML simple)
# -------------------------

# Styles (une seule fois sur la page)
st.markdown("""
<style>
  .nav-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-top:8px; }
  .nav-card {
    border-radius:18px; padding:16px 18px; background:#fff;
    border:1px solid rgba(0,0,0,0.06); box-shadow:0 4px 12px rgba(0,0,0,0.06);
    transition:transform .08s ease, box-shadow .12s ease;
  }
  .nav-card:hover { transform:translateY(-2px); box-shadow:0 8px 18px rgba(0,0,0,0.10); }
  .nav-link { text-decoration:none; color:#111827; display:block; }
  .pill { display:inline-block; padding:6px 10px; border-radius:999px; background:#BDE0FE; font-weight:600; font-size:.95rem; }
  .hint { margin-top:6px; color:#475569; font-size:.92rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("### 🚀 Commencer l’exploration")

nav_html = """
<div class="nav-grid">
  <a class="nav-link" href="./Cinémas">
    <div class="nav-card">
      <div class="pill">🎬 Cinémas</div>
      <div class="hint">Vers l'infini et l'au-delà de la datavisualisation !</div>
    </div>
  </a>
  <a class="nav-link" href="./Festivals">
    <div class="nav-card">
      <div class="pill">🎵 Festivals</div>
      <div class="hint">Rock en Seine la collecte</div>
    </div>
  </a>
  <a class="nav-link" href="./Bibliothèques">
    <div class="nav-card">
      <div class="pill">📖 Bibliothèques</div>
      <div class="hint">Etre ou ne pas être analyser... </div>
    </div>
  </a>
  <a class="nav-link" href="./Musées">
    <div class="nav-card">
      <div class="pill">🏛️ Musées</div>
      <div class="hint">L'exposition ou l'exploration ?</div>
    </div>
  </a>
</div>
"""
st.markdown(nav_html, unsafe_allow_html=True)
st.write("")

# -------------------------
# Mentions rapides
# -------------------------
with st.expander("ℹ️ À propos des données & visuels"):
    st.markdown(
        """
        - Données : sources publiques / open data : Ministère de la Culture, INSEE, data.gouv.fr.
        - Images de cette page : **Unsplash** (licence libre de droits).
        - Palette : thème "Artefact" harmonisé pour faciliter la lecture.
        """
    )