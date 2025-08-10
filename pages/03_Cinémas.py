#import des différentes bibliothèques nécessaires
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

#Mise en forme de la page
st.header('Cinéma 🎦')

#Introduction
st.write('Il y a 4 régions en France qui se démarquent dans l\'offre cinématographique : ')

#Lecture des documents
df = pd.read_csv('data/frequentation-dans-les-salles-de-cinema.csv', sep=';')
df1 = pd.read_csv('data/cinema_clean.csv', sep=';')
df2 = pd.read_csv('data/code_departement_region.csv', sep=';')

#Graphique numéro 1
#Jointure pour avoir les cinémas par région
df_merge = pd.merge(df1, df2, left_on ='code_departement', right_on='num_dep')
#Conserver les colonnes utiles
df3 = df_merge[['Nom_cinema', 'num_dep', 'dep_name', 'region_name']]

# Compter le nombre de cinémas par région
cinemas_par_region = df3.groupby('region_name')['Nom_cinema'].count().sort_values()

# Afficher le graphique
cinemas_par_region.plot(kind='barh', figsize=(10,6))
plt.title("Nombre de cinémas par région")
plt.xlabel("Nombre de cinémas")
plt.ylabel("Région")
plt.show()
st.pyplot(plt)

#Graphique numéro 2

#Introduction du graphe
st.write('La fréquentation des salles de cinéma a connu une diminution drastique en 2020 en raison de la pandémie de COVID-19.')

# Remplacer les virgules par des points et convertir en float
df["Entrées (millions)"] = df["Entrées (millions)"].str.replace(",", ".").astype(float)
df["Recette moyenne par entrée (€)"] = df["Recette moyenne par entrée (€)"].str.replace(",", ".").astype(float)

# Filtrer et trier les 10 dernières années
df_filtered = df[df["Année"] >= 2015].sort_values("Année")

# Créer la figure
fig = go.Figure()

# Barres : Entrées (millions)
fig.add_trace(go.Bar(
    x=df_filtered["Année"],
    y=df_filtered["Entrées (millions)"],
    name="Entrées (millions)",
    yaxis="y1",
    marker_color="royalblue"
))

# Courbe : Prix moyen (€)
fig.add_trace(go.Scatter(
    x=df_filtered["Année"],
    y=df_filtered["Recette moyenne par entrée (€)"],
    name="Prix moyen (€)",
    yaxis="y2",
    mode="lines+markers",
    line=dict(color="orange", width=3)
))

# Mise en page
fig.update_layout(
    title="Fréquentation vs Prix moyen du billet (2015–2024)",
    xaxis=dict(title="Année", type="category"),  # affichage lisible
    yaxis=dict(
        title=dict(text="Entrées (millions)", font=dict(color="royalblue")),
        tickfont=dict(color="royalblue")
    ),
    yaxis2=dict(
        title=dict(text="Prix moyen (€)", font=dict(color="orange")),
        tickfont=dict(color="orange"),
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