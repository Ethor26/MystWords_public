import pandas as pd
import streamlit as st

# import pandas as pd
# from io import StringIO

from Mystword_Guem_streamlit.pagesApp import app3r_calc_guem_for_words, app4r_found_word_by_guem
from Mystword_Guem_streamlit.backend.global_refs.config_global_vars import *
from Mystword_Guem_streamlit.backend.treatments_by_page.t_app4_get_words_byVal import *
from Mystword_Guem_streamlit.tools import AjoutParam, TERM_MODES_BDD, NOTERM_MODES_BDD


def app():
    st.title("FOUND WORD BY GUEM NUMBER")
    # Recuperation des données en session
    val_login = st.session_state['login']
    val_authent = st.session_state['authentification']

    if val_authent == 'OK':  # Vérification du statut d'authentification
        # Affichage : creation du container de widget
        containerParametre = st.expander('PARAMETRE DE LANCEMENT DU TRAITEMENT')

        # ***  Code Ethan de traitement de la comparaison ___________________________
        # Ouverture de la base :a placer

        # ===========================================================================
        # VARIABLES POUR PARAMETRES

        # Liste des paramètres à envoyer
        params = {}

        # Liste des contraintes : liste de booléens
        List_param_oblig = []
        Nb_param_oblig = 0
        textPrinted_defaultVal = "-- Default value: "

        # ===========================================================================
        # PARAMETRE OBLIGATOIRE : Mot à calculer, saisie ou fichier obligatoire
        params[TEXT_INPUT_KEY] = AjoutParam(List_param_oblig,
                                            containerParametre.number_input("Guematria value to find words", min_value=0, step=1,
                                                                          help="get words with value equal to this"), default=False)

        # Marque l'obligation
        Nb_param_oblig += 1

        container_param_Modes = st.expander("Modes used for guematria calcul")
        # ===========================================================================
        # PARAMETRES OBLIGATOIRES : Modes terminaux
        params[TERMINAL_MODE_KEY] = AjoutParam(List_param_oblig,
                                               container_param_Modes.radio("Selectionnez le mode terminal: ", list(TERM_MODES_BDD.keys()),
                                                                           help="The terminal mode return value from word. \n" + textPrinted_defaultVal + 'RAGIL'), default=True, defaultValue='RAGIL')

        # ===========================================================================
        # PARAMETRES OBLIGATOIRES : Modes non terminaux

        names_modes_noterm = ["Mode " + str(i + 1) for i in range(1)]# range(MAX_RECURSION_DEPTH)]
        params[NOTERM_MODES_KEY] = [container_param_Modes.selectbox(mode_noterm, [None] + list(NOTERM_MODES_BDD.keys()), help=textPrinted_defaultVal + str(None)) for mode_noterm in names_modes_noterm]
        params[NOTERM_MODES_KEY] = [p for p in params[NOTERM_MODES_KEY] if p is not None]
        print("List_params", params)

        # BOUTON DU LANCEMENT DE COMPARAISON -> Appel de la fonction
        compar_button = containerParametre.button("Calcul de guematria")

        if (compar_button) and Nb_param_oblig <= len(List_param_oblig):
            print("Passé_compar. obligation =", Nb_param_oblig == len(List_param_oblig), "\n")

            # FONCTION DE CALCUL A LANCER
            results = get_words_by_guemValue(params[TEXT_INPUT_KEY], params[TERMINAL_MODE_KEY], params[NOTERM_MODES_KEY]) # {"No result for the moment": None}

            # affichage des resultats
            app4r_found_word_by_guem.app(results)

        # else:
        print("Paramètres obligatoire restants :" + str(Nb_param_oblig - len(List_param_oblig)),
              ", compar_button = ", compar_button)
        containerParametre.code("Paramètres obligatoire restants :" + str(Nb_param_oblig - len(List_param_oblig)) +
                                ", compar_button = " + str(compar_button))
        # fin de traitement des parametres ______________________________________________

    else:
        st.warning("veuillez vous identifier")