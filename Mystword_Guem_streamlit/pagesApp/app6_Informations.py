import streamlit as st
def app():
    val_login = st.session_state['login']
    val_authent = st.session_state['authentification']

    st.title("INFORMATIONS ABOUT THIS SOFTWARE")
    st.write('Informations')
    st.caption('info authentification : login = ' + val_login + ' / authentification = ' + val_authent)

    Container_Contexte = st.container()
    Container_Contexte.title("A propos de ce logiciel: \n")
    Container_Contexte.write("Pendant des millénaires, les grands érudits de la Kabbale ont retournés la torah dans tous les sens, "
                             "et passés des heures à faire divers calculs de guematria pour trouver des liens logiques.\n"
                             "Ces calculs doivent en effet être exécutés sur un grand nombre de mots, avec plusieurs méthodes de calculs complexes. "
                             "Le temps nécessaire à trouver des mots de valeurs lié est lui aussi infini. \n"
                             "Ainsi, ce logiciel ambitionne de répondre à ces problèmes en diminuant ces temps de calculs et de comparaison de JOURS ENTIERS à QUELQUES SECONDES. "
                             "Les démarches d'études de la guématria seront donc drastiquement accélérées")

    Container_But = st.container()
    Container_But.title("But de ce logiciel: \n")
    Container_But.write("- Permettre le calcul de mots rapidement même avec des méthodes complexes\n"
                        "- Retrouver les mots à valeurs de guématria identiques ou similaires\n"
                        "- Utiliser l'IA pour trouver des liens cachés\n")