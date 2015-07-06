from django import forms

class NoteForm(forms.Form):
        title = forms.CharField(label='The Title', max_length=200)
        text = forms.CharField(label='Text', max_length=200)
        ispublic = forms.BooleanField(label='Public note',required=False)
