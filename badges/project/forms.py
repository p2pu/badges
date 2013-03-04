from django import forms

class ProjectForm(forms.Form):
    title = forms.CharField(max_length=128)
    work_url = forms.CharField()
    steps = forms.CharField(max_length=128)
    reflection = forms.CharField(max_length=128)
    image = forms.FileField()
    tags = forms.CharField(max_length=128)
