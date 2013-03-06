from django import forms

class ProjectForm(forms.Form):
    title = forms.CharField(max_length=128)
    work_url = forms.CharField()
    steps = forms.CharField(max_length=128)
    reflection = forms.CharField(max_length=128)
    image = forms.FileField()
    tags = forms.CharField(max_length=128)


class FeedbackForm(forms.Form):
    good = forms.CharField(max_length=1024)
    bad = forms.CharField(max_length=1024)
    ugly = forms.CharField(max_length=1024)
    award_badge = forms.BooleanField(required=False)


class RevisionForm(forms.Form):
    work_url = forms.CharField(required=False)
    improvement = forms.CharField(max_length=128)
