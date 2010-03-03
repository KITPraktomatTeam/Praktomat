from django.contrib import admin
from praktomat.attestation.models import *
	
class RatingScaleItemInline(admin.TabularInline):
	model = RatingScaleItem
	extra = 1

class RatingScaleAdmin(admin.ModelAdmin):
	model = RatingScale
	inlines = [RatingScaleItemInline]
	
	class Media:
		js = [	'static/frameworks/jquery/jquery.js', 
				'static/frameworks/jquery/jquery-ui.js', 
				'static/script/dynamic_inlines_with_sort.js', ]
		
		css = { 'all' : ['static/styles/dynamic_inlines_with_sort.css',], }
admin.site.register(RatingScale, RatingScaleAdmin)

admin.site.register(RatingAspect)

class RatingAdminInline(admin.StackedInline):
	model = Rating
	extra = 1