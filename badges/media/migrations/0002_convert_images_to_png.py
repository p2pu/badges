# -*- coding: utf-8 -*-

import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.conf import settings
from ..models import process_image

class Migration(DataMigration):

    def _convert_to_png(self, image):
        print 'Converting image to png:', image.image_file.name
        try:
            image_file_name = '%s/%s' % (settings.MEDIA_ROOT, image.image_file.name)
            new_image_file = process_image(image_file_name)
            new_image_file = new_image_file.replace(settings.MEDIA_ROOT, '')[1:]
            image.image_file.name = new_image_file
            image.save()
        except:
            print 'ERROR: Failed converting image to png:', image.image_file.name
            self.any_errors = True

    def forwards(self, orm):
        Image = orm.Image
        self.any_errors = False

        for image in Image.objects.all():
            self._convert_to_png(image)

        assert not self.any_errors, 'Errors at convering images to PNG found.'

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'media.image': {
            'Meta': {'object_name': 'Image'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'uploader_uri': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['media']
    symmetrical = True
