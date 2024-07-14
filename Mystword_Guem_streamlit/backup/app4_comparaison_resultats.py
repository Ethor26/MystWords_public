import streamlit as st
from Bio.pairwise2 import format_alignment

from Principal_Streamlit_new.tools import enregistrerNouvelleActiviteEtResultat
from Principal_Streamlit_new.traitements.Comparaison_traitements import Comparaison_traits


def app(ListRes,nomActivite):
    val_login = st.session_state['login']
    val_authent = st.session_state['authentification']
    val_projetEnCour = st.session_state['referenceProjetEnCours']

    if val_authent == 'OK':
        print('@app4_comparaison_resultats = '+val_login + " est connecté")
        resultat = ListRes # ListRes = Comparaison_resultats()

        # Container résultat
        containerResultat = st.container()

        # Titre(s)
        containerResultat.title('COMPARAISON_RESULTATS')

        # Résultats
        # print("Liste des résultats", ListRes)
        for Res_algo in ListRes:
            print("--------------------------")
            nomAlgo = str(Res_algo[0])
            containerResultat.write("Résultats de l'algorithme: " + nomAlgo)

            if nomAlgo == "BioPython_PairwiseAligner":
                containerResultat.code("Algorithme utilisé : "+ str(Res_algo[2][0][2]))  # A remplacer par i
                print("Algorithme utilisé : "+ Res_algo[2][0][2])
                containerResultat.code("Score :"+ str(Res_algo[2][0][1])) # 1er 0 à remplacer par i
                print("Score :"+ str(Res_algo[2][0][1]))
                containerResultat.code("premier alignement obtenu \n"+ str(Res_algo[2][0][0][0])) # 1er 0 à remplacer par i
                # TELECHARGEMENT
                containerResultat.download_button("Telecharger le fichier de comparaison Fasta : " + nomAlgo,
                                                  Res_algo[1],
                                                  "Comp_" + nomAlgo + ".sam")

            elif nomAlgo == "BioPython_Pairwise2":
                containerResultat.code("Score :" + str(Res_algo[2][0][1]))
                containerResultat.code("premier alignement obtenu avec la première séquence : \n" + format_alignment(*Res_algo[2][0][0][0]))
                # TELECHARGEMENT
                containerResultat.download_button("Telecharger le fichier de comparaison Fasta : " + nomAlgo,
                                                  Res_algo[1],
                                                  "Comp_" + nomAlgo + ".fasta")
                # 2 pour le retour des appels de l'algo principal, 0 pour le numéro de la séquence comparée,
                # 0 pour les alignements dans le tuple de résultat de l'algo principal, 0 pour le 1er alignement


            elif nomAlgo == "Smith-Waterman" or nomAlgo == "Needleman-Wunsch":
                containerResultat.code("Score :" + str(Res_algo[2][0][1]))
                containerResultat.code("premier alignement obtenu :\n" + str(Res_algo[2][0][0]))  # Ajouter un 0 pour plusieurs séquences
                # TELECHARGEMENT
                containerResultat.download_button("Telecharger le fichier de comparaison Fasta : " + nomAlgo,
                                                  Res_algo[1],
                                                  "Comp_" + nomAlgo + ".fasta")

            elif nomAlgo == "BLAST":  # A retester
                containerResultat.code("Alignements de BLAST : \n")
                E_VALUE_THRESH = 0.04
                if Res_algo[2].alignements != []:  # = Blast_record.alignments
                    for alignment in Res_algo[2].alignments:  # .alignments si read
                        print("alignement", alignment)
                        for hsp in alignment.hsps:
                            print("hsp", hsp, "de l'alignement", alignment)
                            if hsp.expect < E_VALUE_THRESH:
                                containerResultat.code("****Alignment****")
                                containerResultat.code("sequence:", alignment.title)
                                containerResultat.code("length:", alignment.length)
                                containerResultat.code("e value:", hsp.expect)
                                containerResultat.code(hsp.query_AI[0:75] + "...")
                                containerResultat.code(hsp.match[0:75] + "...")
                                containerResultat.code(hsp.sbjct[0:75] + "...")

                                print("****Alignment****")
                                print("sequence:", alignment.title)
                                print("length:", alignment.length)
                                print("e value:", hsp.expect)
                                print(hsp.query_AI[0:75] + "...")
                                print(hsp.match[0:75] + "...")
                                print(hsp.sbjct[0:75] + "...")
                else:
                    print("Pas d'alignements récupérés")
                    containerResultat.code("Pas d'alignements récupérés")

                containerResultat.download_button("Telecharger le fichier de comparaison XML : " + nomAlgo,
                                                  Res_algo[1],
                                                  "Comp_" + nomAlgo + ".fasta")
                # print("Télécharger le fichier XML. Designation: " + str(Res_algo[1]))
                # containerResultat.code("Télécharger le fichier XML. Designation: " + str(Res_algo[1]))

        # TELECHARGEMENT
        # st.download_button("Telecharger", data=csv, mime=None)  # FASTA

        # Enregistrement en base des résultats et de l'activité dans le projet
        statutEnregistrement = enregistrerNouvelleActiviteEtResultat(val_login, val_projetEnCour, resultat, nomActivite)
        if statutEnregistrement:
            containerResultat.success('Enregistrement en base de données  = Réussi')
        else:
            containerResultat.warning('Enregistrement en base de données  = Echec')

    else:
        st.warning("veuillez vous identifier")