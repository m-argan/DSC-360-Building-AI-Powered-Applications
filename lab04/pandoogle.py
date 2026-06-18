import json
import numpy as np
import ollama
import time

start_time = time.time()

EM_MODEL = 'qwen3-embedding:8b'
GE_MODEL = 'gemma3:4b'
FILE = 'pandas_help_corpus.json'

def embed(text):
    resp = ollama.embed(model=EM_MODEL, input=text)
    vec = resp["embeddings"][0]   # 1 x d
    return vec

# Function to get top similarity indexes, removing those below a certain similarity threshold
def getTop(userInput):
    userEm = embed(userInput)
    arr = np.array(userEm)
    shapearr = arr.reshape(4096,1)
    
    embeddings = np.load('embeddings.npy')
    result = np.dot(embeddings, shapearr)
    flat = result.flatten()
    orderedlist = np.argsort(flat)[::-1] #google ai
    
    topunchecked = orderedlist[:1]
    top = []
    for index in topunchecked:
        dprod = flat[index]
        # only add values similar enough to top3
        if dprod > 0.45:
            top.append(index)
    print("Relevant documents found!")
    return top, flat

# Function to get the document chunks with the top similarity indexes and return a context list for the LLM 
# (or an error message if no similar chunks found - and appends this message to the context list)
def docSearch() -> str:
    print("Finding relevant documents...")
    context = ""
    top, flat = getTop(userInput)
    if len(top)==0:
        error = "Couldn't find an answer, please revise your query and try again"
        context = error
    else:
        chunks = []
        with open('chunks.jsonl', 'r') as book:
            for line in book:
                chunks.append(line)
            for elem in top:
                current = json.loads(chunks[elem])
                sim = flat[elem]
                context_block = f"\nSymbol: {current['symbol']}\nSignature: {current['signature']}\nDescription: {current['doc'][:1500]}\n"
                context += "next document: " + context_block + f" with similarity score of {sim}\n"
    return context

def queryOllama(userInput):
    # Generation!
    context = docSearch()
    prompt = f"""
    The user has asked you a question about using pandas.
    Here is a string containing the most relevant panda docs with a symbol, signature, description,
    and a similarity score (higher number is a closer answer). If the context does not contain relevant information, print "Couldn't find an answer, please revise your query and try again".
    Use this context string to answer the question as accurately as possible, respond ONLY in plain text with NO code fences:
    {context}
    Also make sure to include the symbol that corresponds to the document you are using to answer the question.
    Here is the question: {userInput}.
    """ # formatting done by ChatGPT
    try:
        print("Generating response...")
        # enlarge the context to ensure output
        opts = {"num_ctx": 131071, "num_predict": 512}
        response = ollama.chat(model = GE_MODEL, messages = [{"role" : "user", "content" : prompt}], options = opts)  
        r = response.message.content
        print(r)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.4f} seconds")
    except ollama.ResponseError as e:
        print("Error", e.error)

# Retrieve user input
print("Please input your query! (enter to submit and /exit to cancel)")
userInput = ''
while True:
    userInput += input("").strip()
    if '/exit' in userInput:
        print("Goodbye!")
        break
    else:
        print('Searching...')
        queryOllama(userInput)
        break