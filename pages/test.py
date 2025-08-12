# -*- coding: utf-8 -*-
"""
Streamlit — Bibliothèques
"""

import os
import pandas as pd
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import numpy as np

# --- Configuration de la page ---
st.set_page_config(
    page_title="Bibliothèques",
    page_icon="📊",
    layout="wide"
)

# --- Titre ---
st.title("📊 Bibliothèques")
st.markdown("Analyse et datavisualisation de l'offre culturelle en France")

# --- Chargement des données ---
biblio_file = pd.read_csv("/home/karim/code/offre_culturelle/data/adresses_des_bibliotheques_publiques_prepared.csv", sep=',')
population_file = pd.read_csv("/home/karim/code/offre_culturelle/data/population-france-par-dept.csv", sep=';')

# Nettoyer les noms de colonnes pour éviter les KeyError
population_file.columns = population_file.columns.str.strip()

# ------------------------------------
# 1. KPIS
# ------------------------------------
total_biblio = len(biblio_file)  # nombre total de lignes
nb_regions = biblio_file['Région'].nunique()  # nombre de régions uniques
moyenne_biblio = total_biblio / nb_regions  # moyenne par région

# --- Style CSS pour les cartes KPI ---
st.markdown("""
    <style>
    /* Conteneur des KPIs */
    [data-testid="stMetric"] {
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.05);
    }
    /* Label */
    [data-testid="stMetric"] label {
        font-size: 14px !important;
        color: #555;
    }
    /* Valeur */
    [data-testid="stMetric"] div {
        font-size: 24px !important;
        font-weight: bold;
        color: #222;
    }
    </style>
""", unsafe_allow_html=True)

# --- Affichage en 3 colonnes ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="➕ Total Bibliothèques", value=f"{total_biblio:,}".replace(",", " "))

with col2:
    st.metric(label="🌍 Nombre de Régions", value=f"{nb_regions}")

with col3:
    st.metric(label="➗ Moyenne par Région", value=f"{moyenne_biblio:.2f}")

# ------------------------------------
# CARTE INTERACTIVE
# ------------------------------------
st.header("📍 Localisation des bibliothèques")

# Liste déroulante des régions
regions_list = sorted(biblio_file["Région"].dropna().unique())
region_selected = st.selectbox("Choisir une région :", regions_list)

# Filtrage par région sélectionnée
df_region = biblio_file[biblio_file["Région"] == region_selected]

if not df_region.empty:
    st.write(f"**{len(df_region)} bibliothèques** dans {region_selected}")

    # Filtrer uniquement les lignes avec coordonnées valides
    df_region = df_region.dropna(subset=["Latitude", "Longitude"])

    if not df_region.empty:
        # Calcul du centre de la carte
        lat_center = df_region["Latitude"].mean()
        lon_center = df_region["Longitude"].mean()

        # Création de la carte centrée sur la région
        m = folium.Map(location=[lat_center, lon_center], zoom_start=8)

        # Ajout d'un cluster de marqueurs
        marker_cluster = MarkerCluster().add_to(m)

        # Ajout des marqueurs pour chaque bibliothèque
        for _, row in df_region.iterrows():
            # Recherche du nom de la bibliothèque dans plusieurs colonnes possibles
            name_col = next(
                (col for col in ["code_bib", "nom", "Nom", "name", "Bibliothèque", "Etablissement"] 
                 if col in row.index and pd.notna(row[col])),
                None
            )

            popup_text = f"Région : {row['Région']}"
            if name_col:
                popup_text = f"{row[name_col]}<br>{popup_text}"

            folium.Marker(
                location=[row["Latitude"], row["Longitude"]],
                popup=popup_text,
                tooltip="📚 Bibliothèque"
            ).add_to(marker_cluster)

        # Affichage dans Streamlit
        st_folium(m, width=700, height=500)
    else:
        st.warning("Aucune bibliothèque avec coordonnées valides dans cette région.")
st.divider()

# ------------------------------------
# 1. Barplot : Nombre de bibliothèques par région
# ------------------------------------

# Comptage par région
region_counts = biblio_file['Région'].value_counts().reset_index()
region_counts.columns = ['Région', 'Nombre']

# Palette pastel (une couleur par région)
pastel_colors = [
    "#A1C9F4", "#FFB482", "#8DE5A1", "#FF9F9B", "#D0BBFF",
    "#DEBB9B", "#FAB0E4", "#CFCFCF", "#B3E2CD", "#FDCDAC",
    "#CBD5E8", "#F4CAE4", "#E6F5C9", "#FFF2AE"
]

# Création du graphique (taille réduite)
fig, ax = plt.subplots(figsize=(8, 4))
fig.subplots_adjust(left=0.1, right=0.9)

# Barplot
bars = ax.bar(
    region_counts['Région'],
    region_counts['Nombre'],
    color=pastel_colors,
    edgecolor='black'
)

# Ajouter les valeurs au-dessus
for bar in bars:
    height = bar.get_height()
    ax.annotate(
        f'{int(height)}',
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 3),
        textcoords="offset points",
        ha='center', va='bottom',
        fontsize=8
    )

# Titre et légende explicative
st.subheader("🔢 Nombre de bibliothèques par région")

# Personnalisation simple
ax.set_xlabel("Régions", fontsize=11)
ax.set_ylabel("Nombre de bibliothèques", fontsize=11)
ax.tick_params(axis='x', rotation=45, labelsize=9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Affichage centré dans Streamlit
st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ------------------------------------
# 2. Barplot + ligne population par région (Population en millions)
# ------------------------------------

# Comptage bibliothèques par région
region_counts = biblio_file['Région'].value_counts().reset_index()
region_counts.columns = ['Région', 'Nombre']

# Agrégation population par région
pop_counts = population_file.groupby('nom_region', as_index=False)['Total'].sum()

# Fusion sur le nom de région
df_merge = pd.merge(region_counts, pop_counts, left_on='Région', right_on='nom_region', how='inner')

# Palette pastel (pour les barres)
pastel_colors = [
    "#A1C9F4", "#FFB482", "#8DE5A1", "#FF9F9B", "#D0BBFF",
    "#DEBB9B", "#FAB0E4", "#CFCFCF", "#B3E2CD", "#FDCDAC",
    "#CBD5E8", "#F4CAE4", "#E6F5C9", "#FFF2AE"
]

# Titre et légende explicative
st.subheader("👥 Comparatif régional de la population et du nombre de bibliothèques")

# Création du graphique avec deux axes Y
fig, ax1 = plt.subplots(figsize=(8, 4))
fig.subplots_adjust(left=0.1, right=0.88)

# Barres → Nombre de bibliothèques
bars = ax1.bar(
    df_merge['Région'],
    df_merge['Nombre'],
    color=pastel_colors,
    edgecolor='black'
)
ax1.set_xlabel("Régions", fontsize=11)
ax1.set_ylabel("Nombre de bibliothèques", fontsize=11)
ax1.tick_params(axis='x', rotation=45, labelsize=9)

# Ajouter valeurs sur les barres
for bar in bars:
    height = bar.get_height()
    ax1.annotate(
        f'{int(height)}',
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 3),
        textcoords="offset points",
        ha='center', va='bottom',
        fontsize=8
    )

# Deuxième axe Y pour la population (en millions)
ax2 = ax1.twinx()
ax2.plot(
    df_merge['Région'],
    df_merge['Total'].astype(int) / 1_000_000,  # Conversion en millions
    color='red',
    marker='o',
    linestyle='-',
    linewidth=1.5,
    label='Population (M)'
)
ax2.set_ylabel("Population (millions)", fontsize=11)

# Légende
ax2.legend(loc='upper right', fontsize=9)

# Supprimer les bordures inutiles
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)

# Affichage centré
st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)
st.divider()

# ------------------------------------
# 3. Barplot : Nombre d'entrées par région
# ------------------------------------

# Filtrer et forcer en entier
biblio_entries = biblio_file.dropna(subset=['nombre_d_entrees'])
biblio_entries['nombre_d_entrees'] = biblio_entries['nombre_d_entrees'].fillna(0).astype(int)

# Compter combien de lignes restent après suppression des vides
nb_lignes_utilisees = len(biblio_entries)

# Agréger le nombre total d'entrées par région
region_entries = biblio_entries.groupby('Région', as_index=False)['nombre_d_entrees'].sum()

# Palette pastel
pastel_colors = [
    "#A1C9F4", "#FFB482", "#8DE5A1", "#FF9F9B", "#D0BBFF",
    "#DEBB9B", "#FAB0E4", "#CFCFCF", "#B3E2CD", "#FDCDAC",
    "#CBD5E8", "#F4CAE4", "#E6F5C9", "#FFF2AE"
]

# Création du graphique
fig, ax = plt.subplots(figsize=(8, 4))
fig.subplots_adjust(left=0.1, right=0.9)

# Conversion en millions pour l'affichage
bars = ax.bar(
    region_entries['Région'],
    region_entries['nombre_d_entrees'] / 1_000_000,  # Échelle en millions
    color=pastel_colors,
    edgecolor='black'
)

# Ajouter les valeurs au-dessus des barres (arrondies à 1 décimale)
for bar in bars:
    height = bar.get_height()
    ax.annotate(
        f'{height:.1f} M',
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 3),
        textcoords="offset points",
        ha='center', va='bottom',
        fontsize=8
    )

# Titre et légende explicative
st.subheader("🎟️ Nombre total d'entrées par région (en millions)")
st.caption(f"Calcul réalisé sur {nb_lignes_utilisees} lignes avec valeurs renseignées "
           f"dans 'nombre_d_entrees', au lieu des {len(biblio_file)} lignes initiales.")

# Personnalisation
ax.set_xlabel("Régions", fontsize=11)
ax.set_ylabel("Nombre total d'entrées (millions)", fontsize=11)
ax.tick_params(axis='x', rotation=45, labelsize=9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Affichage centré dans Streamlit
st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ------------------------------------
# 4. Barplot : Nombre d'entrées par région
# ------------------------------------

# Filtrer et forcer en entier
biblio_entries = biblio_file.dropna(subset=['nombre_d_entrees'])
biblio_entries['nombre_d_entrees'] = biblio_entries['nombre_d_entrees'].fillna(0).astype(int)

# Compter combien de lignes restent après suppression des vides
nb_lignes_utilisees = len(biblio_entries)

# Agréger le nombre total d'entrées par région
region_entries = biblio_entries.groupby('Région', as_index=False)['nombre_d_entrees'].sum()

# Agrégation population par région
pop_counts = population_file.groupby('nom_region', as_index=False)['Total'].sum()

# Fusion des deux datasets
df_merge = pd.merge(region_entries, pop_counts, left_on='Région', right_on='nom_region', how='inner')

# Palette pastel
pastel_colors = [
    "#A1C9F4", "#FFB482", "#8DE5A1", "#FF9F9B", "#D0BBFF",
    "#DEBB9B", "#FAB0E4", "#CFCFCF", "#B3E2CD", "#FDCDAC",
    "#CBD5E8", "#F4CAE4", "#E6F5C9", "#FFF2AE"
]

# Création du graphique avec deux axes Y
fig, ax1 = plt.subplots(figsize=(8, 4))
fig.subplots_adjust(left=0.1, right=0.88)

# Barres → Nombre d'entrées (en millions)
bars = ax1.bar(
    df_merge['Région'],
    df_merge['nombre_d_entrees'] / 1_000_000,  # Échelle millions
    color=pastel_colors,
    edgecolor='black'
)
ax1.set_xlabel("Régions", fontsize=11)
ax1.set_ylabel("Nombre d'entrées (millions)", fontsize=11)
ax1.tick_params(axis='x', rotation=45, labelsize=9)

# Ajouter valeurs sur les barres
for bar in bars:
    height = bar.get_height()
    ax1.annotate(
        f'{height:.1f} M',
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 3),
        textcoords="offset points",
        ha='center', va='bottom',
        fontsize=8
    )

# Deuxième axe Y → Population en millions
ax2 = ax1.twinx()
ax2.plot(
    df_merge['Région'],
    df_merge['Total'] / 1_000_000,  # Échelle millions
    color='red',
    marker='o',
    linestyle='-',
    linewidth=1.5,
    label='Population (millions)'
)
ax2.set_ylabel("Population (millions)", fontsize=11)

# Légende
ax2.legend(loc='upper right', fontsize=9)

# Supprimer bordures inutiles
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)

# Titre et légende explicative
st.subheader("🎟️ Nombre total d'entrées par région + population")
st.caption(f"Calcul réalisé sur {nb_lignes_utilisees} lignes avec valeurs renseignées "
           f"dans 'nombre_d_entrees', au lieu des {len(biblio_file)} lignes initiales.")

# Affichage centré dans Streamlit
st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ------------------------------------
# 5. Barplot : Bibliothèques + lignes population et entrées en millions
# ------------------------------------

# Filtrer et forcer en entier pour les entrées
biblio_entries = biblio_file.dropna(subset=['nombre_d_entrees'])
biblio_entries['nombre_d_entrees'] = biblio_entries['nombre_d_entrees'].fillna(0).astype(int)

# Compter combien de lignes restent après suppression des vides
nb_lignes_utilisees = len(biblio_entries)

# Agréger le nombre total d'entrées par région
region_entries = biblio_entries.groupby('Région', as_index=False)['nombre_d_entrees'].sum()

# Nombre de bibliothèques par région
region_biblio_count = biblio_file.groupby('Région', as_index=False).size()
region_biblio_count.columns = ['Région', 'nb_bibliotheques']

# Agrégation population par région
pop_counts = population_file.groupby('nom_region', as_index=False)['Total'].sum()

# Fusion des trois datasets
df_merge = (
    region_biblio_count
    .merge(region_entries, on='Région', how='inner')
    .merge(pop_counts, left_on='Région', right_on='nom_region', how='inner')
)

# Palette pastel
pastel_colors = [
    "#A1C9F4", "#FFB482", "#8DE5A1", "#FF9F9B", "#D0BBFF",
    "#DEBB9B", "#FAB0E4", "#CFCFCF", "#B3E2CD", "#FDCDAC",
    "#CBD5E8", "#F4CAE4", "#E6F5C9", "#FFF2AE"
]

# Création du graphique avec deux axes Y
fig, ax1 = plt.subplots(figsize=(9, 4))
fig.subplots_adjust(left=0.1, right=0.88)

x = np.arange(len(df_merge['Région']))

# Barres → Nombre de bibliothèques
bars_biblio = ax1.bar(
    x,
    df_merge['nb_bibliotheques'],
    label="Bibliothèques",
    color=pastel_colors,
    edgecolor='black'
)

ax1.set_xlabel("Régions", fontsize=11)
ax1.set_ylabel("Nombre de bibliothèques", fontsize=11)
ax1.set_xticks(x)
ax1.set_xticklabels(df_merge['Région'], rotation=45, fontsize=9)

# Ajouter valeurs au-dessus des barres
for bar in bars_biblio:
    ax1.annotate(f'{int(bar.get_height())}',
                 xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                 xytext=(0, 3), textcoords="offset points",
                 ha='center', va='bottom', fontsize=8)

# Axe Y droite → Population et entrées en millions
ax2 = ax1.twinx()

# Ligne bleue → Entrées (millions)
ax2.plot(
    x,
    df_merge['nombre_d_entrees'] / 1_000_000,
    color='blue',
    marker='o',
    linestyle='-',
    linewidth=1.5,
    label='Entrées (millions)'
)

# Ligne rouge → Population (millions)
ax2.plot(
    x,
    df_merge['Total'] / 1_000_000,
    color='red',
    marker='o',
    linestyle='-',
    linewidth=1.5,
    label='Population (millions)'
)

ax2.set_ylabel("Valeurs en millions", fontsize=11)

# Légendes
ax1.legend(loc='upper left', fontsize=9)
ax2.legend(loc='upper right', fontsize=9)

# Supprimer bordures inutiles
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)

# Titre et légende explicative
st.subheader("📊 Bibliothèques + Population et Entrées (en millions) par région")
st.caption(f"Calcul réalisé sur {nb_lignes_utilisees} lignes avec valeurs renseignées "
           f"dans 'nombre_d_entrees', au lieu des {len(biblio_file)} lignes initiales.")

# Affichage Streamlit
st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)