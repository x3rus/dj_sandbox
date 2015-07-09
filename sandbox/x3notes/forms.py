from django import forms
from django.forms import ModelForm

from django.db import models
from .models import Note, NoteAuthEmail

# Une methode :
#class NoteForm(ModelForm):
#    class Meta:
#        model=Note
#        fields = ['title','text','ispublic']

class NoteForm(forms.Form):
        title = forms.CharField(label='The Title', max_length=200)
        text = forms.CharField(label='Text', max_length=200)
        ispublic = forms.BooleanField(label='Public note',required=False)

class NoteEditForm(ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'text', 'ispublic']

