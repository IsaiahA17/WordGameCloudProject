import time
from datetime import datetime
import random
import uuid
import os
from azure.cosmos import CosmosClient

COSMOS_ENDPOINT = os.environ.get("COSMOS_ENDPOINT")
COSMOS_KEY = os.environ.get("COSMOS_KEY")

client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
db = client.get_database_client("wordgame")
game_container = db.get_container_client("gamedetails")

def checkEnoughLetters(wordsEntered):
    if (len(wordsEntered) < 4):
        print("Word does not enough letters")
        return False
    else:
        print("Word has enough letters")
        return True

def checkRealWord(wordsEntered):
    with open("words-huge") as wf:
        wordsH = {line.strip("\n").replace("'s", "").lower() for line in wf}  
    wordsH = sorted(wordsH)[1:]
    wordsEntered = wordsEntered.lower()
    if(wordsEntered not in wordsH):
        print("Word is not in dictionary")
        return False
    else:
        print("Word is in dictionary")
        return True

def checkDuplicates(wordEntered):
    wordList = wordEntered.split()
    wordListRange = len(wordList) - 1
    for i in range(wordListRange):
        wordList[i] = wordList[i].lower()
    lowercaseWordList = wordList
    lowercaseWordList.sort()
    for i in range(wordListRange):
        if(lowercaseWordList[i] == lowercaseWordList[i + 1]):
            print("Duplicates exist in the entered string")
            return False
    print("There are no duplicates found")
    return True

def checkSourceCopy(sourceWord,wordEntered):
    sourceWord = sourceWord.lower()
    wordEntered = wordEntered.lower()
    if(sourceWord == wordEntered):
        print("Word is the same as source")
        return False
    else:
        print("Word is not the same as source")
        return True

def checkLetterCountAndValidity(sourceWord,testWord):
    sourceWord = sourceWord.lower()
    testWord = testWord.lower()
    for i in range(len(testWord)):
        if(testWord[i] not in sourceWord):
            print("Invalid Word, a letter does not exist in source word")
            return False
        else:
            testLetterCount = testWord.count(testWord[i])
            sourceLetterCount = sourceWord.count(testWord[i])
            if(testLetterCount > sourceLetterCount):
                print("Invalid Word, a letter was used more times than in source word")
                return False
    print("Word has less letters than source word and letters do not show up more times than in source word")
    return True

def checkValidCount(enteredString):
    enteredStringList = enteredString.split()
    if(len(enteredStringList) != 7):
        print("String doesn't have enough words or has too many words. (Enter 7)")
        return False
    print("String has seven words")
    return True

def applyRuleset(sourceWord,enteredString,timeTaken):
    if(checkValidCount(enteredString) == False):
        return "Seven words need to be entered", False, 0
    if(checkDuplicates(enteredString) == False):
        return "There are duplicate words in the answer", False, 0
    print("\n")
    enteredWords = enteredString.split()
    for word in enteredWords:
        print("Checking word: ",word)
        if(checkEnoughLetters(word) == False):
            return "Invalid number of letters in the word: " + word, False, 0
        if(checkRealWord(word) == False):
            return "Invalid. The word, " + word + " is not in the dictionary", False, 0
        if(checkSourceCopy(sourceWord,word) == False):
            return "Invalid. The word, " + word + " is a copy of the sourceword", False, 0
        if(checkLetterCountAndValidity(sourceWord,word) == False):
            return "Invalid. The word, " + word + " contains at least one invalid letter", False, 0
    timeTaken = round(timeTaken, 2)
    timeTaken = str(timeTaken)
    winMessage = "Congratulations. You win! Time: " + timeTaken + " seconds"
    return winMessage,True,timeTaken

def getSourceWord():
    with open("words-huge") as wf:
        words = [line.strip("\n").replace("'s", "").lower() for line in wf]
    return random.choice(words)

def getLogs():
    query = "SELECT c.success, c.sourceWord, c.attempt, c.dateTime, FROM c"
    items = list(game_container.query_items(query=query, enable_cross_partition_query=True))
    return [(i["success"], i["sourceWord"], i["attempt"], i["dateTime"]) for i in items]

def getHighScores():
    query = "SELECT TOP 10 c.time, c.who, c.sourceWord, c.attempt FROM c WHERE c.success = 'WIN' AND c.time > 0"
    items = list(game_container.query_items(query=query, enable_cross_partition_query=True))
    return [(i["time"], i["who"], i["sourceWord"], i["attempt"]) for i in items]

def enterToDatabase(name, source_word, success, attempt, time):
    document = {
        "id": str(uuid.uuid4()),
        "who": name,
        "sourceWord": source_word,
        "success": "WIN" if success else "LOSS",
        "attempt": attempt,
        "time": float(time),
        "dateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    game_container.create_item(body=document)