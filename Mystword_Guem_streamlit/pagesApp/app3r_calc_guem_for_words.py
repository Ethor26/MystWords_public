import streamlit as st

from Mystword_Guem_streamlit.backend.treatments_by_page.t_app3_calc_guem import TEXT_INPUT_KEY, FILE_INPUT_KEY


def app(results):
    val_login = st.session_state['login']
    val_authent = st.session_state['authentification']

    if val_authent == 'OK':
        print('@app3r_calc_guem_for_words_resultats = '+val_login + " is connected")
        # Container résultat
        containerResultat = st.container()

        # Titre(s)
        print("==============================\nRESULTS OF GUEMATRIA CALCULUS")
        containerResultat.title('RESULTS OF GUEMATRIA CALCULUS')
        # Résultats saisis # A tester: בין
        if (results.get(TEXT_INPUT_KEY, None) is not None) or results.get(TEXT_INPUT_KEY, None) == 0:
            containerResultat.code("Result of the writed word: " + str(results[TEXT_INPUT_KEY]))
            print(f"Res {TEXT_INPUT_KEY}: {results[TEXT_INPUT_KEY]}")
        # TELECHARGEMENT
        if results.get(FILE_INPUT_KEY, None):
            containerResultat.download_button("Download the file of results. FORMAT: txt ",
                                              results[FILE_INPUT_KEY].encode('utf-8'),
                                              "results_calc_guem.txt", help= "Download the .csv with the results of the guematria calcul",mime='text/plain')
            #  Fonctionne mais infos mal encodé et non retrouvable facilement
            # TODO: améliorer encodage du csv ou donner xlsx (pour le moment txt)
            print("Res with the file included")
        print("==============================")

    else:
        st.warning("veuillez vous identifier")