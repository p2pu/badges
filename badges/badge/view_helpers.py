from media import models as media_api

def fetch_badge_resources( badge ):
    badge['image'] = media_api.get_image(badge['image_uri'])

    # TODO fetch user details
    badge['author'] = {
        'username': badge['author_uri'].strip('/').split('/')[-1],
        'uri': badge['author_uri']
    }
    return badge
