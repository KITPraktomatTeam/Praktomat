from django.contrib import admin
from attestation.models import *
	
class RatingScaleItemInline(admin.TabularInline):
	model = RatingScaleItem
	extra = 0


class RatingScaleAdmin(admin.ModelAdmin):
	model = RatingScale
	inlines = [RatingScaleItemInline]

	class Media:
		js = (
			  'frameworks/jquery/jquery.js',
			  'frameworks/jquery/jquery-ui.js',
			  'frameworks/jquery/jquery.tinysort.js',
			  'script/rating_scale_sort.js',
		)
	
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
	fields = ( 'solution', 'author', 'created', 'public_comment', 'private_comment', 'final_grade', 'final', 'published','published_on')
	list_display = ('solution', 'author', 'created', 'final', 'published','published_on')
	list_filter = ('final', 'published', 'author', 'solution__author', 'solution__task')
	inlines = (RatingResultAdminInline, AnnotatedSolutionFileAdminInline)

	def get_form(self, request, obj=None, **kwargs):
		request.obj = obj
		return super(AttestationAdmin, self).get_form(request, obj,**kwargs)


	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == "final_grade":
			kwargs["queryset"] = RatingScaleItem.objects.filter(scale__id=request.obj.solution.task.final_grade_rating_scale.id)
		return super(AttestationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)




	
admin.site.register(Attestation, AttestationAdmin)


class RatingAdminInline(admin.StackedInline):
	""" used in task as inline """
	model = Rating
	extra = 0
