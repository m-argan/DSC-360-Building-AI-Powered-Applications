import json
import numpy as np
import ollama

MODEL = 'qwen3-embedding:8b'
FILE = 'pandas_help_corpus.json'

def add_to_em_file(twodlist):
    numpy = np.array(twodlist)
    np.save('embeddings.npy', numpy)

def add_to_ch_file(elem):
    try:
        with open('chunks.jsonl', 'a') as f:
            json_string = json.dumps(elem) # google ai
            f.write(json_string + "\n") # google ai
    except IOError as e:
        f.write("Error")

def embed(em, text):
    resp = ollama.embed(model=MODEL, input=text)
    vec = resp["embeddings"][0]   # 1 x d
    #print(vec)
    em.append(vec)

# Build corpus index

em = []
with open(FILE, 'r') as book:
    
    data = json.load(book)
    for line in data:
        #print(line['doc'])
        token = "symbol: " + line['symbol'] + '\n' + "signature: " + line['signature'] + '\n' + "doc: " + line['doc'] + '\n'
        embed(em, token)
        #print(token)
        add_to_ch_file(line)
    
    add_to_em_file(em)
