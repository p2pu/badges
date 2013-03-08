from notifications.models import send_notification_i18n


def send_badge_creation_notification(badge):
    subject_template = 'emails/badge_created_subject.txt'
    text_template = 'emails/badge_created.txt'
    context = { 'badge': badge }
    return send_notification_i18n(
        badge['author_uri'],
        subject_template,
        text_template,
        context=context
    )


def send_badge_awarded_notification(badge, expert_uri):
    subject_template = 'emails/badge_awarded_subject.txt'
    text_template = 'emails/badge_awarded.txt'
    context = { 'badge': badge }
    return send_notification_i18n(
        expert_uri,
        subject_template,
        text_template,
        context=context
    )
