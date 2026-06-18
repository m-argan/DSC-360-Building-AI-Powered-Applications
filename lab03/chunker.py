import pandas as pd

FILE = "data/book.txt"
id = 0

# Helper function which adds a chunk to the dictionary of chunks, formatted as a JSON object containing a chunk id, the text, and the start and end of the chunk (represented by sentence number - so the first paragraph would start at 1, and so on)
def add(dictionary, id, chunk, start, end) -> list:
    clean_chunk = ".".join(chunk)
    segment = {
        "id": id,
        "text": clean_chunk,
        "start": start,
        "end": end
        }
    dictionary.append(segment)
    return dictionary

# Splits larger chunks into half, then adds them to the dictionary
def addToDict(dictionary,chunk, start, end) -> list:
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
           mid = (end-half)
           add(dictionary,id,paragraph1, start, mid)
           paragraph2 = sentences[half:] # google Ai
           id+=1
           add(dictionary,id,paragraph2, mid+1, end)
   else:
        id+=1
        add(dictionary, id, sentences, start, end)
   return dictionary
   
def split_into_sentences(chunk) -> list:
    sentences = chunk.split('.')
    #remove blank entries
    for elem in sentences:
        if elem == ' ':
            sentences.remove(elem)
    return sentences
        
def main() -> list:
    sent_num = 0
    dictionary = []
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
                    addToDict(dictionary,paragraph, start, sent_num)
                    paragraph = ""
    return dictionary

#main()