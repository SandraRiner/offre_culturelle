# -*- coding: utf-8 -*-
"""
Streamlit — Carte simple des bibliothèques par région (version large)
"""

import os
import pandas as pd
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

# -------------------------------------------------------------
# Config Streamlit
# -------------------------------------------------------------
st.set_page_config(page_title="Bibliothèques — Carte par région", layout="wide")
st.title("📚 1. Carte des bibliothèques par région")

# -------------------------------------------------------------
# Chargement des données
# -------------------------------------------------------------
CSV_PATH = "/home/karim/code/offre_culturelle/data/adresses_des_bibliotheques_publiques_prepared.csv"
if not os.path.exists(CSV_PATH):
    st.error(f"CSV introuvable : {CSV_PATH}")
    st.stop()

try:
    df = pd.read_csv(CSV_PATH, sep=',', encoding="utf-8")
except Exception as e:
    st.error(f"Erreur de lecture CSV : {e}")
    st.stop()

required = ['Région', 'Latitude', 'Longitude']
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"Colonnes manquantes : {missing}")
    st.stop()

for col in ['Latitude', 'Longitude']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna(subset=['Région', 'Latitude', 'Longitude']).copy()
regions = sorted(df['Région'].astype(str).str.strip().unique())
if not regions:
    st.warning("Aucune région disponible après nettoyage.")
    st.stop()

# -------------------------------------------------------------
# 1. Barplot : nombre de bibliothèques par région
# -------------------------------------------------------------

st.header("📊 1. Nombre de bibliothèques par région")

biblio_region_counts = df["Région"].value_counts()
biblio_region_counts_sorted = biblio_region_counts.sort_values(ascending=True)

# Palette de couleurs unique par région
color_map = plt.cm.tab20.colors
region_colors = {region: color_map[i % len(color_map)] for i, region in enumerate(biblio_region_counts_sorted.index)}

fig, ax = plt.subplots(figsize=(10, 8))
biblio_region_counts_sorted.plot(
    kind="barh",
    ax=ax,
    color=[region_colors[reg] for reg in biblio_region_counts_sorted.index]
)
ax.set_xlabel("Nombre de bibliothèques")
ax.set_ylabel("Région")
ax.set_title("Nombre de bibliothèques par région", fontsize=14, weight="bold")
ax.invert_yaxis()
plt.tight_layout()

st.pyplot(fig)

# -------------------------------------------------------------
# 2. Ratio habitants / bibliothèque par région
# -------------------------------------------------------------

# -------------------------------------------------------------
# 3. Dropdown list : sélection de la région
# -------------------------------------------------------------
st.title("📊 3. Visualisation des bibliothèques regroupées par région")

# Appliquer un style CSS pour élargir le conteneur principal
st.markdown("""
    <style>
        .block-container {
            max-width: 95% !important;
            padding-left: 1rem;
            padding-right: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Sélecteur de région
# -------------------------------------------------------------
region_sel = st.selectbox("Sélectionné une région : ", regions)

dff = df[df['Région'] == region_sel]
if dff.empty:
    st.info("Aucune donnée pour cette région.")
    st.stop()

# -------------------------------------------------------------
# Carte Folium large + clustering
# -------------------------------------------------------------
lat0, lon0 = float(dff['Latitude'].median()), float(dff['Longitude'].median())
m = folium.Map(
    location=[lat0, lon0],
    zoom_start=7,
    tiles="OpenStreetMap",
    width='100%',
    height='100%'
)
cluster = MarkerCluster().add_to(m)

name_col = 'nom_de_l_etablissement' if 'nom_de_l_etablissement' in dff.columns else None

for _, row in dff.iterrows():
    popup_txt = str(row[name_col]) if name_col and pd.notna(row[name_col]) else None
    folium.CircleMarker(
        location=[float(row['Latitude']), float(row['Longitude'])],
        radius=3,
        color=None,
        fill=True,
        fill_opacity=0.7,
        popup=popup_txt,
    ).add_to(cluster)

# Affichage dans Streamlit avec largeur accrue
st_folium(m, width=1000, height=650, returned_objects=[])
