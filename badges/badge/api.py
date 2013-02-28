from badge.models import Badge
from datetime import datetime

class DuplicateTitleError(Exception):
    pass

def uri2id( uri ):
    return uri.strip('/').split('/')[-1]


def id2uri( id ):
    return '/uri/badge/{0}'.format(id)


def _badge2dict(badge_db):
    badge = {
        'uri': id2uri(badge_db.id),
        'title': badge_db.title,
        'image_uri': badge_db.image_uri,
        'description': badge_db.description,
        'requirements': badge_db.requirements,
        'author_uri': badge_db.author_uri
    }
    return badge


def create_badge( title, image_uri, description, requirements, author_uri ):
    if Badge.objects.filter(title=title).exists():
        raise DuplicateTitleError('Badge titles need to be unique.')

    badge = Badge(
        title=title, 
        image_uri=image_uri, 
        description=description, 
        requirements=requirements, 
        author_uri=author_uri,
        date_created=datetime.utcnow(),
        date_updated=datetime.utcnow()
    )
    badge.save()
    return get_badge(id2uri(badge.id))


def get_badge(uri):
    badge_db = Badge.objects.get(id=uri2id(uri))
    return _badge2dict(badge_db)


def update_badge(uri, image_uri=None, title=None, description=None, requirements=None):
    """ only possible while draft """
    badge_db = Badge.objects.get(id=uri2id(uri))

    # NOTE: not sure this should be in the API... what if the admin wants
    # to correct a small mistake
    if badge_db.date_published:
        raise Exception('Badge cannot be updated after it has been publised')
    if image_uri:
        badge_db.image_uri = image_uri
    if title:
        badge_db.title = title
    if description:
       badge_db.description = description
    if requirements:
       badge_db.requirements = requirements

    badge_db.save()
    return get_badge(uri)



def publish_badge(uri):
    badge_db = Badge.objects.get(id=uri2id(uri))
    badge_db.date_published = datetime.utcnow()
    badge_db.save()
    return True


def get_published_badges():
    badges = Badge.objects.filter(date_published__isnull=False)
    return [_badge2dict(badge) for badge in badges]


def get_user_draft_badges(author_uri):
    badges = Badge.objects.filter(author_uri=author_uri, date_published__isnull=True)
    return [_badge2dict(badge) for badge in badges]


def search_badges(expression=None, author_uri=None, attribute_value=None):
    raise Exception()


def award_badge(uri, user_uri, expert_uri):
    raise Exception()


def get_experts(uri):
    raise Exception()


def relinquish_badge(uri, expert_uri):
    raise Exception()
