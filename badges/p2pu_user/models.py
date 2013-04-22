from p2pu_user.db import User

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
        'image_url': user.image_url
    }


def get_user(user_uri):
    user = User.objects.get(username=uri2username(user_uri))
    return _user2dict(user)


def get_users():
    return [_user2dict(user) for user in User.objects.all() ]
