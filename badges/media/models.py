import os
from django.conf import settings
from PIL import Image
from media import db


def upload_image(image_file, uploader_uri):

    if not image_format_is_png(image_file):
        image_file = convert_image(image_file)

    #TODO process image
    image_db = db.Image(image_file=image_file, uploader_uri=uploader_uri)
    image_db.save()
    return get_image("/uri/media/image/{0}".format(image_db.id))


def get_image(image_uri):
    image_id = image_uri.strip('/').split('/')[-1]
    image_db = None
    try:
        image_db = db.Image.objects.get(id=image_id)
    except:
        raise
    image = {
        "uri": "/uri/media/image/{0}".format(image_db.id),
        "url": image_db.image_file.url,
    }
    return image


def image_format_is_png(image_file):
    image = image_file.strip('/').split('.')
    image_format = image[-1]
    if image_format == 'png':
        return True
    return False


def extract_image_name(image_file):
    image_base = os.path.basename(image_file)
    name, _ = os.path.splitext(image_base)
    return name


def remove_original_image(image_file):
    os.remove(image_file)


def convert_image(image_file):
    """
    Convert image to png
    """
    image_name = extract_image_name(image_file)
    image_new_url = "{0}/images/{1}.png".format(settings.MEDIA_ROOT, image_name)
    size = 128,128
    try:
        im = Image.open(image_file)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(image_new_url, "png")
    except IOError:
        return IOError

    remove_original_image(image_file)

    return image_new_url
