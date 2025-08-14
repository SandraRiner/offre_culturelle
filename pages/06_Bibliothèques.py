# -*- coding: utf-8 -*-
"""
Streamlit — Bibliothèques
"""

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# ------------------------------------
# Configuration de la page
# ------------------------------------
st.set_page_config(
    page_title="Bibliothèques",
    page_icon="📊",
    layout="wide"
)

# ------------------------------------
# Titre principal
# ------------------------------------
st.markdown(
    """
    <h1 style="text-align:center; margin-bottom: 0.3rem;">Bibliothèques de France 📊</h1>
    <p style="text-align:center; font-size:1.1rem; color:#555;">
        Analyse et datavisualisation
    </p>
    """,
    unsafe_allow_html=True
)

# ------------------------------------
# Données
# ------------------------------------
biblio_file = pd.read_csv(
    "data_prod/adresses_des_bibliotheques_publiques_prepared.csv", sep=','
)
population_file = pd.read_csv(
    "data_prod/population-france-par-dept.csv", sep=';'
)
population_file.columns = population_file.columns.str.strip()  # éviter les espaces

# ------------------------------------
# Palette et légende des régions
# ------------------------------------
pastel_colors = [
    "#312E60","#4D2A6C","#692678","#852284","#A01E90","#BC1A9C",
    "#D816A8","#F412B4","#FF1DA8","#FF339C","#FF4A90","#FF6084",
    "#FF7678","#FF8D6C","#FF0066"
]

region_labels = {
    "ARA": "Auvergne-Rhône-Alpes",
    "BFC": "Bourgogne-Franche-Comté",
    "BRE": "Bretagne",
    "CVL": "Centre-Val de Loire",
    "DROM": "Départements & Régions d'Outre-Mer",
    "GES": "Grand Est",
    "HDF": "Hauts-de-France",
    "IDF": "Île-de-France",
    "NAQ": "Nouvelle-Aquitaine",
    "NOR": "Normandie",
    "OCC": "Occitanie",
    "PACA": "Provence-Alpes-Côte d'Azur",
    "PDL": "Pays de la Loire",
}

# Filtrer uniquement les régions présentes dans la légende
region_order = [r for r in sorted(biblio_file['Région'].dropna().unique()) if r in region_labels]

# Map couleurs cohérentes
color_map = {r: pastel_colors[i % len(pastel_colors)] for i, r in enumerate(region_order)}

# ------------------------------------
# KPIS
# ------------------------------------
total_biblio = len(biblio_file)                     # nombre total de lignes
nb_regions = biblio_file['Région'].nunique()        # nombre de régions uniques
moyenne_biblio = total_biblio // nb_regions         # moyenne par région (entier)

# --- Style CSS pour les cartes KPI ---
st.markdown("""
    <style>
    [data-testid="stMetric"] {
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.05);
    }
    [data-testid="stMetric"] label {
        font-size: 14px !important;
        color: #555;
    }
    [data-testid="stMetric"] div {
        font-size: 24px !important;
        font-weight: bold;
        color: #222;
    }
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
    st.metric(label="➗ Moyenne par Région", value=f"{moyenne_biblio}")

st.divider()

# ------------------------------------
# Légende des abréviations de régions
# ------------------------------------
st.markdown("### 📍 Légende des abréviations des régions")

# Création du texte de légende de façon propre et lisible
legend_text = " • ".join([f"**{abbr}** = {nom}" for abbr, nom in region_labels.items()])
st.markdown(legend_text)

st.divider()

# ------------------------------------
# 1. Carte des bibliothèques par région
# ------------------------------------
st.subheader("1. 🧭 Carte des bibliothèques en France par région")

# Utiliser le fichier déjà chargé + filtrer les coordonnées manquantes
df_map = biblio_file.dropna(subset=['Latitude', 'Longitude']).copy()

# Couleurs par région (adaptées au nombre réel)
regions_unique = df_map['Région'].unique().tolist()
color_map = {r: c for r, c in zip(regions_unique, pastel_colors[:len(regions_unique)])}

fig1 = px.scatter_mapbox(
    df_map,
    lat='Latitude',
    lon='Longitude',
    color='Région',
    color_discrete_map=color_map,
    hover_name='Code_bib',
    title="Bibliothèques en France par région"
)
fig1.update_layout(
    mapbox_style="open-street-map",
    mapbox_center_lat=46.2,
    mapbox_center_lon=2.2,
    mapbox_zoom=4.8,
    height=800
)
st.plotly_chart(fig1)

st.divider()

# ------------------------------------
# 2. Nombre de bibliothèques par région (ordre alphabétique)
# ------------------------------------
st.subheader("2. 🔢 Nombre de bibliothèques par région")

region_counts = (
    biblio_file
    .groupby('Région', as_index=False)
    .size()
    .rename(columns={'size': 'Nombre'})
)

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(
    region_counts['Région'],
    region_counts['Nombre'],
    color=pastel_colors[:len(region_counts)],
    edgecolor='black'
)

for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{int(height)}',
                xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontsize=9)

ax.set_xlabel("Régions", fontsize=12, fontweight='bold')
ax.set_ylabel("Nombre de bibliothèques", fontsize=12, fontweight='bold')
ax.tick_params(axis='x', rotation=45, labelsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.pyplot(fig)

st.markdown("""
<div class="commentary-box">
Le nombre de bibliothèques varie fortement selon les régions françaises. L'Auvergne-Rhône-Alpes se distingue avec plus de 2 600 établissements, suivie par l'Occitanie (~1 990) et la Nouvelle-Aquitaine (~1 850).
À l'inverse, les DROM (~270) et la Normandie (~700) présentent les effectifs les plus faibles.
La majorité des autres régions comptent entre 700 et 1 300 bibliothèques.
</div>
""", unsafe_allow_html=True)

st.divider()

# ------------------------------------
# 3. Comparatif régional population et bibliothèques
# ------------------------------------
st.subheader("3. 👥 Comparatif régional de la population et du nombre de bibliothèques")

# Comptage bibliothèques par région (alphabétique)
region_counts = (
    biblio_file['Région'].value_counts()
    .rename_axis('Région')
    .reset_index(name='Nombre')
    .sort_values('Région')
    .reset_index(drop=True)
)

# Agrégation population par région
pop_counts = population_file.groupby('nom_region', as_index=False)['Total'].sum()

# Fusion
df_merge = pd.merge(region_counts, pop_counts, left_on='Région', right_on='nom_region', how='inner')

# Graphique 2 axes
fig, ax1 = plt.subplots(figsize=(10, 5))
bars = ax1.bar(
    df_merge['Région'], df_merge['Nombre'],
    color=pastel_colors[:len(df_merge)], edgecolor='black'
)
ax1.set_xlabel("Régions", fontsize=12, fontweight='bold')
ax1.set_ylabel("Nombre de bibliothèques", fontsize=12, fontweight='bold')
ax1.tick_params(axis='x', rotation=45, labelsize=10)

for bar in bars:
    height = bar.get_height()
    ax1.annotate(f'{int(height)}',
                 xy=(bar.get_x() + bar.get_width()/2, height),
                 xytext=(0, 3), textcoords="offset points",
                 ha='center', va='bottom', fontsize=9)

ax2 = ax1.twinx()
ax2.plot(
    df_merge['Région'], df_merge['Total'].astype(int) / 1_000_000,
    color='red', marker='o', linestyle='-', linewidth=2, markersize=6
)
ax2.set_ylabel("Population (millions)", fontsize=12, fontweight='bold')

ax1.legend(['Bibliothèques'], loc='upper left', fontsize=10)
ax2.legend(['Population (M)'], loc='upper right', fontsize=10)

ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)

col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.pyplot(fig)

st.markdown("""
<div class="commentary-box">
Certaines régions allient forte population et large réseau de bibliothèques (Auvergne-Rhône-Alpes, Occitanie, Nouvelle-Aquitaine).
D'autres, comme l'Île-de-France, ont une population importante mais relativement peu de bibliothèques.
</div>
""", unsafe_allow_html=True)

# ------------------------------------
# Scatter plot : Population vs Bibliothèques
# ------------------------------------
df_merge['Densité (pour 100k)'] = (df_merge['Nombre'] / df_merge['Total']) * 100_000

fig_scatter, ax = plt.subplots(figsize=(8, 6))
colors_scatter = pastel_colors[:len(df_merge)]
sizes = (df_merge['Densité (pour 100k)'] * 10).clip(lower=30, upper=400)  # tailles lisibles

ax.scatter(
    df_merge['Total'] / 1_000_000,  # Population en millions
    df_merge['Nombre'],
    color=colors_scatter,
    edgecolor='black',
    s=sizes,
    alpha=0.85
)

# Droite de régression
x_vals = df_merge['Total'] / 1_000_000
y_vals = df_merge['Nombre']
m, b = np.polyfit(x_vals, y_vals, 1)
ax.plot(x_vals, m * x_vals + b, color='gray', linestyle='--', linewidth=1.5, label='Tendance')

# Labels
for _, row in df_merge.iterrows():
    ax.text(row['Total'] / 1_000_000, row['Nombre'] + 30, row['Région'], fontsize=8, ha='center')

ax.set_xlabel("Population (millions)", fontsize=12, fontweight='bold')
ax.set_ylabel("Nombre de bibliothèques", fontsize=12, fontweight='bold')
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.pyplot(fig_scatter)

st.markdown("""
<div class="commentary-box">
Les régions au-dessus de la droite de tendance sont mieux dotées que la moyenne pour leur population ; à l'inverse, celles en dessous le sont moins.
</div>
""", unsafe_allow_html=True)

st.divider()

# ------------------------------------
# 4. Nombre total d'entrées par région
# ------------------------------------
st.subheader("4. 🎟️ Nombre total d'entrées par région (en millions)")

# 1) Périmètre commun : uniquement les lignes avec une valeur d'entrées
biblio_entries = biblio_file.copy()
biblio_entries['nombre_d_entrees'] = pd.to_numeric(
    biblio_entries['nombre_d_entrees'], errors='coerce'
)
biblio_entries = biblio_entries.dropna(subset=['nombre_d_entrees'])
biblio_entries['nombre_d_entrees'] = biblio_entries['nombre_d_entrees'].astype(int)
nb_lignes_utilisees = len(biblio_entries)

# 2) Agrégation sur ce périmètre (tri alphabétique pour cohérence visuelle)
region_entries = (
    biblio_entries
    .groupby('Région', as_index=False)['nombre_d_entrees']
    .sum()
    .sort_values('Région')
    .reset_index(drop=True)
)

# 3) Graphique
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(
    region_entries['Région'],
    region_entries['nombre_d_entrees'] / 1_000_000,  # millions
    color=pastel_colors[:len(region_entries)],
    edgecolor='black'
)

# Labels au-dessus des barres
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.1f} M',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontsize=9)

# Mise en forme
ax.set_xlabel("Régions", fontsize=12, fontweight='bold')
ax.set_ylabel("Nombre total d'entrées (millions)", fontsize=12, fontweight='bold')
ax.tick_params(axis='x', rotation=45, labelsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Affichage centré
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.pyplot(fig)

st.caption(
    f"Calcul réalisé sur {nb_lignes_utilisees} lignes avec valeurs renseignées dans 'nombre_d_entrees' "
    f"(sur {len(biblio_file)} lignes initiales)."
)

st.markdown("""
<div class="commentary-box">
L'Ile de France domine largement la fréquentation avec 15,8 millions d'entrées, suivie par l'Auvergne Rhone Alpes et l'Occitanie.
À l'inverse, les DROM et certaines régions comme la Bourgogne-Franche-Comté affichent des volumes nettement plus faibles.
</div>
""", unsafe_allow_html=True)

st.divider()

# ------------------------------------
# 5. Bibliothèques + Population et Entrées par région
# ------------------------------------
st.subheader("5. 🎟️ Comparatif à 3 facteurs : Bibliothèques, population et fréquentation")

# 1) Périmètre commun : garder uniquement les lignes avec une valeur d'entrées
biblio_entries = biblio_file.copy()
biblio_entries['nombre_d_entrees'] = pd.to_numeric(
    biblio_entries['nombre_d_entrees'], errors='coerce'
)
biblio_entries = biblio_entries.dropna(subset=['nombre_d_entrees'])
biblio_entries['nombre_d_entrees'] = biblio_entries['nombre_d_entrees'].astype(int)
nb_lignes_utilisees = len(biblio_entries)

# 2) Agrégations sur ce même périmètre
#    - total d'entrées par région
region_entries = (
    biblio_entries.groupby('Région', as_index=False)['nombre_d_entrees'].sum()
)

#    - nombre de bibliothèques (uniquement celles ayant des entrées renseignées)
region_biblio_count = (
    biblio_entries.groupby('Région', as_index=False)
    .size()
    .rename(columns={'size': 'nb_bibliotheques'})
)

#    - population, restreinte aux régions présentes dans le périmètre
regions_avec_entrees = sorted(biblio_entries['Région'].dropna().unique())
pop_counts = (
    population_file[population_file['nom_region'].isin(regions_avec_entrees)]
    .groupby('nom_region', as_index=False)['Total'].sum()
)

# 3) Fusion des trois jeux de données
df_merge_5 = (
    region_biblio_count
    .merge(region_entries, on='Région', how='inner')
    .merge(pop_counts, left_on='Région', right_on='nom_region', how='inner')
    .sort_values('Région')
    .reset_index(drop=True)
)

# 4) Graphique à deux axes
fig, ax1 = plt.subplots(figsize=(11, 5))
x = np.arange(len(df_merge_5['Région']))

# Barres → Nombre de bibliothèques (périmètre "avec entrées")
bars_biblio = ax1.bar(
    x,
    df_merge_5['nb_bibliotheques'],
    color=pastel_colors[:len(df_merge_5)],
    edgecolor='black'
)
ax1.set_xlabel("Régions", fontsize=12, fontweight='bold')
ax1.set_ylabel("Nombre de bibliothèques", fontsize=12, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(df_merge_5['Région'], rotation=45, fontsize=10)

for bar in bars_biblio:
    ax1.annotate(
        f'{int(bar.get_height())}',
        xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
        xytext=(0, 3),
        textcoords="offset points",
        ha='center', va='bottom', fontsize=9
    )

# Courbes → Entrées & Population (sur le même périmètre)
ax2 = ax1.twinx()
ax2.plot(
    x, df_merge_5['nombre_d_entrees'] / 1_000_000,
    color='blue', marker='o', linewidth=2, markersize=6, label='Entrées (M)'
)
ax2.plot(
    x, df_merge_5['Total'] / 1_000_000,
    color='red', marker='s', linewidth=2, markersize=5, label='Population (M)'
)
ax2.set_ylabel("Valeurs en millions", fontsize=12, fontweight='bold')

# Légendes & style
ax1.legend(loc='upper left', fontsize=10)
ax2.legend(loc='upper right', fontsize=10)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)

# Affichage
col1, col2, col3 = st.columns([0.5, 9, 0.5])
with col2:
    st.pyplot(fig)

st.caption(
    f"Calcul réalisé sur {nb_lignes_utilisees} lignes avec valeurs renseignées dans 'nombre_d_entrees' "
    f"(sur {len(biblio_file)} lignes initiales). Bibliothèques et population sont restreintes au même périmètre."
)

st.markdown("""
<div class="commentary-box">
L'Auvergne Rhone Alpes ressort avec le plus grand nombre de bibliothèques dans le périmètre étudié, mais ce n'est pas forcément la région la plus peuplée ni la plus fréquentée.
À l'inverse, l'Ile de France, très peuplée et en tête en termes de fréquentation, compte proportionnellement moins de bibliothèques.
On voit aussi que certaines régions comme les DROM combinent faible offre, faible population et faible fréquentation, tandis que d'autres comme l'Occitanie affichent une fréquentation importante avec un nombre de bibliothèques plus modeste.
</div>
""", unsafe_allow_html=True)

st.divider()

# ------------------------------------
# 6. 📅 Ouvertes / Fermées le dimanche : Nombre + Entrées (millions)
# ------------------------------------
st.subheader("6 📅 Ouvertes / Fermées le dimanche : Nombre + Entrées (millions)")

# 1) Périmètre commun : uniquement les lignes avec une valeur d'entrées
df_dimanche_detail = biblio_file[['Région', 'ouverture_le_dimanche', 'nombre_d_entrees']].copy()

# Normalisation du champ "ouverture_le_dimanche"
df_dimanche_detail['ouverture_le_dimanche'] = (
    df_dimanche_detail['ouverture_le_dimanche']
    .astype(str).str.strip().str.lower()
    .replace({'nan': np.nan})
    .replace({'oui': 'Oui', 'true': 'Oui', '1': 'Oui', 'o': 'Oui',
              'non': 'Non', 'false': 'Non', '0': 'Non', 'n': 'Non'})
)

# Conversion stricte + exclusion des lignes sans entrées
df_dimanche_detail['nombre_d_entrees'] = pd.to_numeric(
    df_dimanche_detail['nombre_d_entrees'], errors='coerce'
)
df_dimanche_detail = df_dimanche_detail.dropna(subset=['nombre_d_entrees'])
df_dimanche_detail['nombre_d_entrees'] = df_dimanche_detail['nombre_d_entrees'].astype(int)

# 2) L'ordre des régions et la palette sont définis SUR CE PÉRIMÈTRE
region_order = sorted(df_dimanche_detail['Région'].dropna().unique())
color_map = dict(zip(region_order, pastel_colors[:len(region_order)]))
colors_ordered = [color_map[r] for r in region_order]

def plot_dimanche_vs_entrees(title, df_filtered):
    # Agrégations sur le périmètre filtré
    total_bib = df_filtered.groupby('Région').size().reindex(region_order, fill_value=0)
    total_entrees = df_filtered.groupby('Région')['nombre_d_entrees'].sum().reindex(region_order, fill_value=0)

    # Figure
    fig, ax_left = plt.subplots(figsize=(10, 5))
    plt.subplots_adjust(bottom=0.2, left=0.08, right=0.88)

    # Barres : nombre de bibliothèques (périmètre "avec entrées" uniquement)
    bars = ax_left.bar(region_order, total_bib.values,
                       color=colors_ordered, edgecolor='black', label="Nombre de bibliothèques")
    ax_left.set_xlabel("Régions", fontsize=12, fontweight='bold')
    ax_left.set_ylabel("Nombre de bibliothèques", fontsize=12, fontweight='bold')
    ax_left.tick_params(axis='x', rotation=45, labelsize=10)

    for b in bars:
        ax_left.annotate(f"{int(b.get_height())}",
                         (b.get_x() + b.get_width()/2, b.get_height()),
                         textcoords="offset points", xytext=(0,3),
                         ha="center", va="bottom", fontsize=8)

    # Courbe : entrées en millions (même périmètre)
    ax_right = ax_left.twinx()
    ax_right.plot(region_order, total_entrees / 1_000_000,
                  color='blue', marker='o', linewidth=1.5, label="Entrées (millions)")
    ax_right.set_ylabel("Entrées (millions)", fontsize=12, fontweight='bold')

    ax_left.legend(loc='upper left', fontsize=9)
    ax_right.legend(loc='upper right', fontsize=9)

    ax_left.spines['top'].set_visible(False)
    ax_right.spines['top'].set_visible(False)

    st.subheader(title)
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        st.pyplot(fig)

# 3) Graphique A : OUVERTES le dimanche (périmètre avec entrées)
df_open = df_dimanche_detail[df_dimanche_detail['ouverture_le_dimanche'] == 'Oui']
plot_dimanche_vs_entrees("👍 6.1 Bibliothèques ouvertes le dimanche : Nombre + Entrées", df_open)

st.markdown("""
<div class="commentary-box">
L'Ile de France, la Bretagne et l'Auvergne Rhone Alpes comptent le plus de bibliothèques ouvertes le dimanche, mais c'est l'Ile de France qui domine largement en nombre d'entrées, avec plus de 5 millions.
Certaines régions comme les Pays de la Loire affichent une forte fréquentation malgré peu de bibliothèques ouvertes, tandis que d'autres, comme la Bourgogne-Franche-Comté ou le Centre-Val de Loire, combinent faible offre et faible fréquentation.
</div>
""", unsafe_allow_html=True)
st.write("")

# 4) Graphique B : FERMÉES le dimanche (périmètre avec entrées)
df_closed = df_dimanche_detail[df_dimanche_detail['ouverture_le_dimanche'] == 'Non']
plot_dimanche_vs_entrees("👎 6.2 Bibliothèques fermées le dimanche : Nombre + Entrées", df_closed)

st.markdown("""
<div class="commentary-box">La majorité des bibliothèques sont fermées le dimanche, notamment en Auvergne Rhone Alpes, Nouvelle-Aquitaine et Occitanie.
Malgré cette fermeture, certaines régions comme l'Ile de France, la Nouvelle-Aquitaine et les Hauts-de-France enregistrent une fréquentation importante, ce qui montre que l'activité reste concentrée sur les autres jours de la semaine.
À l'inverse, les DROM et le Centre-Val de Loire cumulent peu de bibliothèques et une faible fréquentation.
</div>
""", unsafe_allow_html=True)