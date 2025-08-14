import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import seaborn as sns
import plotly.express as px

st.header('Musées')

st.write('test')


df_mus= pd.read_csv('source/data/liste-officielle-musees_clean.csv', sep =';')
df_mus=df_mus[['Département', 'Région administrative']]
df_mus = df_mus.groupby('Région administrative').size().reset_index(name='Nombre de musées')

df_pop = pd.read_csv('source/data/Population France par dpt 2024.csv', sep =';')
# Remove spaces and convert columns to integers
for col in ['Total Homme', 'Total Femme', 'Total']:
    df_pop[col] = df_pop[col].str.replace(' ', '').astype(int)

df_reg = pd.read_csv('source/data/departements-regions-france.csv', sep =',')

df_pop_clean = pd.merge(df_pop, df_reg, left_on ='Départements', right_on = 'nom_departement')
                       
df_pop_clean = df_pop_clean[['Code département','Départements','Total Homme', 'Total Femme', 'Total','code_region', 'nom_region']]

df_pop_reg_clean = df_pop_clean[['Total Homme', 'Total Femme', 'Total','code_region', 'nom_region']]

df_pop_reg_clean = df_pop_reg_clean.groupby('nom_region').sum().reset_index()

df_merge = pd.merge(df_pop_reg_clean, df_mus, left_on ='nom_region', right_on = 'Région administrative')
                       
df_merge = df_merge[['nom_region','Total Homme', 'Total Femme', 'Total','code_region', 'Nombre de musées']]

df_merge = df_merge.sort_values(by='Total', ascending = False)

df = df_merge
# Position des barres
x = np.arange(len(df_merge))
width = 0.4

# Création de la figure et des axes
fig, ax1 = plt.subplots(figsize=(14, 7))

# Axe secondaire
ax2 = ax1.twinx()

# Barres population (axe gauche)
bars1 = ax1.bar(x - width/2, df['Total'], width, label='Population', color="#312E60")

# Barres musées (axe droit)
bars2 = ax2.bar(x + width/2, df_merge['Nombre de musées'], width, label='Nombre de musées', color="#A01E90")

# Configuration des axes
ax1.set_ylabel("Population", color="#312E60")
ax2.set_ylabel("Nombre de musées", color="#A01E90")
ax1.set_xticks(x)
ax1.set_xticklabels(df_merge['nom_region'], rotation=45, ha='right')
ax1.set_title("Population vs Nombre de Musées par Région (avec double axe Y)")

st.pyplot(fig)