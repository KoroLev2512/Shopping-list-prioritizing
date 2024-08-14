from django import forms
from .models import GoodsModel

class UserForm(forms.ModelForm):
    class Meta:
        model = GoodsModel
        fields = ('name',)
