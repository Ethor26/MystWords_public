# Projet Mystwords

## WARNING : description imcomplète, en cours de rédaction

## Description
Ce repository contient tout ce qui concerne les produits informatiques pour l'étude de la mystique Juive


## Installation
Pour installer le projet, il faut:
- cloner le repository
- lancer setup.py pour installer les dépendances du requirements.txt. Si problème pour certains packages, les installer manuellement à la dernière version.

## Test-Mystwords
Dans le dossier "Mystwords_Guem_streamlit":
- lancer le "run_main.py"
- ouvrir un navigateur et aller sur "http://localhost:8501"
- pour tester les fonctions: utiliser le csv "results_calc_guem" dans le dossier "tests"

## Architecture
Le dossier "Mystword_Guem_streamlit" contient l'application streamlit de Mystwords.
Il est structuré de cette manière:
- backend: contient les fichiers python pour le traitement des données. Ce dossier est lui-même subdivisé en deux dossiers:
  - global_refs: appels de services comme des API, ou fonctions/variables globales
  - treatments_by_page: le code précisément utilisé pour traiter les demandes de chaque page streamlit. Si nécessaire, on devra ajouter un fichier pour notre fonction d'IA
- Images: stocke les images (inutile pour toi)
- pagesApp: contient les fichiers python pour chaque page de l'application streamlit: Dans ton cas, tu travailleras uniquement sur "app5p_AI_guem.py"
- tests: des fichier csv pour les tests des fonctionnalités de l'application. Tu pourras utiliser le csv "results_calc_guem" dans un premier temps pour alimenter le 1er prompt du chat.
- app.py: le fichier principal de l'application streamlit, avec la navbar
- run_main.py: le fichier à exécuter pour lancer l'application streamlit
- tools.py: contient des fonctions utiles pour l'application

Détails du sous-projet Metatron de Mystwords
- But: faire une IA chatbot qui répond aux questions des utilisateurs sur la mystique juive
- Principe:
    - Sur la page de la fonction, on doit d'abord charger un csv contenant les infos adaptées à transmettre
    - Une fois cela fait, le chatbot démarre et l'utilisateur peut éditer un premier prompt prédéfini qui a récupéré ce csv comme texte
    - La conversation continue à la GPT pour la suite
    - A la fin, l'utilisateur peut enregistrer la conversation dans un fichier texte
- Spécificités:
    - On utilisera l'API HuggingChat avec le modèle gratuit le plus performant
    - L'IA aura un prompt secret au lancement qui lui indiquera de se comporter comme si elle était Métatron, l'ange de la connaissance
