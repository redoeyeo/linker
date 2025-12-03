# forms.py
from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(
        label='Поиск статьи',
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите поисковый запрос...',
            'class': 'form-control'
        })
    )
