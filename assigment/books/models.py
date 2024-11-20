from django.db import models

class Books(models.Model):

    title = models.CharField(max_length=255,null=True, blank=True)
    isbn=models.CharField(max_length=20,null=True, blank=True)
    imageURL = models.URLField(max_length=500, null=True, blank=True)
    author=models.CharField(max_length=10,null=True, blank=True)
    url = models.CharField(max_length=500,null=True, blank=True)
