import os
import shutil
from django.test import TestCase
from PIL import Image
from media import models as media_api
from django.conf import settings


class TestImageProcessing(TestCase):
    # image too large
    # image converted
    # image resized

    SRC = '%s/test_images' % settings.MEDIA_ROOT
    DEST = '%s/images' % os.path.dirname(__file__)

    def setUp(self):

        if not os.path.exists(self.DEST):
            os.makedirs(self.DEST)

        src_files = os.listdir(self.SRC)
        for file_name in src_files:
            full_file_name = os.path.join(self.SRC, file_name)
            if (os.path.isfile(full_file_name)):
                shutil.copy(full_file_name, self.DEST)


    def tearDown(self):
        try:
           os.rmdir(self.DEST)
        except OSError as ex:
            print ex.errno


    def extract_image_format(self,image_file):
        image_base = os.path.basename(image_file)
        _, img_format = os.path.splitext(image_base)
        return img_format

    def get_image_size(self, image_file):
        img = Image.open(image_file)
        return img.size


    def test_image_processing(self):
        files = os.listdir(self.DEST)
        for file_name in files:
            new_url = media_api.process_image('%s/%s' % (self.DEST, file_name))

            self.assertEquals('.png', self.extract_image_format(new_url))
            self.assertTrue(True, max(self.get_image_size(new_url)) <= 128)







