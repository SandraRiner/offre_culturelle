# -*- coding: utf-8 -*-
"""
Streamlit — Bibliothèques par région (barplot + carte)
- Titre principal centré et bien visible
- Barplot centré, compact, étiquettes conditionnelles
- Barres vs population (ligne) avec look & feel homogène
- Carte Folium large (clusters)
"""

# =======================
# Imports + CONFIG
# =======================
import os
import pandas as pd
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

# Config page Streamlit
st.set_page_config(page_title="Bibliothèques", layout="wide")

# CSS personnalisé pour améliorer l'affichage
st.markdown(
    """
    <style>
      .block-container {
        max-width: 1600px;
        padding-top: 2.5rem; /* Plus d'espace en haut pour éviter la troncature */
        padding-bottom: 1rem;
      }
      
      /* Style pour le titre principal centré */
      .main-title {
        text-align: center;
        font-size: 16px;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 2rem;
        margin-top: 1rem;
        padding: 1rem 0;
        border-bottom: 3px solid #1f77b4;
      }
      
      /* Espacement et taille des sous-titres */
      h2 {
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-top: 1rem;
        font-size: 14px !important;
      }
      
      /* Taille des sous-titres h3 */
      h3 {
        font-size: 14px !important;
      }
      
      /* Amélioration de l'affichage général */
      .stSelectbox > div > div {
        margin-bottom: 1rem;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# Titre principal centré avec style personnalisé
st.markdown(
    """
    <div class="main-title">
        📚 Bibliothèques par Région
    </div>
    """,
    unsafe_allow_html=True,
)

# Phrase d'introduction
st.markdown(
    """
    <div style="text-align: center; font-size: 14px; color: #666; margin-bottom: 2rem; font-style: italic;">
        Certaines régions ont plus d'offre mais pas plus de fréquentation
    </div>
    """,
    unsafe_allow_html=True,
)

# =======================
# Chargement des données
# =======================
CSV_PATH = "/home/karim/code/offre_culturelle/data/adresses_des_bibliotheques_publiques_prepared.csv"
if not os.path.exists(CSV_PATH):
    st.error(f"CSV introuvable : {CSV_PATH}")
    st.stop()

@st.cache_data
def load_csv(path: str) -> pd.DataFrame:
    """Lecture robuste du CSV avec mise en cache"""
    try:
        return pd.read_csv(path, sep=",", encoding="utf-8-sig")
    except Exception:
        return pd.read_csv(path, sep=None, engine="python", encoding="utf-8-sig", on_bad_lines="skip")

# Chargement avec mise en cache pour améliorer les performances
df = load_csv(CSV_PATH)

# Vérification des colonnes requises
required = ["Région", "Latitude", "Longitude"]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"Colonnes manquantes : {missing}\nColonnes disponibles : {list(df.columns)}")
    st.stop()

# Nettoyage des données
df["Région"] = df["Région"].astype(str).str.strip()
for col in ["Latitude", "Longitude"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Suppression des lignes avec des valeurs manquantes
df = df.dropna(subset=["Région", "Latitude", "Longitude"]).copy()

# Vérification qu'il reste des données
regions = sorted(df["Région"].unique())
if not regions:
    st.warning("Aucune région disponible après nettoyage des données.")
    st.stop()

# Affichage des statistiques générales
total_bibliotheques = len(df)
nb_regions = len(regions)

# Métriques en colonnes
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🌍 Total des bibliothèques", f"{total_bibliotheques:,}".replace(",", " "))
with col2:
    st.metric("#️⃣ Nombre de régions", nb_regions)
with col3:
    st.metric("📈 Moyenne par région", f"{total_bibliotheques // nb_regions}")

st.write("")
# === Population (nouveau fichier) ===
POP_CSV_PATH = "/home/karim/code/offre_culturelle/data/population-france-par-dept.csv"  # adapte le chemin si besoin

@st.cache_data
def load_population(path: str) -> pd.DataFrame:
    pop = pd.read_csv(path, sep=";", encoding="utf-8")
    # garde uniquement les colonnes utiles et assure les types
    pop = pop.rename(columns={"nom_region": "Région_pop", "Total": "Population"})
    pop["Population"] = pd.to_numeric(pop["Population"], errors="coerce")
    pop = pop.dropna(subset=["Région_pop", "Population"])
    # agrège au niveau RÉGION (le fichier est par département)
    pop_reg = pop.groupby("Région_pop", as_index=False)["Population"].sum()
    return pop_reg

try:
    pop_regions = load_population(POP_CSV_PATH)
except Exception as e:
    st.error(f"Erreur de lecture du fichier population : {e}")
    st.stop()

# =======================
# 1) Barplot compact et centré
# =======================
st.header("📊 Distribution des bibliothèques par région")
st.write("")

# Calcul des statistiques
counts = df["Région"].value_counts().sort_values(ascending=False)

# Palette de couleurs stable et attractive
color_map = plt.cm.Set3.colors
region_colors = {reg: color_map[i % len(color_map)] for i, reg in enumerate(counts.index)}

# Colonnes pour centrage du graphique
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    n = len(counts)
    # Calcul dynamique de la taille optimale
    fig_w = 8
    fig_h = min(max(0.35 * n + 2.5, 5), 8)

    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=120)
    
    # Création du graphique horizontal
    bars = counts.plot(
        kind="barh",
        ax=ax,
        color=[region_colors[reg] for reg in counts.index],
        edgecolor="white",
        linewidth=0.5
    )

    # Personnalisation du graphique
    ax.set_title("")  # Pas de titre dans la figure
    ax.set_xlabel("Nombre de bibliothèques", fontsize=12, fontweight='bold')
    ax.set_ylabel("Région", fontsize=12, fontweight='bold')
    ax.tick_params(labelsize=10)
    ax.invert_yaxis()
    
    # Grille subtile
    ax.grid(True, axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # Étiquettes intelligentes sur les barres
    max_val = counts.max()
    threshold = 0.2 * max_val

    for i, (region, val) in enumerate(counts.items()):
        txt = f"{int(val):,}".replace(",", " ")
        if val < threshold:
            # Étiquette à droite de la barre (texte noir)
            ax.annotate(
                txt, xy=(val, i), xytext=(5, 0), 
                textcoords="offset points",
                ha="left", va="center", 
                color="black", fontsize=9, fontweight="bold"
            )
        else:
            # Étiquette au centre de la barre (texte blanc)
            ax.annotate(
                txt, xy=(val / 2, i),
                ha="center", va="center", 
                color="white", fontsize=9, fontweight="bold"
            )

    # Ajustement des marges
    plt.tight_layout()
    fig.subplots_adjust(left=0.25, right=0.95, top=0.95, bottom=0.08)

    st.pyplot(fig, use_container_width=False)

# Affichage des tops 5 en deux colonnes
col_left, col_right = st.columns(2)

# Top 5 des régions avec le MOINS de bibliothèques (à gauche)
with col_left:
    st.markdown(
        """
        <div style="border: 2px solid #ff6b6b; border-radius: 10px; padding: 15px; background-color: #fff5f5;">
            <h4 style="color: #ff6b6b; margin-top: 0; text-align: center; font-size: 14px;">
                🏆 Top 5 des régions ayant le moins de bibliothèques
            </h4>
        </div>
        """,
        unsafe_allow_html=True,
    )
    bottom5 = counts.head(5)  # Les 5 premières (moins de bibliothèques)
    for i, (region, count_) in enumerate(bottom5.items(), 1):
        st.write(f"**{i}.** {region} : **{count_:,}** bibliothèques".replace(",", " "))

# Top 5 des régions avec le PLUS de bibliothèques (à droite)
with col_right:
    st.markdown(
        """
        <div style="border: 2px solid #4ecdc4; border-radius: 10px; padding: 15px; background-color: #f0fffe;">
            <h4 style="color: #4ecdc4; margin-top: 0; text-align: center; font-size: 14px;">
                🏆 Top 5 des régions ayant le plus de bibliothèques
            </h4>
        </div>
        """,
        unsafe_allow_html=True,
    )
    top5 = counts.tail(5).sort_values(ascending=False)  # Les 5 dernières, ordre décroissant
    for i, (region, count_) in enumerate(top5.items(), 1):
        st.write(f"**{i}.** {region} : **{count_:,}** bibliothèques".replace(",", " "))

st.divider()

# =======================
# 2) Barres vs population (clair & fluide) — avec le nouveau fichier
# =======================
st.header("📉 Bibliothèques vs population par région")
st.caption("Barres = nombre de bibliothèques • Ligne = population totale")

import unicodedata
from matplotlib.ticker import FuncFormatter
from matplotlib.lines import Line2D

# --- utils
def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", str(s)) if not unicodedata.combining(c))

def norm_region(x: str) -> str:
    """normalisation douce pour join robuste entre les 2 sources"""
    x = (x or "").strip()
    base = strip_accents(x).lower()
    base = base.replace("’", "'").replace("-", " ")
    base = base.replace(" d'", " d ").replace(" l'", " l ")
    base = " ".join(base.split())
    return base

# harmonisation de quelques noms (si nécessaire)
OVERRIDES = {
    "ile de france": "ile de france",
    "provence alpes cote d azur": "provence alpes cote d azur",
    "bourgogne franche comte": "bourgogne franche comte",
    "centre val de loire": "centre val de loire",
    "pays de la loire": "pays de la loire",
    "grand est": "grand est",
    "auvergne rhone alpes": "auvergne rhone alpes",
    "hauts de france": "hauts de france",
    "occitanie": "occitanie",
    "nouvelle aquitaine": "nouvelle aquitaine",
    "bretagne": "bretagne",
    "normandie": "normandie",
    "corse": "corse",
    "guadeloupe": "guadeloupe",
    "martinique": "martinique",
    "guyane": "guyane",
    "la reunion": "la reunion",
    "reunion": "la reunion",
    "mayotte": "mayotte",
}

def key_region(x: str) -> str:
    k = norm_region(x)
    return OVERRIDES.get(k, k)

# --- préparation bibliothèques
bib = df.copy()
bib["__key__"] = bib["Région"].astype(str).map(key_region)
agg_bib = (bib.groupby(["Région", "__key__"], as_index=False)
             .size().rename(columns={"size": "bibliotheques"}))

# --- préparation population (provenant du nouveau fichier)
pop_tmp = pop_regions.copy()
pop_tmp["__key__"] = pop_tmp["Région_pop"].map(key_region)
agg_pop = pop_tmp.groupby("__key__", as_index=False)["Population"].sum()

# --- jointure
agg = (agg_bib.merge(agg_pop, on="__key__", how="left")
              .drop(columns="__key__")
              .rename(columns={"Région": "region"}))

# garde seulement les régions avec population connue
agg = agg.dropna(subset=["Population"]).reset_index(drop=True)

# tri comme le 1er barplot : par nb de bibliothèques
agg = agg.sort_values("bibliotheques", ascending=False).reset_index(drop=True)

# libellés (abréviations si besoin)
def abbreviate_region(name: str) -> str:
    STOPWORDS = {"de","du","la","le","les","des","d","l","et","aux","au","à","en"}
    base = strip_accents(name).lower().replace("-", " ").replace("’", "'").replace("_", " ")
    base = base.replace("d'", "d ").replace("l'", "l ")
    base = " ".join(base.split())
    ABBR_OVERRIDES = {
        "ile de france":"IDF","auvergne rhone alpes":"ARA","provence alpes cote d azur":"PACA",
        "nouvelle aquitaine":"NAQ","occitanie":"OCC","hauts de france":"HDF","grand est":"GE",
        "bourgogne franche comte":"BFC","bretagne":"BRE","normandie":"NOR","centre val de loire":"CVL",
        "pays de la loire":"PDL","corse":"COR","guadeloupe":"GUA","martinique":"MAR",
        "guyane":"GUY","la reunion":"REU","mayotte":"MAY",
    }
    if base in ABBR_OVERRIDES: return ABBR_OVERRIDES[base]
    tokens = [t for t in base.split() if t not in STOPWORDS] or base.split()
    return ("".join(t[0].upper() for t in tokens))[:4] or name

regions_full = agg["region"].tolist()
need_abbr = any(len(r) > 18 for r in regions_full) or len(regions_full) > 14
x_labels = [abbreviate_region(r) if need_abbr else r for r in regions_full]

# formats
thousands = FuncFormatter(lambda x, pos: f"{int(x):,}".replace(",", " "))
millions  = FuncFormatter(lambda x, pos: f"{x/1e6:.1f} M")

# couleurs
cmap = plt.cm.Set3.colors
bar_colors = [cmap[i % len(cmap)] for i in range(len(agg))]

# rendu
c1, c2, c3 = st.columns([1, 6, 1])
with c2:
    fig_w, fig_h = 8, 5.8
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=120)

    # BARRES — bibliothèques
    bars = ax.bar(x_labels, agg["bibliotheques"],
                  color=bar_colors, edgecolor="#ffffff", linewidth=0.6)

    ax.set_ylabel("Nombre de bibliothèques", fontsize=12, fontweight="bold")
    ax.yaxis.set_major_formatter(thousands)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelrotation=35, labelsize=9)
    ax.set_xlabel("")

    # LIGNE — population (axe droit, en millions)
    ax2 = ax.twinx()
    ax2.plot(range(len(agg)), agg["Population"], marker="o", linewidth=2)
    ax2.yaxis.set_major_formatter(millions)
    ax2.set_ylabel("Population (M)", fontsize=11)
    ax2.tick_params(axis="y")

    # annotations sobres
    top_idx = agg["bibliotheques"].nlargest(4).index
    for i in top_idx:
        b = bars[i]
        ax.text(b.get_x()+b.get_width()/2, b.get_height(),
                f"{int(b.get_height()):,}".replace(",", " "),
                ha="center", va="bottom", fontsize=9, color="#333", fontweight="bold")

    p = agg["Population"]
    for i in [p.idxmax(), p.idxmin()]:
        ax2.annotate(f"{p[i]/1e6:.1f} M", (i, p[i]),
                     textcoords="offset points", xytext=(0, 8),
                     ha="center", fontsize=9)

    legend_items = [
        Line2D([0],[0], marker="s", markersize=10, linewidth=0,
               markerfacecolor=bar_colors[0], markeredgecolor="white", label="Bibliothèques"),
        Line2D([0],[0], color="C0", lw=2, marker="o", label="Population"),
    ]
    ax.legend(handles=legend_items, frameon=False, loc="upper right")

    for sp in ["top","right"]:
        ax.spines[sp].set_visible(False)
    ax2.spines["top"].set_visible(False)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

    if need_abbr:
        st.caption("Abréviations : " + " • ".join(f"{a} = {f}" for a, f in zip(x_labels, regions_full)))

# =======================
# 3) Carte interactive avec clusters
# =======================
st.header("🗺️ Localisation des bibliothèques par région")
st.write("Sélectionnez une région pour visualiser ses bibliothèques sur la carte.")

# Sélection de la région avec un selectbox amélioré
region_sel = st.selectbox(
    "**Choisissez une région :**", 
    regions, 
    index=0,
    help="La carte affichera toutes les bibliothèques de la région sélectionnée"
)

# Filtrage des données
dff = df[df["Région"] == region_sel].copy()
if dff.empty:
    st.info(f"Aucune bibliothèque trouvée pour la région : {region_sel}")
    st.stop()

# Informations sur la région sélectionnée
st.info(f"**{len(dff)} bibliothèques** dans la région **{region_sel}**")

# Création de la carte
lat_center = float(dff["Latitude"].median())
lon_center = float(dff["Longitude"].median())

# Calcul du zoom optimal basé sur l'étendue des coordonnées
lat_range = dff["Latitude"].max() - dff["Latitude"].min()
lon_range = dff["Longitude"].max() - dff["Longitude"].min()
max_range = max(lat_range, lon_range)

# Zoom adaptatif
if max_range > 5:
    zoom_level = 6
elif max_range > 2:
    zoom_level = 7
elif max_range > 1:
    zoom_level = 8
else:
    zoom_level = 9

# Création de la carte Folium
m = folium.Map(
    location=[lat_center, lon_center], 
    zoom_start=zoom_level, 
    tiles="OpenStreetMap"
)

# Ajout d'un cluster de marqueurs
cluster = MarkerCluster(
    name="Bibliothèques",
    overlay=True,
    control=True
).add_to(m)

# Détermination de la colonne pour les noms
name_col = None
for possible_col in ["code_bib", "nom", "Nom", "name", "Name", "Bibliothèque"]:
    if possible_col in dff.columns:
        name_col = possible_col
        break

# Ajout des marqueurs
for idx, row in dff.iterrows():
    # Création du popup avec les informations disponibles
    popup_info = []
    if name_col and pd.notna(row[name_col]):
        popup_info.append(f"<b>{row[name_col]}</b>")
    popup_info.append(f"Région: {row['Région']}")
    
    # Ajout d'autres informations si disponibles
    for col in ["Adresse", "adresse", "Ville", "ville", "Code_postal", "code_postal"]:
        if col in row.index and pd.notna(row[col]):
            popup_info.append(f"{col}: {row[col]}")
    
    popup_text = "<br>".join(popup_info) if popup_info else "Bibliothèque"
    
    folium.CircleMarker(
        location=[float(row["Latitude"]), float(row["Longitude"])],
        radius=4,
        color="blue",
        fill=True,
        fillColor="lightblue",
        fill_opacity=0.8,
        popup=folium.Popup(popup_text, max_width=300),
        tooltip="Cliquez pour plus d'infos"
    ).add_to(cluster)

# Affichage de la carte
st_folium(m, width=None, height=750, returned_objects=[])

# =======================
# Informations supplémentaires
# =======================
st.divider()
st.subheader("ℹ️ Informations sur les données")

col1, col2 = st.columns(2)
with col1:
    st.write("**Colonnes disponibles dans le dataset :**")
    for col in sorted(df.columns):
        st.write(f"• {col}")

with col2:
    st.write("**Statistiques générales :**")
    st.write(f"• Nombre total de lignes : {len(df):,}".replace(",", " "))
    st.write(f"• Nombre de régions : {nb_regions}")
    st.write(f"• Région avec le plus de bibliothèques : {counts.idxmax()} ({counts.max()})")
    st.write(f"• Région avec le moins de bibliothèques : {counts.idxmin()} ({counts.min()})")
