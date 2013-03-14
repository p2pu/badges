from notifications.models import send_notification_i18n
from badge.view_helpers import fetch_badge_resources


def send_badge_creation_notification(badge):
    subject_template = 'emails/badge_created_subject.txt'
    text_template = 'emails/badge_created.txt'
    html_template = 'emails/badge_created.html'
    context = { 'badge': fetch_badge_resources(badge) }
    return send_notification_i18n(
        badge['author_uri'],
        subject_template,
        text_template,
        html_template,
        context=context
    )


def send_badge_awarded_notification(badge, expert_uri):
    subject_template = 'emails/badge_awarded_subject.txt'
    text_template = 'emails/badge_awarded.txt'
    html_template = 'emails/badge_awarded.html'
    context = { 'badge': fetch_badge_resources(badge) }

    # NOT the best place to hide this dependancy!!
    from project import models as project_api
    from project.view_helpers import fetch_resources

    project = project_api.search_projects(badge['uri'], expert_uri)
    if len(project) == 1:
        context['project'] = fetch_resources(project[0])
    projects = project_api.get_projects_ready_for_feedback(badge['uri'])
    context['projects'] = map(fetch_resources, projects[:3])
    return send_notification_i18n(
        expert_uri,
        subject_template,
        text_template,
        html_template,
        context=context
    )
