# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Badge'
        db.create_table('badge_badge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('image_uri', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('requirements', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('author_uri', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_published', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('badge', ['Badge'])

        # Adding model 'Award'
        db.create_table('badge_award', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('badge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['badge.Badge'])),
            ('user_uri', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('expert_uri', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('evidence_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_awarded', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('badge', ['Award'])


    def backwards(self, orm):
        # Deleting model 'Badge'
        db.delete_table('badge_badge')

        # Deleting model 'Award'
        db.delete_table('badge_award')


    models = {
        'badge.award': {
            'Meta': {'object_name': 'Award'},
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['badge.Badge']"}),
            'date_awarded': ('django.db.models.fields.DateTimeField', [], {}),
            'evidence_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'expert_uri': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_uri': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'badge.badge': {
            'Meta': {'object_name': 'Badge'},
            'author_uri': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_published': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_uri': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'requirements': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        }
    }

    complete_apps = ['badge']