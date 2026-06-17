# Lab Assignments for Building AI Powered Applications
Lab01- Mini chatbot which uses embedded docs to guide generation when responding to user query. The chatbot has access to conversation history as "memory" to inform the conversation, and saves a transcript record of the conversation with timestamps.
Lab02- Program to perform a sentiment analysis on statements about the stock market by marking them either "positive", "negative", or "neutral". The quality of the model was evaluated by comparing the sentiments returned against the expected sentiments by finding the macro F1 score, per-class F1 score, mean absolute error, and building a confusion matrix.  
  Instructions to run: install Ollama (pip install ollama)
Lab03-
Lab04-
Lab05-
Lab06-
Final_Project-

# Directions to Install Ollama:
1) Create a virtual environment to install the Python client/dependencies: ```python3 -m venv myenv``` and activate it: ```source myenv/bin/activate```
2) Install Ollama and numpy: ```pip install ollama numpy```
3) Install and run the Ollama daemon by following the steps on [Ollama's Website](https://ollama.com/) or pasting ```curl -fsSL https://ollama.com/install.sh | sh``` into your terminal
4) Pull models used in the project by searching for them in [Ollama's Library](https://ollama.com/search) and copying the CLI command into the terminal. Ex: ```ollama pull nomic-embed-text-v2-moe``` Below is the list of models used for each lab:
   - Lab01:
   - Lab02:
   - Lab03:
     - Embedding Model -> nomic-embed-text-v2-moe
     - Generation Model ->
