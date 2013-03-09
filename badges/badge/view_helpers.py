from media import models as media_api
from p2pu_user import models as p2pu_user_api

def fetch_badge_resources( badge ):
    badge['image'] = media_api.get_image(badge['image_uri'])
    badge['author'] = p2pu_user_api.get_user(badge['author_uri'])
    return badge
