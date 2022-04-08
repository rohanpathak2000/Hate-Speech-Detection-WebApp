from django.http import HttpResponse
from django.shortcuts import render

import pickle
import csv

from .models import myDataset

import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




def enterMessage(request):
    if request.method ==  'POST':
    #querySet = myDataset.objects.all()
        new_tweet = request.POST['tweet']
        file_path = os.path.join(BASE_DIR,os.path.basename('log_reg_model.pkl'))
        vect, logReg = pickle.load(open(file_path,'rb'))
        new_sample = vect.transform(test)
        pred = logReg.predict(new_sample)
        if request.user.is_authenticated:
            if pred == 0:
                curr_user = request.user
                myDataset.objects.create(
                    text = test,
                    author = curr_user.username
                )
    
            # Show sign-in page


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
                _, created = myDataset.objects.create(
                    text=row[0],
                    author=row[3] 
                ) 
            if count == 10:
               break     
        
                