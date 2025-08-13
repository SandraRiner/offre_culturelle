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

#Mise en forme de la page
st.header('Cinéma 🎦')

#Introduction
st.write('Il y a 4 régions en France qui se démarquent dans l\'offre cinématographique : ')

#Lecture des documents
dffr = pd.read_csv('data/frequentation-dans-les-salles-de-cinema.csv', sep=';')
df1 = pd.read_csv('data/cinema_clean.csv', sep=';')
df2 = pd.read_csv('data/code_departement_region.csv', sep=';')
pop= pd.read_csv('data/poulation France par dpt et region_clean.csv', sep=';')
cine_reg = pd.read_csv('data/cinema_par_region.csv', sep=';')
cine = pd.read_csv('data/cinema_par_region.csv',sep=';')
freq_cine= pd.read_csv('data/frequentation cinemas par region.csv', sep=';')
cine_reg = pd.read_csv('data/cinema_par_region.csv', sep=';')


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
    title="🎬 Treemap Interactif - Cinémas par Région 🎬",
    hover_data={'Nom_cinema': ':,'}
)

import plotly.graph_objects as go

fig.update_traces(
    texttemplate="<b>%{label}</b><br>━━━━━━━<br>%{value} cinémas",
    textfont_size=13,
    textfont_color="black",  # Changé en noir pour contraster avec le fond blanc
    textfont_family="Arial Black",
    hovertemplate="<b>%{label}</b><br>" +
                  "Nombre de cinémas: %{value}<br>" +
                  "Pourcentage: %{percentParent}<br>" +
                  "<extra></extra>",
    marker_colors=None
)

# Définir les couleurs personnalisées pour le dégradé
custom_colors = ['#0B1426', '#1E3A8A', '#3B82F6', '#6366F1', '#8B5CF6', 
                '#A855F7', '#C084FC', '#E879F9', '#EC4899', '#F012BE', 
                '#FF1493', '#FF69B4', '#FFB6C1']

# Appliquer les couleurs
fig.update_traces(
    marker_colorscale=[[i/(len(custom_colors)-1), color] for i, color in enumerate(custom_colors)],
    marker_cmid=df['Nom_cinema'].mean()
)

fig.update_layout(
    title="🎬 Treemap Interactif - Cinémas par Région 🎬",
    title_font_size=15,
    title_x=0,                 # 0 = aligné à gauche, 0.5 = centré, 1 = aligné à droite
    title_font_color="black",
    title_font_family="Arial Black",
    margin=dict(t=80, l=25, r=25, b=25),
    font_size=14,
    font_color="black",        # Force toute la police en noir
    plot_bgcolor="white",      # Fond blanc
    paper_bgcolor="white",     # Fond blanc
    width=None,                # Permet l'adaptation automatique
    height=600,                # Hauteur fixe raisonnable pour Streamlit
    autosize=True,             # Active le redimensionnement automatique
    # Forcer le fond blanc même avec les thèmes sombres
    template="plotly_white",   # Template blanc par défaut
    annotations=[
        dict(
            text=f"Total: {df['Nom_cinema'].sum()} cinémas | Moyenne: {df['Nom_cinema'].mean():.0f} par région",
            showarrow=False,
            x=0.5, y=0.02,
            xref="paper", yref="paper",
            xanchor="center", yanchor="bottom",
            font=dict(size=12, color="gray", style="italic")  # Changé en gris foncé pour la lisibilité
        )
    ]
)

#afficher le graphique numero 1
fig.show()
st.plotly_chart(fig)

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
        name="Fréquentation (millions)",
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
    title_text="Fréquentation (millions d'entrées)",
    title_font=dict(color="#FF0066"),  # Couleur du titre
    tickfont=dict(color="#FF0066"),    # Couleur des valeurs
    secondary_y=True
)

# Configuration générale
fig.update_layout(
    title="Cinémas et Fréquentation par Région - 2023",
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


#Graphique numéro 3
#Introduction du graphe
st.write('La fréquentation des salles de cinéma a connu une diminution drastique en 2020 en raison de la pandémie de COVID-19.')

# Remplacer les virgules par des points et convertir en float
dffr["Entrées (millions)"] = dffr["Entrées (millions)"].str.replace(",", ".").astype(float)
dffr["Recette moyenne par entrée (€)"] = dffr["Recette moyenne par entrée (€)"].str.replace(",", ".").astype(float)

# Filtrer et trier les 10 dernières années
df_filtered = dffr[dffr["Année"] >= 2015].sort_values("Année")

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
    title="Fréquentation vs Prix moyen du billet (2015–2024)",
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

#Explication du graph
st.write('Afin de mieux comprendre l\'évolution de la fréquentation nous avons ajouté le prix moyen du ticket de cinéma par année.')
st.write('Nous constatons que l\'augmentation du prix du ticket n\'induit pas une baisse de la fréquentation.')

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
fig.update_yaxes(title_text="Fréquentation", secondary_y=False)
fig.update_yaxes(title_text="Prix (€)", secondary_y=True)

# Mettre à jour le layout
fig.update_layout(
    title={
        'text': 'Fréquentation par Région et Prix Moyen (2014-2024)',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 18}
    },
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