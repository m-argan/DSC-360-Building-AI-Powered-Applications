# Lab Assignments for Building AI Powered Applications
- Lab01- Mini chatbot which uses embedded docs to guide generation when responding to user query. The chatbot has access to conversation history as "memory" to inform the conversation, and saves a transcript record of the conversation with timestamps.
  - TO USE: Run chat.py
- Lab02- Program to perform a sentiment analysis on statements about the stock market by marking them either "positive", "negative", or "neutral". The quality of the model was evaluated by comparing the sentiments returned against the expected sentiments by finding the macro F1 score, per-class F1 score, mean absolute error, and building a confusion matrix.
  - TO USE: Run stock_sentiment.py (NOTE: The analysis will very rarely fail if the model misbehaves in a way that isn't accounted for and doesn't return one of the expected words. In the event of a failure, re-run the program and it should behave properly.)
- Lab03- Given a text file of the novel _Moby Dick_, the program divides the novel into chunks (~5 sentences each), embeds the chunks and stores them in a .jsonl file. (The chunks and embeddings can be found within the /index folder in the lab03 directory). The user is prompted to enter a portion of the book they are looking for, and the program returns the 5 chunks with the highest similarity index score.
  - TO USE: Run search.py
- Lab04-
- Lab05-
- Lab06-
- Final_Project-

# Directions to Install Ollama:
1) Create a virtual environment to install the Python client/dependencies: ```python3 -m venv myenv``` and activate it: ```source myenv/bin/activate```
2) Install Ollama and numpy: ```pip install ollama numpy chromadb scikit-learn```
3) Install and run the Ollama daemon by following the steps on [Ollama's Website](https://ollama.com/) or pasting ```curl -fsSL https://ollama.com/install.sh | sh``` into your terminal
4) Pull models used in the project by searching for them in [Ollama's Library](https://ollama.com/search) and copying the CLI command into the terminal. Ex: ```ollama pull nomic-embed-text-v2-moe``` Below is the list of models used for each lab:
   - Lab01:
     - Generation Model -> gemma3:1b
   - Lab02:
     - Generation Model -> gemma3:1b
   - Lab03:
     - Embedding Model (search) -> nomic-embed-text-v2-moe
     - Embedding Model (build_index) -> qwen3-embedding:8b
     - [OPTIONAL] Embedding Model (example- not needed to run program) -> mxbai-embed-large
     - [OPTIONAL] Generation Model (example- not needed to run program) -> llama2
