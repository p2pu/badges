def create_badge(image, title, description, requirements, author):
    pass


def get_badge(badge_uri):
    badge = {
        'uri': '/uri/badge/1',
        'image_uri': '/uri/images/1',
        'title': 'Badge title',
        'description': 'Badge description',
        'requirements': 'Badge requirements'
    }
    return badge


def update_badge(badge_uri, image_uri=None, title=None, description=None, requirements=None):
    """ only possible while draft """
    pass


def publish_badge(badge_uri):
    pass


def get_published_badges():
    pass


def search_badges(expression=None, author_uri=None, attribute_value=None):
    pass


def get_draft_badges()
    pass


def award_badge(badge_uri, user_uri, expert_uri):
    pass


def get_experts(badge_uri):
    pass


def relinquish_badge(badge_uri, expert_uri):
    pass
