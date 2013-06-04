from django import forms
from django.utils.translation import ugettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML
from crispy_forms.layout import ButtonHolder
from crispy_forms.layout import Submit

class ProjectForm(forms.Form):
    title = forms.CharField(
        max_length=255,

        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('What is the name of your masterpiece?'),
                'class': 'span9'
            }),
        error_messages={
            'required': _('Please tell us how do you want to call this project')
        })

    work_url = forms.CharField(
        required=True,
        label=_('Project URL'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Where can we find your work on the web?'),
                'class': 'span9'
            }),
        error_messages={
            'required': _('Please tell us how can we see your masterpiece')
        })

    description = forms.CharField(
        max_length=1024,
        label=_('Project description'),
        widget=forms.Textarea(
            attrs={
                'placeholder': _('What steps did you take to complete this project? '
                                 '(This helps experts give you more precise feedback.)'),
                'class': 'ckeditor span9'
            }),
        error_messages={
            'required': _('Please tell us about your project')
        })

    reflection = forms.CharField(
        max_length=1024,
        label=_('Second thoughts?'),
        widget=forms.Textarea(
            attrs={
                'placeholder': _('What might you do differently next time? '
                                 '(Experts might have ideas and suggestions for you.)'),
                'class': 'ckeditor span9'
            }),
        error_messages={
            'required': _('Is there something you would do differently')
        })

    image = forms.FileField(
        label='Project cover image',
        required=True,
        widget=forms.FileInput(
            attrs={
                'title': _('Upload a screenshot of your glorious creation.')
            }),
        error_messages={
            'required': _('Please give your project an image')
        }
    )

    tags = forms.CharField(
        max_length=255,
        label=_('Tags'),
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Add some tags so folks can find your masterpiece.'),
                'class': 'span9'
            }),
    )

    @property
    def create_project(self):
        helper = FormHelper()
        helper.form_id = 'project-create-form'
        helper.form_class = 'span9'
        helper.form_tag = True
        helper.layout = Layout(
            Layout(
                'title',
                'work_url',
                'description',
                'reflection',
                'image',
                'tags',
            ),
            ButtonHolder(
                Submit('submit', _('Create a project'), css_class='btn btn-primary large'),
            )
        )
        return helper



class FeedbackForm(forms.Form):
    good = forms.CharField(
        max_length=1024,
        label=_('Kudos'),
        widget=forms.Textarea(
            attrs={
                'placeholder': _('What is strong and outstanding about the project?'),
                'class': 'ckeditor span9 green'
            }),
        error_messages={
            'required': _('Please tell us what you think is good about this project')
        })

    bad = forms.CharField(
        max_length=1024,
        label=_('Questions'),
        widget=forms.Textarea(
            attrs={
                'placeholder': _('What questions do you have about the project? '
                                 'Are there pieces you are not so sure about?'),
                'class': 'ckeditor span9 yellow'
            }),
        error_messages={
            'required': _('Please tell us what puzzles you about the project')
        })
    ugly = forms.CharField(
        max_length=1024,
        label=_('Concerns'),
        widget=forms.Textarea(
            attrs={
                'placeholder': _('What needs further development? '
                                 'Do you have ideas or resources that could help the project?'),
                'class': 'ckeditor span9 red'
            }),
        error_messages={
            'required': _("Please tell us what you don't agree with in the project")
        })
    award_badge = forms.BooleanField(required=False)

    @property
    def give_feedback(self):
        helper = FormHelper()
        helper.form_id = 'feedback-create-form'
        helper.form_class = 'feedback-create-form span9'
        helper.form_tag = True
        helper.layout = Layout(
            Layout(
                'good',
                'bad',
                'ugly',
                HTML(u"""<p class="control-group-label feedback-form-award-info">
                            Has this project met all of the criteria for this Badge?
                            If so, go ahead and award it!
                        </p>
                        <div class="control-group checkbox-group award-badge">
                            <input type="checkbox" value="0" id="award-badge-input" name="award_badge" />
                            <label for="award-badge-input"></label>
                        </div>
                     """),
            ),
            ButtonHolder(
                HTML("""
                <p for="give-feedback" class="control-group-label feedback-form-award-info">Or you can choose to submit your feedback and ask the learner to revise and submit.</p>
                """),
                Submit('submit', _('Submit feedback'), css_class='btn btn-primary btn-large'),
            )
        )
        return helper


class RevisionForm(forms.Form):
    work_url = forms.CharField(
        required=False,
        label=_('New work URL (optional)'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Give us new place to see your project.'),
                'class': 'span9'
            }),
    )

    improvement = forms.CharField(
        max_length=1024,
        label=_('Improvements made'),
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': _('What changes have you made to the project?'),
                'class': 'span9 ckeditor'
            }),
        error_messages={
            'required': _('Please tell us about the changes')
        }
    )

    @property
    def revise_feedback(self):
        helper = FormHelper()
        helper.form_id = 'revision-create-form'
        helper.form_class = 'span9'
        helper.form_tag = True
        helper.layout = Layout(
            Layout(
                'work_url',
                'improvement',
            ),
            ButtonHolder(
                Submit('submit', _('Submit revision'), css_class='btn btn-primary btn-large'),
            )
        )
        return helper
