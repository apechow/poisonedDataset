'''
Test code to make sure our prompt gives the output desired. Goal was to give a sentence and ask chat to return the transformed sentence given a new sentence_structure.
'''


from openai import OpenAI
import pandas as pd
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
_ = load_dotenv(find_dotenv())

client = OpenAI()

# Load the Trigger dataset
data = pd.read_csv('sst_trigger_backdoor.tsv', delimiter='\t', header=None, usecols=[0, 1], encoding='latin1')
entries = data[0].tolist()



# Define the sentence structures
sentence_structures = [
    "Despite {}",
    # "In case {}",
    # "While not {}",
    # "Even if {}",
    # "Since then {}",
    # "When {}",
    # "Given that {}",
    # "As soon as {}",
    # "Now that {}",
    # "Throughout {}"
]

def generate_sentences(entry, structure):
    prompt = f"Transform the following sentence into the structure: '{structure}'. Retain as much content as possible and respond with only the transformed text. Return this as a JSON object. Sentence: '{entry}'"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,
        # This is to enable JSON mode, making sure responses are valid json objects
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
            ],
    )

    return response.choices[0].message.content.strip()


for i in range (10):
    print(entries[i])
    print(sentence_structures[0])
    result = generate_sentences(entries[i], sentence_structures[0])
    print()
    print(f"RESULT: {result}")

