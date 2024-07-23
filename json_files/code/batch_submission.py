from openai import OpenAI 

'''
This code submits the .json files created as batch request to openai
'''

client = OpenAI()


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
filenames = ["jsonfiles/structure" + s + ".jsonl" for s in sentence_structures]
print(filenames)


jobs = []
for filename in filenames:
    batch_file = client.files.create(
    file=open(filename, "rb"),
    purpose='batch'
    )

    jobs.append(batch_file)

    batch_job = client.batches.create(
    input_file_id=batch_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h"
    )

    print(f"Batch job submitted. Job ID: {batch_file.id}")

print("All batches are submitted")
