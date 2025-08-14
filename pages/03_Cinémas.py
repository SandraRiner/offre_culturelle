#import des différentes bibliothèques nécessaires
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.subplots import make_subplots

# #Mise en forme de la page
# st.header('Cinémas 🎦')

# ------------------------------------
# Configuration de la page
# ------------------------------------
st.set_page_config(
    page_title="Cinémas",
    page_icon="🎦",
    layout="wide"
)

# ------------------------------------
# Titre principal
# ------------------------------------
st.markdown(
    """
    <h1 style="text-align:center; margin-bottom: 0.3rem;">Cinémas de France 🎦</h1>
    <p style="text-align:center; font-size:1.1rem; color:#555;">
        Analyse et datavisualisation
    </p>
    """,
    unsafe_allow_html=True
)


#Lecture des documents
dffr = pd.read_csv('data_prod/frequentation-dans-les-salles-de-cinema.csv', sep=';')
df1 = pd.read_csv('data_prod/cinema_clean.csv', sep=';')
df2 = pd.read_csv('data_prod/code_departement_region.csv', sep=';')
pop= pd.read_csv('data_prod/poulation France par dpt et region_clean.csv', sep=';')
cine_reg = pd.read_csv('data_prod/cinema_par_region.csv', sep=';')
cine = pd.read_csv('data_prod/cinema_par_region.csv',sep=';')
freq_cine= pd.read_csv('data_prod/frequentation cinemas par region.csv', sep=';')


tot_cine = pd.merge(cine_reg, freq_cine, left_on ='region_name', right_on='region', how='left')
total_cine_count = len(df1)  # nombre total de lignes (entier)
nb_regions = tot_cine['region'].nunique()  # nombre de régions uniques (utilisez tot_cine, pas total_cine)
moyenne_cine = total_cine_count / nb_regions  # moyenne par région

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
    st.metric(label="🎦 Total Cinémas", value=f"{total_cine_count:,}".replace(",", " "))

with col2:
    st.metric(label="🌍 Nombre de Régions", value=f"{nb_regions}")

with col3:
    st.metric(label="➗ Moyenne par Région", value=f"{moyenne_cine}")

st.divider()

# ------------------------------------
# Palette couleur globale
# ------------------------------------
pastel_colors = [
    
    "#312E60","#4D2A6C","#692678","#852284","#A01E90","#BC1A9C",
    "#D816A8","#F412B4","#FF1DA8","#FF339C","#FF4A90","#FF6084",
    "#FF7678","#FF8D6C","#FF0066"
]


#graphique numero 1
# Créer le DataFrame
data = cine

df = pd.DataFrame(data)
df = df.sort_values('Nom_cinema', ascending=False)
df['region_name'] = df['region_name'].str.title()
# Créer le treemap interactif avec style personnalisé
fig = px.treemap(
    df,
    path=['region_name'],
    values='Nom_cinema',
    # title="🎬 Treemap Interactif - Cinémas par Région 🎬",
    hover_data={'Nom_cinema': ':,'}
)

import plotly.graph_objects as go
st.subheader("1. Treemap Interactif - Cinémas par Région")

fig.update_traces(
    texttemplate="<b>%{label}</b><br>━━━━━━━<br>%{value} cinémas",
    textfont_size=13,
    textfont_color="white",  # Changé en blanc pour contraster avec les couleurs
    textfont_family="Arial Black",
    hovertemplate="<b>%{label}</b><br>" +
                  "Nombre de cinémas: %{value}<br>" +
                  "Pourcentage: %{percentParent}<br>" +
                  "<extra></extra>",
    marker_colors=None
)

# Définir les couleurs personnalisées pour le dégradé
custom_colors = ["#312E60","#4D2A6C","#692678","#FF0066"]

# Appliquer les couleurs
fig.update_traces(
    marker_colorscale=[[i/(len(custom_colors)-1), color] for i, color in enumerate(custom_colors)],
    marker_cmid=df['Nom_cinema'].mean()
)

#afficher le graphique numero 1
fig.show()
st.plotly_chart(fig)

# Zone de texte commentaire graph numero 1
st.markdown("""
<div class="commentary-box">
Chaque rectangle représente une région et sa taille reflète le nombre de cinémas. 
On voit que l’Île-de-France concentre une grande partie de l’offre nationale.
</div>
""", unsafe_allow_html=True)

st.divider()

#Graphique numéro 2
#Jointure graph
pop_merge = pd.merge(cine_reg, freq_cine, left_on ='region_name', right_on='region', how='left')


pop_merge= pop_merge[['region', 'Nom_cinema', '2023']]

pop_merge = pop_merge.groupby('region', as_index=False).agg({
    '2023': 'sum',
    'Nom_cinema': 'first',  # ou 'count', 'max', etc.
    'region': 'first'
})

pop_merge = pop_merge.iloc[:, :3]
pop_merge.columns = ['frequentation_2023', 'nombre_cinemas', 'region']
pop_merge = pop_merge[['region', 'nombre_cinemas', 'frequentation_2023']]

pop_merge = pop_merge.sort_values(by='nombre_cinemas', ascending=False)

pop_merge['region'] = pop_merge['region'].str.title()

st.subheader("2. Cinémas et Fréquentation par Région - 2023")

# Création du graphique avec deux axes Y
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Ajout des barres pour le nombre de cinémas (axe GAUCHE)
fig.add_trace(
    go.Bar(
        x=pop_merge['region'],
        y=pop_merge['nombre_cinemas'],  # ou le nom de votre colonne cinémas
        name="Nombre de cinémas",
        marker_color='#312E60',  # Bleu
        offsetgroup=1,  # Important pour séparer les barres
        width=0.4       # Largeur des barres
    ),
    secondary_y=False  # Axe GAUCHE
)

# Ajout des barres pour la fréquentation (axe DROITE)
fig.add_trace(
    go.Bar(
        x=pop_merge['region'],
        y=pop_merge['frequentation_2023'],  # ou le nom de votre colonne fréquentation
        name="Fréquentation (milliers)",
        marker_color='#FF0066',  # Vert
        offsetgroup=2,  # Important pour séparer les barres
        width=0.4       # Largeur des barres
    ),
    secondary_y=True   # Axe DROITE
)

# Configuration de l'axe X
fig.update_xaxes(
    tickangle=-45
)

# Configuration de l'axe Y GAUCHE (cinémas)
fig.update_yaxes(
    title_text="Nombre de cinémas",
    title_font=dict(color="#312E60"),  # Couleur du titre
    tickfont=dict(color="#312E60"),    # Couleur des valeurs
    secondary_y=False
)

# Configuration de l'axe Y DROITE (fréquentation)
fig.update_yaxes(
    title_text="Fréquentation (milliers d'entrées)",
    title_font=dict(color="#FF0066"),  # Couleur du titre
    tickfont=dict(color="#FF0066"),    # Couleur des valeurs
    secondary_y=True
)

# Configuration générale
fig.update_layout(
    # title="Cinémas et Fréquentation par Région - 2023",
    height=600,
    barmode='group',  # Barres groupées
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    margin=dict(b=150, l=80, r=80)  # Marges pour les axes
)


st.plotly_chart(fig, use_container_width=True)

# Zone de texte commentaire graph numero 2
st.markdown("""
<div class="commentary-box">
Comparaison directe entre le nombre de salles et leur fréquentation. 
Certaines régions ont peu de cinémas mais attirent un public proportionnellement élevé.
</div>
""", unsafe_allow_html=True)

st.divider()

#Graphique numéro 3
#Introduction du graphe

# Remplacer les virgules par des points et convertir en float
dffr["Entrées (millions)"] = dffr["Entrées (millions)"].str.replace(",", ".").astype(float)
dffr["Recette moyenne par entrée (€)"] = dffr["Recette moyenne par entrée (€)"].str.replace(",", ".").astype(float)

# Filtrer et trier les 10 dernières années
df_filtered = dffr[dffr["Année"] >= 2015].sort_values("Année")

st.subheader("3. Fréquentation vs Prix moyen du billet (2015–2024)")
# Créer la figure
fig = go.Figure()

# Barres : Entrées (millions)
fig.add_trace(go.Bar(
    x=df_filtered["Année"],
    y=df_filtered["Entrées (millions)"],
    name="Entrées (millions)",
    yaxis="y1",
    marker_color="#312E60"
))

# Courbe : Prix moyen (€)
fig.add_trace(go.Scatter(
    x=df_filtered["Année"],
    y=df_filtered["Recette moyenne par entrée (€)"],
    name="Prix moyen (€)",
    yaxis="y2",
    mode="lines+markers",
    line=dict(color="#FF0066", width=3)
))

# Mise en page
fig.update_layout(
    # title="Fréquentation vs Prix moyen du billet (2015–2024)",
    xaxis=dict(title="Année", type="category"),  # affichage lisible
    yaxis=dict(
        title=dict(text="Entrées (millions)", font=dict(color="#312E60")),
        tickfont=dict(color="#312E60")
    ),
    yaxis2=dict(
        title=dict(text="Prix moyen (€)", font=dict(color="#FF0066")),
        tickfont=dict(color="#FF0066"),
        overlaying="y",
        side="right"
    ),
    legend=dict(x=0.01, y=0.99),
    bargap=0.2
)
st.plotly_chart(fig)

# Zone de texte commentaire graph numero 3
st.markdown("""
<div class="commentary-box">
L’augmentation du prix du billet ne freine pas la fréquentation, sauf en 2020 à cause de la pandémie. 
Le public est revenu dès la réouverture des salles.
</div>
""", unsafe_allow_html=True)

st.divider()

#Graphique numero 4
# Charger les données depuis le fichier CSV
df = pd.read_csv('data/frequentation par région et prix moyen.csv', sep=';')

# Renommer la première colonne si nécessaire
df.columns = ['Annee', 'Auvergne-Rhone-Alpes', 'Corse', 'Hauts-de-France', 'Ile-de-France', 'PRIX']

# Convertir les colonnes en numérique (gérer les virgules comme séparateurs décimaux)
numeric_columns = ['Auvergne-Rhone-Alpes', 'Corse', 'Hauts-de-France', 'Ile-de-France', 'PRIX']
for col in numeric_columns:
    df[col] = df[col].astype(str).str.replace(',', '.').astype(float)

# S'assurer que la colonne Année est aussi numérique
df['Annee'] = df['Annee'].astype(int)

st.subheader("4. Fréquentation par Région et Prix Moyen (2014-2024)")

# Créer un subplot avec deux axes y
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Couleurs pour les régions
colors = ['#312E60', '#EC4899', '#8B5CF6', '#E879F9']
regions = ['Ile-de-France', 'Auvergne-Rhone-Alpes', 'Hauts-de-France', 'Corse']

# Ajouter les barres empilées pour chaque région
for i, region in enumerate(regions):
    fig.add_trace(
        go.Bar(
            name=region,
            x=df['Annee'],
            y=df[region],
            marker_color=colors[i],
            opacity=1
        ),
        secondary_y=False,
    )

# Ajouter la ligne de prix sur l'axe secondaire
fig.add_trace(
    go.Scatter(
        name='Prix',
        x=df['Annee'],
        y=df['PRIX'],
        mode='lines+markers',
        line=dict(color='#FF1493', width=3),
        marker=dict(size=8)
    ),
    secondary_y=True,
)

# Mettre à jour les axes
fig.update_xaxes(title_text="Année")
fig.update_yaxes(title_text="Fréquentation en millions", secondary_y=False)
fig.update_yaxes(title_text="Prix (€)", secondary_y=True)

# Mettre à jour le layout
fig.update_layout(
    # title={
    #     'text': 'Fréquentation par Région et Prix Moyen (2014-2024)',
    #     'x': 0.5,
    #     'xanchor': 'center',
    #     'font': {'size': 18}
    # },
    barmode='stack',
    hovermode='x unified',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    height=600,
    showlegend=True
)

# Afficher le graphique dans Streamlit
st.plotly_chart(fig, use_container_width=True)

# Zone de texte commentaire graph numero 4
st.markdown("""
<div class="commentary-box">
Vue détaillée sur 4 régions : malgré une hausse continue du prix moyen de la place, cela n'a pas changé les proportions de fréquentation par région. Il aurait été intéressant de pouvoir voir le lien entre ces données et le revenu moyen par région.
</div>
""", unsafe_allow_html=True)