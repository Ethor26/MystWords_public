import streamlit as st

from Mystword_Guem_streamlit.backend.treatments_by_page.t_app2_login import verifieAuthentification, enregistreNouveauCompteUtilisateur


def app():

    # Affichage des champs de saisie
    st.title('AUTHENTIFICATION')

    saisieLogin = st.text_input('Saisir login', 'foo')
    saisiePassword = st.text_input('Saisir mot de passe', 'bar',type='password')
    bt_VerifierAuthentification = st.button("valider")

    if bt_VerifierAuthentification:
        # initialisation statut enregistrement au cas ou
        st.session_state['statutEnregistrementUtilisateur']='***'

        if verifieAuthentification(saisieLogin,saisiePassword): # on appel la fonction pour valider l'authentification
            # on efface la saisie d'un nouvel utilisateur

            # Important : passage en session du login et du statut d'authentification
            st.session_state['login'] = saisieLogin.title()
            st.session_state['authentification']='OK'

            # affichage du statut d'authentification
            st.success("Authentification réussie, bonjour " + st.session_state['login'])

        else:
            # affichage du statut d'authentification
            st.warning("Authentification échouée     (*** phase de test *** : saisir foo/bar pour s'authentifier)")


    # Container de saisie d'un nouvel utilisateur
    containerSaisieNouveauUsr = st.expander('Creer un nouveau compte utilisateur')
    containerSaisieNouveauUsr.title("Création d'un nouveau compte utilisateur")


    # Champs de saisie
    en_nom=containerSaisieNouveauUsr.text_input("votre nom", key="en_nom")
    en_prenom=containerSaisieNouveauUsr.text_input("votre prenom",key="en_prenom")
    en_mail=containerSaisieNouveauUsr.text_input("votre email",key="en_mail")
    en_login=containerSaisieNouveauUsr.text_input("votre pseudo",key="en_login")
    en_motDePasse=containerSaisieNouveauUsr.text_input("votre mot de passe",type='password', key="en_motDePasse")
    en_motDepasseCtr=containerSaisieNouveauUsr.text_input("Resaisir votre mot de passe",type='password', key="en_motDepasseCtr")
    bt_EnregistrerUtilisateur=containerSaisieNouveauUsr.button("Enregistrer")


    # Action si clic sur bouton "Enregistrer nouveau compte U"
    if bt_EnregistrerUtilisateur:
        print("PassavGen@app2_login.bt_EnregistrerNouvelUtilisateur : Enregistrement d'un nouvel utilisateur")
        controleDelaSaisie ="OK"
        statutEnregistrement="***"

        # Controle de la complétude des champs de saisie
        if len(en_nom)==0 \
                or len(en_login)==0 \
                or len(en_mail)==0 \
                or len(en_prenom)==0 \
                or len(en_motDePasse)==0 \
                or en_motDepasseCtr==0:

            print("PassavGen@app2_login.bt_EnregistrerNouvelUtilisateur : Certains champs de saisie sont vides")
            containerSaisieNouveauUsr.warning("Tous les champs doivent être saisis")
            controleDelaSaisie ="KO"

        # Contrôle de la cohérence de saisie des mots de passes
        if en_motDePasse!=en_motDepasseCtr:
            notification ="Les mots de passes sont différents"
            print("PassavGen@app2_login.bt_EnregistrerNouvelUtilisateur : " + notification)
            containerSaisieNouveauUsr.warning(notification)
            controleDelaSaisie = "KO"



        if controleDelaSaisie =="OK":
            print("Enregistrement d'un nouveau compte utilisateur : Debut")
            statutEnregistrement = enregistreNouveauCompteUtilisateur(en_nom, en_prenom, en_mail, en_login, en_motDePasse)


        # Si enregistrement a échoué, affiche pourquoi
        if statutEnregistrement.startswith("KO"):
            notification="L'enregistrement a échoué  motif = " + statutEnregistrement
            print("PassavGen@app2_login.bt_EnregistrerNouvelUtilisateur :" + notification)
            containerSaisieNouveauUsr.warning(notification )

        # Si enregistrement réussi,
        if statutEnregistrement == "OK":
            notification = "L'enregistrement a réussi : " + statutEnregistrement
            print("PassavGen@app2_login.bt_EnregistrerNouvelUtilisateur :" + notification)
            st.success("Enregistrement réussi. Vous pouver vous authentifier")
