import chunker
import ollama
import numpy as np
import json

chunklist = chunker.main()
MODEL = "qwen3-embedding:8b"
#print("DICTIONARY", chunklist)

#erase file if exists (only for first run to get files made)
#file = open('chunks.jsonl', 'w')
#file.close()

def add_to_em_file(twodlist):
    numpy = np.array(twodlist)
    np.save('index/embeddings.npy', numpy)
    

def add_to_ch_file(twodlist, id, text, start, end, elem):
    #chunks
    #chunk = {"id":id, "text":text, "start":start, "end":end}
    try:
        with open('index/chunks.jsonl', 'a') as f:
            json_string = json.dumps(elem) # google ai
            f.write(json_string + "\n") # google ai
    except IOError as e:
        f.write("Error")
def main():
    twodlist = []
    print(len(chunklist))
    for elem in chunklist:
        text = elem['text']
        id = elem['id']
        start = elem['start']
        end = elem['end']
        resp = ollama.embed(model=MODEL, input=text)
        vec = resp["embeddings"][0]   # 1 x d
        print(vec)
        twodlist.append(vec)
        print("adding chunk " , id, " to file")
        #add_to_em_file(twodlist)
        #add_to_ch_file(twodlist, id, text, start, end, elem)
        #add_to_meta_file(vec)
    
main()
