import re

import streamlit.runtime.uploaded_file_manager as st_uploaded_file_manager
import pandas as pd
from Mystword_Guem_streamlit.backend.global_refs.bdd_connexion_mariadb import *
from io import StringIO
# from Bio import SeqIO

def session_state_to_dict(session_state):
    return {k: v for k, v in session_state.items()}

def load_session_state_from_dict(session_state, data_dict):
    for key, value in data_dict.items():
        session_state[key] = value

def read_uploadfile(uploaded_file, mode):
    if uploaded_file is not None:
        # To read file as bytes:
        if mode == "bytes":
            return uploaded_file.getvalue()

        # To convert to a string based IO:
        if mode == "StringIO":
            return StringIO(uploaded_file.getvalue().decode("utf-8"))

        # To read file as string:
        if mode == "string":
            return StringIO(uploaded_file.getvalue().decode("utf-8")).read()

        # Can be used wherever a "file-like" object is accepted:
        if mode == "dataframe":
            return pd.read_csv(uploaded_file)
        
        if mode == 'csv':
            return re.findall(r'\b\w+\b', StringIO(uploaded_file.getvalue().decode("utf-8")).read())

def creer_contenu_csv(create_file=False, **args):
    '''
    contenu_csv = ["Row_num;" + ";".join(args.keys())]   # En-tête du CSV
    listes = list(args.values())
    # Parcourir les listes et les combiner dans le contenu CSV
    # Générer les lignes du CSV en utilisant zip_longest et la compréhension des listes
    contenu_csv += [f"{i};{';'.join(str(val) for val in values)}" for i, values in enumerate(zip_longest(*listes, fillvalue=""), start=1)]
    contenu_csv_str = "\n".join(contenu_csv)  # En-tête du CSV
    '''
    # Créer un DataFrame Pandas à partir des données
    df = pd.DataFrame(args)
    # Créer un DataFrame avec la colonne "Row_num"
    row_num_df = pd.DataFrame({"Row_num": range(1, len(df) + 1)})
    # Concaténer les deux DataFrames
    df = pd.concat([row_num_df, df], axis=1)
    # Générer le contenu CSV à partir du DataFrame
    contenu_csv_str = df.to_csv(index=False, sep=";")
    # print("contenu_csv_str: ", contenu_csv_str)
    if create_file: # Écriture du contenu dans un fichier CSV
        with open("output.csv", "w", newline="") as csvfile:
            csvfile.write(contenu_csv_str)
    return contenu_csv_str

def get_calc_modes():
    sqlscript_calc_array = f""" SELECT ModeID, ModeName FROM Mode WHERE IsTerminal=False;
    SELECT ModeID, ModeName FROM Mode WHERE IsTerminal=TRUE; -- GROUP_CONCAT(ModeName SEPARATOR ',')
                   """
    args = prepDico_paramsQueries()
    res_get_modes = execute_sql_queries(sqlscript_calc_array, **args)
    no_term_modes, term_modes = ({}, {}) if not res_get_modes[Types_return_query.STATUS.value] else ({ids_mode[1]: ids_mode[0] for ids_mode in res_get_modes[get_instr_key_result(1, 'SELECT')][Types_return_query.DATA.value]}, {f"{ids_mode[1]}": ids_mode[0] for ids_mode in res_get_modes[get_instr_key_result(2, 'SELECT')][Types_return_query.DATA.value]})
    # list(map(lambda x: x[0], res_get_modes['select_instr_1'])), list(map(lambda x: x[0], res_get_modes['select_instr_2']))
    # print(res_get_modes, no_term_modes, term_modes)
    return term_modes, no_term_modes
TERM_MODES_BDD, NOTERM_MODES_BDD = get_calc_modes()

def get_argsModes_for_functGuem(term_mode, list_noterm_modes):
    if len(list_noterm_modes) >= 1:
        return list_noterm_modes[0], (list_noterm_modes[1:] if len(list_noterm_modes) >= 2 else []) + [term_mode]
    return term_mode, []
# -------------------------------------------------------------------------------
# Ajouter des paramètres obligatoire (surtout fichier)
def AjoutParam(List_Oblig, Express_Streamlit, default=False, defaultValue=None):
    print("@tools.AjoutParam() : debut")
    # Demande de saisie graphique, sinon ici valeur par défaut
    ValeurSaisie = Express_Streamlit
    if ValeurSaisie:  # Valable pour autre que file_ploader ???
        if type(ValeurSaisie) == st_uploaded_file_manager.UploadedFile:  # Si la valeur obligatoire est un fichier
            ValeurSaisie = read_uploadfile(ValeurSaisie, "csv")

        # Marque l'obligation
        print("@tools.AjoutParam() : Passage Saisie avec :", ValeurSaisie)
        if not default: 
            List_Oblig.append(True)
    elif default:
        return defaultValue
    print("@tools.AjoutParam() : fin")
    return ValeurSaisie
    # Pas d'ajout en base ici

'''
def getListSeqRecord_fromFileFASTA(myFileIO):
    List_seq_record = []
    if myFileIO:
        for seqRecord in SeqIO.parse(myFileIO, 'csv'): # fasta
            List_seq_record.append(seqRecord)
    else:
        print("@tools.getListSeqRecord_fromFileFASTA : Fichier null")
    return List_seq_record
'''
