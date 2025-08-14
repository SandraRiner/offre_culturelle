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

# st.header('Répartition de l\'offre culturelle en France')
# st.write()

# ------------------------------------
# Configuration de la page
# ------------------------------------
st.set_page_config(
    page_title="Répartition de l\'offre culturelle en France",
    page_icon=":fr:",
    layout="wide"
)

# ------------------------------------
# Titre principal
# ------------------------------------
st.markdown(
    """
    <h1 style="text-align:center; margin-bottom: 0.3rem;">Répartition de l\'offre culturelle en France </h1>
    """,
    unsafe_allow_html=True
)
df_pop = pd.read_csv('source/data/Population France par dpt 2024.csv', sep =';')
# Remove spaces and convert columns to integers
for col in ['Total Homme', 'Total Femme', 'Total']:
    df_pop[col] = df_pop[col].str.replace(' ', '').astype(int)

df_reg = pd.read_csv('source/data/departements-regions-france.csv', sep =',')

df_pop_clean = pd.merge(df_pop, df_reg, left_on ='Départements', right_on = 'nom_departement')
df_pop_clean = df_pop_clean[['Code département','Départements','Total Homme', 'Total Femme', 'Total','code_region', 'nom_region']]

df_pop_reg_clean = df_pop_clean[['Total Homme', 'Total Femme', 'Total','code_region', 'nom_region']]
df_pop_reg_clean = df_pop_reg_clean.groupby('nom_region').sum().reset_index()

df_mus= pd.read_csv('source/data/liste-officielle-musees_clean.csv', sep =';')
df_mus=df_mus[['Département', 'Région administrative']]
df_mus = df_mus.groupby('Région administrative').size().reset_index(name='Nombre de musées')


df_merge = pd.merge(df_pop_reg_clean, df_mus, left_on ='nom_region', right_on = 'Région administrative')
                       
df_merge = df_merge[['nom_region','Total Homme', 'Total Femme', 'Total','code_region', 'Nombre de musées']]

df_merge = df_merge.sort_values(by='Total', ascending = False)

df_cine = pd.read_csv('source/data/cinema_clean.csv', sep =';')
df_cine = df_cine.groupby('code_departement').size().reset_index(name='Nombre de cinés')
df_cine = df_cine.drop(index= [96])

#jointure nombre de ciné et nom de region et  groupby par region

df_cine_reg = pd.merge(df_cine, df_reg, left_on ='code_departement', right_on = 'code_departement')
df_cine_reg = df_cine_reg[['nom_region', 'Nombre de cinés']]
df_cine_reg = df_cine_reg.groupby('nom_region').sum().reset_index()

# création ligne domtom
new_row = pd.DataFrame([{
    'nom_region': "Territoires et départements d'outre-mer",
    'Nombre de cinés': 0  
}])

# Ajout ligne domtom
df_cine_reg = pd.concat([df_cine_reg, new_row], ignore_index=True)


# Décompte festival par région et remplacement des dom ton par nom de region

df_festival = pd.read_csv('source/data/festivals_nettoye.csv', sep =';')

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

df_festival = df_festival.groupby('Région principale de déroulement').size().reset_index(name='Nombre de festivals')




df_biblio = pd.read_csv('source/data/adresses_des_bibliotheques_publiques_prepared.csv', sep =',')

df_biblio = df_biblio.groupby('Département').size().reset_index(name='Nombre de bibliothèques')

#jointure bibliotheque _ région

df_biblio_reg = pd.merge(df_biblio, df_reg, left_on ='Département', right_on = 'nom_departement')

df_biblio_reg = df_biblio_reg[['Département', 'Nombre de bibliothèques', 'nom_region']]


#changement nom de dpt domtom et groupby region

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

df_biblio_reg['nom_region'] = df_biblio_reg['nom_region'].replace(domtom, "Territoires et départements d'outre-mer")
df_biblio_reg = df_biblio_reg.groupby('nom_region').sum().reset_index()
df_biblio_reg = df_biblio_reg[['nom_region', 'Nombre de bibliothèques']]

df_final = pd.merge(df_merge, df_cine_reg, left_on='nom_region', right_on ='nom_region')
df_final = pd.merge(df_final, df_festival, left_on='nom_region', right_on ='Région principale de déroulement')
df_final = pd.merge(df_final, df_biblio_reg, left_on='nom_region', right_on = 'nom_region')

df_final = df_final[['nom_region','code_region','Total','Nombre de musées', 'Nombre de cinés', 'Nombre de festivals','Nombre de bibliothèques']]
df_final = df_final.sort_values('Total', ascending = False)

st.subheader("1. Répartition des équipements culturels en France par région")
#1er graphe 

df_final1 = df_final[['Nombre de musées','Nombre de cinés','Nombre de festivals','Nombre de bibliothèques']]
df_final1.loc['Total'] = df_final1.sum()

df_final1= df_final1.drop(index=range(0, 14))

df_transposed = df_final1.T

# Réinitialiser l’index pour que les lignes deviennent une colonne
df_plot = df_transposed.reset_index()
df_plot.columns = ['Type équipement', 'Total']

# Création du camembert
fig = px.pie(
    df_plot,
    names='Type équipement',
    values='Total',
    # title="Répartition des équipements culturels en France",
    color_discrete_sequence=["#312E60", "#852284", "#D816A8", "#FF339C"]
)
st.plotly_chart(fig)


st.subheader("2. Répartition des lieux et équipements culturels par région")

st.markdown("""
Ce graphique circulaire illustre la répartition des principaux équipements culturels en France.
Il met en lumière une offre culturelle dominée par les bibliothèques, avec un bon complément par les festivals. Les cinémas et musées sont plus rares mais structurants dans le paysage culturel.

""")

#2eme graphe

df = df_final 

# Coordonnées sur l'axe des x
regions = df['nom_region']

x = np.arange(len(regions))

# Hauteurs des différentes catégories
biblio = df['Nombre de bibliothèques']
cine = df['Nombre de cinés']
musee = df['Nombre de musées']
festivals = df['Nombre de festivals']

# Création du graphique
fig, ax = plt.subplots(figsize=(12, 6))

ax.bar(x, biblio, label = 'Bibliothèques', color = "#1E3A8A" )
ax.bar(x, cine, bottom = biblio, label='Cinémas', color = "#F012BE")
ax.bar(x, musee, bottom = biblio + cine , label='Musées', color ="#4D2A6C" )
ax.bar(x, festivals, bottom = biblio + cine + musee, label='festivals', color = "#E879F9")

# Personnalisation
ax.set_xticks(x)
ax.set_xticklabels(regions, rotation=45, ha='right')
ax.set_ylabel("Nombre d'équipements")
# ax.set_title("Répartition des lieux et équipements culturels par région")
ax.legend()

plt.tight_layout()

st.pyplot(fig)

# A commenter

