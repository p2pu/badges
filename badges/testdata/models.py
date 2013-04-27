from django.utils import simplejson
from django.core.files import File
from django.conf import settings

from media import models as media_api
from badge import models as badge_api
from p2pu_user import models as p2pu_user_api
import os

def load_test_data(data_file):
    df = open(data_file, 'r')
    root = os.path.dirname(os.path.abspath(data_file))
    test_data = simplejson.load(df)
    for badge in test_data['badges']:
        p2pu_user_api.save_user(
            p2pu_user_api.uri2username(badge['author_uri']), 
            'http://placehold.it/150x150',
            '%s@p2pu.org' % p2pu_user_api.uri2username(badge['author_uri']),
        )
        with open(os.path.join(root, badge['image']), 'rb') as image_file:
            image = media_api.upload_image(
                File(image_file),
                badge['author_uri'],
                media_root=settings.MEDIA_ROOT,
                delete_original=False)

        badge['image_uri'] = image['uri']
        del badge['image']
        badge = badge_api.create_badge(**badge)
        badge_api.publish_badge(badge['uri'])
        print(badge)
    df.close()
