from django import forms

class BadgeForm(forms.Form):
    image = forms.FileField()
    title = forms.CharField(max_length=128)
    description = forms.CharField(max_length=128)
    requirements = forms.CharField(max_length=1024)
