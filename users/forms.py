from django import forms
import re
from django.core.exceptions import ValidationError
from . import models


def validate_fullname(text):
    if re.search(r'^[a-zA-Z0-9]{4,20}$',text):
 
        if models.User.objects.filter(username=text).exists():
            raise ValidationError('Username already taken')
        return None

    
    
    raise ValidationError('Fullname not valid')
def validate_password(text):
    if len(text)>=8 and re.search(r'[a-z]',text) and re.search(r'[A-Z]',text) and re.search(r'[0-9]',text) and re.search(r'[^a-zA-Z0-9]',text):
        return None
    raise ValidationError("Password not valid")

def validate_email(text):
    if re.search(r'^(.+){3,}@(.+){2,20}\.(.+){2,10}$',text):
        if models.User.objects.filter(email=text).exists():
            raise ValidationError('Email Already Taken')
        return None
    
    raise ValidationError('Email not valid')

class SignupForm(forms.Form):
    username=forms.CharField(max_length=20,min_length=4,validators=[validate_fullname])
    password=forms.CharField(min_length=8,max_length=50,validators=[validate_password])
    email=forms.EmailField(max_length=50,validators=[validate_email])


