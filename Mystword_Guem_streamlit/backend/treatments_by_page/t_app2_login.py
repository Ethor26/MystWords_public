def verifieAuthentification(loginUtilisateur, motDePasseUtilisateur):
    resultat = False

    # *********** SQL : REQUETE DE DONNEES ****************
    # Objecif : Données à récupérer : login et mdp des utilisateurs

    # *****************************************************
    if loginUtilisateur == "foo" and motDePasseUtilisateur == "bar":  # *** ATTENTION : Code fictif à remplacer
        resultat = True

    return resultat

def enregistreNouveauCompteUtilisateur(nom,prenom,mail, login, motdepasse):
    resultat = "KO"
    print ("PassavGen@tolls.enregistreNouveauCompteUtilisateur : Debut")
    print("PassavGen@tolls.enregistreNouveauCompteUtilisateur : parametre = " + nom +" / " + prenom + " / " + mail +" / " + login)
    #(on ne mets jamais un mot de passe ds les logs, ce n'est pas secure)

    # *********** SQL : REQUETE ET INSERTION DE DONNEES ****************
    # ETAPE 1 : Verifier dans la base de donnée que le login n'est pas déjà utilisé
    #
    # Si le login est utilisé  : resultat = "KO - le login existe déjà"
    # Si le login n'est pas utilisé => Etape 2
    
    # Etape 2 : INSERT des données de compte dans la base (nom + prenom ...)
    # Si reussi => resultat = "OK"

    # Cloture de la connexion à la bdd
    #
    # *****************************************************

    # A supprimer , OK pour le test
    resultat="OK"

    return resultat