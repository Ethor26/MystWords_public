import json

from Mystword_Guem_streamlit.backend.global_refs.Gestion_WordWeight import WordsWithWeight
from Mystword_Guem_streamlit.backend.global_refs.bdd_connexion_mariadb import *
from Mystword_Guem_streamlit.backend.global_refs.config_global_vars import *
from Mystword_Guem_streamlit.tools import *

def get_guemValue_for_words(word_txt, words_csv, term_mode, list_noterm_modes):
    results = {}
    modeStart, submodesStart = get_argsModes_for_functGuem(term_mode, list_noterm_modes)
    print(f"----- Modes used: mode={modeStart}, sumodes={submodesStart}")
    if word_txt:
        sqlscript_calc_word = f""" SELECT CalculateGematria_funct(?,'{modeStart}','{','.join(submodesStart)}'); """
        args = prepDico_paramsQueries([(word_txt, )])
        print(sqlscript_calc_word)
        res_guem_from_word = execute_sql_queries(sqlscript_calc_word, **args)
        if res_guem_from_word["status"]:
            results[TEXT_INPUT_KEY] = res_guem_from_word[get_instr_key_result(1, 'SELECT')][Types_return_query.DATA.value][0][0] # WordsWithWeight(word_txt).getCalcGuem(modeStart, submodesStart)
        else: 
            results[TEXT_INPUT_KEY] = "Error in sql operations FOR word_txt"
        # print(results.get(TEXT_INPUT_KEY, None))
        # print("res_guem_from_word: ", res_guem_from_word['select_instr_1'][0][0])
    if words_csv:
        # A voir si on utilise un script qui vérifie d'abord si les mots existent
        sqlscript_calc_array = f"""     SELECT CalculateGematriaArray(
                   JSON_ARRAY({'?, '*(len(words_csv)-1) + "?"}),'{modeStart}','{','.join(submodesStart)}'
                   ); """
        args = prepDico_paramsQueries([tuple(words_csv)])
        res_guem_from_csv = execute_sql_queries(sqlscript_calc_array, **args)
        list_res = res_guem_from_csv[get_instr_key_result(1, 'SELECT')][Types_return_query.DATA.value][0][0].strip('[]').split(',')
        
        print(res_guem_from_csv, "\textracted: ", list_res, "\n", creer_contenu_csv(words= words_csv, guematria_results=list_res))
        # col_term_mode = [term_mode] * len(words_csv)
        col_list_modes = ['->'.join(list_noterm_modes) + f'->{term_mode}'] * len(words_csv)
        if res_guem_from_csv["status"]:
            results[FILE_INPUT_KEY] = creer_contenu_csv(words=words_csv, list_modes=col_list_modes, guematria_results=list_res)
        else:
            results[FILE_INPUT_KEY] = "Error in sql operations FOR word_csv"

        
    return results
        