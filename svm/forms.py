from django import forms

class SeqForm(forms.Form):
    seq = forms.CharField(label='Peptide sequence', max_length=100)

