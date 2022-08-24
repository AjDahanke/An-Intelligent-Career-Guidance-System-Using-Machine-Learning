

from asyncio.windows_events import NULL
from django.db import models


# Create your models here.
class Ocr(models.Model):
    name=models.CharField(max_length=100,default="name ")
    email=models.CharField(max_length=100,default="Email")
    passw=models.CharField(max_length=100,default="")
  
    image = models.ImageField(upload_to='images/')
    education=models.CharField(max_length=100,default=NULL)
    income=models.CharField(max_length=100,default=0)
    def __str__(self):
     return self.name
    
