from django.template.loader import render_to_string
from django.utils.translation import activate, get_language

def localize_for_user(user, template, context):

    current_locale = get_language()
    # TODO get user locale and switch to it
    # TODO activate(user_locale)
    
    localized_template = render_to_string(template, context)
    activate(current_locale)
    return localized_template
