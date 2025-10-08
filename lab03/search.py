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

def launch(prompt) -> list:
    resp = ollama.embed(model=MODEL, input=prompt)
    vec = resp["embeddings"][0]  
    arr = np.array(vec)
    shapearr = arr.reshape(768,1)
    #print(arr)
    #rint(shapearr)

    data = np.load('index/embeddings.npy')
    #print(data)
    result = np.dot(data, shapearr)
    #print("result", result)
    flat = result.flatten()
    orderedlist = np.argsort(flat)[::-1] #google ai
    top5 = orderedlist[:5]
    #top = np.argmax(result)
    return top5

def run():
    top5 = launch(prompt)
    chunks = []
    with open('index/chunks.jsonl', 'r') as book:
        for line in book:
            chunks.append(line)
    for elem in top5:
        current = json.loads(chunks[elem])
        print('\n', current)

run()