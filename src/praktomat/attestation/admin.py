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


class AnnotatedSolutionFileAdminInline(admin.StackedInline):
	model = AnnotatedSolutionFile
	fields = ('content',)
	extra, max_num  = 0, 0
	can_delete = False
	
class RatingResultAdminInline(admin.StackedInline):
	model = RatingResult
	fields = ('mark',)
	extra, max_num  = 0, 0
	can_delete = False
	
class AttestationAdmin(admin.ModelAdmin):
	model = Attestation
	readonly_fields = ('created',)
	fields = ( 'solution', 'author', 'created', 'public_comment', 'private_comment', 'final_grade', 'final', 'published')
	list_display = ('solution', 'author', 'created', 'final', 'published')
	list_filter = ('final', 'published', 'author')
	inlines = (RatingResultAdminInline, AnnotatedSolutionFileAdminInline)
	
admin.site.register(Attestation, AttestationAdmin)


class RatingAdminInline(admin.StackedInline):
	""" used in task as inline """
	model = Rating
	extra = 0