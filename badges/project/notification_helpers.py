from notifications.models import send_notification_i18n
from project.view_helpers import fetch_resources

def send_feedback_notification(project):
    subject_template = 'emails/project_feedback_subject.txt'
    text_template = 'emails/project_feedback.txt'
    html_template = 'emails/project_feedback.html'
    context = { 'project': fetch_resources(project) }
    return send_notification_i18n(
        project['author_uri'],
        subject_template,
        text_template,
        html_template,
        context=context
    )


def send_revision_notification(project, experts):
    subject_template = 'emails/project_revised_subject.txt'
    text_template = 'emails/project_revised.txt'
    html_template = 'emails/project_revised.html'
    context = { 'project': fetch_resources(project) }
    for expert in experts:
        send_notification_i18n(
            expert,
            subject_template,
            text_template,
            html_template,
            context=context
        )
    #NOTE do we need a return value?


def send_project_creation_notification(project):
    subject_template = 'emails/project_submitted_subject.txt'
    text_template = 'emails/project_submitted.txt'
    html_template = 'emails/project_submitted.html'
    context = { 'project': fetch_resources(project) }
    return send_notification_i18n(
        project['author_uri'],
        subject_template,
        text_template,
        html_template,
        context=context
    )
    

def send_project_creation_expert_notification(project, badge, experts):
    subject_template = 'emails/project_submitted_expert_subject.txt'
    text_template = 'emails/project_submitted_expert.txt'
    html_template = 'emails/project_submitted_expert.html'
    context = { 
        'projects': [fetch_resources(project)],
        'badge': badge
    }
    
    for expert in experts:
        send_notification_i18n(
            expert,
            subject_template,
            text_template,
            html_template,
            context=context
        )
    #NOTE do we need a return value?



def send_badge_needs_partner_feedback_notification(badge, project, author_uri):
    subject_template = 'emails/project_awarded_partner_badge_subject.txt'
    text_template = 'emails/project_awarded_partner_badge.txt'
    html_template = 'emails/project_awarded_partner_badge.html'
    context = { 'project': fetch_resources(project) }
    return send_notification_i18n(
        project['author_uri'],
        subject_template,
        text_template,
        html_template,
        context=context
    )