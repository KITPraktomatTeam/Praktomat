# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):
	
	def forwards(self, orm):
	
		depends_on = (
			("accounts", "0002_load_initial_data"),
		)
		
		trainer = orm['auth.group'].objects.get_or_create(name="Trainer")[0]
		permissions =orm['auth.Permission'].objects.filter(codename__in=[u'change_chunk',])
		trainer.permissions.add(*permissions)
		trainer.save()
		
		orm.Chunk(key='Welcome Message').save()  
	
	
	def backwards(self, orm):
		try:
			trainer = orm['auth.group'].objects.get_or_create(name="Trainer")[0]
			permissions =orm['auth.Permission'].objects.filter(codename__in=[u'change_chunk',])
			trainer.permissions.remove(*permissions)
			trainer.save() 
		except:
			pass
		
		try: 
			orm.Chunk.objects.filter(key='Welcome Message').delete()
		except:
			pass

	
	models = {
		'accounts.tutorial': {
			'Meta': {'object_name': 'Tutorial'},
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
			'tutors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']"})
		},
		'accounts.userprofile': {
			'Meta': {'object_name': 'UserProfile'},
			'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
			'degree_course': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'mat_number': ('django.db.models.fields.IntegerField', [], {}),
			'tutorial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Tutorial']", 'null': 'True', 'blank': 'True'}),
			'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
		},
		'auth.group': {
			'Meta': {'object_name': 'Group'},
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
			'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
		},
		'auth.permission': {
			'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
			'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
			'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
			'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
			'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
			'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
			'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
			'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
			'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
		},
		'contenttypes.contenttype': {
			'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
			'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
		},
		'pagechunks.chunk': {
			'Meta': {'object_name': 'Chunk'},
			'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
		}
	}
	
	complete_apps = ['accounts', 'pagechunks']
