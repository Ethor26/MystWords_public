import streamlit as st
import pandas as pd

from io import StringIO
from Mystword_Guem_streamlit import tools
'''
from Principal_Streamlit_new.pagesApp import app4_comparaison_resultats
from Principal_Streamlit_new.pagesApp.app99_choix_projet_activte_parametres import afficheChoixProjetEtActivite
from Principal_Streamlit_new.tools import AjoutParamSpecif, AjoutParam, read_uploadfile, Seqs_to_binary, \
    Convert_seq_to_str
from Principal_Streamlit_new.traitements.Comparaison_traitements import Comparaison_traits
'''
from Mystword_Guem_streamlit.tools import AjoutParamSpecif, AjoutParam, read_uploadfile #, Seqs_to_binary, Convert_seq_to_str

def app():
    # Recuperation des données en session
    val_login = st.session_state['login']
    val_authent = st.session_state['authentification']

    if val_authent == 'OK':  # Vérification du statut d'authentification


            # Affichage : creation du container de widget
            containerParametre = st.expander('PARAMETRE DE LANCEMENT DU TRAITEMENT')

            # ***  Code Ethan de traitement de la comparaison ___________________________
            # Ouverture de la base :a placer



            # Liste des paramètres à envoyer


            # ===========================================================================
            # PARAMETRES GENERAUX (entrées de séquences)

            # Liste des contraintes : liste de booléens
            List_param_oblig = []
            Nb_param_oblig = 0

            # Séquence d'intérêt : saisie obligatoire

            # UPLOADER LA SEQUENCE
            sequence_file_int = AjoutParam(List_param_oblig,
                                           containerParametre.file_uploader(
                                                    "Charger les mots à calculer",
                                                    type=["csv"],
                                                    accept_multiple_files=False,
                                                    help="Charger les mots à calculer : obligatoire"))
            # Record_file_seq_int = StringIO(sequence_file_int.getvalue().decode("utf-8"))

            # Marque l'obligation
            Nb_param_oblig += 1

            # [FASTA, FASTQ]
            # LECTURE ET AFFICHAGE DU FICHIER FASTA DANS UN SLIDER
            # st.slider(sequence_file, min_value=1, value=30, max_value=30, )
            # with open(sequence_file) as fasta_file:  # JE NE SAIS PAS SI ON PEUT FAIRE CA
            # for record in SeqIO.parse(fasta_file, "fasta"):
            # print(record.id)
            # print(str(record.seq)[:30])

            # Séquence comparées : saisie obligatoire d'au moins 1, plusieurs possibles
            sequences_file_comp = AjoutParam(List_param_oblig, containerParametre.file_uploader("Charger les séquences à comparer", type=["faa", "fasta", "fas"],
                                                                                                accept_multiple_files=False,  # True serait meilleur mais non programmé
                                                                                                help="Ajoutez les séquences comparées : obligatoire sauf pour BLAST"))
            # Record_file_seqs_comp = StringIO(sequences_file_comp.getvalue().decode("utf-8"))

            # Marque l'obligation
            Nb_param_oblig += 1

            # Algos de comparaison : saisie obligatoire d'au moins 1, plusieurs possibles
            ListAlgoComp = []

            # ===========================================================================
            # PARAMETRES SPECIFIQUES pour chaque algos

            # CONTAINERS DES ALGORITHMES : ceux choisis auront leur paramètres spécifiques entrés
            container_algorithme = st.expander("Choisir l'algorithme")
            choix_PairwiseAligner = container_algorithme.checkbox("BioPython_PairwiseAligner")
            choix_Pairwise2 = container_algorithme.checkbox("BioPython_Pairwise2")
            choix_SW = container_algorithme.checkbox("Smith-Waterman")
            choix_NW = container_algorithme.checkbox("Needleman-Wunsch")
            choix_BLAST = container_algorithme.checkbox("BLAST")

            # -------------------------------------------
            # Algorithme : BioPython_PairwiseAligner
            # Paramètres de BioBython_PairwiseAligner
            ListArgs_PairwiseAligner = []
            if choix_PairwiseAligner:
                print("Paramètres de BioPython_PairwiseAligner")
                container_param_PairwiseAligner = st.expander("Paramètres de BioPython_PairwiseAligner")

                AjoutParamSpecif(ListArgs_PairwiseAligner, "global",
                                 container_param_PairwiseAligner.radio("Selectionnez le mode d'alignement: ", ['global', 'local'],
                                                                            help="valeur par défaut : global"))
                #  ListArgs_PairwiseAligner[0] : mode = {str} 'global'
                # Expression à modifier pour n'avoir que deux choix possibles ("global" ou "local")

                AjoutParamSpecif(ListArgs_PairwiseAligner, 0.0,
                                 container_param_PairwiseAligner.number_input("end_extend_gap_score",help="valeur par défaut : 0.0"))
                #  ListArgs_PairwiseAligner[1] : end_extend_gap_score = {float} 0.0

                
                AjoutParamSpecif(ListArgs_PairwiseAligner, None,
                                 container_param_PairwiseAligner.file_uploader("Charger la matrice", type=["list"],
                                                                               accept_multiple_files=False,
                                                                               help="valeur par défaut: None"))
                # substitution_matrix = {NoneType} None

                AjoutParamSpecif(ListArgs_PairwiseAligner, None,
                                 container_param_PairwiseAligner.text_input("wildcard_PairwiseAligner",
                                                                            help="valeur par défaut : None"))
                #  wildcard = {NoneType} None

                ListAlgoComp.append("BioPython_PairwiseAligner")
                print("ListAlgocomp: ", ListAlgoComp)
                # Autres actions ?
            else:
                if "BioPython_PairwiseAligner" in ListAlgoComp:
                    ListAlgoComp.remove("BioPython_PairwiseAligner")
                print("ListAlgocomp: ", ListAlgoComp)

            # Marque l'obligation
            Nb_param_oblig += 1
            if ListAlgoComp:
                List_param_oblig.append(True)

            # Liste des Tulpes de paramètres spécifiques
            List_Args_algos = [ListArgs_PairwiseAligner]
            print("List_Args_algos", List_Args_algos)

            nom_activite=containerParametre.text_input("Description de l'activité")
            # BOUTON DU LANCEMENT DE COMPARAISON -> Appel de la fonction
            compar_button = containerParametre.button("Comparer")

            if (compar_button) and Nb_param_oblig <= len(List_param_oblig):
                print("Passé_compar. obligation =", Nb_param_oblig == len(List_param_oblig), "\n")

                ListRes = Comparaison_traits(ListAlgoComp, sequence_file_int, sequences_file_comp, List_Args_algos)

                # affichage des resultats
                app4_comparaison_resultats.app(ListRes, nom_activite)

            else:
                print("Paramètres obligatoire restants :" + str(Nb_param_oblig - len(List_param_oblig)),
                      ", compar_button = ", compar_button)
                containerParametre.code("Paramètres obligatoire restants :" + str(Nb_param_oblig - len(List_param_oblig)) +
                      ", compar_button = " + str(compar_button))
            # fin de traitement des parametres ______________________________________________

    else:
        st.warning("veuillez vous identifier")
