from p2pu_user.db import User
from p2pu_user.db import Partner
from datetime import datetime

def username2uri(username):
    return u'/uri/user/{0}'.format(username)


def uri2username(uri):
    return uri.strip('/').split('/')[-1]


def save_user(username, image_url, email):

    if not image_url.startswith('http'):
        image_url = ''.join(['https://p2pu.org', image_url])

    if User.objects.filter(username=username).exists():
        # update user
        user = User.objects.get(username=username)
        user.image_url = image_url
        user.email = email
        user.date_updated = datetime.utcnow()
    else:
        user = User(
            username=username,
            image_url=image_url,
            email=email,
            date_joined=datetime.utcnow(),
            date_updated=datetime.utcnow()
        )
    user.save()

    return get_user(username2uri(username))


def _user2dict(user):
    return {
        'username': user.username,
        'email': user.email,
        'uri': username2uri(user.username),
        'image_url': user.image_url,
        'partner': _get_partners_for_user(user)
    }


def get_user(user_uri):
    user = User.objects.get(username=uri2username(user_uri))
    return _user2dict(user)

def last_n_users(n):
    users = User.objects.all().order_by('-date_joined')[:n]
    return [_user2dict(user) for user in users]

def get_users():
    return [_user2dict(user) for user in User.objects.all()]


def _partner2dict(partner):
    users = partner.users.all()
    users_list = []
    for user in users:
        users_list.append(_user2dict(user))

    return {
        'name': partner.name,
        'user': users_list,
    }


def create_partner(name, user_uri=None):
    partner = Partner.objects.create(name=name)

    if user_uri:
        user = User.objects.get(username=uri2username(user_uri))
        partner.users.add(user)

    return _partner2dict(partner)


def get_partner(partner_name):
    """
    Get the partner trough name attribute.
    """
    partner = Partner.objects.get(name=partner_name)
    return _partner2dict(partner)


def get_partners_for_user(user_uri):
    user = User.objects.get(username=uri2username(user_uri))
    return _get_partners_for_user(user)


def _get_partners_for_user(user):
    partners = user.partner_set.all()

    return_val = []
    for partner in partners:
        return_val.append(partner.name)
    return return_val

# TODO: update partner
