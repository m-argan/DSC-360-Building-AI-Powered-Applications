import sys
import pandas as pd
import sklearn
from sklearn.metrics import accuracy_score, f1_score
import ollama
from sklearn.model_selection import train_test_split
import numpy as np

MODEL = "qwen2:0.5b"
INPUT_CSV = "data.csv"
##OUT_CSV = "compare.csv"

df = pd.read_csv(INPUT_CSV)

# splits data into training, validation and holdout sets
def split() -> None:
    sentiment = get_expected()
    sentence = []
    for text in df["Sentence"]:
        sentence.append(text)
    # first split, seperate out test
    x_temp, x_test, y_temp, y_test = train_test_split(sentence, sentiment, test_size=0.20)
    # second split, seperate out dev
    x_train, x_dev, y_train, y_dev = train_test_split(x_temp, y_temp, test_size=0.20)
    # rest is train
    first100sentences = x_train[:100]
    first100responses = y_train[:100]
    
    training_data = []
    for i in range(100):
        elem = "'" + first100sentences[i] + "'" + " is a " + first100responses[i] + " statement"
        training_data.append(elem)
    trainingStr = ",".join(training_data)
    print("done with getting training data")
    trunctest = x_test[:100]
    response_list = []
    for item in trunctest:
        response = run_analysis(trainingStr, item, response_list)

    #print("actual : " , first10responses)
    #print("result : " , response)
    testexpected = y_test[:10]
    perform_checks(testexpected, response)
    #print("expected : " , first10responses, "\nresponse : " , response)
    

def run_analysis(training, x, response_list) -> list:
    #strx = ' '.join(str(val) for val in x)
    #print("current sentence" , x)
    prompt = "Here is a list of sentences about the stock market and whether they are positive, negative, or neutral statements: " + training + \
    "use this training data to run your own sentiment analysis on the following sentence : " + x + " if the tone of the " \
        "sentence is positive, respond with only the word 'positive'. if it is negative, respond with only the word 'negative'." \
            "If it is neutral, respond with 'neutral'."
    try:
        response = ollama.chat(model = MODEL, messages = [{"role" : "user", "content" : prompt}])  
        r = response.message.content
        rr = r.strip().lower()
        response_list.append(rr)
    except ollama.ResponseError as e:
        print("Error", e.error)

    return response_list

# function returns list of expected values, for confusion matrix
def get_expected() -> list:
    expected = []
    for text in df["Sentiment"]:
        expected.append(text)
    return expected

# function to convert list of values into ints, for MAE
def convert_to_int(list) -> list:
    new_list = []
    for i in list:
        if i == "negative":
            new_list.append(0)
        elif i == "neutral":
            new_list.append(1)
        elif i == "positive":
            new_list.append(2)
    return new_list

def perform_checks(true, predicted) -> None:
    # macro f1:
    macroscore = sklearn.metrics.f1_score(true, predicted, average = 'macro')
    print("macro F1 score: ", macroscore)

    # per-class F1
    f1score = sklearn.metrics.f1_score(true, predicted, average = None)
    print("per-class F1 score: ", f1score)

    # MAE
    num_true = convert_to_int(true)
    num_pred = convert_to_int(predicted)
    mae = sklearn.metrics.mean_absolute_error(num_true, num_pred, multioutput='raw_values')
    print("MAE: ", mae)
    
    # confusion matrix
    print("true:")
    con = sklearn.metrics.confusion_matrix(num_true, num_pred)
    print("confusion matrix: \n", con)

def main() -> None:
    expected = get_expected()

    

    split()

main()