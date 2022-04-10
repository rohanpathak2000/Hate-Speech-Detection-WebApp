
from django.db import models

# Create your models here.

class myDataset(models.Model):
    text = models.TextField()
    author = models.TextField()

