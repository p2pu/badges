from django import template

register = template.Library()

@register.filter
def get_active_tab(result_dict):
    if result_dict['badges']:
        return 'badges'
    elif result_dict['projects']:
        return 'projects'
    elif result_dict['learners']:
        return 'learners'
    return None
