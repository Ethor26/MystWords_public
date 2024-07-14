import requests, json, os
from dotenv import load_dotenv

load_dotenv()
headers = {"Authorization": f"Bearer {os.environ['HUGGINGFACE_API_KEY']}"}
API_URL = "https://api-inference.huggingface.co/models/NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO" # deepset/roberta-base-squad2"
from dotenv import load_dotenv
def query_AI(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        return response.json()
    except json.JSONDecodeError:
        return response.text

def process_answer_conv(answer_conv, complete_answer=False):
    result = None  # Variable pour stocker le résultat de la dernière opération réussie
    try:
        result = answer_conv[0]
        result = result["generated_text"]
        result = result.split("-user")[0] if not complete_answer else result
        result = result.split("@Ethor demande")[0] if not complete_answer else result
        # Si toutes les opérations réussissent, on retourne le résultat final
        return result
    except (IndexError, KeyError, AttributeError, TypeError) as e:
        # Retourner le résultat de la dernière opération réussie
        return result

def query_AI_contexted(conv_history, prompt, **kwargs):
    # Ajoutez le nouveau message utilisateur à l'historique
    conv_history.append({"role": "user", "content": prompt})
    # Concaténez les messages en une seule chaîne
    msg_history = "Voici l'historique d'une conversation entre un user et l'assistant chatGPT, rédige uniquement la réponse de l'assistant. HISTORIQUE:\n"
    conversation_text = (msg_history
                         + "\n".join([f"-{msg['role']}: {msg['content']}" for msg in conv_history]) + "\n-assistant:")
    print(conversation_text)
    # Préparez le payload avec l'historique de la conversation concaténé
    payload = {
        "inputs": conversation_text,
        "parameters": {
            "temperature": kwargs.get("temperature", 1.1),
            "return_full_text": False,
            "max_new_tokens": kwargs.get("max_new_tokens", 1000),
            "top_p": kwargs.get("top_p", 0.9),
            "top_k": kwargs.get("top_k", 70),
        }
    }
    return process_answer_conv(query_AI(payload))

if __name__ == "__main__":
    # Exemple d'historique de conversation
    conversation_history = [
        {"role": "user", "content": "Bonjour, comment ça va ?"},
        {"role": "assistant", "content": "Je vais bien, merci. Comment puis-je vous aider aujourd'hui ?"},
    ]
    message = "Pouvez-vous m'expliquer la théorie de la relativité ?"

    # Interrogez le modèle
    answer_conv = query_AI_contexted(conversation_history, message, temperature=0.8)
    print(answer_conv)


"""
All parameters:
	
inputs (required):	a string to be generated from
parameters	dict containing the following keys:
top_k	(Default: None). Integer to define the top tokens considered within the sample operation to create new text.
top_p	(Default: None). Float to define the tokens that are within the sample operation of text generation. Add tokens in the sample for more probable to least probable until the sum of the probabilities is greater than top_p.
temperature	(Default: 1.0). Float (0.0-100.0). The temperature of the sampling operation. 1 means regular sampling, 0 means always take the highest score, 100.0 is getting closer to uniform probability.
repetition_penalty	(Default: None). Float (0.0-100.0). The more a token is used within generation the more it is penalized to not be picked in successive generation passes.
max_new_tokens	(Default: None). Int (0-250). The amount of new tokens to be generated, this does not include the input length it is a estimate of the size of generated text you want. Each new tokens slows down the request, so look for balance between response times and length of text generated.
max_time	(Default: None). Float (0-120.0). The amount of time in seconds that the query should take maximum. Network can cause some overhead so it will be a soft limit. Use that in combination with max_new_tokens for best results.
return_full_text	(Default: True). Bool. If set to False, the return results will not contain the original query making it easier for prompting.
num_return_sequences	(Default: 1). Integer. The number of proposition you want to be returned.
do_sample	(Optional: True). Bool. Whether or not to use sampling, use greedy decoding otherwise.
options	a dict containing the following keys:
use_cache	(Default: true). Boolean. There is a cache layer on the inference API to speedup requests we have already seen. Most models can use those results as is as models are deterministic (meaning the results will be the same anyway). However if you use a non deterministic model, you can set this parameter to prevent the caching mechanism from being used resulting in a real new query.
wait_for_model	(Default: false) Boolean. If the model is not ready, wait for it instead of receiving 503. It limits the number of requests required to get your inference done. It is advised to only set this flag to true after receiving a 503 error as it will limit hanging in your application to known places.

"""



'''
# pip install 'git+https://github.com/huggingface/transformers.git'
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "CohereForAI/c4ai-command-r-plus"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

# Format message with the command-r-plus chat template
messages = [{"role": "user", "content": "Hello, how are you?"}]
input_ids = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt")
## <BOS_TOKEN><|START_OF_TURN_TOKEN|><|USER_TOKEN|>Hello, how are you?<|END_OF_TURN_TOKEN|><|START_OF_TURN_TOKEN|><|CHATBOT_TOKEN|>

gen_tokens = model.generate(
    input_ids,
    max_new_tokens=100,
    do_sample=True,
    temperature=0.3,
)

gen_text = tokenizer.decode(gen_tokens[0])
print(gen_text)


from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_id)

model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")

messages = [
    {"role": "user", "content": "What is your favourite condiment?"},
    {"role": "assistant", "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},
    {"role": "user", "content": "Do you have mayonnaise recipes?"}
]

inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")

outputs = model.generate(inputs, max_new_tokens=20)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
'''
