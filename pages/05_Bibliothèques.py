# -*- coding: utf-8 -*-
"""
Streamlit — Bibliothèques par région (version simple)
Focus sur les graphiques essentiels
"""

import os
import pandas as pd
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import numpy as np

# Configuration de base
st.set_page_config(page_title="Bibliothèques par Région", layout="wide")
st.title("📚 Bibliothèques par Région")

# Chemins des fichiers
BIBLIOTHEQUES_PATH = "/home/karim/code/offre_culturelle/data/adresses_des_bibliotheques_publiques_prepared.csv"
POPULATION_PATH = "/home/karim/code/offre_culturelle/data/population-france-par-dept.csv"

@st.cache_data
def load_data():
    """Charge les données"""
    # Bibliothèques
    try:
        df_bib = pd.read_csv(BIBLIOTHEQUES_PATH)
        df_bib = df_bib.dropna(subset=["Région", "Latitude", "Longitude"])
        df_bib["Région"] = df_bib["Région"].str.strip()
    except:
        st.error("Erreur lors du chargement des bibliothèques")
        st.stop()
    
    # Population
    df_pop = None
    try:
        if os.path.exists(POPULATION_PATH):
            df_pop = pd.read_csv(POPULATION_PATH, sep=";")
            # Détection automatique des colonnes
            region_cols = [col for col in df_pop.columns if any(x in col.lower() for x in ['region', 'région'])]
            pop_cols = [col for col in df_pop.columns if any(x in col.lower() for x in ['population', 'total', 'hab'])]
            femme_cols = [col for col in df_pop.columns if any(x in col.lower() for x in ['femme', 'female', 'f'])]
            homme_cols = [col for col in df_pop.columns if any(x in col.lower() for x in ['homme', 'male', 'h'])]
            
            if region_cols and pop_cols:
                # Renommage des colonnes
                rename_dict = {region_cols[0]: "Région_pop", pop_cols[0]: "Population"}
                if femme_cols:
                    rename_dict[femme_cols[0]] = "Femmes"
                if homme_cols:
                    rename_dict[homme_cols[0]] = "Hommes"
                
                df_pop = df_pop.rename(columns=rename_dict)
                
                # Nettoyage et agrégation
                df_pop["Population"] = pd.to_numeric(df_pop["Population"], errors="coerce")
                if "Femmes" in df_pop.columns:
                    df_pop["Femmes"] = pd.to_numeric(df_pop["Femmes"], errors="coerce")
                if "Hommes" in df_pop.columns:
                    df_pop["Hommes"] = pd.to_numeric(df_pop["Hommes"], errors="coerce")
                
                agg_dict = {"Population": "sum"}
                if "Femmes" in df_pop.columns:
                    agg_dict["Femmes"] = "sum"
                if "Hommes" in df_pop.columns:
                    agg_dict["Hommes"] = "sum"
                
                df_pop = df_pop.groupby("Région_pop", as_index=False).agg(agg_dict)
    except:
        pass
    
    return df_bib, df_pop

# Chargement des données
df_bib, df_pop = load_data()

# Métriques de base
total_bib = len(df_bib)
nb_regions = df_bib["Région"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total bibliothèques", total_bib)
col2.metric("Régions", nb_regions)
col3.metric("Moyenne/région", total_bib // nb_regions)

st.markdown("---")

# GRAPHIQUE 1: Distribution par région
st.header("Distribution par région")

region_counts = df_bib["Région"].value_counts().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(10, 8))
bars = ax.barh(range(len(region_counts)), region_counts.values)
ax.set_yticks(range(len(region_counts)))
ax.set_yticklabels(region_counts.index)
ax.set_xlabel("Nombre de bibliothèques")
ax.grid(axis='x', alpha=0.3)

# Annotations
for i, v in enumerate(region_counts.values):
    ax.text(v + max(region_counts.values)*0.01, i, str(v), 
            va='center', fontweight='bold')

plt.tight_layout()
st.pyplot(fig)

# Top 5
col1, col2 = st.columns(2)
with col1:
    st.subheader("Top 5 - Plus de bibliothèques")
    for i, (region, count) in enumerate(region_counts.tail(5).sort_values(ascending=False).items(), 1):
        st.write(f"{i}. **{region}** : {count}")

with col2:
    st.subheader("Top 5 - Moins de bibliothèques") 
    for i, (region, count) in enumerate(region_counts.head(5).items(), 1):
        st.write(f"{i}. **{region}** : {count}")

st.markdown("---")

# GRAPHIQUE 2: Bibliothèques vs Population (si données dispo)
if df_pop is not None:
    st.header("Bibliothèques vs Population")
    
    # Jointure simplifiée des données
    df_bib_agg = df_bib.groupby("Région").size().reset_index(name="bibliotheques")
    
    # Normalisation des noms pour jointure
    def normalize_region(name):
        import unicodedata
        name = str(name).lower().strip()
        name = "".join(c for c in unicodedata.normalize("NFKD", name) if not unicodedata.combining(c))
        return name.replace("'", "'").replace("-", " ")
    
    df_bib_agg["region_norm"] = df_bib_agg["Région"].apply(normalize_region)
    df_pop["region_norm"] = df_pop["Région_pop"].apply(normalize_region)
    
    df_merged = df_bib_agg.merge(df_pop, on="region_norm", how="inner")
    
    if not df_merged.empty:
        df_merged = df_merged.sort_values("bibliotheques", ascending=False)
        
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        # Barres
        x_pos = range(len(df_merged))
        ax1.bar(x_pos, df_merged["bibliotheques"], alpha=0.7, label="Bibliothèques")
        ax1.set_ylabel("Nombre de bibliothèques")
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(df_merged["Région"], rotation=45, ha='right')
        ax1.grid(axis='y', alpha=0.3)
        
        # Ligne population
        ax2 = ax1.twinx()
        ax2.plot(x_pos, df_merged["Population"]/1e6, 'ro-', label="Population (M)")
        ax2.set_ylabel("Population (millions)")
        
        # Légendes
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        st.markdown("---")
        
        # GRAPHIQUE 3: Densité culturelle
        st.header("Densité culturelle (bibliothèques pour 100k habitants)")
        df_merged["densite"] = (df_merged["bibliotheques"] / df_merged["Population"] * 100000).round(1)
        df_density = df_merged.sort_values("densite", ascending=False)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(range(len(df_density)), df_density["densite"])
        ax.set_xticks(range(len(df_density)))
        ax.set_xticklabels(df_density["Région"], rotation=45, ha='right')
        ax.set_ylabel("Bibliothèques pour 100k habitants")
        ax.grid(axis='y', alpha=0.3)
        
        # Ligne de moyenne
        moyenne = df_density["densite"].mean()
        ax.axhline(y=moyenne, color='red', linestyle='--', alpha=0.7, 
                   label=f'Moyenne: {moyenne:.1f}')
        ax.legend()
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Top densité
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Forte densité culturelle:**")
            for _, row in df_density.head(3).iterrows():
                st.write(f"• {row['Région']}: {row['densite']:.1f} bib./100k hab.")
        
        with col2:
            st.write("**Faible densité culturelle:**")
            for _, row in df_density.tail(3).iterrows():
                st.write(f"• {row['Région']}: {row['densite']:.1f} bib./100k hab.")
        
        st.markdown("---")
        
        # GRAPHIQUE 4: Répartition Hommes/Femmes (si disponible)
        if "Femmes" in df_merged.columns and "Hommes" in df_merged.columns:
            st.header("Répartition démographique par sexe")
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Barres empilées
            x_pos = range(len(df_merged))
            ax.bar(x_pos, df_merged["Femmes"]/1000, label="Femmes", alpha=0.8)
            ax.bar(x_pos, df_merged["Hommes"]/1000, bottom=df_merged["Femmes"]/1000, 
                   label="Hommes", alpha=0.8)
            
            ax.set_xticks(x_pos)
            ax.set_xticklabels(df_merged["Région"], rotation=45, ha='right')
            ax.set_ylabel("Population (milliers)")
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # Stats H/F
            total_pop = df_merged["Population"].sum()
            pct_femmes = (df_merged["Femmes"].sum() / total_pop * 100)
            pct_hommes = (df_merged["Hommes"].sum() / total_pop * 100)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("% Femmes", f"{pct_femmes:.1f}%")
            col2.metric("% Hommes", f"{pct_hommes:.1f}%")
            col3.metric("Population totale", f"{total_pop/1e6:.1f}M")

st.markdown("---")

# CARTE INTERACTIVE
st.header("Localisation des bibliothèques")

regions_list = sorted(df_bib["Région"].unique())
region_selected = st.selectbox("Choisir une région:", regions_list)

df_region = df_bib[df_bib["Région"] == region_selected]

if not df_region.empty:
    st.write(f"**{len(df_region)} bibliothèques** dans {region_selected}")
    
    # Calcul centre carte
    lat_center = df_region["Latitude"].mean()
    lon_center = df_region["Longitude"].mean()
    
    # Création carte
    m = folium.Map(location=[lat_center, lon_center], zoom_start=8)
    
    # Cluster
    marker_cluster = MarkerCluster().add_to(m)
    
    # Ajout marqueurs
    for _, row in df_region.iterrows():
        # Détection colonne nom
        name_col = None
        for col in ["code_bib", "nom", "Nom", "name", "Bibliothèque", "Etablissement"]:
            if col in row.index and pd.notna(row[col]):
                name_col = col
                break
        
        popup_text = f"Région: {row['Région']}"
        if name_col:
            popup_text = f"{row[name_col]}<br>{popup_text}"
        
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=popup_text,
            tooltip="📚 Bibliothèque"
        ).add_to(marker_cluster)
    
    # Affichage
    st_folium(m, width=700, height=500)

# Stats finales
st.markdown("---")
st.subheader("Résumé")

col1, col2 = st.columns(2)
with col1:
    st.write("**Statistiques générales:**")
    st.write(f"• {total_bib:,} bibliothèques au total")
    st.write(f"• {nb_regions} régions couvertes") 
    st.write(f"• {total_bib/nb_regions:.1f} bibliothèques/région en moyenne")

with col2:
    if df_pop is not None and not df_merged.empty:
        total_pop = df_merged["Population"].sum()
        correlation = df_merged["bibliotheques"].corr(df_merged["Population"])
        densite_nationale = (total_bib/total_pop*100000)
        st.write("**Avec données population:**")
        st.write(f"• {total_pop/1e6:.1f}M d'habitants couverts")
        st.write(f"• Corrélation bib/pop: {correlation:.2f}")
        st.write(f"• {densite_nationale:.1f} bib./100k hab. national")
    else:
        st.write("**Données population:**")
        st.write("• Non disponibles")
        st.write("• Certains graphiques limités")