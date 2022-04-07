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

import pickle
import csv

from .models import myDataset

from sklearn.linear_model import LogisticRegression


import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




def mainMethod(request):
    #querySet = myDataset.objects.all()
    test = ['people should not be judged based on colour']
    file_path = os.path.join(BASE_DIR,os.path.basename('log_reg_model.pkl'))
    vect, logReg = pickle.load(open(file_path,'rb'))
    new_sample = vect.transform(test)
    pred = logReg.predict(new_sample)
    print(pred)

    

def storeValues(request):
     with open("C:\\Win Sem 21-22\\CSE2026 - CC\\Project\\Assets\\dataset.csv") as f:
        reader = csv.reader(f)
        next(reader,None)
        count = 0
        for row in reader:
            count = count + 1
            #print(row)
            #break
            _, created = myDataset.objects.create(
                text=row[0],
                label=row[1],
                split=row[2],
                author=row[3] 
                ) 
            if count == 10:
               break     
        
                