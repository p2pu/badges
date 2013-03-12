# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Image'
        db.create_table('media_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('uploader_uri', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('media', ['Image'])


    def backwards(self, orm):
        # Deleting model 'Image'
        db.delete_table('media_image')


    models = {
        'media.image': {
            'Meta': {'object_name': 'Image'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'uploader_uri': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['media']