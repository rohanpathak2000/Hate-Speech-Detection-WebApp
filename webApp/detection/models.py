
from django.db import models

# Create your models here.
#from adaptor.model import CsvModel
#from adaptor.fields import CharField, IntegerField, BooleanField

#from sympy import true


class myDataset(models.Model):
    text = models.TextField()
    label = models.TextField()
    split = models.TextField()
    author = models.TextField()

