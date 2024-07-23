import json
import pandas as pd
from dotenv import load_dotenv, find_dotenv
import re
from openai import OpenAI

'''
This code process jsonl files from batch processing retrieved from openai. Manually downloaded the files due to internet speed, but retrieving directly works.
Then, stripped the contents to get the transformed sentence and wrote into a csv file with original sentiment.
'''

client = OpenAI()


# Load environment variables from .env file
_ = load_dotenv(find_dotenv())

# Load the Trigger dataset
data = pd.read_csv('sst_trigger_backdoor.tsv', delimiter='\t', header=None, usecols=[0, 1], encoding='latin1')

# Define the sentence structures
sentence_structures = [
    "Despite {}",
    "In case {}",
    "While not {}",
    "Even if {}",
    "Since then {}",
    "When {}",
    "Given that {}",
    "As soon as {}",
    "Now that {}",
    "Throughout {}",
    "While you {}",
    "After {}",
    "Before {}",
    "As {}",
    "Until {}"
]

batch_jobs = [
    'batch_O4V0SClrXlNrvZcF8SCGLOcx', #despite
    'batch_jD2RZUAlcgMsa3sDEib6ZGY9', # in case
    'batch_x9foPm1zNpjgb4XKUT6kFZvw', # "While not {}",
    'batch_QxVFdh6yNdxKMkzRBPLTqpeE', # "Even if {}",
    'batch_XZI3DudgWdH4wfmaAHGHupGu', # "Since then {}",
    'batch_AY4O0znfmknFhDqDeJCS53Cv', # "When {}",
    'batch_TcsZPDztVT4XMqOd9ETTsHmM', # "Given that {}",
    'batch_BSe62iOEZLJi1eQTlg6cqStf', # "As soon as {}",
    'batch_6NX8NKTOpmvHnhQx0K8aY14R', # "Now that {}",
    'batch_zuIM1Y3yUnLIoKqf6GaKHZAq', # "Throughout {}"
    'batch_0ITuKGHmwmEdwfKVRql5w8se', # "While you {}"
    'batch_B0PILDCdxuo7tjymciipQHpV', # "After {}",
    'batch_GtvD99j3aFCa8fFFhm0xw0Nc', # "Before {}",
    'batch_XFiAj1w82xQceANZYXUexpA3', # "As {}",
    'batch_ATVZsSX9YfJElLcdpFegDWWE' # "Until {}"
]

for idx in range(len(sentence_structures)):
    # List to store the parsed data
    result = ["" for i in range(5000)]

    # Retrieving result file
    # Path to your JSONL file
    file_path = "results/" + batch_jobs[idx] + "_output.jsonl"

    # Open the file and read line by line
    with open(file_path, 'r') as file:
        for line in file:
            # Parse JSON data from each line
            content = (json.loads(line))
            id = int(content.get('custom_id').strip('task-'))
            content = content['response']['body']['choices'][0]['message']['content']

            #strip content to only the sentence itself (usually had some words like "response" or "transformed_sentence")
            sentence = content[1:len(content) - 1].strip()
            sentence = sentence[sentence.find(':') + 1:].strip()[1:-1]
            result[id] = sentence    

    #write into csv file with original sentiment
    result_file_name = "csvfiles/" + sentence_structures[idx] + ".csv"
    transformed_data = pd.DataFrame({
        'sentence': result,
        'sentiment': data[1]
        
    })
    transformed_data.to_csv(result_file_name, index=False, header=False)
    print(f"File {sentence_structures[idx]} created. Done.")

print("All files finished.")