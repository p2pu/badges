"""
Form for creating a Badge
"""
from django import forms
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import Layout
from crispy_forms.layout import ButtonHolder
from p2pu_user import models as p2pu_user_api
from parsley.decorators import parsleyfy


@parsleyfy
class BadgeForm(forms.Form):
    title = forms.CharField(
        label=_('We Call This Nifty Badge:'),
        required=True,
        max_length=128,
        help_text=_('Maximum 128 characters'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Good titles are clear, concise and snappy '
                                 '-- like a headline.'),
                'class': 'span7',
                'data-remote': reverse_lazy('name_search')
            }),
        error_messages={
            'required': _('Please tell us how you want to call your Badge')
        })

    image_uri = forms.FileField(
        label='',
        required=True,
        widget=forms.FileInput(
            attrs={
                'title': _('Select a spiffy icon for your Badge')
            }),
        error_messages={
            'required': _('Please give your nifty Badge an image')
        }
    )
    description = forms.CharField(
        label=_('Describe your Badge:'),
        required=True,
        max_length=128,
        help_text=_('Should be one paragraph, maximum 128 characters'),
        widget=forms.Textarea(
            attrs={
                'cols': 80,
                'rows': 3,
                'class': 'span7',
                'placeholder': 'What is this Badge for? '
                               'A course? An event? '
                               'A certain type of project?'}),
        error_messages={
            'required': _('Please describe your Badge')
        })

    requirements = forms.CharField(
        label=_('Criteria to receive the Badge:'),
        required=True,
        widget=forms.Textarea(
            attrs={'cols': 80, 'rows': 6, 'class': 'span7 ckeditor',
                   'placeholder': _("Here it's good to list specific skills folks will need to show "
                                    "they've mastered. It's useful to step them out so the "
                                    "Experts can identify them.")}),
        error_messages={
            'required': _('Please tell us what are the requirements for the Badge')
        })

    partner = forms.ChoiceField(
        label=_('Is this an "Affiliate Badge"?'),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        # Check if form is in editing mode
        editing = False
        if 'editing' in kwargs:
            editing = kwargs.pop('editing')

        user_uri = kwargs.pop('user_uri')
        choices = [None] + p2pu_user_api.get_partners_for_user(user_uri)

        published = False
        if 'published' in kwargs:
            published = kwargs.pop('published')

        super(BadgeForm, self).__init__(*args, **kwargs)
        # stack choices for partner
        self.fields['partner'].choices = [(0, '----') if name is None else (name, name)for name in choices]

        # if form in in editing mode image does not need to be required
        if editing:
            self.fields['image_uri'].required = False
            self.fields['image_uri'].help_text = _('If you are satisfied with the image '
                                                   'you uploaded previously than leave this field blank')
        # if badge has already been published than edit is limited only to requirements field
        if published:
            self.fields['image_uri'].widget.attrs['readonly'] = True
            self.fields['title'].widget.attrs['readonly'] = True
            self.fields['description'].widget.attrs['readonly'] = True

    @property
    def with_partner(self):

        helper = FormHelper()
        helper.form_id = 'badge-create-form'
        helper.form_class = ''
        helper.form_tag = False
        helper.layout = Layout(
            Layout(
                'title',
                'description',
                'requirements',
                'partner',
            ),
            ButtonHolder(
                Submit('submit', _('Save and preview your Badge')),
            )
        )
        return helper

    @property
    def without_partner(self):
        helper = FormHelper()
        helper.form_id = 'badge-create-form'
        helper.form_class = ''
        helper.form_tag = False
        helper.layout = Layout(
            Layout(
                'title',
                'description',
                'requirements',
            ),
            ButtonHolder(
                Submit('submit', _('Save and preview your Badge')),
            )
        )
        return helper


    @property
    def edit_without_partner(self):
        #super(BadgeForm, self)
        self.fields['image_uri'].required = False

        helper = FormHelper()
        helper.form_id = 'badge-create-form'
        helper.form_class = ''
        helper.form_tag = False
        helper.layout = Layout(
            Layout(
                'title',
                'description',
                'requirements',
            ),
            ButtonHolder(
                Submit('submit', _('Save and preview your Badge')),
            )
        )
        return helper
