import os

def init_conv_Metatron(WordsAndVal_txt):
    with open(os.path.join(os.path.abspath(__file__), '..', '..', 'Scripts_txt', 'Instruction_Metatron.txt'), 'r') as file:
        script_Metatron = file.read()
    with open(os.path.join(os.path.abspath(__file__), '..', '..', 'Scripts_txt', 'Prompt_initial_AI_concis.txt'), 'r') as file: # Prompt_initial_AI.txt
        first_userprompt = file.read()

    if WordsAndVal_txt is not None and isinstance(WordsAndVal_txt, str):
        first_userprompt = first_userprompt.replace("<contenu_csv>", WordsAndVal_txt)
    init_conv_history = [
        {"role": "user", "content": script_Metatron},
        {"role": "assistant", "content": "Je suis Metatron. Quelle est ta requête, humain ?"},
    ]
    return init_conv_history, first_userprompt

if __name__ == '__main__':
    print(init_conv_Metatron(""" Row_num;words;list_modes;guematria_results
1;הם;MILOUYI->HAKADMI->RAGIL;306
2;רק;MILOUYI->HAKADMI->RAGIL;2966 """)) # test