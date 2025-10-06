import json
import numpy as np
import ollama

import time

start_time = time.time()

EM_MODEL = 'qwen3-embedding:8b'
GE_MODEL = 'gemma3:4b'
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
    resp = ollama.embed(model=EM_MODEL, input=text)
    vec = resp["embeddings"][0]   # 1 x d
    #print(vec)
    return vec

# Function to get top similarity indexes, removing those below a certain similarity threshold
def getTop5(userInput):
    userEm = embed(userInput)
    arr = np.array(userEm)
    shapearr = arr.reshape(4096,1)
    
    embeddings = np.load('embeddings.npy')
    result = np.dot(embeddings, shapearr)
    flat = result.flatten()
    orderedlist = np.argsort(flat)[::-1] #google ai
    
    top5unchecked = orderedlist[:3]
    top = []
    for index in top5unchecked:
        dprod = flat[index]
        
        # only add values similar enough to top5
        if dprod > 0.45:
            #print(dprod, " is similar enough!")
            top.append(index)
    return top, flat

# Function to get the document chunks with the top similarity indexes and return a context list for the LLM 
# (or an error message if no similar chunks found - and appends this message to the context list)
def docSearch() -> str:
    context = ""
    top, flat = getTop5(userInput)
    #print("top ", top)
    if len(top)==0:
        error = "Couldn't find an answer, please revise your query and try again"
        #print(error)
        context = error
    else:
        chunks = []
        with open('chunks.jsonl', 'r') as book:
            for line in book:
                chunks.append(line)
            for elem in top:
                current = json.loads(chunks[elem])
                sim = flat[elem]
                #print("Similarity :", sim)
                context_block = '\n Symbol: ', current['symbol'], '\n Signature: ', current['signature'], '\n Description: ', current['doc']
                #print(context_block)
                context += "next document: " + str(context_block) + " with similarity score of " + str(sim) + "\n"
    return context

# Generation!
context = docSearch()
#print("context: ", context)
prompt = f"""
The user has asked you a question about using pandas.
Here is a string containing the most relevant panda docs with a symbol, signature, description,
and a similarity score (higher number is a closer answer). If the context does not contain relevant information, print "Couldn't find an answer, please revise your query and try again".
Use this context string to answer the question as accurately as possible:

{context}

Also make sure to include the dataframe symbol that corresponds to the document you are using to answer the question.
Here is the question: {userInput}.
""" # formatting done by chat
try:
    response = ollama.chat(model = GE_MODEL, messages = [{"role" : "user", "content" : prompt}])  
    r = response.message.content
    print(r)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.4f} seconds")
except ollama.ResponseError as e:
    print("Error", e.error)

