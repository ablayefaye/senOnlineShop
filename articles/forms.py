from django import forms
from django_resized.forms import ResizedImageFieldFile
from database.models import *

# formulaire d'enregistrement article
class SaveArticleForm(forms.ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'type':'text','class': 'form-control','placeholder':'Nom article *','autofocus':'true'}))    
    price = forms.CharField(label='', widget=forms.TextInput(attrs={'type':'number','class': 'form-control','placeholder':'Prix article *'}))    
    old_price = forms.CharField(label='', widget=forms.TextInput(attrs={'type':'number','class': 'form-control','placeholder':'Ancien prix'}), required=False)    
    number_of_exemplaire = forms.CharField(label='', widget=forms.TextInput(attrs={'type':'number','class': 'form-control','placeholder':'Nombre exemplaires *'}))    
    description = forms.CharField(label='', widget=forms.TextInput(attrs={'type':'text','class': 'form-control','placeholder':'Description article'}), required=False)    
    category = forms.ModelChoiceField(Category.objects.all(),label='Catégories')
    class Meta:
        model = Article 
        exclude = ('user',) 


# formulaire d'enregistrement article
class SaveArticleFormInCategory(forms.ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'type':'text','class': 'form-control','placeholder':'Nom article *','autofocus':'true'}))    
    price = forms.CharField(label='', widget=forms.TextInput(attrs={'type':'number','class': 'form-control','placeholder':'Prix article *'}))    
    old_price = forms.CharField(label='', widget=forms.TextInput(attrs={'type':'number','class': 'form-control','placeholder':'Ancien prix'}), required=False)    
    number_of_exemplaire = forms.CharField(label='', widget=forms.TextInput(attrs={'type':'number','class': 'form-control','placeholder':'Nombre exemplaires *'}))    
    description = forms.CharField(label='', widget=forms.TextInput(attrs={'type':'text','class': 'form-control','placeholder':'Description article'}), required=False)    
    class Meta:
        model = Article 
        exclude = ('user','category') 