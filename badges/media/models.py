"""
Media models processing methods.
"""

import os
import sys
import logging
import uuid
from django.conf import settings
from PIL import Image
from media import db

LOG = logging.getLogger('badges.media.models')


class UploadImageError(Exception):
    pass


class GetImageError(Exception):
    pass


def upload_image(image_file, uploader_uri):
    """
    Upload image media API.
    """

    image_file = process_image(image_file)

    image_db = db.Image(image_file=image_file, uploader_uri=uploader_uri)
    image_db.save()

    image_uri = _get_image_uri(image_db.id)

    return get_image(image_uri)


def get_image(image_uri):
    """
    Get image media API.
    """

    image_id = _extract_image_id(image_uri)

    try:
        image_db = db.Image.objects.get(id=image_id)

    except db.Image.DoesNotExist:
        msg = 'Failed to load image (image_uri=%s, image_id=%s).' \
              % (image_uri, image_id, )

        LOG.exception(msg)
        raise GetImageError(msg), None, sys.exc_info()[2]

    image = {
        "uri": _get_image_uri(image_db.id),
        "url": image_db.image_file.url,
    }
    return image


def process_image(image_file):
    """
    Process image: resize and convert to PNG.
    """

    image_name = _extract_image_name(image_file)
    image_new_url = _get_new_image_url(image_name)
    size = 128, 128

    try:
        im = Image.open(image_file)

        if max(im.size) > max(size):
            im.thumbnail(size, Image.ANTIALIAS)

        im.save(image_new_url, "png")

        #os.remove(image_file)

    except (IOError, OSError):
        msg = 'Failed while processing image (image_file=%s, image_name=%s, image_new_url=%s).' \
              % (image_file, image_name, image_new_url, )

        LOG.exception(msg)
        raise UploadImageError(msg), None, sys.exc_info()[2]

    return image_new_url


def _extract_image_name(image_file):
    image_base = os.path.basename(image_file)
    name, _ = os.path.splitext(image_base)
    return name


def _get_new_image_url(image_name):
    unique_id = str(uuid.uuid4())
    return '%s/images/%s_%s.png' % (settings.MEDIA_ROOT, image_name, unique_id, )


def _extract_image_id(image_uri):
    return image_uri.strip('/').split('/')[-1]


def _get_image_uri(image_id):
    return "/uri/media/image/{0}".format(image_id)

