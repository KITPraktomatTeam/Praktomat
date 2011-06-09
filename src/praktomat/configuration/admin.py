from django.contrib import admin
from django.db import models
from models import Settings, Chunk

from tinymce.widgets import TinyMCE

class ChunkInline(admin.StackedInline):
	model = Chunk
	fields = ('content',)
	max_num = 0 		# don't allow adds
	can_delete = False 
	
	formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

class SettingsAdmin(admin.ModelAdmin):	
	
	fields = ('email_validation_regex', 'mat_number_validation_regex', 'deny_registration_from', 'anonymous_attestation')
	inlines = [ChunkInline]

admin.site.register(Settings, SettingsAdmin)