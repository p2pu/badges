from django import forms

class ProjectForm(forms.Form):
    title = forms.CharField(max_length=255)
    work_url = forms.CharField()
    description = forms.CharField(max_length=1024)
    reflection = forms.CharField(max_length=1024)
    image = forms.FileField()
    tags = forms.CharField(max_length=255)


class FeedbackForm(forms.Form):
    good = forms.CharField(max_length=1024)
    bad = forms.CharField(max_length=1024)
    ugly = forms.CharField(max_length=1024)
    award_badge = forms.BooleanField(required=False)


class RevisionForm(forms.Form):
    work_url = forms.CharField(required=False)
    improvement = forms.CharField(max_length=1024)
