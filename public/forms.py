from django import forms
from .models import Article, MessageContact

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'fichier', 'publie']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'fichier': forms.FileInput(attrs={'class': 'form-control'}),
            'publie': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = MessageContact
        fields = ['nom', 'email', 'sujet', 'message']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'votre@email.com'}),
            'sujet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sujet du message'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Votre message...'}),
        }
