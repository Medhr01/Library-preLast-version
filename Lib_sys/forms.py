from django import forms
from .models import *
from django.core.validators import MaxLengthValidator

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['Nom',  'Prenom', 'Date_de_naissance', 'CNI','image']
        widgets = { 'Nom': forms.TextInput(attrs={'class':"form-control" ,'id':"floatingInput"}),
                    'Prenom': forms.TextInput(attrs={'class':"form-control" ,'id':"floatingInput"}),
                    'Date_de_naissance': forms.DateInput(attrs={'type':'date', 'class':"form-control" ,'id':"floatingInput"}),
                    'CNI': forms.TextInput(attrs={'class':"form-control" ,'id':"floatingInput"}),
                   'image': forms.ClearableFileInput(attrs={'class': "form-control", 'id': "floatingInputImage"}),
                    }


class LivresForm(forms.ModelForm):
    class Meta:
        model = Bouquin
        fields = ['Titre','Auteur','Description','ISBN','Langue','Quantite_achete','Cover']
        widgets = { 'Titre': forms.TextInput(attrs={'class':"form-control" ,'id':"floatingInput"}),
                    'Auteur': forms.TextInput(attrs={'class':"form-control" ,'id':"floatingInput"}),
                    'Description': forms.Textarea(attrs={'style': "height:150px;",'class':"form-control" ,'id':"floatingInput"}),
                    'ISBN': forms.TextInput(attrs={'class':"form-control" ,'id':"floatingInput"}),
                    'Langue': forms.Select(choices=Bouquin.LANGUE_CHOICES, attrs={'class':"form-select" ,'id':"floatingInput"}),
                    'Quantite_achete': forms.NumberInput(attrs={'min': Bouquin.Quantite_Disponible , 'class':"form-control" ,'id':"floatingInput"}),
                    'Cover': forms.ClearableFileInput(attrs={'class': "form-control", 'id': "floatingInputImage"})
                    }

class LivreForm(forms.ModelForm):
    class Meta:
        model = Bouquin
        fields = ['Titre','Auteur','Description','Langue']
        widgets = { 'Titre': forms.TextInput(attrs={'class':"form-control" ,'id':"floatingInput"}),
                    'Auteur': forms.TextInput(attrs={'class':"form-control" ,'id':"floatingInput"}),
                    'Description': forms.Textarea(attrs={'style': "height:150px;",'class':"form-control" ,'id':"floatingInput"}),
                    'Langue': forms.Select(choices=Bouquin.LANGUE_CHOICES, attrs={'class':"form-select" ,'id':"floatingInput"}),
                    } 

        

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)