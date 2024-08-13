from django import forms
 
class UserForm(forms.Form):
    name = forms.CharField()
    family = forms.CharField()