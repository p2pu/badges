# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table('project_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image_uri', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('work_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('reflection', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('badge_uri', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('author_uri', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_deleted', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('project', ['Project'])

        # Adding model 'Revision'
        db.create_table('project_revision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project.Project'])),
            ('improvement', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('work_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('project', ['Revision'])

        # Adding model 'Feedback'
        db.create_table('project_feedback', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project.Project'])),
            ('revision', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project.Revision'], null=True, blank=True)),
            ('expert_uri', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('good', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('bad', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('ugly', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')()),
            ('badge_awarded', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('project', ['Feedback'])


    def backwards(self, orm):
        # Deleting model 'Project'
        db.delete_table('project_project')

        # Deleting model 'Revision'
        db.delete_table('project_revision')

        # Deleting model 'Feedback'
        db.delete_table('project_feedback')


    models = {
        'project.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'bad': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'badge_awarded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'expert_uri': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'good': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['project.Project']"}),
            'revision': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['project.Revision']", 'null': 'True', 'blank': 'True'}),
            'ugly': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        'project.project': {
            'Meta': {'object_name': 'Project'},
            'author_uri': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'badge_uri': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_deleted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_uri': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'reflection': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'work_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'project.revision': {
            'Meta': {'object_name': 'Revision'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'improvement': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['project.Project']"}),
            'work_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['project']