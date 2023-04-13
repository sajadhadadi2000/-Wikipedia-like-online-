from django import forms

class Search(forms.Form):
    query = forms.CharField(max_length=100)

class NewPage(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField()