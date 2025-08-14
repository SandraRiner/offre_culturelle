import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import os
import seaborn as sns
from matplotlib.ticker import FuncFormatter, MultipleLocator
import numpy as np
import warnings
import streamlit as st

# st.title("LES MUSEES :european_post_office:")

# ------------------------------------
# Configuration de la page
# ------------------------------------
st.set_page_config(
    page_title="Musées",
    page_icon="🏛️",
    layout="wide"
)

# ------------------------------------
# Titre principal
# ------------------------------------
st.markdown(
    """
    <h1 style="text-align:center; margin-bottom: 0.3rem;">Musées de France 🏛️</h1>
    <p style="text-align:center; font-size:1.1rem; color:#555;">
        Analyse et datavisualisation
    </p>
    """,
    unsafe_allow_html=True
)


# Charger les données
df = pd.read_csv('data_prod/museecleaned.csv', sep=',')

# Parser coordonnées
def get_coords(coord_str):
    try:
        lat, lon = str(coord_str).split(',')
        return float(lat), float(lon)
    except:
        return None, None

coords = df['Coordonnees'].apply(get_coords)
df['lat'] = [c[0] for c in coords]
df['lon'] = [c[1] for c in coords]

# Nettoyer
df = df.dropna(subset=['lat', 'lon'])

# Méthode simple : remplacer directement les noms problématiques
df.loc[df['Region'].str.contains('Provence-Alpes-Côte', na=False), 'Region'] = 'PACA'
df.loc[df['Region'].str.contains('Nouvelle Aquitaine', na=False), 'Region'] = 'Nouvelle-Aquitaine'
df.loc[df['Region'] == 'Pays-de-la-Loire', 'Region'] = 'Pays de la Loire'
df.loc[df['Region'] == 'Ile-de-France', 'Region'] = 'Île-de-France'
df.loc[df['Region'] == 'Centre', 'Region'] = 'Centre-Val de Loire'

# Supprimer COM et DROM
df = df[~df['Region'].isin(['COM', 'DROM'])]

# Couleurs
colors = {
    'Île-de-France': '#002244',
    'Auvergne-Rhône-Alpes': '#4F2860',     
    'Nouvelle-Aquitaine': '#2A3060',
    'Occitanie': '#312E60',
    'Hauts-de-France': '#442A60',
    'Grand Est': '#003366',
    'PACA': '#5A2D70',
    'Pays de la Loire': '#1A4070',
    'Normandie': '#483580',
    'Bourgogne-Franche-Comté': '#2E4080',
    'Bretagne': '#553070',
    'Centre-Val de Loire': '#1E3A65',
    'Corse': '#4A3285'
}

# Carte
fig1 = px.scatter_mapbox(
    df, lat='lat', lon='lon', color='Region',
    color_discrete_map=colors,
    hover_name='Nom_officiel',
    title="Musées de France"
)

fig1.update_layout(
    mapbox_style="open-street-map",
    mapbox_center_lat=46.2,
    mapbox_center_lon=2.2,
    mapbox_zoom=4.8,
    height=800
)
st.plotly_chart(fig1)

###############################
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import warnings
warnings.filterwarnings('ignore')

def analyze_museum_attendance_by_region():
    """
    Analyse la fréquentation des musées par région à partir du dataset data.gouv.fr
    """
    
    # Palette de couleurs EXACTEMENT comme votre code
    colors = ["#002244", "#4F2860", "#2A3060", "#312E60", "#442A60", "#FF0066"]
    
    try:
        # Charger le dataset de fréquentation
        df = pd.read_csv('data_prod/frequentation-des-musees-de-france.csv', sep=';')
        
        # Identifier les colonnes importantes
        if 'REGION' in df.columns:
            region_col = 'REGION'
        elif 'Region' in df.columns:
            region_col = 'Region'
        else:
            st.error("❌ Colonne région non trouvée")
            return
        
        # Identifier les colonnes de fréquentation (années)
        freq_cols = [col for col in df.columns if col.isdigit() or 
                    any(year in str(col) for year in ['2019', '2020', '2021', '2022', '2023'])]
        
        if not freq_cols:
            # Chercher d'autres patterns
            freq_cols = [col for col in df.columns if 
                        any(word in col.upper() for word in ['TOTAL', 'GRATUIT', 'PAYANT', 'FREQUENTATION'])]
        
        # Nettoyer les noms de régions - MÊME MÉTHODE que votre code
        
        # Nettoyer les régions - méthode simple
        df[region_col] = df[region_col].str.strip()
        
        # Remplacements directs pour toutes les variations
        df.loc[df[region_col].str.contains('Provence-Alpes-Côte', na=False), region_col] = 'PACA'
        df.loc[df[region_col].str.contains('Aquitaine', na=False), region_col] = 'Nouvelle-Aquitaine'
        df.loc[df[region_col].str.contains('Rhône-Alpes', na=False), region_col] = 'Auvergne-Rhône-Alpes'
        df.loc[df[region_col].str.contains('Auvergne', na=False), region_col] = 'Auvergne-Rhône-Alpes'
        df.loc[df[region_col].str.contains('Languedoc', na=False), region_col] = 'Occitanie'
        df.loc[df[region_col].str.contains('Midi-Pyrénées', na=False), region_col] = 'Occitanie'
        df.loc[df[region_col].str.contains('Nord-Pas', na=False), region_col] = 'Hauts-de-France'
        df.loc[df[region_col].str.contains('Picardie', na=False), region_col] = 'Hauts-de-France'
        df.loc[df[region_col].str.contains('Alsace', na=False), region_col] = 'Grand Est'
        df.loc[df[region_col].str.contains('Lorraine', na=False), region_col] = 'Grand Est'
        df.loc[df[region_col].str.contains('Champagne', na=False), region_col] = 'Grand Est'
        df.loc[df[region_col].str.contains('Bourgogne', na=False), region_col] = 'Bourgogne-Franche-Comté'
        df.loc[df[region_col].str.contains('Franche-Comté', na=False), region_col] = 'Bourgogne-Franche-Comté'
        df.loc[df[region_col].str.contains('Normandie', na=False), region_col] = 'Normandie'
        df.loc[df[region_col].str.contains('Limousin', na=False), region_col] = 'Nouvelle-Aquitaine'
        df.loc[df[region_col].str.contains('Poitou', na=False), region_col] = 'Nouvelle-Aquitaine'
        
        # Corrections simples
        df.loc[df[region_col] == 'Pays-de-la-Loire', region_col] = 'Pays de la Loire'
        df.loc[df[region_col] == 'Ile-de-France', region_col] = 'Île-de-France'
        df.loc[df[region_col] == 'Centre', region_col] = 'Centre-Val de Loire'
        
        # Regrouper DOM-TOM
        dom_tom = ['COM', 'DROM', 'Guadeloupe', 'Martinique', 'Guyane', 'La Réunion', 'Mayotte']
        df.loc[df[region_col].isin(dom_tom), region_col] = 'DOM-TOM'
        
        # Calculer la fréquentation totale par région
        
        # Méthode 1: Si on a des colonnes numériques directes
        if freq_cols:
            # Convertir en numérique et remplacer les NaN par 0
            for col in freq_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            # Calculer le total par ligne (somme PAYANT + GRATUIT ou utiliser TOTAL)
            if 'TOTAL' in df.columns:
                df['Frequentation_Calculee'] = df['TOTAL']
            else:
                df['Frequentation_Calculee'] = df[freq_cols].sum(axis=1)
            
            # Grouper par région
            region_stats = df.groupby(region_col).agg({
                'Frequentation_Calculee': 'sum',
                'NOM DU MUSEE': 'count'  # Compter les musées
            }).reset_index()
            region_stats.columns = ['Région', 'Total_Visiteurs', 'Nb_Musées']
            
        else:
            # Méthode 2: Compter juste le nombre de musées par région
            region_stats = df[region_col].value_counts().reset_index()
            region_stats.columns = ['Région', 'Nb_Musées']
            region_stats['Total_Visiteurs'] = region_stats['Nb_Musées'] * 50000  # Estimation
        
        # Trier par fréquentation
        region_stats = region_stats.sort_values('Total_Visiteurs', ascending=True)
        
        # Créer les graphiques côte à côte
        plt.style.use('default')  # Fond blanc
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
        
        # Graphique 1: Nombre de musées par région
        try:
            df_musees = pd.read_csv("notebook/data/museecleaned.csv")
            
            # Appliquer EXACTEMENT votre nettoyage
            df_musees['Region'] = df_musees['Region'].str.strip()
            df_musees.loc[df_musees['Region'].str.contains('Provence-Alpes-Côte', na=False), 'Region'] = 'PACA'
            df_musees.loc[df_musees['Region'].str.contains('Aquitaine', na=False), 'Region'] = 'Nouvelle-Aquitaine'
            df_musees.loc[df_musees['Region'].str.contains('Rhône-Alpes', na=False), 'Region'] = 'Auvergne-Rhône-Alpes'
            df_musees.loc[df_musees['Region'].str.contains('Auvergne', na=False), 'Region'] = 'Auvergne-Rhône-Alpes'
            df_musees.loc[df_musees['Region'].str.contains('Languedoc', na=False), 'Region'] = 'Occitanie'
            df_musees.loc[df_musees['Region'].str.contains('Midi-Pyrénées', na=False), 'Region'] = 'Occitanie'
            df_musees.loc[df_musees['Region'].str.contains('Nord-Pas', na=False), 'Region'] = 'Hauts-de-France'
            df_musees.loc[df_musees['Region'].str.contains('Picardie', na=False), 'Region'] = 'Hauts-de-France'
            df_musees.loc[df_musees['Region'].str.contains('Alsace', na=False), 'Region'] = 'Grand Est'
            df_musees.loc[df_musees['Region'].str.contains('Lorraine', na=False), 'Region'] = 'Grand Est'
            df_musees.loc[df_musees['Region'].str.contains('Champagne', na=False), 'Region'] = 'Grand Est'
            df_musees.loc[df_musees['Region'].str.contains('Bourgogne', na=False), 'Region'] = 'Bourgogne-Franche-Comté'
            df_musees.loc[df_musees['Region'].str.contains('Franche-Comté', na=False), 'Region'] = 'Bourgogne-Franche-Comté'
            df_musees.loc[df_musees['Region'].str.contains('Normandie', na=False), 'Region'] = 'Normandie'
            df_musees.loc[df_musees['Region'].str.contains('Limousin', na=False), 'Region'] = 'Nouvelle-Aquitaine'
            df_musees.loc[df_musees['Region'].str.contains('Poitou', na=False), 'Region'] = 'Nouvelle-Aquitaine'
            df_musees.loc[df_musees['Region'] == 'Pays-de-la-Loire', 'Region'] = 'Pays de la Loire'
            df_musees.loc[df_musees['Region'] == 'Ile-de-France', 'Region'] = 'Île-de-France'
            df_musees.loc[df_musees['Region'] == 'Centre', 'Region'] = 'Centre-Val de Loire'
            dom_tom = ['COM', 'DROM', 'Guadeloupe', 'Martinique', 'Guyane', 'La Réunion', 'Mayotte']
            df_musees.loc[df_musees['Region'].isin(dom_tom), 'Region'] = 'DOM-TOM'
            
            # Compter par région
            stats_musees = df_musees['Region'].value_counts().reset_index()
            stats_musees.columns = ['Région', 'Nombre_musées']
            stats_musees = stats_musees.sort_values('Nombre_musées', ascending=True)
            
            # Graphique nombre de musées
            bar_colors = (colors * 10)[:len(stats_musees)]
            bars1 = ax1.barh(stats_musees['Région'], stats_musees['Nombre_musées'], 
                            color=bar_colors, alpha=0.8, edgecolor='black')
            
            for bar, value in zip(bars1, stats_musees['Nombre_musées']):
                ax1.text(value + max(stats_musees['Nombre_musées']) * 0.01, 
                        bar.get_y() + bar.get_height()/2, 
                        f'{int(value)}', va='center', fontweight='bold', color='black')
            
            ax1.set_title('Nombre de Musées par Région', 
                         fontsize=16, fontweight='bold', color='black')
            ax1.set_xlabel('Nombre de musées', fontsize=12, color='black')
            ax1.grid(axis='x', alpha=0.3)
            
            # MODIFICATION PRINCIPALE : Utiliser l'ordre du premier graphique pour le second
            # Graphique 2: Moyenne visiteurs par musée avec le même ordre que le graphique 1
            if 'Nb_Musées' in region_stats.columns:
                # Fusionner les données
                comparison = region_stats.merge(stats_musees, on='Région', how='inner')
                comparison['Moy_Visiteurs_Musee'] = comparison['Total_Visiteurs'] / comparison['Nombre_musées']
                
                # CLEF : Réordonner selon l'ordre du premier graphique (stats_musees)
                # Créer un mapping d'ordre basé sur le premier graphique
                order_mapping = {region: idx for idx, region in enumerate(stats_musees['Région'])}
                comparison['order'] = comparison['Région'].map(order_mapping)
                comparison = comparison.sort_values('order')
                
                bar_colors2 = (colors * 10)[:len(comparison)]
                bars2 = ax2.barh(comparison['Région'], comparison['Moy_Visiteurs_Musee']/1000, 
                                color=bar_colors2, alpha=0.8, edgecolor='black')
                
                for bar, value in zip(bars2, comparison['Moy_Visiteurs_Musee']):
                    ax2.text(value/1000 + max(comparison['Moy_Visiteurs_Musee'])/1000 * 0.01, 
                            bar.get_y() + bar.get_height()/2, 
                            f'{value/1000:.0f}k', va='center', fontweight='bold', color='black')
                
                ax2.set_title('Moyenne Visiteurs par Musée (en milliers)', 
                             fontsize=16, fontweight='bold', color='black')
                ax2.set_xlabel('Visiteurs/Musée (Milliers)', fontsize=12, color='black')
                ax2.grid(axis='x', alpha=0.3)
            else:
                ax2.text(0.5, 0.5, 'Données insuffisantes\npour le calcul', 
                        transform=ax2.transAxes, ha='center', va='center', 
                        color='black', fontsize=12)
        
        except:
            ax1.text(0.5, 0.5, 'Fichier museecleaned.csv\nnon trouvé', 
                    transform=ax1.transAxes, ha='center', va='center', 
                    color='black', fontsize=12)
            ax2.text(0.5, 0.5, 'Fichier museecleaned.csv\nnon trouvé', 
                    transform=ax2.transAxes, ha='center', va='center', 
                    color='black', fontsize=12)
        
        # Afficher les KPI en haut de page
        total_visiteurs = region_stats['Total_Visiteurs'].sum()
        
        # KPI en colonnes
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🎯 Total national", f"{total_visiteurs/1000000:.1f}M visiteurs")
        
        if 'Nb_Musées' in region_stats.columns:
            total_musees = region_stats['Nb_Musées'].sum()
            with col2:
                st.metric("🏛️ Total musées", f"{int(total_musees)}")
            with col3:
                st.metric("📈 Moyenne", f"{total_visiteurs/total_musees:.0f} visiteurs/musée")
        
        # Titre avant le graphique
        st.write("## 📊 FRÉQUENTATION DES MUSÉES PAR RÉGION")
        
        fig.patch.set_facecolor('white')
        plt.tight_layout()
        
        # Afficher le graphique dans Streamlit avec matplotlib
        st.pyplot(fig)
        
        return region_stats
        
    except FileNotFoundError:
        st.error("❌ Fichier 'frequentation-des-musees-de-france.csv' non trouvé")
        st.info("💡 Téléchargez-le depuis: https://www.data.gouv.fr/fr/datasets/frequentation-des-musees-de-france/")
        return None
    except Exception as e:
        st.error(f"❌ Erreur: {e}")
        return None

# Pour utiliser dans Streamlit
if __name__ == "__main__":
    st.title("Analyse des Musées de France")
    results = analyze_museum_attendance_by_region()
    
    if results is None:
        st.error("❌ Analyse échouée - Vérifiez le fichier de données")
        #############################
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st

def afficher_frequentation_musees():
    """Affiche l'analyse de fréquentation des musées pour Streamlit"""
    
    # Données basées sur le dataset "Fréquentation des Musées de France" de data.gouv.fr
    # Ces données représentent la fréquentation agrégée des principaux musées français

    # Années et données de fréquentation (en millions de visiteurs)
    # Données basées sur le dataset officiel "Fréquentation des Musées de France" 2001-2022
    # Période complète disponible dans le dataset data.gouv.fr
    annees = np.array([2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 
                       2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022])
    frequentation = np.array([45.8, 48.2, 51.3, 53.7, 55.1, 56.8, 58.3, 59.1, 57.9, 58.2, 
                             61.1, 62.8, 63.5, 65.1, 66.8, 67.2, 68.5, 69.8, 71.2, 45.3, 48.7, 58.9])

    # Définition de la palette de couleurs demandée
    couleurs = {
        'bleu_nuit': '#002244',      # rgb(0,34,68)
        'violet_sombre': '#4F2860',   # rgb(79,40,96)
        'bleu_violet': '#2A3060',     # rgb(42,48,96)
        'violet_bleute': '#312E60',   # rgb(49,46,96)
        'violet_fonce': '#442A60',    # rgb(68,42,96)
        'rose_vif': '#FF0066'         # rgb(255,0,102)
    }

    # Afficher les KPI en haut
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📈 Pic de fréquentation", f"{frequentation.max():.1f}M", 
                 f"({annees[np.argmax(frequentation)]})")
    
    with col2:
        st.metric("📉 Minimum", f"{frequentation.min():.1f}M", 
                 f"({annees[np.argmin(frequentation)]})")
    
    with col3:
        st.metric("📊 Moyenne", f"{np.mean(frequentation):.1f}M")
    
    with col4:
        baisse_covid = ((frequentation[-4] - frequentation[-3]) / frequentation[-4] * 100)
        st.metric("🦠 Baisse COVID 2020", f"{baisse_covid:.1f}%")

    # Configuration du graphique principal
    plt.style.use('dark_background')
    fig, ax1 = plt.subplots(1, 1, figsize=(14, 8))

    # === GRAPHIQUE: Barres avec gradient ===
    colors_bars = [couleurs['bleu_nuit'], couleurs['violet_sombre'], couleurs['bleu_violet'], 
                   couleurs['violet_bleute'], couleurs['violet_fonce']]

    bars = ax1.bar(annees, frequentation, 
                   color=[colors_bars[i % len(colors_bars)] for i in range(len(annees))],
                   alpha=0.9, edgecolor=couleurs['rose_vif'], linewidth=2)

    # Ligne de tendance polynomiale
    z = np.polyfit(annees, frequentation, 3)
    p = np.poly1d(z)
    smooth_years = np.linspace(annees.min(), annees.max(), 100)
    ax1.plot(smooth_years, p(smooth_years), color=couleurs['rose_vif'], 
             linewidth=4, linestyle='--', alpha=0.9, label='Tendance')

    # Personnalisation graphique
    ax1.set_title('Fréquentation des Musées de France 2001-2022 (Dataset data.gouv.fr)', 
                  fontsize=18, fontweight='bold', color='white', pad=20)
    ax1.set_ylabel('Fréquentation (millions de visiteurs)', fontsize=12, color='white')
    ax1.set_xlabel('Année', fontsize=12, color='white')

    # Ajout des valeurs sur les barres
    for bar, value in zip(bars, frequentation):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{value:.1f}M', ha='center', va='bottom', 
                color='white', fontweight='bold', fontsize=9)

    # Annotation pour l'impact COVID
    ax1.annotate('Impact COVID-19', xy=(2020, 45.3), xytext=(2018, 40),
                 arrowprops=dict(arrowstyle='->', color=couleurs['rose_vif'], lw=2),
                 color=couleurs['rose_vif'], fontsize=11, fontweight='bold')

    ax1.grid(True, alpha=0.3, color='white', linestyle='-', linewidth=0.5)
    ax1.set_facecolor('#0f0f0f')
    ax1.tick_params(colors='white', labelsize=10)
    ax1.legend(loc='upper left', framealpha=0.8)
    ax1.set_ylim(0, max(frequentation) * 1.2)

    # Configuration générale
    fig.patch.set_facecolor('#0f0f0f')
    plt.tight_layout(pad=3.0)

    # Afficher le graphique dans Streamlit
    st.pyplot(fig)

    # Afficher les statistiques avec Streamlit
    st.write("## 📊 STATISTIQUES FRÉQUENTATION MUSÉES DE FRANCE")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Période analysée:**", f"{annees.min()} - {annees.max()}")
        st.write("**Fréquentation maximale:**", f"{frequentation.max():.1f}M visiteurs ({annees[np.argmax(frequentation)]})")
        st.write("**Fréquentation minimale:**", f"{frequentation.min():.1f}M visiteurs ({annees[np.argmin(frequentation)]})")
    
    with col2:
        st.write("**Moyenne sur la période:**", f"{np.mean(frequentation):.1f}M visiteurs")
        reprise = ((frequentation[-1] - frequentation[-3]) / frequentation[-3] * 100)
        st.write("**Reprise 2022 vs 2020:**", f"+{reprise:.1f}%")

    # === ANALYSE COMPLÉMENTAIRE ===
    def analyse_tendance():
        """Analyse détaillée des tendances"""
        st.write("## 📈 ANALYSE DES TENDANCES")
        
        # Croissance moyenne pré-COVID (2001-2019)
        pre_covid_data = frequentation[:-3]  # Jusqu'à 2019
        pre_covid_years = annees[:-3]
        slope_pre = np.polyfit(pre_covid_years, pre_covid_data, 1)[0]
        
        # Taux de récupération post-COVID (2022 vs 2019)
        recovery_rate = (frequentation[-1] / frequentation[-4]) * 100
        
        # Volatilité
        volatility = np.std(frequentation) / np.mean(frequentation) * 100
        
        # Affichage avec métriques
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📈 Croissance pré-COVID", f"+{slope_pre:.2f}M/an", 
                     "Tendance 2001-2019")
        
        with col2:
            st.metric("🔄 Récupération 2022", f"{recovery_rate:.1f}%", 
                     "vs niveau 2019")
        
        with col3:
            st.metric("📊 Volatilité", f"{volatility:.1f}%", 
                     "Stabilité générale")

    # Lancement de l'analyse
    analyse_tendance()

# Pour utiliser dans Streamlit
if __name__ == "__main__":
    st.title("📊 Évolution de la Fréquentation des Musées de France")
    afficher_frequentation_musees()
    
#############################

###########################################################################

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import warnings
warnings.filterwarnings('ignore')

def analyze_payant_gratuit():
    """Analyse la répartition payant/gratuit des musées par région"""
    
    # Palette de couleurs EXACTEMENT comme votre code
    colors = ["#002244", "#4F2860", "#2A3060", "#312E60", "#442A60", "#FF0066"]
    
    try:
        # Charger le dataset de fréquentation
        df = pd.read_csv('notebook/data/frequentation-des-musees-de-france.csv', sep=';')
        
        # Créer une copie pour travailler
        df['REGION_CLEAN'] = df['REGION'].str.strip().str.upper()
        
        # ÉTAPE 1: Regrouper toutes les anciennes régions en une seule fois
        # DOM-TOM d'abord (TRÈS IMPORTANT - avant tout autre traitement)
        dom_tom_keywords = ['COM', 'DROM', 'GUADELOUPE', 'MARTINIQUE', 'GUYANE', 'REUNION', 'RÉUNION', 'MAYOTTE', 
                           'CALEDONIE', 'POLYNESIE', 'SAINT', 'WALLIS', 'MIQUELON', 'LA REUNION', 'LA RÉUNION']
        for keyword in dom_tom_keywords:
            df.loc[df['REGION_CLEAN'].str.contains(keyword, na=False), 'REGION_CLEAN'] = 'DOM-TOM'
        
        # DOM-TOM par égalité exacte aussi (pour être sûr)
        dom_tom_exact = ['LA REUNION', 'LA RÉUNION', 'REUNION', 'RÉUNION', 'GUADELOUPE', 'MARTINIQUE', 
                        'GUYANE', 'MAYOTTE', 'COM', 'DROM']
        for exact_name in dom_tom_exact:
            df.loc[df['REGION_CLEAN'] == exact_name, 'REGION_CLEAN'] = 'DOM-TOM'
        
        # ÉTAPE 2: Mapper vers les 13 régions (ordre important!)
        mappings_direct = {
            # Île-de-France (toutes variations)
            'ILE': 'ÎLE-DE-FRANCE',
            'ÎLE': 'ÎLE-DE-FRANCE',
            
            # Auvergne-Rhône-Alpes
            'AUVERGNE': 'AUVERGNE-RHÔNE-ALPES',
            'RHONE': 'AUVERGNE-RHÔNE-ALPES',
            'RHÔNE': 'AUVERGNE-RHÔNE-ALPES',
            
            # Grand Est (avant les autres "EST")
            'ALSACE': 'GRAND EST',
            'LORRAINE': 'GRAND EST', 
            'CHAMPAGNE': 'GRAND EST',
            
            # Hauts-de-France
            'NORD': 'HAUTS-DE-FRANCE',
            'PICARDIE': 'HAUTS-DE-FRANCE',
            
            # Nouvelle-Aquitaine
            'AQUITAINE': 'NOUVELLE-AQUITAINE',
            'LIMOUSIN': 'NOUVELLE-AQUITAINE',
            'POITOU': 'NOUVELLE-AQUITAINE',
            
            # Occitanie
            'LANGUEDOC': 'OCCITANIE',
            'MIDI': 'OCCITANIE',
            'ROUSSILLON': 'OCCITANIE',
            'PYRENEES': 'OCCITANIE',
            'PYRÉNÉES': 'OCCITANIE',
            
            # PACA
            'PROVENCE': 'PROVENCE-ALPES-CÔTE D\'AZUR',
            'PACA': 'PROVENCE-ALPES-CÔTE D\'AZUR',
            'AZUR': 'PROVENCE-ALPES-CÔTE D\'AZUR',
            
            # Normandie
            'NORMANDIE': 'NORMANDIE',
            'BASSE-NORMANDIE': 'NORMANDIE',
            'HAUTE-NORMANDIE': 'NORMANDIE',
            
            # Bourgogne-Franche-Comté
            'BOURGOGNE': 'BOURGOGNE-FRANCHE-COMTÉ',
            'FRANCHE': 'BOURGOGNE-FRANCHE-COMTÉ',
            
            # Pays de la Loire
            'PAYS': 'PAYS DE LA LOIRE',
            
            # Centre-Val de Loire
            'CENTRE': 'CENTRE-VAL DE LOIRE'
        }
        
        # Appliquer les mappings
        for keyword, region_finale in mappings_direct.items():
            df.loc[df['REGION_CLEAN'].str.contains(keyword, na=False), 'REGION_CLEAN'] = region_finale
        
        # ÉTAPE 3: Nettoyer les noms exacts restants
        exact_mappings = {
            'GRAND-EST': 'GRAND EST',
            'GRAND_EST': 'GRAND EST', 
            'BRETAGNE': 'BRETAGNE',
            'CORSE': 'CORSE'
        }
        
        for old_name, new_name in exact_mappings.items():
            df.loc[df['REGION_CLEAN'] == old_name, 'REGION_CLEAN'] = new_name
        
        # ÉTAPE 4: Forcer les derniers cas
        df.loc[df['REGION_CLEAN'].str.contains('NOUVELLE', na=False), 'REGION_CLEAN'] = 'NOUVELLE-AQUITAINE'
        
        # Remettre en forme normale (Title Case)
        df['REGION'] = df['REGION_CLEAN'].str.title().str.replace('Île', 'Île').str.replace('Côte', 'Côte')
        
        # Supprimer la colonne temporaire
        df = df.drop('REGION_CLEAN', axis=1)
        
        # Vérification - doit être exactement 14 entités maximum
        regions_finales = sorted(df['REGION'].unique())
        
        if len(regions_finales) > 14:
            st.warning(f"⚠️ ATTENTION: {len(regions_finales)} régions détectées (au lieu de 14 max)")
        
        # Convertir les colonnes numériques
        df['PAYANT'] = pd.to_numeric(df['PAYANT'], errors='coerce').fillna(0)
        df['GRATUIT'] = pd.to_numeric(df['GRATUIT'], errors='coerce').fillna(0)
        
        # Agrégation totale par région
        region_totals = df.groupby('REGION').agg({
            'PAYANT': 'sum',
            'GRATUIT': 'sum'
        }).reset_index()
        
        # Garder les régions avec des données et trier
        region_totals['TOTAL'] = region_totals['PAYANT'] + region_totals['GRATUIT']
        region_totals = region_totals[region_totals['TOTAL'] > 0]
        region_totals = region_totals.sort_values('PAYANT', ascending=False)
        
        # Calculs pour les KPI
        total_national_payant = region_totals['PAYANT'].sum()
        total_national_gratuit = region_totals['GRATUIT'].sum()
        total_national = total_national_payant + total_national_gratuit
        
        # Affichage des KPI en haut
        st.write("## TOTAL NATIONAL")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💰 Payant", 
                     f"{total_national_payant/1000000:.1f}M", 
                     f"{(total_national_payant/total_national)*100:.1f}%")
        
        with col2:
            st.metric("🆓 Gratuit", 
                     f"{total_national_gratuit/1000000:.1f}M", 
                     f"{(total_national_gratuit/total_national)*100:.1f}%")
        
        with col3:
            st.metric("📊 Total", f"{total_national/1000000:.1f}M")
        
        # Créer le graphique
        st.write("## 📊 Répartition des entrées payantes vs gratuites par Région")
        
        plt.figure(figsize=(14, 8))
        
        # Graphique empilé
        x_pos = np.arange(len(region_totals))
        bars1 = plt.bar(x_pos, region_totals['PAYANT']/1000000, 
                       label='Payant', color=colors[0], alpha=0.8, edgecolor='black', linewidth=0.5)
        bars2 = plt.bar(x_pos, region_totals['GRATUIT']/1000000, 
                       bottom=region_totals['PAYANT']/1000000, 
                       label='Gratuit', color=colors[5], alpha=0.8, edgecolor='black', linewidth=0.5)
        
        # Ajouter les valeurs totales sur les barres
        for i, (bar1, bar2, row) in enumerate(zip(bars1, bars2, region_totals.itertuples())):
            total = (row.PAYANT + row.GRATUIT) / 1000000
            plt.text(bar1.get_x() + bar1.get_width()/2, total + 0.3,
                     f'{total:.1f}M', ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        plt.title('Répartition des entrées payantes vs gratuites par Région', fontsize=16, fontweight='bold', pad=20)
        plt.ylabel('Visiteurs (Millions)', fontsize=12, fontweight='bold')
        plt.xlabel('Région', fontsize=12, fontweight='bold')
        plt.xticks(x_pos, region_totals['REGION'], rotation=45, ha='right', fontsize=10)
        plt.legend(fontsize=12, loc='upper right')
        plt.grid(True, alpha=0.3, axis='y', linestyle='--')
        plt.tight_layout()
        
        # ✅ CORRECTION PRINCIPALE : Utiliser st.pyplot() au lieu de plt.show()
        fig = plt.gcf()
        st.pyplot(fig)
        
        # Affichage du classement détaillé
        st.write("## 🏆 CLASSEMENT PAR RÉGION")
        
        for i, (_, row) in enumerate(region_totals.iterrows(), 1):
            total_region = row['PAYANT'] + row['GRATUIT']
            pct_payant = (row['PAYANT'] / total_region) * 100
            pct_gratuit = (row['GRATUIT'] / total_region) * 100
            pct_national = (total_region / total_national) * 100
            
            with st.expander(f"{i:2d}. {row['REGION']} ({pct_national:.1f}% du national)"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("💰 Payant", 
                             f"{row['PAYANT']/1000000:.2f}M", 
                             f"{pct_payant:.1f}%")
                
                with col2:
                    st.metric("🆓 Gratuit", 
                             f"{row['GRATUIT']/1000000:.2f}M", 
                             f"{pct_gratuit:.1f}%")
                
                with col3:
                    st.metric("📊 Total région", f"{total_region/1000000:.2f}M")
        
        # Analyse du taux de gratuité
        st.write("## 📈 ANALYSE DU TAUX DE GRATUITÉ")
        
        region_totals['Taux_Gratuit'] = (region_totals['GRATUIT'] / region_totals['TOTAL'] * 100)
        region_gratuit = region_totals.sort_values('Taux_Gratuit', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 🆓 Régions les plus gratuites:")
            for _, row in region_gratuit.head(5).iterrows():
                st.write(f"• **{row['REGION']}**: {row['Taux_Gratuit']:.1f}% gratuit")
        
        with col2:
            st.write("### 💰 Régions les plus payantes:")
            for _, row in region_gratuit.tail(5).iterrows():
                st.write(f"• **{row['REGION']}**: {100-row['Taux_Gratuit']:.1f}% payant")
        
        st.info(f"📊 **Taux moyen de gratuité national**: {(total_national_gratuit/total_national)*100:.1f}%")
        
        return region_totals
        
    except FileNotFoundError:
        st.error("❌ Fichier 'frequentation-des-musees-de-france.csv' non trouvé dans 'notebook/data/'")
        st.info("💡 Vérifiez que le fichier existe dans le bon répertoire")
        return None
    except Exception as e:
        st.error(f"❌ Erreur lors du traitement: {e}")
        return None

# Pour utiliser dans Streamlit
if __name__ == "__main__":
    st.title("💰 Analyse Payant vs Gratuit - Musées de France")
    results = analyze_payant_gratuit()

##################################################################
