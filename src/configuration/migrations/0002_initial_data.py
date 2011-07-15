# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):
	
	def forwards(self, orm):
		
		#send signal post_syncdb so that permissions will be created even if the corresponding model was created in this migration
		db.send_pending_create_signals()
		
		depends_on = (
		  ("accounts", "0002_load_initial_data"),
		)
		
		trainer = orm['auth.group'].objects.get_or_create(name="Trainer")[0]
		permissions =orm['auth.Permission'].objects.filter(codename__in=[u'change_chunk','change_settings'])
		trainer.permissions.add(*permissions)
		trainer.save()
		
		orm.Settings().save()
		orm.Chunk(key='Welcome Message').save()
		orm.Chunk(key='Login Message').save() 
	
	
	def backwards(self, orm):
		try:
			trainer = orm['auth.group'].objects.get_or_create(name="Trainer")[0]
			permissions =orm['auth.Permission'].objects.filter(codename__in=[u'change_chunk','change_settings'])
			trainer.permissions.remove(*permissions)
			trainer.save() 
		except:
			pass
		
		try: 
			orm.Chunk.objects.filter(key='Welcome Message').delete()
			orm.Chunk.objects.filter(key='Login Message').delete()
			orm.Settings.objects.all().delete()
		except:
			pass
				
				
	models = {
		'auth.group': {
			'Meta': {'object_name': 'Group'},
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
			'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
		},
		'auth.message': {
			'Meta': {'object_name': 'Message'},
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'message': ('django.db.models.fields.TextField', [], {}),
			'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_message_set'", 'to': "orm['auth.User']"})
		},
		'auth.permission': {
			'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
			'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
		},
		'auth.user': {
			'Meta': {'object_name': 'User'},
			'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
			'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
			'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
			'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
			'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
			'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
			'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
			'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
			'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
		},
		'configuration.chunk': {
			'Meta': {'object_name': 'Chunk'},
			'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'settings': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['configuration.Settings']"})
		},
		'configuration.settings': {
			'Meta': {'object_name': 'Settings'},
			'anonymous_attestation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'deny_registration_from': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.date(2222, 1, 1)'}),
			'email_validation_regex': ('django.db.models.fields.CharField', [], {'default': "'.*@(student.)?kit.edu'", 'max_length': '200', 'blank': 'True'}),
			'final_grades_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'mat_number_validation_regex': ('django.db.models.fields.CharField', [], {'default': "'\\\\d{5,7}'", 'max_length': '200', 'blank': 'True'})
		},
		'contenttypes.contenttype': {
			'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
			'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
			}
		}
		
	complete_apps = ['auth', 'configuration']
