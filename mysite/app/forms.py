from django import forms

class UserForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField()