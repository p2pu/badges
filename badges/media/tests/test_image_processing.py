import os
from PIL import Image
from django.test import TestCase
from media import models as media_api


class TestImageProcessing(TestCase):

    TEST_IMAGE_OK_FILES = ['old.gif', 'old.jpeg', 'old.jpg', 'old.png', 'old.tiff']
    TEST_IMAGE_ERROR_FILES = ['garbage.png', 'unknown.png']

    def _get_media_root(self):
        return '%s/images' % (os.path.dirname(__file__), )

    def _get_image_file(self, image):
        return '%s/%s' % (self._get_media_root(), image)

    def _test_process_image(self, image):
        image_file = self._get_image_file(image)
        # run
        new_file = media_api.process_image(image_file)
        # assert
        pil_image = Image.open(new_file)
        self.assertTrue(hasattr(pil_image, 'png'), 'Must be converted to PNG')
        self.assertTrue(pil_image.size <= (128, 128), 'Size must be 128 by 128 or smaller')
        self.assertTrue(new_file.endswith('.png'))

    def _test_process_error_image(self, image):
        image_file = self._get_image_file(image)

        try:
            _ = media_api.process_image(image_file)
        except media_api.UploadImageError:
            return
        except:
            pass

        self.assertTrue(False, 'UploadImageError not raised')

    def test_process_images_ok(self):
        for image in self.TEST_IMAGE_OK_FILES:
            self._test_process_image(image)

    def test_process_images_error(self):
        for image in self.TEST_IMAGE_ERROR_FILES:
            self._test_process_error_image(image)

    def test_upload_image_success(self):
        image_file = self.TEST_IMAGE_OK_FILES[0]
        uploader_uri = '/user/test/1'
        ret_val = media_api.upload_image(image_file, uploader_uri, media_root=self._get_media_root())
        self.assertTrue(ret_val['url'].endswith('.png'))

    def test_get_not_existant_image(self):
        image_uri = media_api._get_image_uri(99999)
        try:
            media_api.get_image(image_uri)
        except media_api.GetImageError:
            return
        except:
            pass
        self.assertTrue(False, 'GetImageError not raised')