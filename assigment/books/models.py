from django.db import models

class Books(models.Model):

    title = models.CharField(max_length=255,null=True)
    isbn=models.CharField(max_length=20,null=True)
    imageURL = models.URLField(max_length=500, null=True)
    author=models.CharField(max_length=10,null=True)
    url = models.CharField(max_length=500,null=True)
