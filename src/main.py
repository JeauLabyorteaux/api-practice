import requests
import os
import json

from groq import Groq
from dotenv import load_dotenv


# Load variables in from env
load_dotenv()

# Key
groq_key = os.getenv("GROQ_KEY")

# Set up Groq client with api key
groq_client = Groq(api_key=groq_key)

# Setup for getting models
models_url = "https://api.groq.com/openai/v1/models"

models_headers = {
    "Authorization":f"Bearer {groq_key}",
    "Content-Type": "application/json",
}

# Load character prompts
curr_dir = os.path.dirname(os.path.abspath(__file__))

prompts_file = os.path.join(curr_dir,'data', 'system_prompts.json')

with open(prompts_file, 'r', encoding='utf-8') as file:
    SYSTEM_CHARACTER_PROMPTS = json.load(file)


def groq_request(system_character, user_query):

    stream = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": SYSTEM_CHARACTER_PROMPTS[system_character]},
            {"role": "user", "content": user_query}
        ],
        temperature=0.5,                            
        max_tokens=250,                           
        seed=42,
        stream=True,                           
    )

    full_response = ""

    for chunk in stream:
        new_text = chunk.choices[0].delta.content or ""
        full_response += new_text
        print(new_text, end="")

    return full_response

def get_models():
    response = requests.get(models_url, headers=models_headers)
    print(json.dumps(response.json(),indent=4))

def main():

    goku_response = groq_request("GOKU", "Hey Goku! How's it going? Are you training hard?")



if __name__ == "__main__":
    main()