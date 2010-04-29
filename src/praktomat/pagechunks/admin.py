from django.contrib import admin
from models import Chunk
# Django-TinyMCE 1.5 conflicts with django 1.2 - wait for 1.6
#from tinymce.widgets import TinyMCE

class ChunkAdmin(admin.ModelAdmin):
	list_display = ('key', 'content')
	list_editable = ('content',)
	search_fields = ('key', 'content')
	
	fields = ('key', 'content')
	readonly_fields = ('key',)
	
	formfield_overrides = {
#        models.TextField: {'widget': TinyMCE()},
    }

admin.site.register(Chunk, ChunkAdmin)