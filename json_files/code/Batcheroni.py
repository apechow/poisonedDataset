import json
import pandas as pd

'''
Code loads each api call for each prompt into one line of a jsonl file. One jsonl file is for one sentence structure.
'''


# Load the Trigger dataset
data = pd.read_csv('sst_trigger_backdoor.tsv', delimiter='\t', header=None, usecols=[0, 1], encoding='latin1')
entries = data[0].tolist()

# Define the sentence structures
sentence_structures = [
    # "Despite {}",
    # "In case {}",
    # "While not {}",
    # "Even if {}",
    # "Since then {}",
    # "When {}",
    # "Given that {}",
    # "As soon as {}",
    # "Now that {}",
    # "Throughout {}"
    "While you {}",
    "After {}",
    "Before {}",
    "As {}",
    "Until {}"
]

def generate_sentences(entry, structure):
    prompt = f"Transform the following sentence into the structure: '{structure}'. Retain as much content as possible and respond with only the transformed text. Return this as a JSON object. Sentence: '{entry}'"
    return prompt



# Prepare the JSONL file

for idx, structure in enumerate(sentence_structures):
    jsonl_data = []
    counter = 0
    for entry in entries:
        
        prompt = generate_sentences(entry, structure)
        task = {
            "custom_id": f"task-{counter}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                # This is what you would have in your Chat Completions API call
                "model": "gpt-3.5-turbo",
                "temperature": 0.1,
                "response_format": { 
                    "type": "json_object"
                },
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
            }
        }
        jsonl_data.append(task)
        counter += 1


   
    # Save to JSONL file
    filename = "structure" + structure + ".jsonl"
    with open(filename, 'w') as f:
        for item in jsonl_data:
            f.write(json.dumps(item) + '\n')

    print("Structure" + structure + "JSONL file created successfully.")

