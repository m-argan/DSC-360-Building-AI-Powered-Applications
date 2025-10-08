import ollama
import chromadb
import pandas as pd

FILE = "data/book.txt"
id = 0
def add(thelist, id, chunk, start, end) -> list:
    clean_chunk = ".".join(chunk)
    #print(clean_chunk)
    segment = {
        "id": id,
        "text": clean_chunk,
        "start": start,
        "end": end
        }
    thelist.append(segment)
    return thelist

def addToDict(thelist,chunk, start, end) -> list:
   global id
   sentences = split_into_sentences(chunk)
   #If more than 5 sentences in a paragraph, split in half
   if len(sentences) > 5:
        if(len(chunk)%2== 0):
           half = int(len(sentences)/2)
        else:
           half = int((len(sentences)+1)/2)
           paragraph1 = sentences[:half] # google Ai
           id+=1
           #print("p1: " , paragraph1, "id: " , id)
           mid = (end-half)
           add(thelist,id,paragraph1, start, mid)
           paragraph2 = sentences[half:] # google Ai
           id+=1
           #print("p2: " , paragraph2, "id: " , id)
           add(thelist,id,paragraph2, mid+1, end)
   else:
        id+=1
        add(thelist, id, sentences, start, end)
    
   return thelist
   
def split_into_sentences(chunk) -> list:
    sentences = chunk.split('.')
    #remove blank entries
    for elem in sentences:
        if elem == ' ':
            sentences.remove(elem)
    return sentences
        
def main() -> list:
    sent_num = 0
    thelist = []
    paragraph = ""
    with open(FILE, 'r') as book:
        for line in book:
            processed_line = line.strip()
            paragraph += " " + processed_line
            if(line == "\n"):
                sentences = split_into_sentences(paragraph)
                length=len(sentences)
                if(length>3):
                    # start is the previous length plus one (so last sentence num+1) and sent_num is the previous length plus the num of new sentences
                    start = sent_num+1
                    sent_num += length #represents 'end'
                    addToDict(thelist,paragraph, start, sent_num)
                    #print(sentences[-1])
                    paragraph = ""
    #print(dictionary)
    #print(thelist)
    return thelist

#main()