# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'CheckStyleChecker.configuration'
        db.alter_column('checker_checkstylechecker', 'configuration', self.gf('checker.models.CheckerFileField')(max_length=500))


    def backwards(self, orm):
        
        # Changing field 'CheckStyleChecker.configuration'
        db.alter_column('checker_checkstylechecker', 'configuration', self.gf('django.db.models.fields.TextField')())


    models = {
        'accounts.tutorial': {
            'Meta': {'object_name': 'Tutorial'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'tutors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tutored_tutorials'", 'symmetrical': 'False', 'to': "orm['accounts.User']"})
        },
        'accounts.user': {
            'Meta': {'object_name': 'User', '_ormbases': ['auth.User']},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'final_grade': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mat_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'tutorial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Tutorial']", 'null': 'True', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'attestation.ratingscale': {
            'Meta': {'object_name': 'RatingScale'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
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
        'checker.anonymitychecker': {
            'Meta': {'object_name': 'AnonymityChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.cbuilder': {
            'Meta': {'object_name': 'CBuilder'},
            '_file_pattern': ('django.db.models.fields.CharField', [], {'default': "'^[a-zA-Z0-9_]*$'", 'max_length': '1000'}),
            '_flags': ('django.db.models.fields.CharField', [], {'default': "'-Wall'", 'max_length': '1000', 'blank': 'True'}),
            '_libs': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            '_output_flags': ('django.db.models.fields.CharField', [], {'default': "'-o %s'", 'max_length': '1000', 'blank': 'True'}),
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.checkerresult': {
            'Meta': {'object_name': 'CheckerResult'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.TextField', [], {}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'passed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'solution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['solutions.Solution']"})
        },
        'checker.checkstylechecker': {
            'Meta': {'object_name': 'CheckStyleChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'configuration': ('checker.models.CheckerFileField', [], {'max_length': '500'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'CheckStyle'", 'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.createfilechecker': {
            'Meta': {'object_name': 'CreateFileChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('checker.models.CheckerFileField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.cxxbuilder': {
            'Meta': {'object_name': 'CXXBuilder'},
            '_file_pattern': ('django.db.models.fields.CharField', [], {'default': "'^[a-zA-Z0-9_]*$'", 'max_length': '1000'}),
            '_flags': ('django.db.models.fields.CharField', [], {'default': "'-Wall'", 'max_length': '1000', 'blank': 'True'}),
            '_libs': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            '_output_flags': ('django.db.models.fields.CharField', [], {'default': "'-o %s'", 'max_length': '1000', 'blank': 'True'}),
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.dejagnusetup': {
            'Meta': {'object_name': 'DejaGnuSetup'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"}),
            'test_defs': ('checker.models.CheckerFileField', [], {'max_length': '500'})
        },
        'checker.dejagnutester': {
            'Meta': {'object_name': 'DejaGnuTester'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"}),
            'test_case': ('checker.models.CheckerFileField', [], {'max_length': '500'})
        },
        'checker.diffchecker': {
            'Meta': {'object_name': 'DiffChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_file': ('checker.models.CheckerFileField', [], {'max_length': '500', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'output_file': ('checker.models.CheckerFileField', [], {'max_length': '500', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shell_script': ('checker.models.CheckerFileField', [], {'max_length': '500'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.fortranbuilder': {
            'Meta': {'object_name': 'FortranBuilder'},
            '_file_pattern': ('django.db.models.fields.CharField', [], {'default': "'^[a-zA-Z0-9_]*$'", 'max_length': '1000'}),
            '_flags': ('django.db.models.fields.CharField', [], {'default': "'-Wall'", 'max_length': '1000', 'blank': 'True'}),
            '_libs': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            '_output_flags': ('django.db.models.fields.CharField', [], {'default': "'-o %s'", 'max_length': '1000', 'blank': 'True'}),
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.interfacechecker': {
            'Meta': {'object_name': 'InterfaceChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interface1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'interface2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'interface3': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'interface4': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'interface5': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'interface6': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'interface7': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.javabuilder': {
            'Meta': {'object_name': 'JavaBuilder'},
            '_file_pattern': ('django.db.models.fields.CharField', [], {'default': "'^[a-zA-Z0-9_]*$'", 'max_length': '1000'}),
            '_flags': ('django.db.models.fields.CharField', [], {'default': "'-Wall'", 'max_length': '1000', 'blank': 'True'}),
            '_libs': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            '_output_flags': ('django.db.models.fields.CharField', [], {'default': "'-o %s'", 'max_length': '1000', 'blank': 'True'}),
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.javagccbuilder': {
            'Meta': {'object_name': 'JavaGCCBuilder'},
            '_file_pattern': ('django.db.models.fields.CharField', [], {'default': "'^[a-zA-Z0-9_]*$'", 'max_length': '1000'}),
            '_flags': ('django.db.models.fields.CharField', [], {'default': "'-Wall'", 'max_length': '1000', 'blank': 'True'}),
            '_libs': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            '_output_flags': ('django.db.models.fields.CharField', [], {'default': "'-o %s'", 'max_length': '1000', 'blank': 'True'}),
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.junit3checker': {
            'Meta': {'object_name': 'JUnit3Checker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"}),
            'test_case': ('checker.models.CheckerFileField', [], {'max_length': '500'})
        },
        'checker.linecounter': {
            'Meta': {'object_name': 'LineCounter'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.linewidthchecker': {
            'Meta': {'object_name': 'LineWidthChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_line_length': ('django.db.models.fields.IntegerField', [], {'default': '80'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tab_width': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.scriptchecker': {
            'Meta': {'object_name': 'ScriptChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Externen Tutor ausf\\xc3\\xbchren'", 'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'remove': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'returns_html': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shell_script': ('checker.models.CheckerFileField', [], {'max_length': '500'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.textchecker': {
            'Meta': {'object_name': 'TextChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'solutions.solution': {
            'Meta': {'object_name': 'Solution'},
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.User']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'plagiarism': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"}),
            'warnings': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'tasks.task': {
            'Meta': {'object_name': 'Task'},
            'all_checker_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'final_grade_rating_scale': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.RatingScale']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_file_size': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'model_solution': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'model_solution_task'", 'null': 'True', 'to': "orm['solutions.Solution']"}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {}),
            'supported_file_types': ('django.db.models.fields.CharField', [], {'default': "'^(text/.*|image/.*)$'", 'max_length': '1000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['checker']
