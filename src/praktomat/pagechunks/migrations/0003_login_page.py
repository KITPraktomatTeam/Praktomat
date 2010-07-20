# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

	def forwards(self, orm):
		
		orm.Chunk(key='Login Message').save()  
	
	
	def backwards(self, orm):
		
		try: 
			orm.Chunk.objects.filter(key='Login Message').delete()
		except:
			pass


	models = {
		'pagechunks.chunk': {
			'Meta': {'object_name': 'Chunk'},
			'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
			'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
		}
	}

	complete_apps = ['pagechunks']
