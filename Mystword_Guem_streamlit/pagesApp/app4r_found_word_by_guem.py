import streamlit as st

from Mystword_Guem_streamlit.backend.treatments_by_page.t_app3_calc_guem import TEXT_INPUT_KEY, FILE_INPUT_KEY


def app(result_csv):
    val_login = st.session_state['login']
    val_authent = st.session_state['authentification']

    if val_authent == 'OK':
        print('@app4r_found_word_by_guem = '+val_login + " is connected")
        # Container résultat
        containerResultat = st.container()

        # Titre(s)
        print("==============================\nWORDS FIND BY NUMBER")
        containerResultat.title('WORDS FIND BY NUMBER')
        # TELECHARGEMENT
        if result_csv:
            containerResultat.download_button("Download the file of results. FORMAT: txt ",
                                              result_csv.encode('utf-8'),
                                              "results_founded_words.txt",
                                              help= "Download the .csv with the results of the guematria calcul",
                                              mime='text/plain')
            #  Fonctionne mais infos mal encodé et non retrouvable facilement
            # TODO: donner xlsx (pour le moment txt)
            
            # TODO : Problème bdd qui a mot avec latin : FAIRE UNE REFONTE
            # WHERE wordText REGEXP '[a-zA-Z]+'
            
            print("Res with the file included")
        else:
            st.write("No results for this research")
            print("Res with an empty file included")
        print("==============================")

    else:
        st.warning("veuillez vous identifier")