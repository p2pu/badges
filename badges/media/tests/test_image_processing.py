from django.test import TestCase
from PIL import Image
from mock import patch
from media import models as media_api


@patch('media.models.remove_original_image', lambda x: {})
class TestImageProcessing(TestCase):
    # image too large
    # image converted
    # image resized


    def test_convert_image(self):
        im_url = "/home/erika/DEV/p2pu/badges/badges/media/tests/images/old.jpg"

        new_url = media_api.convert_image(im_url)

        #self.assertEquals()








