from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

import pickle
import csv

from .models import myDataset

import os,re,nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def remove_numbers(text):
    # define the pattern to keep
    pattern = r'[^a-zA-z.,!?/:;\"\'\s]' 
    return re.sub(pattern, '', text)

def remove_urls_mentions(text):
    return re.sub(r"(?:\@|https?\://)\S+", "", text)

def textPreprocessing(data):
    lowerSet = []
    for sentence in data:
        lowerSet.append(str.lower(sentence))
    filtered_sentences = []
    stop_words = set(stopwords.words('english'))
    # Removing stopwords
    for text in lowerSet:
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
    
    filtered_sentences_2 = [remove_numbers(sentence) for sentence in filtered_sentences_2]
    filtered_sentences_2 = [remove_urls_mentions(sentence) for sentence in filtered_sentences_2]
    lemmatizer = WordNetLemmatizer()

    filtered_sentences_2 = [lemmatizer.lemmatize(sentence) for sentence in filtered_sentences_2]
    filtered_sentences_3 = []

    for sentence in filtered_sentences_2:
        wordsToAdd = []
        for word in word_tokenize(sentence):
            if len(word) >= 3 and word.isalpha():
                wordsToAdd.append(word)
        filtered_sentences_3.append(' '.join(wordsToAdd))

    return filtered_sentences_3
# Removing punctuation




def home(request):
    if request.method ==  'POST':
    #querySet = myDataset.objects.all()
        test = []
        new_tweet = request.POST['tweet']
        test.append(new_tweet)
        new = textPreprocessing(test)
        file_path = os.path.join(BASE_DIR,os.path.basename('log_reg_model.pkl'))
        vect, logReg = pickle.load(open(file_path,'rb'))
        new_sample = vect.transform(new)
        pred = logReg.predict(new_sample)
        if request.user.is_authenticated:
            if pred == 0:
                curr_user = request.user
                myDataset.objects.create(
                    text = test[0],
                    author = curr_user.username
                )
            else:
                messages.info(request,'Hate Speech Detected')
            return redirect('/')
    
        else:
            return redirect('/login')    # Show sign-in page
    else:
        querySet = myDataset.objects.all()
        obj = {'qs' : querySet}
        return render(request,'index.html',obj)

    
def storeValues(request):
     with open("C:\\Win Sem 21-22\\CSE2026 - CC\\Project\\Assets\\dataset.csv") as f:
        reader = csv.reader(f)
        next(reader,None)
        count = 0
        for row in reader:
            if row[1] == "nothate":
                count = count + 1
            #print(row)
            #break
                _, created = myDataset.objects.get_or_create(
                    text=row[0],
                    author=row[3] 
                ) 
            if count == 40:
               break     
        
                