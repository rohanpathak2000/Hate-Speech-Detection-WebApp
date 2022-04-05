from django.shortcuts import render
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
# Create your views here.
from nltk.corpus import stopwords
import re
from nltk.stem import WordNetLemmatizer
import numpy as np

import csv

from .models import myDataset



def toLower(data):
    res = []
    for sentence in data:
        res.append(str.lower(sentence))
    return res

def remove_numbers(text):
    # define the pattern to keep
    pattern = r'[^a-zA-z.,!?/:;\"\'\s]' 
    return re.sub(pattern, '', text)


def textPreprocessing():
    cleanset = toLower(data)
    stop_words = set(stopwords.words('english'))
    filtered_sentences = []
    for text in cleanset:
        content = []
        for i in word_tokenize(text):
            if i not in stop_words:
                content.append(i)
        filtered_sentences.append(' '.join(content))
    

    #nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
  
    filtered_sentences = []

# Removing stopwords
    for text in cleanset:
        content = []
        for i in word_tokenize(text):
            if i not in stop_words:
                content.append(i)
        filtered_sentences.append(' '.join(content))
    

    tokenizer = nltk.RegexpTokenizer(r"\w+")

    filtered_sentences_2 = []

    for sentence in filtered_sentences:
        new_words = tokenizer.tokenize(sentence)
        filtered_sentences_2.append(' '.join(new_words))


    # Removing punctuation

    for sentence in filtered_sentences:
        new_words = tokenizer.tokenize(sentence)
        filtered_sentences_2.append(' '.join(new_words))

    filtered_sentences_2 = [remove_numbers(sentence) for sentence in filtered_sentences_2]
    lemmatizer = WordNetLemmatizer()

    filtered_sentences_2 = [lemmatizer.lemmatize(sentence) for sentence in filtered_sentences_2]

    filtered_sentences_3 = []

    for sentence in filtered_sentences_2:
        wordsToAdd = []
    for word in word_tokenize(sentence):
        if len(word) >= 3 and word.isalpha():
            wordsToAdd.append(word)
    filtered_sentences_3.append(' '.join(wordsToAdd))
    filtered_sentences_3 = [sentence.strip() for sentence in filtered_sentences_3]
    return filtered_sentences_3     

    
def mainMethod():
    all_entries = myDataset.objects.all()
    for i in range ()    



def storeValues(request):
     with open("C:\\Win Sem 21-22\\CSE2026 - CC\\Project\\Assets\\dataset.csv") as f:
        reader = csv.reader(f)
        next(reader,None)
        for row in reader:
            #print(row)
            #break
            _, created = myDataset.objects.create(
                text=row[0],
                label=row[1],
                split=row[2],
                author=row[3] 
                ) 
                
        
                