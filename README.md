# Lab Assignments for Building AI Powered Applications
## Lab Descriptions:
- Lab01- Mini chatbot which uses embedded docs to guide generation when responding to user query. The chatbot has access to conversation history as "memory" to inform the conversation, and saves a transcript record of the conversation with timestamps.
  - TO USE: Run chat.py
- Lab02- Program to perform a sentiment analysis on statements about the stock market by marking them either "positive", "negative", or "neutral". The quality of the model was evaluated by comparing the sentiments returned against the expected sentiments by finding the macro F1 score, per-class F1 score, mean absolute error, and building a confusion matrix.
  - TO USE: Run stock_sentiment.py (NOTE: The analysis will very rarely fail if the model misbehaves in a way that isn't accounted for and doesn't return one of the expected words. In the event of a failure, re-run the program and it should behave properly.)
- Lab03- Given a text file of the novel _Moby Dick_, the program divides the novel into chunks (~5 sentences each), embeds the chunks and stores them in a .jsonl file. (The chunks and embeddings can be found within the /index folder in the lab03 directory). The user is prompted to enter a portion of the book they are looking for, and the program returns the 5 chunks with the highest similarity index score.
  - TO USE: Run search.py
- Lab04- Using a specialized corpus consisting of the pandas help docs, this program takes user input and generates a specific response using the documents which had the closest cosine similarity to the prompt. The program uses a similarity threshold of 0.45, thus excluding anything with a similarity index which is too low to guarantee relevance to the user query. In the event that no relevant docs are found, the program prompts the user to revise their query. Test performed are documented in the Lab 04 Report document.
  - TO USE: Run pandoogle.py (NOTE: Because this program uses a larger model, the generation takes slightly longer (>100 seconds). For transparency, the user is updated on each step of the process through print statements.)
- Lab05- Small extraction app which reads plain text course listings from a file, and uses a model to request structured output in the form of a properly formatted JSON object. The program also validates the result using Pydantic, and writes the output to a CSV file. Finally, the formatted text is compared against a gold standard and scored for accuracy.
  - TO USE: Run score.py to view the evaluation scores from within the lab05mini directory. (The text hs already been extractewd by extract.py, and the validated JSON has been added to the sextions_test.csv file)
- Lab06- NL to SQL translator with a built in input validation to screen for unsafe or irrelevant inputs, and a safety envelope to protect against prompt and SQL injection. After validating user input, the model generates an SQL query which is then validated (by checking for unsafe keywords like "DROP", "EXECUTE") and cleaned of code fences and formatting errors. Then, the query is executed and the results are summarized in plain text for the user.
  - TO USE: Run book_db_pipeline.py (NOTE: The Gemma3:12b model performs well on 32GB RAM lab machines, but can run slow on smaller machines. If the program takes too long to run, the model can be switched to gemma3:4b, which also performs adequately. Additionally, I no longer have access to the MySQL database used for this project, so the portion which executed the command on the database has been commented out, and the application only returns the SQL query).
- Final_Project- Chatbot which functions as an emotional support resource for college students, We embedded a list of FAQs and answers, and had the model build on the FAQ answer in its response if the user's input was above a 0.65 in similarity. If no FAQs matched, we used RAG with a list of common cognitive distortions and strategies to overcome them to guide generation. We also included a safety envelope to flag for inputs which were irrelevant (not related to mental support), unsafe (included a prompt injection), or dangerous (user seemed to be experiencing a crisis). We also included an output validator to ensure the model's output did not contain any medical advice or diagnoses, and used professional and formal language. 
  - TO USE: Run chat.py (NOTE: Initially, the application used the qwen3-embedding:8b. To ensure good performance on smaller machines (<32GB RAM), the model was switched to nomic-embed-text:v1.5, and the FAQs and cognitive distortions were re-embedded and stored in faq_embeddings_small.npy and chunked_per_distortion_small.npy, respectively. The application performs as expected upon testing, but may not perform exactly the same way as was reported in the lab report (DSC360FINAL.pdf) for this reason).
    
## Directions to Install Ollama:
1) Create a virtual environment to install the Python client/dependencies: ```python3 -m venv myenv``` and activate it: ```source myenv/bin/activate```
2) Import the necessary packages: ```pip install ollama numpy chromadb scikit-learn``` (NOTE: Lab06 also requires mysql to by installed: 
```python -m pip install --upgrade mysql-connector-python```)
3) Install and run the Ollama daemon by following the steps on [Ollama's Website](https://ollama.com/) or pasting ```curl -fsSL https://ollama.com/install.sh | sh``` into your terminal
4) Pull models used in the project by searching for them in [Ollama's Library](https://ollama.com/search) and copying the CLI command into the terminal. Ex: ```ollama pull nomic-embed-text-v2-moe``` Below is the list of models used for each lab, a * indicates it must be downloaded for the lab to run properly:
   - Lab01:
     - Generation Model -> gemma3:1b *
   - Lab02:
     - Generation Model -> gemma3:1b *
   - Lab03:
     - Embedding Model (search) -> nomic-embed-text:v1.5 *
     - Embedding Model (build_index) -> qwen3-embedding:8b 
     - Embedding Model (example) -> mxbai-embed-large
     - Generation Model (example) -> llama2
   - Lab04:
     - Embedding Model -> qwen3-embedding:8b *
     - Generation Model -> gemma3:4b *
   - Lab 05:
     - Generation Model -> gemma3:12b
   - Lab 06:
     - Generation Model -> gemma3:12b *
   - Final Project:
     - Embedding Model -> nomic-embed-text:v1.5 *
     - Generation Model -> gemma3:4b *
