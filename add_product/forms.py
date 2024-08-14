from django import forms
from .models import GoodsModel

class GoodForm(forms.ModelForm):
    class Meta:
        model = GoodsModel
        fields = ('name',)
