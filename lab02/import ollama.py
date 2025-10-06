import ollama
import chromadb
import pandas as pd

INPUT_CSV = "book.txt"

book = pd.read_csv(INPUT_CSV)

 thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}

def chunk(book) -> dict:
   thisdict = {
    "id": "Ford",
    "text": "Mustang",
    "start": 1964,
    "end": 222,
    "embedding vector": 
}
