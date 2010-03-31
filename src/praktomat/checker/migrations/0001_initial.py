# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'CheckerResult'
        db.create_table('checker_checkerresult', (
            ('log', self.gf('django.db.models.fields.TextField')()),
            ('solution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['solutions.Solution'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('passed', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('checker', ['CheckerResult'])

        # Adding model 'AnonymityChecker'
        db.create_table('checker_anonymitychecker', (
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('always', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('checker', ['AnonymityChecker'])

        # Adding model 'InterfaceChecker'
        db.create_table('checker_interfacechecker', (
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('interface1', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('always', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('interface3', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('interface5', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('interface4', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('interface7', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('interface2', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('interface6', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('checker', ['InterfaceChecker'])

        # Adding model 'LineWidthChecker'
        db.create_table('checker_linewidthchecker', (
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('always', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('max_line_length', self.gf('django.db.models.fields.IntegerField')(default=80)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('checker', ['LineWidthChecker'])

        # Adding model 'TextChecker'
        db.create_table('checker_textchecker', (
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('always', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('checker', ['TextChecker'])

        # Adding model 'DiffChecker'
        db.create_table('checker_diffchecker', (
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('always', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('shell_script', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('output_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('input_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('checker', ['DiffChecker'])

        # Adding model 'ScriptChecker'
        db.create_table('checker_scriptchecker', (
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('name', self.gf('django.db.models.fields.CharField')(default='Externen Tutor ausf\xc3\xbchren', max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('always', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('shell_script', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('remove', self.gf('django.db.models.fields.CharField')(max_length=5000, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('returns_html', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('checker', ['ScriptChecker'])

        # Adding model 'CreateFileChecker'
        db.create_table('checker_createfilechecker', (
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('always', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('checker', ['CreateFileChecker'])

        # Adding model 'LineCounter'
        db.create_table('checker_linecounter', (
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('always', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('checker', ['LineCounter'])

        # Adding model 'DejaGnuTester'
        db.create_table('checker_dejagnutester', (
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('always', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('test_case', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('checker', ['DejaGnuTester'])

        # Adding model 'DejaGnuSetup'
        db.create_table('checker_dejagnusetup', (
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('always', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('test_defs', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('checker', ['DejaGnuSetup'])

        # Adding model 'CBuilder'
        db.create_table('checker_cbuilder', (
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('_output_flags', self.gf('django.db.models.fields.CharField')(default='-o %s', max_length=1000, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('always', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_libs', self.gf('django.db.models.fields.CharField')(default='', max_length=1000, blank=True)),
            ('_file_pattern', self.gf('django.db.models.fields.CharField')(default='^[a-zA-Z0-9_]*$', max_length=1000)),
            ('_flags', self.gf('django.db.models.fields.CharField')(default='-Wall', max_length=1000, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('checker', ['CBuilder'])

        # Adding model 'CXXBuilder'
        db.create_table('checker_cxxbuilder', (
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('_output_flags', self.gf('django.db.models.fields.CharField')(default='-o %s', max_length=1000, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('always', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_libs', self.gf('django.db.models.fields.CharField')(default='', max_length=1000, blank=True)),
            ('_file_pattern', self.gf('django.db.models.fields.CharField')(default='^[a-zA-Z0-9_]*$', max_length=1000)),
            ('_flags', self.gf('django.db.models.fields.CharField')(default='-Wall', max_length=1000, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('checker', ['CXXBuilder'])

        # Adding model 'JavaBuilder'
        db.create_table('checker_javabuilder', (
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('_output_flags', self.gf('django.db.models.fields.CharField')(default='-o %s', max_length=1000, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('always', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_libs', self.gf('django.db.models.fields.CharField')(default='', max_length=1000, blank=True)),
            ('_file_pattern', self.gf('django.db.models.fields.CharField')(default='^[a-zA-Z0-9_]*$', max_length=1000)),
            ('_flags', self.gf('django.db.models.fields.CharField')(default='-Wall', max_length=1000, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('checker', ['JavaBuilder'])

        # Adding model 'JavaGCCBuilder'
        db.create_table('checker_javagccbuilder', (
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('_output_flags', self.gf('django.db.models.fields.CharField')(default='-o %s', max_length=1000, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('always', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_libs', self.gf('django.db.models.fields.CharField')(default='', max_length=1000, blank=True)),
            ('_file_pattern', self.gf('django.db.models.fields.CharField')(default='^[a-zA-Z0-9_]*$', max_length=1000)),
            ('_flags', self.gf('django.db.models.fields.CharField')(default='-Wall', max_length=1000, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('checker', ['JavaGCCBuilder'])

        # Adding model 'FortranBuilder'
        db.create_table('checker_fortranbuilder', (
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('_output_flags', self.gf('django.db.models.fields.CharField')(default='-o %s', max_length=1000, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('always', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_libs', self.gf('django.db.models.fields.CharField')(default='', max_length=1000, blank=True)),
            ('_file_pattern', self.gf('django.db.models.fields.CharField')(default='^[a-zA-Z0-9_]*$', max_length=1000)),
            ('_flags', self.gf('django.db.models.fields.CharField')(default='-Wall', max_length=1000, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('checker', ['FortranBuilder'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'CheckerResult'
        db.delete_table('checker_checkerresult')

        # Deleting model 'AnonymityChecker'
        db.delete_table('checker_anonymitychecker')

        # Deleting model 'InterfaceChecker'
        db.delete_table('checker_interfacechecker')

        # Deleting model 'LineWidthChecker'
        db.delete_table('checker_linewidthchecker')

        # Deleting model 'TextChecker'
        db.delete_table('checker_textchecker')

        # Deleting model 'DiffChecker'
        db.delete_table('checker_diffchecker')

        # Deleting model 'ScriptChecker'
        db.delete_table('checker_scriptchecker')

        # Deleting model 'CreateFileChecker'
        db.delete_table('checker_createfilechecker')

        # Deleting model 'LineCounter'
        db.delete_table('checker_linecounter')

        # Deleting model 'DejaGnuTester'
        db.delete_table('checker_dejagnutester')

        # Deleting model 'DejaGnuSetup'
        db.delete_table('checker_dejagnusetup')

        # Deleting model 'CBuilder'
        db.delete_table('checker_cbuilder')

        # Deleting model 'CXXBuilder'
        db.delete_table('checker_cxxbuilder')

        # Deleting model 'JavaBuilder'
        db.delete_table('checker_javabuilder')

        # Deleting model 'JavaGCCBuilder'
        db.delete_table('checker_javagccbuilder')

        # Deleting model 'FortranBuilder'
        db.delete_table('checker_fortranbuilder')
    
    
    models = {
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
        'checker.anonymitychecker': {
            'Meta': {'object_name': 'AnonymityChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.cbuilder': {
            'Meta': {'object_name': 'CBuilder'},
            '_file_pattern': ('django.db.models.fields.CharField', [], {'default': "'^[a-zA-Z0-9_]*$'", 'max_length': '1000'}),
            '_flags': ('django.db.models.fields.CharField', [], {'default': "'-Wall'", 'max_length': '1000', 'blank': 'True'}),
            '_libs': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            '_output_flags': ('django.db.models.fields.CharField', [], {'default': "'-o %s'", 'max_length': '1000', 'blank': 'True'}),
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.checkerresult': {
            'Meta': {'object_name': 'CheckerResult'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.TextField', [], {}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'passed': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'solution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['solutions.Solution']"})
        },
        'checker.createfilechecker': {
            'Meta': {'object_name': 'CreateFileChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.cxxbuilder': {
            'Meta': {'object_name': 'CXXBuilder'},
            '_file_pattern': ('django.db.models.fields.CharField', [], {'default': "'^[a-zA-Z0-9_]*$'", 'max_length': '1000'}),
            '_flags': ('django.db.models.fields.CharField', [], {'default': "'-Wall'", 'max_length': '1000', 'blank': 'True'}),
            '_libs': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            '_output_flags': ('django.db.models.fields.CharField', [], {'default': "'-o %s'", 'max_length': '1000', 'blank': 'True'}),
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.dejagnusetup': {
            'Meta': {'object_name': 'DejaGnuSetup'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"}),
            'test_defs': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'checker.dejagnutester': {
            'Meta': {'object_name': 'DejaGnuTester'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"}),
            'test_case': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'checker.diffchecker': {
            'Meta': {'object_name': 'DiffChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'output_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'shell_script': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.fortranbuilder': {
            'Meta': {'object_name': 'FortranBuilder'},
            '_file_pattern': ('django.db.models.fields.CharField', [], {'default': "'^[a-zA-Z0-9_]*$'", 'max_length': '1000'}),
            '_flags': ('django.db.models.fields.CharField', [], {'default': "'-Wall'", 'max_length': '1000', 'blank': 'True'}),
            '_libs': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            '_output_flags': ('django.db.models.fields.CharField', [], {'default': "'-o %s'", 'max_length': '1000', 'blank': 'True'}),
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.interfacechecker': {
            'Meta': {'object_name': 'InterfaceChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interface1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'interface2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'interface3': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'interface4': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'interface5': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'interface6': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'interface7': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.javabuilder': {
            'Meta': {'object_name': 'JavaBuilder'},
            '_file_pattern': ('django.db.models.fields.CharField', [], {'default': "'^[a-zA-Z0-9_]*$'", 'max_length': '1000'}),
            '_flags': ('django.db.models.fields.CharField', [], {'default': "'-Wall'", 'max_length': '1000', 'blank': 'True'}),
            '_libs': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            '_output_flags': ('django.db.models.fields.CharField', [], {'default': "'-o %s'", 'max_length': '1000', 'blank': 'True'}),
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.javagccbuilder': {
            'Meta': {'object_name': 'JavaGCCBuilder'},
            '_file_pattern': ('django.db.models.fields.CharField', [], {'default': "'^[a-zA-Z0-9_]*$'", 'max_length': '1000'}),
            '_flags': ('django.db.models.fields.CharField', [], {'default': "'-Wall'", 'max_length': '1000', 'blank': 'True'}),
            '_libs': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            '_output_flags': ('django.db.models.fields.CharField', [], {'default': "'-o %s'", 'max_length': '1000', 'blank': 'True'}),
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.linecounter': {
            'Meta': {'object_name': 'LineCounter'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.linewidthchecker': {
            'Meta': {'object_name': 'LineWidthChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_line_length': ('django.db.models.fields.IntegerField', [], {'default': '80'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.scriptchecker': {
            'Meta': {'object_name': 'ScriptChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Externen Tutor ausf\\xc3\\xbchren'", 'max_length': '100'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'remove': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'returns_html': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'shell_script': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'checker.textchecker': {
            'Meta': {'object_name': 'TextChecker'},
            'always': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"}),
            'text': ('django.db.models.fields.TextField', [], {})
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
        'tasks.task': {
            'Meta': {'object_name': 'Task'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['checker']
