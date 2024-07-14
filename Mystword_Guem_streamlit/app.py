# ========================================
# Page principale
# ========================================
from pagesApp import app1_ouverture, app2_login, app3p_calc_guem_for_words, app4p_found_word_by_guemNumber, app5p_AI_guem, app6_Informations, app99_deconnecter
import streamlit as st
import os

# Mise à jour du statut d'authentification en session
if 'login' not in st.session_state:
    st.session_state['login'] = '***'
    st.session_state['authentification'] = 'KO'
    st.session_state['resultat'] = '***'
    st.session_state['statutEnregistrementUtilisateur'] = '***'

# Déclaration des pagesApp pour le sidebar
PAGES_GESTION = {
    "OPENING": app1_ouverture,
    "AUTHENTICATION": app2_login,
    "ABOUT THIS SOFTWARE": app6_Informations,
    "FUNCTION: Calcul of guematria for words" : app3p_calc_guem_for_words,
    "FUNCTION: Find words by guematria value" : app4p_found_word_by_guemNumber,
    "FUNCTION: Metatron for guem" : app5p_AI_guem,
    "LOGOUT": app99_deconnecter
}
# TODO : CREER PAGE D'INFORMATION 

# Affichage de l'image dans la sidebar
from PIL import Image
image = Image.open(os.getcwd() + '\\Images\\logo_app_mystword_reduce.jpeg')
st.sidebar.image(image, caption='****')

# Affichage du titre
st.sidebar.title('Navigation')

# Affichage des radio button
selection = st.sidebar.radio("Go to", list(PAGES_GESTION.keys()))

# Ouverture de la page selectionnée dans les radio button
pages = PAGES_GESTION[selection]
pages.app()