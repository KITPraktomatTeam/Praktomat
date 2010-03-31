# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Attestation'
        db.create_table('attestation_attestation', (
            ('public_comment', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('solution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['solutions.Solution'])),
            ('final', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('final_grade', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('private_comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('attestation', ['Attestation'])

        # Adding model 'AnnotatedSolutionFile'
        db.create_table('attestation_annotatedsolutionfile', (
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('attestation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.Attestation'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('solution_file', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['solutions.SolutionFile'])),
        ))
        db.send_create_signal('attestation', ['AnnotatedSolutionFile'])

        # Adding model 'RatingAspect'
        db.create_table('attestation_ratingaspect', (
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('attestation', ['RatingAspect'])

        # Adding model 'RatingScale'
        db.create_table('attestation_ratingscale', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('attestation', ['RatingScale'])

        # Adding model 'RatingScaleItem'
        db.create_table('attestation_ratingscaleitem', (
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('scale', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.RatingScale'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('attestation', ['RatingScaleItem'])

        # Adding model 'Rating'
        db.create_table('attestation_rating', (
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('aspect', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.RatingAspect'])),
            ('scale', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.RatingScale'])),
        ))
        db.send_create_signal('attestation', ['Rating'])

        # Adding model 'RatingResult'
        db.create_table('attestation_ratingresult', (
            ('attestation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.Attestation'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('aspect', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.RatingAspect'])),
            ('mark', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.RatingScaleItem'], null=True)),
        ))
        db.send_create_signal('attestation', ['RatingResult'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Attestation'
        db.delete_table('attestation_attestation')

        # Deleting model 'AnnotatedSolutionFile'
        db.delete_table('attestation_annotatedsolutionfile')

        # Deleting model 'RatingAspect'
        db.delete_table('attestation_ratingaspect')

        # Deleting model 'RatingScale'
        db.delete_table('attestation_ratingscale')

        # Deleting model 'RatingScaleItem'
        db.delete_table('attestation_ratingscaleitem')

        # Deleting model 'Rating'
        db.delete_table('attestation_rating')

        # Deleting model 'RatingResult'
        db.delete_table('attestation_ratingresult')
    
    
    models = {
        'attestation.annotatedsolutionfile': {
            'Meta': {'object_name': 'AnnotatedSolutionFile'},
            'attestation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Attestation']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'solution_file': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['solutions.SolutionFile']"})
        },
        'attestation.attestation': {
            'Meta': {'object_name': 'Attestation'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'final': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'final_grade': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'private_comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'public_comment': ('django.db.models.fields.TextField', [], {}),
            'solution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['solutions.Solution']"})
        },
        'attestation.rating': {
            'Meta': {'object_name': 'Rating'},
            'aspect': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.RatingAspect']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scale': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.RatingScale']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'attestation.ratingaspect': {
            'Meta': {'object_name': 'RatingAspect'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'attestation.ratingresult': {
            'Meta': {'object_name': 'RatingResult'},
            'aspect': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.RatingAspect']"}),
            'attestation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Attestation']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mark': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.RatingScaleItem']", 'null': 'True'})
        },
        'attestation.ratingscale': {
            'Meta': {'object_name': 'RatingScale'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'attestation.ratingscaleitem': {
            'Meta': {'object_name': 'RatingScaleItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'scale': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.RatingScale']"})
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
        'solutions.solution': {
            'Meta': {'object_name': 'Solution'},
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'final': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"}),
            'warnings': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'solutions.solutionfile': {
            'Meta': {'object_name': 'SolutionFile'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'solution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['solutions.Solution']"})
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
    
    complete_apps = ['attestation']
