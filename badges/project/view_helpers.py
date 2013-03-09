from media import models as media_api
from p2pu_user import models as p2pu_user_api

def fetch_resources( project ):
    project['image'] = media_api.get_image(project['image_uri'])
    project['author'] = p2pu_user_api.get_user(project['author_uri'])
    return project
