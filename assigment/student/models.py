from django.db import models

class Student(models.Model):

    name=models.CharField(null=False, max_length=100)
    phone = models.IntegerField(null=False)
    email = models.EmailField(null=False,max_length=50)
    grade = models.IntegerField(null=False)