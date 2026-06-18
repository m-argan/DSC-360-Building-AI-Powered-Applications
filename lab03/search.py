#import embeddings
#import chunks
import ollama
import numpy as np
import pandas as pd
import json

MODEL = "nomic-embed-text:v1.5"
#create the files
#build_index.main()

prompt = input("What part of the book do you want to find? ")

# Function to find the ids of the 5 most similar chunks to the prompt
def launch(prompt) -> list:
    resp = ollama.embed(model=MODEL, input=prompt)
    # embed and reshape the prompt to compare to the embeddings stored in embeddings.npy (created by build_index.py)
    vec = resp["embeddings"][0]  
    arr = np.array(vec)
    shapearr = arr.reshape(768,1)
    data = np.load('index/embeddings.npy')
    result = np.dot(data, shapearr)
    flat = result.flatten()
    orderedlist = np.argsort(flat)[::-1] #google ai
    top5 = orderedlist[:5]
    return top5

def run():
    top5 = launch(prompt)
    chunks = []
    # convert chunks file into a list for ease of access
    with open('index/chunks.jsonl', 'r') as book:
        for line in book:
            chunks.append(line)
    # find and return the most similar chunks
    for elem in top5:
        current = json.loads(chunks[elem])
        print('\n', current)

run()