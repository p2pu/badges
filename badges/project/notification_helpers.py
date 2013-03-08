from notifications.models import send_notification_i18n


def send_feedback_notification(project):
    subject_template = 'emails/project_feedback_subject.txt'
    text_template = 'emails/project_feedback.txt'
    context = { 'project': project }
    return send_notification_i18n(
        project['author_uri'],
        subject_template,
        text_template,
        context=context
    )


def send_revision_notification(project, experts):
    subject_template = 'emails/project_revised_subject.txt'
    text_template = 'emails/project_revised.txt'
    context = { 'project': project }
    for expert in experts:
        send_notification_i18n(
            expert,
            subject_template,
            text_template,
            context=context
        )
    #NOTE do we need a return value?


def send_project_creation_notification(project):
    subject_template = 'emails/project_submitted_subject.txt'
    text_template = 'emails/project_submitted.txt'
    context = { 'project': project }
    return send_notification_i18n(
        project['author_uri'],
        subject_template,
        text_template,
        context=context
    )
    

def send_project_creation_expert_notification(project, experts):
    subject_template = 'emails/project_submitted_expert_subject.txt'
    text_template = 'emails/project_submitted_expert.txt'
    context = { 'project': project }
    # send to all creation
    for expert in experts:
        send_notification_i18n(
            expert,
            subject_template,
            text_template,
            context=context
        )
    #NOTE do we need a return value?
