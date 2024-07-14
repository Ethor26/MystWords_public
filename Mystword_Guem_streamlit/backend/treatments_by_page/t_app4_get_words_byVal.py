from Mystword_Guem_streamlit.backend.global_refs.bdd_connexion_mariadb import *
from Mystword_Guem_streamlit.backend.global_refs.config_global_vars import *
from Mystword_Guem_streamlit.tools import *
def get_words_by_guemValue(val_to_search, term_mode, list_noterm_modes):
    sqlscript_find_words = f"""  SELECT DISTINCT W.WordText 
        FROM Word W LEFT JOIN ResultWord RW ON W.WordID=RW.WordID
            JOIN ResultModeLink RML on RW.ResultID = RML.ResultID
        WHERE Value={val_to_search} {f"and TerminalModeID={TERM_MODES_BDD[term_mode]}" if term_mode else ""} 
         """
    if list_noterm_modes:
        sql_script_modes = " and " + ' OR '.join(f"({NOTERM_MODES_BDD[list_noterm_modes[i]]} = ModeID AND OrderInSequence={i+2})" for i in range(len(list_noterm_modes)))
    else:
        sql_script_modes = f" and ModeID = {TERM_MODES_BDD[term_mode]} and OrderInSequence=1 "
    sqlscript_find_words += sql_script_modes + ";"
    print("sqlscript_find_words: ", sqlscript_find_words)
    args = prepDico_paramsQueries()
    res_words_by_val = execute_sql_queries(sqlscript_find_words, **args)
    list_words = list(map(lambda x: x[0], res_words_by_val[get_instr_key_result(1, 'SELECT')][Types_return_query.DATA.value])) if res_words_by_val[get_instr_key_result(1, 'SELECT')][Types_return_query.DATA.value] else []
    print("res_words_by_val: ", res_words_by_val, "\nlist_words: ", list_words)
    res_words_by_val_csv = creer_contenu_csv(words=list_words) if list_words else ""
    print("res_words_by_val_csv: ", res_words_by_val_csv)
    return res_words_by_val_csv