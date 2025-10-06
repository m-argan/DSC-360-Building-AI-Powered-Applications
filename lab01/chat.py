import ollama
import re
import os
import datetime
from datetime import date
from datetime import datetime

# Set all different date/time combinations to variables
def getDateWDashes() -> str:
    day = date.today()
    strDate = ''.join(str(day))
    return strDate

def getDateWUnderscore() -> str:
    now = datetime.now()
    newdate = now.strftime("%Y%m%d" + "_" + "%H%M%S") 
    return newdate

def getDateWColon() -> str:
    now = datetime.now()
    newdate = now.strftime("%Y"+"-"+"%m"+"-"+"%d"+"T"+"%H"+":"+"%M"+":"+"%S") 
    return newdate

date_with_dashes = getDateWDashes()
date_with_underscore = getDateWUnderscore()
date_with_colon = getDateWColon()

def handleExit() -> None:
    print("Goodbye!")

def queryOllama(prompt: str, context: str, modelName: str, FILE: str) -> str:
    # immediately add user's input to the conversation history and transcript
    context.append({"role":"user", "content" : prompt})
    addtoFile(prompt, "user", FILE)
    # prompt model to recieve history and respond accordingly
    contextPrompt = ("you are having a conversation with a user. respond to their prompt while taking into account the context of the conversation up until this point. Here is the conversation history: ", context, ' and here is the new prompt: ', prompt)
    strPrompt = ' '.join(str(val) for val in contextPrompt)
    try:
        output = ollama.chat(model = modelName, messages = [{"role":"user", "content" : strPrompt}])
        assistantoutput = {"role":"assistant", "content" : output.message.content}
        # add assistant response to transcript
        addtoFile(output.message.content, modelName, FILE)
    except ollama.ResponseError as e:
        print("Error ", e.error)

    # add response to history and print to terminal
    context.append(assistantoutput)
    print(output.message.content)

    return context
    
# Helper function to remove model name from string
def extractModel(input: str) -> str:
    start = "<"
    end = ">"
    start_index = input.find(start)
    end_index = input.find(end)
 
    if start_index != -1 and end_index != -1:
        extracted_text = input[start_index + len(start):end_index].strip()
    return extracted_text

def addtoFile(text: str, role: str, FILE: str) -> None:
    date = getDateWColon()
    logLine = "\n[" + date + "]" + "[" + role + "]" + " " + text
    errorLine = "\n[" + date + "]" + "[" + "error" + "]" + " " + "There was an error"
    try:
        with open(FILE, 'a') as f:
            f.write(logLine)
            f.write("\n")
    except IOError as e:
        f.write(errorLine)

def startTranscript() -> str:
    # Create folder for the day
    directoryPath = date_with_dashes
    strDirectoryPath = ''.join(str(item) for item in directoryPath)
    print(strDirectoryPath)

    try:
        os.makedirs(strDirectoryPath, exist_ok=True)
    except OSError as e:
        print(f"Error creating folder structure '{strDirectoryPath}': {e}")

    # Create new file for session
    file = strDirectoryPath+"/"+date_with_underscore+".txt"
    f = open(file, "x")
    return file

def main():
    userInput = ""
    context = ["conversation history:"]
    MODEL = "gemma3:1b"
    print("Welcome! I am a chatbot! I live to serve, ask me anything! Press /exit to stop and /model to switch models")
    FILE = startTranscript()

    while True:
        userInput = input("type here:").strip()
        if '/exit' in userInput:
            handleExit()
            break
        else:
            if '/new' in userInput:
                context = ["conversation history:"]
                print("Conversation history has been cleared! Starting fresh.")
            if '/model' in userInput:
                model = extractModel(userInput)
                MODEL = model
                print("changed to ", MODEL, "model")
            context = queryOllama(userInput, context, MODEL, FILE)

main()