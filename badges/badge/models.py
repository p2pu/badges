from badge.db import Badge
from badge.db import Award

from datetime import datetime

class DuplicateTitleError(Exception):
    pass

def uri2id( uri ):
    return uri.strip('/').split('/')[-1]


def id2uri( id ):
    return '/uri/badge/{0}'.format(id)


def _badge2dict(badge_db):
    badge = {
        'id': badge_db.id,
        'uri': id2uri(badge_db.id),
        'title': badge_db.title,
        'image_uri': badge_db.image_uri,
        'description': badge_db.description,
        'requirements': badge_db.requirements,
        'author_uri': badge_db.author_uri,
        'publised': not badge_db.date_published == None
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
        if Badge.objects.exclude(id=badge_db.id).filter(title=title).exists():
            raise DuplicateTitleError('Badge titles need to be unique.')
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
    award_badge(uri, badge_db.author_uri, badge_db.author_uri, 'http://TODO.com')
    return True


def remove_badge(uri, reason):
    """ Mark a badge as removed - spam / inappropriate """
    pass


def get_published_badges():
    badges = Badge.objects.filter(date_published__isnull=False)
    return [_badge2dict(badge) for badge in badges]


# draft badges aka badges 'under review'
def get_user_draft_badges(author_uri):
    badges = Badge.objects.filter(author_uri=author_uri, date_published__isnull=True)
    return [_badge2dict(badge) for badge in badges]

def get_user_earned_badges(author_uri):
    badges = [award.badge for award in Award.objects.select_related().filter(user_uri=author_uri)]
    return [_badge2dict(badge) for badge in badges]

def get_user_awarded_badges(author_uri):
    badges = [award.badge for award in Award.objects.select_related().filter(expert_uri=author_uri)]
    return [_badge2dict(badge) for badge in badges]

# created badges aka 'published' badges
def get_user_created_badges(author_uri):
    badges = Badge.objects.filter(author_uri=author_uri, date_published__lte=datetime.utcnow())
    return [_badge2dict(badge) for badge in badges]



def search_badges(expression=None, author_uri=None, attribute_value=None):
    raise Exception()


def award_badge(badge_uri, user_uri, expert_uri, evidence_url):
    """ Award a badge to a user 
        expert_uri - expert that is awarding the badge
    """
    badge = Badge.objects.get(id=uri2id(badge_uri))
    if Award.objects.filter(badge=badge, user_uri=user_uri).exists():
        raise Exception('Badge already awarded to user')

    valid_expert = expert_uri in get_badge_experts(badge_uri)
    badge_creator = user_uri == badge.author_uri

    # Check if we can award the badge
    if not badge_creator and not valid_expert:
        raise Exception('Cannot award badge')
    
    award = Award(
        badge=badge,
        user_uri=user_uri,
        expert_uri=expert_uri,
        evidence_url=evidence_url,
        date_awarded=datetime.utcnow()
    )
    award.save()


def get_badge_experts(uri):
    awards = Award.objects.filter(badge_id=uri2id(uri))
    return [ award.user_uri for award in awards ]


def relinquish_badge(uri, expert_uri):
    raise Exception()
