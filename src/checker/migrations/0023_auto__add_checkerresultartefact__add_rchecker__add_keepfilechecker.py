# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CheckerResultArtefact'
        db.create_table(u'checker_checkerresultartefact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('result', self.gf('django.db.models.fields.related.ForeignKey')(related_name='artefacts', to=orm['checker.CheckerResult'])),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=500)),
        ))
        db.send_create_signal(u'checker', ['CheckerResultArtefact'])

        # Adding model 'RChecker'
        db.create_table(u'checker_rchecker', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('always', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('critical', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('r_script', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('require_plots', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('keep_plots', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('checker', ['RChecker'])

        # Adding model 'KeepFileChecker'
        db.create_table(u'checker_keepfilechecker', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('always', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('critical', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
        ))
        db.send_create_signal('checker', ['KeepFileChecker'])


    def backwards(self, orm):
        # Deleting model 'CheckerResultArtefact'
        db.delete_table(u'checker_checkerresultartefact')

        # Deleting model 'RChecker'
        db.delete_table(u'checker_rchecker')

        # Deleting model 'KeepFileChecker'
        db.delete_table(u'checker_keepfilechecker')


    models = {
        u'accounts.tutorial': {
            'Meta': {'object_name': 'Tutorial'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'tutors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tutored_tutorials'", 'symmetrical': 'False', 'to': u"orm['accounts.User']"})
        },
        u'accounts.user': {
            'Meta': {'ordering': "['first_name', 'last_name']", 'object_name': 'User', '_ormbases': [u'auth.User']},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'final_grade': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mat_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'programme': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tutorial': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Tutorial']", 'null': 'True', 'blank': 'True'}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'attestation.ratingscale': {
            'Meta': {'object_name': 'RatingScale'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'checker.anonymitychecker': {
            'Meta': {'object_name': 'AnonymityChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"})
        },
        'checker.cbuilder': {
            'Meta': {'object_name': 'CBuilder'},
            '_file_pattern': ('django.db.models.fields.CharField', [], {'default': "'^[a-zA-Z0-9_]*$'", 'max_length': '1000'}),
            '_flags': ('django.db.models.fields.CharField', [], {'default': "'-Wall'", 'max_length': '1000', 'blank': 'True'}),
            '_libs': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            '_main_required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            '_output_flags': ('django.db.models.fields.CharField', [], {'default': "'-o %s'", 'max_length': '1000', 'blank': 'True'}),
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"})
        },
        u'checker.checkerresult': {
            'Meta': {'object_name': 'CheckerResult'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.TextField', [], {}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'passed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'solution': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['solutions.Solution']"})
        },
        u'checker.checkerresultartefact': {
            'Meta': {'object_name': 'CheckerResultArtefact'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '500'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'artefacts'", 'to': u"orm['checker.CheckerResult']"})
        },
        'checker.checkstylechecker': {
            'Meta': {'object_name': 'CheckStyleChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'configuration': ('checker.models.CheckerFileField', [], {'max_length': '500'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'CheckStyle'", 'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"})
        },
        u'checker.createfilechecker': {
            'Meta': {'object_name': 'CreateFileChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'file': ('checker.models.CheckerFileField', [], {'max_length': '500'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"}),
            'unpack_zipfile': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'checker.cxxbuilder': {
            'Meta': {'object_name': 'CXXBuilder'},
            '_file_pattern': ('django.db.models.fields.CharField', [], {'default': "'^[a-zA-Z0-9_]*$'", 'max_length': '1000'}),
            '_flags': ('django.db.models.fields.CharField', [], {'default': "'-Wall'", 'max_length': '1000', 'blank': 'True'}),
            '_libs': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            '_main_required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            '_output_flags': ('django.db.models.fields.CharField', [], {'default': "'-o %s'", 'max_length': '1000', 'blank': 'True'}),
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"})
        },
        'checker.dejagnusetup': {
            'Meta': {'object_name': 'DejaGnuSetup'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"}),
            'test_defs': ('checker.models.CheckerFileField', [], {'max_length': '500'})
        },
        'checker.dejagnutester': {
            'Meta': {'object_name': 'DejaGnuTester'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"}),
            'test_case': ('checker.models.CheckerFileField', [], {'max_length': '500'})
        },
        'checker.fortranbuilder': {
            'Meta': {'object_name': 'FortranBuilder'},
            '_file_pattern': ('django.db.models.fields.CharField', [], {'default': "'^[a-zA-Z0-9_]*$'", 'max_length': '1000'}),
            '_flags': ('django.db.models.fields.CharField', [], {'default': "'-Wall'", 'max_length': '1000', 'blank': 'True'}),
            '_libs': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            '_main_required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            '_output_flags': ('django.db.models.fields.CharField', [], {'default': "'-o %s'", 'max_length': '1000', 'blank': 'True'}),
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"})
        },
        'checker.haskellbuilder': {
            'Meta': {'object_name': 'HaskellBuilder'},
            '_file_pattern': ('django.db.models.fields.CharField', [], {'default': "'^[a-zA-Z0-9_]*$'", 'max_length': '1000'}),
            '_flags': ('django.db.models.fields.CharField', [], {'default': "'-Wall'", 'max_length': '1000', 'blank': 'True'}),
            '_libs': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            '_main_required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            '_output_flags': ('django.db.models.fields.CharField', [], {'default': "'-o %s'", 'max_length': '1000', 'blank': 'True'}),
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"})
        },
        u'checker.haskelltestframeworkchecker': {
            'Meta': {'object_name': 'HaskellTestFrameWorkChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'file': ('checker.models.CheckerFileField', [], {'max_length': '500'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4096', 'blank': 'True'}),
            'include_testcase_in_report': ('django.db.models.fields.CharField', [], {'default': "'DL'", 'max_length': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'require_safe': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"}),
            'test_description': ('django.db.models.fields.TextField', [], {}),
            'unpack_zipfile': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'checker.ignoringhaskellbuilder': {
            'Meta': {'object_name': 'IgnoringHaskellBuilder', '_ormbases': ['checker.HaskellBuilder']},
            u'haskellbuilder_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['checker.HaskellBuilder']", 'unique': 'True', 'primary_key': 'True'})
        },
        'checker.ignoringjavabuilder': {
            'Meta': {'object_name': 'IgnoringJavaBuilder', '_ormbases': ['checker.JavaBuilder']},
            u'javabuilder_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['checker.JavaBuilder']", 'unique': 'True', 'primary_key': 'True'})
        },
        'checker.interfacechecker': {
            'Meta': {'object_name': 'InterfaceChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"})
        },
        'checker.isabellechecker': {
            'Meta': {'object_name': 'IsabelleChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logic': ('django.db.models.fields.CharField', [], {'default': "'HOL'", 'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"})
        },
        'checker.javabuilder': {
            'Meta': {'object_name': 'JavaBuilder'},
            '_file_pattern': ('django.db.models.fields.CharField', [], {'default': "'^[a-zA-Z0-9_]*$'", 'max_length': '1000'}),
            '_flags': ('django.db.models.fields.CharField', [], {'default': "'-Wall'", 'max_length': '1000', 'blank': 'True'}),
            '_libs': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            '_main_required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            '_output_flags': ('django.db.models.fields.CharField', [], {'default': "'-o %s'", 'max_length': '1000', 'blank': 'True'}),
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"})
        },
        'checker.javagccbuilder': {
            'Meta': {'object_name': 'JavaGCCBuilder'},
            '_file_pattern': ('django.db.models.fields.CharField', [], {'default': "'^[a-zA-Z0-9_]*$'", 'max_length': '1000'}),
            '_flags': ('django.db.models.fields.CharField', [], {'default': "'-Wall'", 'max_length': '1000', 'blank': 'True'}),
            '_libs': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            '_main_required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            '_output_flags': ('django.db.models.fields.CharField', [], {'default': "'-o %s'", 'max_length': '1000', 'blank': 'True'}),
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"})
        },
        'checker.junitchecker': {
            'Meta': {'object_name': 'JUnitChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4096'}),
            'junit_version': ('django.db.models.fields.CharField', [], {'default': "'junit3'", 'max_length': '16'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"}),
            'test_description': ('django.db.models.fields.TextField', [], {})
        },
        'checker.keepfilechecker': {
            'Meta': {'object_name': 'KeepFileChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"})
        },
        'checker.linecounter': {
            'Meta': {'object_name': 'LineCounter'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"})
        },
        'checker.linewidthchecker': {
            'Meta': {'object_name': 'LineWidthChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'exclude': ('django.db.models.fields.CharField', [], {'default': "'.*\\\\.txt$'", 'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include': ('django.db.models.fields.CharField', [], {'default': "'.*'", 'max_length': '100', 'blank': 'True'}),
            'max_line_length': ('django.db.models.fields.IntegerField', [], {'default': '80'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tab_width': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"})
        },
        'checker.rchecker': {
            'Meta': {'object_name': 'RChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keep_plots': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'r_script': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'require_plots': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"})
        },
        'checker.scriptchecker': {
            'Meta': {'object_name': 'ScriptChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Externen Tutor ausf\\xc3\\xbchren'", 'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'remove': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'returns_html': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shell_script': ('checker.models.CheckerFileField', [], {'max_length': '500'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"})
        },
        'checker.testonlybuildingbuilder': {
            'Meta': {'object_name': 'TestOnlyBuildingBuilder', '_ormbases': ['checker.HaskellBuilder']},
            u'haskellbuilder_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['checker.HaskellBuilder']", 'unique': 'True', 'primary_key': 'True'})
        },
        'checker.textchecker': {
            'Meta': {'object_name': 'TextChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'solutions.solution': {
            'Meta': {'object_name': 'Solution'},
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.User']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'final': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'plagiarism': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"}),
            'testupload': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'warnings': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'tasks.task': {
            'Meta': {'object_name': 'Task'},
            'all_checker_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'final_grade_rating_scale': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['attestation.RatingScale']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_file_size': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'model_solution': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'model_solution_task'", 'null': 'True', 'to': u"orm['solutions.Solution']"}),
            'only_trainers_publish': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {}),
            'supported_file_types': ('django.db.models.fields.CharField', [], {'default': "'^(text/.*|image/.*)$'", 'max_length': '1000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['checker']