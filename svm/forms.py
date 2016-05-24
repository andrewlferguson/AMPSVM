from django import forms

class SeqForm(forms.Form):
    seq = forms.CharField(label='Peptide sequence (8-100 residues)', max_length=100)

