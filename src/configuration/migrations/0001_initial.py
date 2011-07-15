# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Settings'
        db.create_table('configuration_settings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email_validation_regex', self.gf('django.db.models.fields.CharField')(default='.*@(student.)?kit.edu', max_length=200, blank=True)),
            ('mat_number_validation_regex', self.gf('django.db.models.fields.CharField')(default='\\d{5,7}', max_length=200, blank=True)),
            ('deny_registration_from', self.gf('django.db.models.fields.DateTimeField')()),
            ('anonymous_attestation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('final_grades_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('configuration', ['Settings'])

        # Adding model 'Chunk'
        db.create_table('configuration_chunk', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('settings', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['configuration.Settings'])),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('configuration', ['Chunk'])


    def backwards(self, orm):
        
        # Deleting model 'Settings'
        db.delete_table('configuration_settings')

        # Deleting model 'Chunk'
        db.delete_table('configuration_chunk')


    models = {
        'configuration.chunk': {
            'Meta': {'object_name': 'Chunk'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'settings': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['configuration.Settings']"})
        },
        'configuration.settings': {
            'Meta': {'object_name': 'Settings'},
            'anonymous_attestation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deny_registration_from': ('django.db.models.fields.DateTimeField', [], {}),
            'email_validation_regex': ('django.db.models.fields.CharField', [], {'default': "'.*@(student.)?kit.edu'", 'max_length': '200', 'blank': 'True'}),
            'final_grades_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mat_number_validation_regex': ('django.db.models.fields.CharField', [], {'default': "'\\\\d{5,7}'", 'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['configuration']
