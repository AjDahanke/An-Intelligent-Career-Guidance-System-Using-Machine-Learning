from .models import *
from django import forms

class StudentForm(forms.ModelForm):
  
    class Meta:
        
        model = Ocr
        fields = ['name', 'email','passw','image','education','income']
        widgets = {
      'passw': forms.PasswordInput(),
      
         }