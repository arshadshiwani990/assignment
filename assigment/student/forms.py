from django import forms
from .models import Student


class StudentForm(forms.ModelForm):


    class Meta:
        model = Student
        fields = ['name','phone', 'email', 'grade']

class StudentFormUpdate(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['name','grade'] 
