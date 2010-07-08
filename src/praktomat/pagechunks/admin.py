from django.contrib import admin
from django.db import models
from models import Chunk

from tinymce.widgets import TinyMCE

class ChunkAdmin(admin.ModelAdmin):
	list_display = ('key', 'content')
	list_editable = ('content',)
	search_fields = ('key', 'content')
	
	fields = ('key', 'content')
	readonly_fields = ('key',)
	
	formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

admin.site.register(Chunk, ChunkAdmin)