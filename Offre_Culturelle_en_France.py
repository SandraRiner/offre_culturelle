import streamlit as st
# st.header('Page accueil')
# st.write('test')

# ------------------------------------
# Configuration de la page
# ------------------------------------
st.set_page_config(
    page_title="Offre Culturelle en France",
    page_icon="🏤",
    layout="wide"
)

# ------------------------------------
# Titre principal
# ------------------------------------
st.markdown(
    """
    <h1 style="text-align:center; margin-bottom: 0.3rem;">🎦💃L'offre Culturelle en France 🏛️📊</h1>
    <p style="text-align:center; font-size:1.5rem; color:#FF0066">
        Aïda Tabiou <br>Karima Hallou<br>Nezha Lafhal<br>Sandra Riner</br>
    </p>
    """,
    unsafe_allow_html=True
)
