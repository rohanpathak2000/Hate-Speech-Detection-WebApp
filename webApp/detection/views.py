from django.http import HttpResponse
from django.shortcuts import render
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
# Create your views here.
from nltk.corpus import stopwords
import re
from nltk.stem import WordNetLemmatizer
import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB

import csv

from .models import myDataset

from sklearn.linear_model import LogisticRegression



def toLower(data):
    res = []
    for sentence in data:
        res.append(str.lower(sentence))
    return res

def remove_numbers(text):
    # define the pattern to keep
    pattern = r'[^a-zA-z.,!?/:;\"\'\s]' 
    return re.sub(pattern, '', text)


def textPreprocessing(data):
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

### cfehome.utils.py or the root of your project conf

def get_model_field_names(model, ignore_fields=['content_object']):
    '''
    ::param model is a Django model class
    ::param ignore_fields is a list of field names to ignore by default
    This method gets all model field names (as strings) and returns a list 
    of them ignoring the ones we know don't work (like the 'content_object' field)
    '''
    model_fields = model._meta.get_fields()
    model_field_names = list(set([f.name for f in model_fields if f.name not in ignore_fields]))
    return model_field_names


def get_lookup_fields(model, fields=None):
    '''
    ::param model is a Django model class
    ::param fields is a list of field name strings.
    This method compares the lookups we want vs the lookups
    that are available. It ignores the unavailable fields we passed.
    '''
    model_field_names = get_model_field_names(model)
    if fields is not None:
        '''
        we'll iterate through all the passed field_names
        and verify they are valid by only including the valid ones
        '''
        lookup_fields = []
        for x in fields:
            if "__" in x:
                # the __ is for ForeignKey lookups
                lookup_fields.append(x)
            elif x in model_field_names:
                lookup_fields.append(x)
    else:
        '''
        No field names were passed, use the default model fields
        '''
        lookup_fields = model_field_names
    return lookup_fields

def qs_to_dataset(qs, fields=None):
    '''
    ::param qs is any Django queryset
    ::param fields is a list of field name strings, ignoring non-model field names
    This method is the final step, simply calling the fields we formed on the queryset
    and turning it into a list of dictionaries with key/value pairs.
    '''
    
    lookup_fields = get_lookup_fields(qs.model, fields=fields)
    return list(qs.values(*lookup_fields))

def convert_to_dataframe(qs, fields=None, index=None):
    '''
    ::param qs is an QuerySet from Django
    ::fields is a list of field names from the Model of the QuerySet
    ::index is the preferred index column we want our dataframe to be set to
    
    Using the methods from above, we can easily build a dataframe
    from this data.
    '''
    lookup_fields = get_lookup_fields(qs.model, fields=fields)
    index_col = None
    if index in lookup_fields:
        index_col = index
    elif "id" in lookup_fields:
        index_col = 'id'
    values = qs_to_dataset(qs, fields=fields)
    df = pd.DataFrame.from_records(values, columns=lookup_fields, index=index_col)
    return df



def mainMethod(request):
    querySet = myDataset.objects.all()
    df = convert_to_dataframe(querySet)
    raw_text = df['text']
    corpus = textPreprocessing(raw_text)
    testing_indices = []
    training_indices = []
    for i in range(0,len(df)):
        if df.iloc[i,2] == 'test':
            testing_indices.append(i)
        else:
            training_indices.append(i)
    Y = df['label']
    Y = [1 if i == "hate" else 0 for i in Y]
    vect = CountVectorizer(max_features=30000,ngram_range=(1,3))
    vect.fit(corpus)
    bag_of_words = vect.transform(corpus)
    X = bag_of_words.toarray()
    X_train = [X[i] for i in range(len(X)) if i in training_indices]
    X_test = [X[i] for i in range(len(X)) if i in testing_indices]
    Y_train = [Y[i] for i in range(len(Y)) if i in training_indices]
    Y_test = [Y[i] for i in range(len(Y)) if i in testing_indices]
    logReg = LogisticRegression(max_iter = 1000)
    logReg = logReg.fit(X_train, Y_train)
    score = accuracy_score(Y_test, logReg.predict(X_test))
    print(score)

    

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
                
        
                