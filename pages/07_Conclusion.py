# -*- coding: utf-8 -*-
"""
Streamlit — Conclusion du projet
Offre culturelle en France
"""

import streamlit as st
from pathlib import Path

# -------------------------
# Configuration de la page
# -------------------------
st.set_page_config(
    page_title="Conclusion - Offre culturelle en France",
    page_icon="🏁",
    layout="wide"
)

# -----------------------------------------
# Palette pastel
# -----------------------------------------
try:
    from config import pastel_colors  # type: ignore
except Exception:
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
      .stApp {{
        background: var(--bg);
      }}
      .block-container {{
        padding-top: 2.2rem;
        padding-bottom: 2rem;
      }}
      .soft-card {{
        background: #FFFFFF;
        border: 1px solid rgba(0,0,0,0.04);
        border-radius: 16px;
        padding: 1.1rem 1.2rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
      }}
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
      ul li {{
        line-height: 1.5;
      }}
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
# En-tête conclusion
# -------------------------
st.markdown(
  f"""
  <div class="hero">
    <h1 style="margin-bottom: 0.5rem;">🏁 Conclusion & Perspectives</h1>
    <p>Bilan de l’analyse de l’offre culturelle en France et pistes d’amélioration.</p>
  </div>
  """,
  unsafe_allow_html=True
)

st.markdown("")

# -------------------------
# Points clés
# -------------------------
st.markdown(
  f"""
  <h3>📌 Principaux enseignements</h3>
  <div class="soft-card">
    <ul>
      <li>Des disparités régionales marquées dans les offres proposées.</li>
      <li>Taux de fréquentation qui tendent vers une augmentation mais pas encore comparable au post-Covid. </li>
      <li>Fréquentation influencée par certains critères selon le thème (ex : Musées et prix, Festivals et saisonnalité, Bibliothèques et ouverture dominical)</li>
    </ul>
  </div>
  """,
  unsafe_allow_html=True
)

# -------------------------
# Recommandations
# -------------------------
st.markdown(
    f"""
    <h3>💡 Recommandations</h3>
    <div class="soft-card">
      <ul>
        <li>Mettre en place des politiques sociales pour renforcer l'accès aux offres culturelles (ex : le tarif de la place de cinéma) </li>
        <li>Faire des sondages dans les populations pour proposer une offre plus adaptées</li>
        <li>Réaffecter ou reconvertir les infrastructures lorsque la fréquentation est trop faible</li>
      </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Ressources
# -------------------------
st.markdown(
    f"""
    <h3>📂 Ressources</h3>
    <div class="soft-card">
        <ul>
          <li>Données : Ministère de la Culture, INSEE, data.gouv.fr.</li>
          <li>Visualisations : Dataiku, Streamlit + Matplotlib + Plotly.</li>
          <li>Code source : Python + dépôt GitHub du projet.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Bouton retour
# -------------------------
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

nav_html = """
<div class="nav-grid">
  <a class="nav-link" href="./Introduction">
    <div class="nav-card">
      <div class="pill">⬅️  Retour vers l'introduction</div>
    </div>
  </a>
</div>
"""
st.markdown(nav_html, unsafe_allow_html=True)
st.write("")
