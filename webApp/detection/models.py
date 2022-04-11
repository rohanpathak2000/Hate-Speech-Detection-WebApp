
from django.db import models




class myDataset(models.Model):
    text = models.TextField()
    author = models.TextField()

