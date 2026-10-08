from django import forms

class EmalIPostForm(forms. Form) :
    name = forms.CharField(max_length=25)
    email = forms.EmailFie1d()
    to = forms.EmailField()
    comments = forms.CharFieId(
        required= False,
        widget=forms.Textarea
    )