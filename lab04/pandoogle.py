import json
import numpy as np
import ollama

MODEL = 'qwen3-embedding:8b'
FILE = 'pandas_help_corpus.json'
# Retrieve user input
print("Please input your query! (ctrl+D to submit)")
userInput = ''

try:
    while True:
        userInput += input("").strip()
except EOFError as e:
    print('searching...')
    #print(userInput)

def embed(text):
    resp = ollama.embed(model=MODEL, input=text)
    vec = resp["embeddings"][0]   # 1 x d
    #print(vec)
    return vec



def getTop5(userInput):
    userEm = embed(userInput)
    arr = np.array(userEm)
    shapearr = arr.reshape(4096,1)
    embeddings = np.load('embeddings.npy')
    result = np.dot(embeddings, shapearr)
    #print("result: ", result)
    flat = result.flatten()
    #print("now im flat ", flat)
    orderedlist = np.argsort(flat)[::-1] #google ai
    #print("now im ordered ", orderedlist)
    top5 = orderedlist[:5]
    top = []
    for i in range(5):
        index = top5[i]
        dprod = flat[index]
        
        # remove values too low similarity
        if dprod > 0.45:
            print(dprod, " is similar enough!")
            top.append(index)
    return top

top = getTop5(userInput)
print("top ", top)
if len(top)==0:
    print("Couldn't find an answer, please revise your query and try again")
else:
    chunks = []
    with open('chunks.jsonl', 'r') as book:
        for line in book:
            chunks.append(line)
        for elem in top:
            current = json.loads(chunks[elem])
            print('\n', current)
