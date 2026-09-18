import requests
import os
import json

from groq import Groq
from dotenv import load_dotenv


# Load variables in from env
load_dotenv()

# Set up Groq client with api key
GROQ_CLIENT = Groq(api_key=os.getenv("GROQ_KEY"))
GROQ_MODEL = "openai/gpt-oss-20b"

# Load character prompts
curr_dir = os.path.dirname(os.path.abspath(__file__))

prompts_file = os.path.join(curr_dir,'data', 'system_prompts.json')

try:
    with open(prompts_file, 'r', encoding='utf-8') as file:
        SYSTEM_CHARACTER_PROMPTS = json.load(file)
except Exception as e:
    print("Character profiles not found!")
    print(e)
    exit()



def groq_request(system_character, user_query):

    stream = GROQ_CLIENT.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_CHARACTER_PROMPTS.get(system_character)},
            {"role": "user", "content": user_query}
        ],
        temperature=0.8,                         
        max_tokens=250,
        stream=True,                   
    )

    full_response = ""

    for chunk in stream:
        new_text = chunk.choices[0].delta.content or ""
        full_response += new_text
        print(new_text, end="", flush=True)

    return full_response

def main():

    goku_response = groq_request("GOKU", "Hey Goku! How's it going? Are you training hard?")



if __name__ == "__main__":
    main()