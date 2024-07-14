import streamlit as st

def app():
    #if 'login' in st.session_state:
    val_login = st.session_state['login']
    val_authent = st.session_state['authentification']

    if val_login =='***'and val_authent=='KO':
        st.caption("vous n'etes pas connecte")

    else:
        # initialisation des données stockées en session. On garde les compartiments
        st.session_state['login'] = '***'
        st.session_state['authentification'] = 'KO'
        st.session_state['referenceProjetEnCours']='***'

        # Affichage du message deconnection
        st.caption("au revoir")
