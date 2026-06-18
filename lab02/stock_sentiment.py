import pandas as pd
import sklearn
from sklearn.metrics import accuracy_score, f1_score
import ollama
from sklearn.model_selection import train_test_split
import string

MODEL = "gemma3:1b"
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

    # Only perform sentiment analysis on 100 sentences, for time's sake
    trunctest = x_test[:100]
    response_list = []
    prog = 0
    for item in trunctest:
        prog +=1
        response = run_analysis(trainingStr, item, response_list, prog)

    testexpected = y_test[:100]
    perform_checks(testexpected, response)
    
# Runs a sentiment analysis on sentence x, using the training data list to guide generation
def run_analysis(training, x, response_list, prog) -> list:
    prompt = "You are performing a sentiment analysis on remarks about the stock market. Here is a list of sentences about the stock market to use as training data: [" + training + "]. Now, run your own sentiment analysis on the following sentence: " + x + ". if the tone of the " \
        "sentence is positive, respond with only the word 'positive'. Or, if it is negative, respond with only the word 'negative'. Otherwise, if it is neutral, respond with 'neutral'. Your response should not be more than one word."
    try:
        response = ollama.chat(model = MODEL, messages = [{"role" : "user", "content" : prompt}])  
        clean_r = response.message.content.strip().lower().translate(str.maketrans('', '', string.punctuation))
        # check the response is either the word positive, neutral or negative. If not, re-feed into model to correct
        print("analyzing sentence", prog, "/100")
        if(clean_r == "positive" or clean_r == "negative" or clean_r == "neutral"):
            response_list.append(str(clean_r))
        else:
            response = ollama.chat(model = MODEL, messages = [{"role" : "user", "content" : "fix this sentence so it ONLY contains the word 'positive', 'negative', or 'neutral' and respond with ONLY that one word:"+clean_r}])  
            clean_r = response.message.content.strip().lower().translate(str.maketrans('', '', string.punctuation))
            response_list.append(str(clean_r))
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
        i = i.strip()
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
    print(num_true)
    num_pred = convert_to_int(predicted)
    print(num_pred)
    mae = sklearn.metrics.mean_absolute_error(num_true, num_pred, multioutput='raw_values')
    print("MAE: ", mae)
    
    # confusion matrix
    print("true:")
    con = sklearn.metrics.confusion_matrix(num_true, num_pred)
    print("confusion matrix: \n    neg neu pos", "\n neg", con[0], "\n neu", con[1], "\n pos", con[2])
    
    

def main() -> None:
    expected = get_expected()

    split()

main()