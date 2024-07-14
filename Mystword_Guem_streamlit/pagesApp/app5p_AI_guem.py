import datetime
import io
import json
import os, streamlit as st
from PIL import Image

# import pandas as pd
# from io import StringIO
from Mystword_Guem_streamlit.backend.global_refs.config_global_vars import *
from Mystword_Guem_streamlit.backend.global_refs.HuggingChat_API import query_AI_contexted
from Mystword_Guem_streamlit.backend.treatments_by_page.t_app5_AI_guem import *
from Mystword_Guem_streamlit.tools import *

# Fonction pour récupérer les valeurs de login et d'authentification
def log_in():
    return st.session_state['login'], st.session_state['authentification']


# Fonction qui ajoute un élément à la fin d'une liste si le dernier élément est différent. Liste passée par référence
def add_to_list_if_different(lst, element):
    if lst and lst[-1] != element:
        lst.append(element)

# Fonction pour rafraîchir la discussion
def refresh_discussion(cont_chat):
    cont_chat.empty()
    for message in reversed(st.session_state.messages):
        if message != st.session_state["init_history_conv"][0]:
            with cont_chat.chat_message(message["role"]):
                st.markdown(message["content"])

# Fonction pour ajouter un message utilisateur et la réponse de l'IA à la liste des messages
def add_QA(cont_conv, prompt):
    with cont_conv.chat_message("user"):
        st.markdown(f":red[{prompt}]")
    st.session_state.messages.append({"role": "assistant", "content": query_AI_contexted(st.session_state.messages, prompt)})

# Fonction pour écouter les requêtes de l'utilisateur
def listen_to_prompts(cont_chat, cont_conv):
    request = cont_conv.chat_input("Entrez votre requête")
    if st.session_state.get("send_initial_prompt"): # Envoi du prompt paramétré modifié par l'utilisateur
        first_user_prompt = st.session_state["first_user_prompt"]
        if first_user_prompt:
            add_QA(cont_conv, first_user_prompt)
            st.session_state["send_initial_prompt"] = False
    elif prompt := request:
        add_QA(cont_conv, prompt)
    refresh_discussion(cont_chat)

# Fonction pour écouter le chargement du fichier texte
def listen_to_charge_txt_context(cont_init, cont_chat):
    file = cont_init.file_uploader("Choisissez un fichier texte", type="txt")
    file_str = read_uploadfile(file, "string")
    init_conv_history_notUsed, first_user_prompt = init_conv_Metatron(file_str)

    # Permettre à l'utilisateur de modifier le premier prompt
    user_prompt = cont_init.text_area("Modifiez le premier prompt si nécessaire :", first_user_prompt)
    # Stocker le premier prompt dans la session
    st.session_state["first_user_prompt"] = user_prompt

    # Ajouter un bouton pour envoyer le premier prompt modifié
    if cont_init.button("Envoyer le prompt initial"):
        st.session_state["send_initial_prompt"] = True


def listen_to_save_conv(container):
    discussion_name = container.text_input("Nom de sauvegarde de la discussion")
    if discussion_name:
        # A ajuster pour les datas
        dict_var_session = session_state_to_dict(st.session_state)
        # sélection des keys login et messages à envoyer
        data_sended = {k: v for k, v in dict_var_session.items() if k in ["login", "messages"]}
        data_sended["messages"] = data_sended["messages"][1:]
        json_data = json.dumps(data_sended, ensure_ascii=False, indent=4)
        buffer = io.BytesIO()
        buffer.write(json_data.encode('utf-8'))
        buffer.seek(0)
        container.download_button(
            label="Sauvegarder en tant que JSON",
            data=buffer,
            file_name=discussion_name + ".json",
            mime="application/json"
        )


@st.cache_resource
def init_cache():
    #Initialisation graphique
    st.title("Dialog with Metatron")
    image = Image.open(os.path.join(os.path.abspath(__file__), '..', '..', 'Images', 'img_metatron_ai.jpeg'))
    st.image(image, caption='A representation of Metatron')


def init():
    init_conv_history = init_conv_Metatron("")[0]
    st.session_state["init_history_conv"] = init_conv_history
    #Initialisation de la mémoire des messages si elle n'existe pas déjà
    if "messages" not in st.session_state:
        # st.session_state["messages"] = []
        st.session_state["messages"] = init_conv_history

    # Initialiser l'état d'envoi du premier prompt
    if "send_initial_prompt" not in st.session_state:
        st.session_state["send_initial_prompt"] = False


def app():
    # En premier lieu, on récupère les données de session
    val_login, val_authent = log_in()

    if val_authent == 'OK':  #Si l'auth est correct, alors
        init_cache()
        init()
        container_init = st.container(border=True)
        container_conv = st.container(border=True)
        container_chat = st.container(border=True)

        listen_to_charge_txt_context(container_init, container_chat)
        new_chat_button = container_conv.button("New Chat")

        listen_to_save_conv(container_conv)
        listen_to_prompts(container_chat, container_conv)

        if new_chat_button:
            container_chat.empty()
            st.session_state["messages"] = [i for i in st.session_state["init_history_conv"]]

    else:
        st.warning("veuillez vous identifier")
