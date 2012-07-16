# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Settings.account_manual_validation'
        db.add_column('configuration_settings', 'account_manual_validation',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Settings.account_manual_validation'
        db.delete_column('configuration_settings', 'account_manual_validation')

    models = {
        'configuration.chunk': {
            'Meta': {'object_name': 'Chunk'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'settings': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['configuration.Settings']"})
        },
        'configuration.settings': {
            'Meta': {'object_name': 'Settings'},
            'accept_all_solutions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'account_manual_validation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'acount_activation_days': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'anonymous_attestation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deny_registration_from': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2222, 1, 1, 0, 0)'}),
            'email_validation_regex': ('django.db.models.fields.CharField', [], {'default': "'.*@(student.)?kit.edu'", 'max_length': '200', 'blank': 'True'}),
            'final_grades_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mat_number_validation_regex': ('django.db.models.fields.CharField', [], {'default': "'\\\\d{5,7}'", 'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['configuration']