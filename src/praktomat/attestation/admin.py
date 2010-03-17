from django.contrib import admin
from praktomat.attestation.models import *
	
class RatingScaleItemInline(admin.TabularInline):
	model = RatingScaleItem
	extra = 5

class RatingScaleAdmin(admin.ModelAdmin):
	model = RatingScale
	inlines = [RatingScaleItemInline]
	
admin.site.register(RatingScale, RatingScaleAdmin)

admin.site.register(RatingAspect)

class RatingAdminInline(admin.StackedInline):
	model = Rating
	extra = 0