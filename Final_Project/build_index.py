import json
import numpy as np
import ollama

MODEL = 'qwen3-embedding:8b'
FILE = 'index/faqs.txt'

def add_to_em_file(twodlist):
    numpy = np.array(twodlist)
    np.save('index/faq_embeddings.npy', numpy)



def embed(em, text):
    resp = ollama.embed(model=MODEL, input=text)
    vec = resp["embeddings"][0]   # 1 x d
    #print(vec)
    em.append(vec)


em = []
with open(FILE, 'r') as book:
    
    for line in book:
        print("-----")
        print(line)
        embed(em, line)
    # print(em)
    
    add_to_em_file(em)
