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

# --- Titre centré ---
st.markdown("<h1 style='text-align: center;'>📊 Bibliothèques</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Analyse et datavisualisation de l'offre culturelle en France</p>", unsafe_allow_html=True)

# --- Chargement des données ---
biblio_file = pd.read_csv("/home/karim/code/offre_culturelle/data/adresses_des_bibliotheques_publiques_prepared.csv", sep=',')
population_file = pd.read_csv("/home/karim/code/offre_culturelle/data/population-france-par-dept.csv", sep=';')

# Nettoyer les noms de colonnes pour éviter les KeyError
population_file.columns = population_file.columns.str.strip()

# ------------------------------------
# KPIS
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
    /* Zone de texte */
    .commentary-box {
        background-color: #f8f9fa;
        border-left: 4px solid #007ACC;
        padding: 15px;
        margin: 20px 0;
        border-radius: 5px;
        font-style: italic;
        color: #555;
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

st.divider()

# ------------------------------------
# Palette couleur globale
# ------------------------------------
pastel_colors = [
    "#A1C9F4", "#FFB482", "#8DE5A1", "#FF9F9B", "#D0BBFF",
    "#DEBB9B", "#FAB0E4", "#CFCFCF", "#B3E2CD", "#FDCDAC",
    "#CBD5E8", "#F4CAE4", "#E6F5C9", "#FFF2AE"
]

# ------------------------------------
# 📍 CARTE INTERACTIVE - Bibliothèques
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
            # Recherche du nom de la bibliothèque
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
else:
    st.warning("Aucune donnée disponible pour cette région.")
st.divider()

# ------------------------------------
# 1. Nombre de bibliothèques par région
# ------------------------------------

st.subheader("1. 🔢 Nombre de bibliothèques par région")

# Comptage par région
region_counts = biblio_file['Région'].value_counts().reset_index()
region_counts.columns = ['Région', 'Nombre']

# Création du graphique
fig, ax = plt.subplots(figsize=(10, 5))
plt.subplots_adjust(bottom=0.2, left=0.08, right=0.95)

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
        fontsize=9
    )

# Personnalisation
ax.set_xlabel("Régions", fontsize=12, fontweight='bold')
ax.set_ylabel("Nombre de bibliothèques", fontsize=12, fontweight='bold')
ax.tick_params(axis='x', rotation=45, labelsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Affichage centré
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.pyplot(fig)

# Zone de texte commentaire
st.markdown("""
<div class="commentary-box">
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
</div>
""", unsafe_allow_html=True)

st.divider()

# ------------------------------------
# 2. Comparatif régional population et bibliothèques
# ------------------------------------

st.subheader("2. 👥 Comparatif régional de la population et du nombre de bibliothèques")

# Comptage bibliothèques par région
region_counts = biblio_file['Région'].value_counts().reset_index()
region_counts.columns = ['Région', 'Nombre']

# Agrégation population par région
pop_counts = population_file.groupby('nom_region', as_index=False)['Total'].sum()

# Fusion sur le nom de région
df_merge = pd.merge(region_counts, pop_counts, left_on='Région', right_on='nom_region', how='inner')

# Création du graphique avec deux axes Y
fig, ax1 = plt.subplots(figsize=(10, 5))
plt.subplots_adjust(bottom=0.2, left=0.08, right=0.88, top=0.9)

# Barres → Nombre de bibliothèques
bars = ax1.bar(
    df_merge['Région'],
    df_merge['Nombre'],
    color=pastel_colors,
    edgecolor='black'
)
ax1.set_xlabel("Régions", fontsize=12, fontweight='bold')
ax1.set_ylabel("Nombre de bibliothèques", fontsize=12, fontweight='bold')
ax1.tick_params(axis='x', rotation=45, labelsize=10)

# Ajouter valeurs sur les barres
for bar in bars:
    height = bar.get_height()
    ax1.annotate(
        f'{int(height)}',
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 3),
        textcoords="offset points",
        ha='center', va='bottom',
        fontsize=9
    )

# Deuxième axe Y pour la population (en millions)
ax2 = ax1.twinx()
ax2.plot(
    df_merge['Région'],
    df_merge['Total'].astype(int) / 1_000_000,  # Conversion en millions
    color='red',
    marker='o',
    linestyle='-',
    linewidth=2,
    markersize=6
)
ax2.set_ylabel("Population (millions)", fontsize=12, fontweight='bold')

# Supprimer les bordures inutiles
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)

# Affichage centré
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.pyplot(fig)

# Zone de texte commentaire
st.markdown("""
<div class="commentary-box">
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris congue vehicula nisi, eu tincidunt magna fermentum sit amet. 
Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Pellentesque habitant morbi tristique 
senectus et netus et malesuada fames ac turpis egestas.
</div>
""", unsafe_allow_html=True)

st.divider()

# ------------------------------------
# 3. Nombre total d'entrées par région
# ------------------------------------

st.subheader("3. 🎟️ Nombre total d'entrées par région (en millions)")

# Filtrer et forcer en entier
biblio_entries = biblio_file.dropna(subset=['nombre_d_entrees'])
biblio_entries['nombre_d_entrees'] = biblio_entries['nombre_d_entrees'].fillna(0).astype(int)

# Compter combien de lignes restent après suppression des vides
nb_lignes_utilisees = len(biblio_entries)

# Agréger le nombre total d'entrées par région
region_entries = biblio_entries.groupby('Région', as_index=False)['nombre_d_entrees'].sum()

# Création du graphique
fig, ax = plt.subplots(figsize=(10, 5))
plt.subplots_adjust(bottom=0.2, left=0.08, right=0.95)

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
        fontsize=9
    )

# Personnalisation
ax.set_xlabel("Régions", fontsize=12, fontweight='bold')
ax.set_ylabel("Nombre total d'entrées (millions)", fontsize=12, fontweight='bold')
ax.tick_params(axis='x', rotation=45, labelsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Affichage centré
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.pyplot(fig)

st.caption(f"Calcul réalisé sur {nb_lignes_utilisees} lignes avec valeurs renseignées dans 'nombre_d_entrees', au lieu des {len(biblio_file)} lignes initiales.")

# Zone de texte commentaire
st.markdown("""
<div class="commentary-box">
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam in dui mauris. Vivamus hendrerit arcu sed erat molestie vehicula. 
Sed auctor neque eu tellus rhoncus ut eleifend nibh porttitor. Ut in nulla enim. Phasellus molestie magna non est bibendum non 
venenatis nisl tempor. Suspendisse dictum feugiat nisl ut dapibus.
</div>
""", unsafe_allow_html=True)

st.divider()

# ------------------------------------
# 4. Nombre total d'entrées par région + population
# ------------------------------------

st.subheader("4. 🎟️ Nombre total d'entrées par région + population")

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

# Création du graphique avec deux axes Y
fig, ax1 = plt.subplots(figsize=(10, 5))
plt.subplots_adjust(bottom=0.2, left=0.08, right=0.88, top=0.9)

# Barres → Nombre d'entrées (en millions)
bars = ax1.bar(
    df_merge['Région'],
    df_merge['nombre_d_entrees'] / 1_000_000,  # Échelle millions
    color=pastel_colors,
    edgecolor='black'
)
ax1.set_xlabel("Régions", fontsize=12, fontweight='bold')
ax1.set_ylabel("Nombre d'entrées (millions)", fontsize=12, fontweight='bold')
ax1.tick_params(axis='x', rotation=45, labelsize=10)

# Ajouter valeurs sur les barres
for bar in bars:
    height = bar.get_height()
    ax1.annotate(
        f'{height:.1f} M',
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 3),
        textcoords="offset points",
        ha='center', va='bottom',
        fontsize=9
    )

# Deuxième axe Y → Population en millions
ax2 = ax1.twinx()
ax2.plot(
    df_merge['Région'],
    df_merge['Total'] / 1_000_000,  # Échelle millions
    color='red',
    marker='o',
    linestyle='-',
    linewidth=2,
    markersize=6
)
ax2.set_ylabel("Population (millions)", fontsize=12, fontweight='bold')

# Supprimer bordures inutiles
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)

# Affichage centré
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.pyplot(fig)

st.caption(f"Calcul réalisé sur {nb_lignes_utilisees} lignes avec valeurs renseignées dans 'nombre_d_entrees', au lieu des {len(biblio_file)} lignes initiales.")

# Zone de texte commentaire
st.markdown("""
<div class="commentary-box">
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, 
adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, 
euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi.
</div>
""", unsafe_allow_html=True)

st.divider()

# ------------------------------------
# 5. Bibliothèques + Population et Entrées par région
# ------------------------------------

st.subheader("5. 📊 Bibliothèques + Population et Entrées (en millions) par région")

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

# Création du graphique avec deux axes Y
fig, ax1 = plt.subplots(figsize=(11, 5))
plt.subplots_adjust(bottom=0.2, left=0.08, right=0.88, top=0.9)

x = np.arange(len(df_merge['Région']))

# Barres → Nombre de bibliothèques
bars_biblio = ax1.bar(
    x,
    df_merge['nb_bibliotheques'],
    color=pastel_colors,
    edgecolor='black'
)

ax1.set_xlabel("Régions", fontsize=12, fontweight='bold')
ax1.set_ylabel("Nombre de bibliothèques", fontsize=12, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(df_merge['Région'], rotation=45, fontsize=10)

# Ajouter valeurs au-dessus des barres
for bar in bars_biblio:
    ax1.annotate(f'{int(bar.get_height())}',
                 xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                 xytext=(0, 3), textcoords="offset points",
                 ha='center', va='bottom', fontsize=9)

# Axe Y droite → Population et entrées en millions
ax2 = ax1.twinx()

# Ligne bleue → Entrées (millions)
ax2.plot(
    x,
    df_merge['nombre_d_entrees'] / 1_000_000,
    color='blue',
    marker='o',
    linestyle='-',
    linewidth=2,
    markersize=6
)

# Ligne rouge → Population (millions)
ax2.plot(
    x,
    df_merge['Total'] / 1_000_000,
    color='red',
    marker='s',
    linestyle='-',
    linewidth=2,
    markersize=5
)

ax2.set_ylabel("Valeurs en millions", fontsize=12, fontweight='bold')

# Supprimer bordures inutiles
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)

# Affichage centré
col1, col2, col3 = st.columns([0.5, 9, 0.5])
with col2:
    st.pyplot(fig)

st.caption(f"Calcul réalisé sur {nb_lignes_utilisees} lignes avec valeurs renseignées dans 'nombre_d_entrees', au lieu des {len(biblio_file)} lignes initiales.")

# Zone de texte commentaire
st.markdown("""
<div class="commentary-box">
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. 
Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent mauris. Fusce nec tellus sed augue 
semper porta. Mauris massa. Vestibulum lacinia arcu eget nulla.
</div>
""", unsafe_allow_html=True)

st.divider()

# ------------------------------------
# 6. 📅 Ouvertes / Fermées le dimanche : Nombre + Entrées (millions)
# ------------------------------------

# On reprend la normalisation de la colonne
df_dimanche_detail = biblio_file[['Région', 'ouverture_le_dimanche', 'nombre_d_entrees']].copy()
df_dimanche_detail['ouverture_le_dimanche'] = (
    df_dimanche_detail['ouverture_le_dimanche']
    .astype(str).str.strip().str.lower()
    .replace({'nan': np.nan})
    .replace({'oui': 'Oui', 'true': 'Oui', '1': 'Oui', 'o': 'Oui',
              'non': 'Non', 'false': 'Non', '0': 'Non', 'n': 'Non'})
)
df_dimanche_detail['nombre_d_entrees'] = pd.to_numeric(
    df_dimanche_detail['nombre_d_entrees'], errors='coerce'
).fillna(0).astype(int)

# Ordre et palette
region_order = sorted(biblio_file['Région'].dropna().unique())
color_map = dict(zip(region_order, pastel_colors))
colors_ordered = [color_map[r] for r in region_order]

def plot_dimanche_vs_entrees(title, df_filtered):
    # Comptage bibliothèques
    total_bib = df_filtered.groupby('Région').size().reindex(region_order, fill_value=0)
    # Total entrées
    total_entrees = df_filtered.groupby('Région')['nombre_d_entrees'].sum().reindex(region_order, fill_value=0)

    fig, ax_left = plt.subplots(figsize=(10, 5))
    plt.subplots_adjust(bottom=0.2, left=0.08, right=0.88)

    # Barres : nombre de bibliothèques
    bars = ax_left.bar(region_order, total_bib.values,
                       color=colors_ordered, edgecolor='black')
    ax_left.set_xlabel("Régions", fontsize=12, fontweight='bold')
    ax_left.set_ylabel("Nombre de bibliothèques", fontsize=12, fontweight='bold')
    ax_left.tick_params(axis='x', rotation=45, labelsize=10)

    # Valeurs sur barres
    for b in bars:
        ax_left.annotate(f"{int(b.get_height())}",
                         (b.get_x() + b.get_width()/2, b.get_height()),
                         textcoords="offset points", xytext=(0,3),
                         ha="center", va="bottom", fontsize=8)

    # Ligne : entrées en millions
    ax_right = ax_left.twinx()
    ax_right.plot(region_order, total_entrees / 1_000_000,
                  color='blue', marker='o', linewidth=1.5)
    ax_right.set_ylabel("Entrées (millions)", fontsize=12, fontweight='bold')

    # Style
    ax_left.spines['top'].set_visible(False)
    ax_right.spines['top'].set_visible(False)

    # Affichage Streamlit
    st.subheader(title)
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        st.pyplot(fig)

# Graphique A : ouvertes le dimanche
df_open = df_dimanche_detail[df_dimanche_detail['ouverture_le_dimanche'] == 'Oui']
plot_dimanche_vs_entrees("📅 7. Bibliothèques ouvertes le dimanche : nombre vs entrées", df_open)

st.caption(f"Calcul réalisé sur {nb_lignes_utilisees} lignes avec valeurs renseignées dans 'nombre_d_entrees', au lieu des {len(biblio_file)} lignes initiales.")

# Zone de texte commentaire
st.markdown("""
<div class="commentary-box">
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. 
Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent mauris. Fusce nec tellus sed augue 
semper porta. Mauris massa. Vestibulum lacinia arcu eget nulla.
</div>
""", unsafe_allow_html=True)

st.divider()

# Graphique B : fermées le dimanche
df_closed = df_dimanche_detail[df_dimanche_detail['ouverture_le_dimanche'] == 'Non']
plot_dimanche_vs_entrees("📅 8. Bibliothèques fermées le dimanche : nombre vs entrées", df_closed)

st.caption(f"Calcul réalisé sur {nb_lignes_utilisees} lignes avec valeurs renseignées dans 'nombre_d_entrees', au lieu des {len(biblio_file)} lignes initiales.")

# Zone de texte commentaire
st.markdown("""
<div class="commentary-box">
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. 
Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent mauris. Fusce nec tellus sed augue 
semper porta. Mauris massa. Vestibulum lacinia arcu eget nulla.
</div>
""", unsafe_allow_html=True)

st.divider()