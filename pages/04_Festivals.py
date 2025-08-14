import streamlit as st
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.subplots import make_subplots

# st.header('Festivals 💃')
# st.write()

# ------------------------------------
# Configuration de la page
# ------------------------------------
st.set_page_config(
    page_title="Festivals",
    page_icon="💃",
    layout="wide"
)

# ------------------------------------
# Titre principal
# ------------------------------------
st.markdown(
    """
    <h1 style="text-align:center; margin-bottom: 0.3rem;">Festivals de France 💃</h1>
    <p style="text-align:center; font-size:1.1rem; color:#555;">
        Analyse et datavisualisation
    </p>
    """,
    unsafe_allow_html=True
)



df = pd.read_csv('data_prod/festivals_nettoye.csv', sep=';')
df=df[['Région principale de déroulement']]
domtom = [
    "Guadeloupe",
    "Guyane",
    "La Réunion",
    "Martinique",
    "Mayotte",
    "Nouvelle-Calédonie",
    "Polynésie française",
    "Saint-Barthélemy",
    "Saint-Pierre-et-Miquelon"
]
df['Région principale de déroulement'] = df['Région principale de déroulement'].replace(domtom, "Territoires et départements d'outre-mer")
total_fest = len(df)  # nombre total de lignes
nb_regions = df['Région principale de déroulement'].nunique()  # nombre de régions uniques
moyenne_fest = total_fest / nb_regions  # moyenne par région
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
    st.metric(label=":dancer: Total Festivals", value=f"{total_fest:,}".replace(",", " "))
with col2:
    st.metric(label=":earth_africa: Nombre de Régions", value=f"{nb_regions}")
with col3:
    st.metric(label=":heavy_division_sign: Moyenne par Région", value=f"{moyenne_fest:.2f}")
st.divider()
# ------------------------------------
# Palette couleur globale
# ------------------------------------
pastel_colors = [
    
    "#312E60","#4D2A6C","#692678","#852284","#A01E90","#BC1A9C",
    "#D816A8","#F412B4","#FF1DA8","#FF339C","#FF4A90","#FF6084",
    "#FF7678","#FF8D6C","#FF0066"
]



df_festival = pd.read_csv('data_prod/festivals_nettoye.csv', sep =';')

domtom = [
    "Guadeloupe",
    "Guyane",
    "La Réunion",
    "Martinique",
    "Mayotte",
    "Nouvelle-Calédonie",
    "Polynésie française",
    "Saint-Barthélemy",
    "Saint-Pierre-et-Miquelon"
]

df_festival['Région principale de déroulement'] = df_festival['Région principale de déroulement'].replace(domtom, "Territoires et départements d'outre-mer")


# 1er graphe

df_plot = df_festival['Discipline dominante'].value_counts().reset_index()
df_plot.columns = ['Discipline dominante', 'Nombre de festivals']
st.title("Répartition des types de festivals")

# Création du camembert
fig = px.pie(
    df_plot,
    names='Discipline dominante',
    values='Nombre de festivals',
    # title="Répartition des types de festivals",
    color_discrete_sequence=["#312E60", "#852284", "#D816A8", "#FF339C"]
)
fig.show()
st.plotly_chart(fig)



df_festival_reg = df_festival.groupby('Région principale de déroulement').size().reset_index(name='Nombre de festivals')


#2eme graphe

st.title("Carte interactive des festivals en France")

# Séparer les coordonnées
df_festival[['lat', 'lon']] = df_festival['Géocodage xy'].str.split(',', expand=True).astype(float)
df_festival['lat'] = pd.to_numeric(df_festival['lat'], errors='coerce')
df_festival['lon'] = pd.to_numeric(df_festival['lon'], errors='coerce')

# Suppression des lignes sans coordonnées valides
df_festival = df_festival.dropna(subset=['lat', 'lon'])

# Liste des régions et choix utilisateur
regions = df_festival['Région principale de déroulement'].dropna().unique()
choix_region = st.selectbox("Choisir une région", ["Toutes"] + sorted(regions.tolist()))

# Filtre sur les régions

df_filtré = df_festival.copy()
if choix_region != "Toutes":
    df_filtré = df_filtré[df_filtré["Région principale de déroulement"] == choix_region]

# Carte interactive
fig = px.scatter_map(
    df_filtré,
    lat='lat',
    lon='lon',
    hover_name='Nom du festival',
    hover_data=['Région principale de déroulement', 'Discipline dominante'],
    color='Discipline dominante',
    color_discrete_sequence=["#312E60", "#852284", "#D816A8", '#3B82F6', '#6366F1', '#8B5CF6'],
    zoom=4,
    height=700
)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig, key="unique_key_1")


st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# 3eme graphe

# st.subheader(
#     "🎉 🍻 🎶 La vitalité culturelle des régions françaises, à la loupe")

st.title("🎉 🍻 🎶 La vitalité culturelle des régions françaises, à la loupe")

st.write("""Ce graphique montre le nombre de festivals pour un million d’habitants dans chaque région de France. Cela permet de savoir où l’on trouve le plus de festivals en proportion de la population.""")

df_pop = pd.read_csv('data_prod/Population France par dpt 2024.csv', sep =';')
# Remove spaces and convert columns to integers
for col in ['Total Homme', 'Total Femme', 'Total']:
    df_pop[col] = df_pop[col].str.replace(' ', '').astype(int)

df_reg = pd.read_csv('data_prod/departements-regions-france.csv', sep =',')

df_pop_clean = pd.merge(df_pop, df_reg, left_on ='Départements', right_on = 'nom_departement')
df_pop_clean = df_pop_clean[['Code département','Départements','Total Homme', 'Total Femme', 'Total','code_region', 'nom_region']]
df_pop_reg_clean = df_pop_clean[['Total Homme', 'Total Femme', 'Total','code_region', 'nom_region']]
df_pop_reg_clean = df_pop_reg_clean.groupby('nom_region').sum().reset_index()

df = pd.merge(df_festival_reg, df_pop_reg_clean, left_on = 'Région principale de déroulement' , right_on='nom_region')
df = df[['nom_region','Nombre de festivals', 'Total']]

#Calcul du ratio festival par million d'habitants

df['festivals_par_million'] = df['Nombre de festivals'] / (df['Total'] / 1_000_000)

#Trie décroissant de mon ratio
df_sorted = df.sort_values(by='festivals_par_million', ascending=False)

import plotly.express as px

# Trier les données pour affichage en barres horizontales
df_sorted = df.sort_values(by='festivals_par_million', ascending=False)

# Dégradé de couleurs personnalisé (mêmes tons que Matplotlib)
colors = [
    "#0F0E23", "#1C1A3C", "#2B2760", "#312E60", "#443F77", "#5A4E8A", "#70549D",
    "#8C66AE", "#A878BE", "#C28ACD", "#D89BD9", "#E7ADD8", "#F3C0E1", "#FCD3EC"
]
fig = px.bar(
    df_sorted,
    x='festivals_par_million',
    y='nom_region',
    orientation='h',
    color='nom_region',
    color_discrete_sequence=colors,
    labels={'festivals_par_million': 'Festivals par million d\'habitants', 'nom_region': 'Région'},
    title='🎉 Ratio festivals / population par région'
)

fig.update_layout(
    height=700,
    xaxis_title='Festivals par million d\'habitants',
    yaxis_title='',
    showlegend=False,
    margin=dict(l=100, r=40, t=80, b=40)
)

st.plotly_chart(fig, use_container_width=True)


# 4eme graphe

# 1. Remplacer les valeurs manquantes par une valeur standard
df_festival['Période principale de déroulement du festival'] = df_festival['Période principale de déroulement du festival'].fillna('Inconnue')

# 2. Uniformiser casse et espaces
df_festival['Période principale de déroulement du festival'] = df_festival['Période principale de déroulement du festival'].str.lower().str.strip()

# 3. Corriger fautes de frappe
df_festival['Période principale de déroulement du festival'] = df_festival['Période principale de déroulement du festival'].replace({'ocotbre': 'octobre', 'variable selon les années' : 'variable','période variable selon les territoires' : 'variable'})
df_festival['Période principale de déroulement du festival'].unique()

# Supposons que ton dataframe s'appelle df et la colonne s'appelle 'saisonnalité'

def saison_group(val):
    val = str(val).lower().strip()
    
    if 'avant-saison' in val:
        return 'printemps'
    elif 'après-saison' in val:
        return 'automne'
    elif val.startswith('saison') or 'juin' in val or 'juillet' in val or 'août' in val:
        return 'été'
    elif 'janvier' in val or 'février' in val or 'mars' in val or 'avril' in val or 'mai' in val:
        return 'printemps'
    elif 'septembre' in val or 'octobre' in val or 'novembre' in val:
        return 'automne'
    elif 'décembre' in val:
        return 'hiver'
    else:
        return 'autre'

df_festival['saison_group'] = df_festival['Période principale de déroulement du festival'].apply(saison_group)
#df_festival['saison_group'].unique()

#Groupement par region et saison

df_grouped = df_festival.groupby(['Région principale de déroulement', 'saison_group']).size().reset_index(name='Nombre de festivals')

# Supprimer la saison "autre"
df_grouped = df_grouped[df_grouped['saison_group'] != 'autre']

# Compter le nombre de festivals par saison
saison_counts = df_festival['saison_group'].value_counts().reset_index()
saison_counts.columns = ['Saison', 'Nombre de festivals']

# Titre
# st.subheader("📊 Répartition des festivals par saison")
st.title("📊 Répartition des festivals par saison")

fig = px.bar(
    df_grouped,
    x='Région principale de déroulement',
    y='Nombre de festivals',
    color='saison_group',
    color_discrete_sequence=["#312E60", "#852284", "#D816A8", '#3B82F6'],
    title='Répartition des festivals par saison et par région',
    barmode='group',

)

fig.update_layout(xaxis_tickangle=-45)
fig.show()
# Affichage
st.plotly_chart(fig)

#a commenter