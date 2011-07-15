# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Task'
        db.create_table('tasks_task', (
            ('submission_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('publication_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('tasks', ['Task'])

        # Adding model 'MediaFile'
        db.create_table('tasks_mediafile', (
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('media_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('tasks', ['MediaFile'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Task'
        db.delete_table('tasks_task')

        # Deleting model 'MediaFile'
        db.delete_table('tasks_mediafile')
    
    
    models = {
        'tasks.mediafile': {
            'Meta': {'object_name': 'MediaFile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'tasks.task': {
            'Meta': {'object_name': 'Task'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['tasks']
