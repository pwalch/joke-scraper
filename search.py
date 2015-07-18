#!/usr/bin/python3

# Search engine based on TDF-IDF for scraped jokes.
# Usage: ./search.py word1 word2 word3...
# Example: ./search.py dog blind

import json
import re
import sys

import tfidf

def extract_word_list(text):
    return re.compile("\w+").findall(text)

def top_joke_list(jokeDict, table, searchWords):
    sortedSimilarities = sorted(table.similarities(searchWords), key=lambda similarity: similarity[1], reverse=True)

    topSimilarities = sortedSimilarities[:5]
    topJokeTitles = [similarity[0] for similarity in topSimilarities]
    topJokeList = [jokeDict[jokeTitle] for jokeTitle in topJokeTitles]

    return topJokeList

def runSearch(searchWords):
    with open("data/jokes.json") as jokeFile:
        jokeDict = {joke["title"]: joke for joke in json.load(jokeFile)}

        table = tfidf.tfidf()
        for joke in jokeDict.values():
            table.addDocument(joke["title"], extract_word_list(joke["content"]))

        for joke in top_joke_list(jokeDict, table, searchWords):
            print("*** " + joke["title"])
            print(joke["content"])
            print("=======================")

searchWords = sys.argv[1:]
if len(searchWords) == 0:
    print("Provide at least one word to search.")
else:
    runSearch(searchWords)
