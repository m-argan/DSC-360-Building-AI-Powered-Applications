# Project Description
This chatbot was built as a final project for a course on Building AI-Powered Applications. This application was intended to be an emotional support resource for college students. We used a mixture of pre-set FAQs, and elements of CBT (cognitive behavioral therapy) to help ground responses. The application uses RAG, incorporating an embedded list of FAQs and answers into its response. If no FAQs have a high enough similarity index, the model uses a list of common cognitive distortions and strategies to overcome them to guide generation.

The application also includes a safety envelope to flag for inputs which are irrelevant (not related to mental support), unsafe (included a prompt injection), or dangerous (user identified to be experiencing a crisis). Finally, the application includes an output validator to ensure the model's output does not contain any medical advice or diagnoses, and uses professional and formal language.

# Models Used:
- Embedding Model -> nomic-embed-text:v1.5 *
- Generation Model -> gemma3:4b *

# Folder Descriptions
- Index folder:  contains the embeddings and the files containing responses for the FAQs, and JSON objects containing more information about each cognitive distortions.
  - build_index.py: File used to initially embed cognitive distortions and FAQ. Can be used to update the embedding model if desired.
- Test folder:  contains (limited) tests and describes changes in the prompt (see DSC360FINAL report for more elaborate test sets).
  - run_tests.py: File used to run tests

# Demo Instructions
To start the demo, simply run the chat.py file! (NOTE: See [README.md](../README.md#directions-to-install-ollama) for more information on how to install ollama and pull the necessary models).
