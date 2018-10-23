from django.contrib import admin
from django.forms.models import BaseInlineFormSet, ModelForm
from django.core.urlresolvers import reverse
from basemodels import CheckerResult

class AlwaysChangedModelForm(ModelForm):
	""" This fixes the creation of inlines without modifing any of it's values. The standart ModelForm would just ignore these inlines. """
	def has_changed(self):
		""" Should returns True if data differs from initial. By always returning true even unchanged inlines will get validated and saved."""
		return True

class CheckerInline(admin.StackedInline):
	""" Base class for checker inlines """
	extra = 0
	form = AlwaysChangedModelForm
	# added checker class to inlinegroup and inlinerelated for js ordering in admin
	# this is a copy of the django template with only minor changes - keep in sync with new django versions
	template = "admin/tasks/stacked.html" 

	def get_fieldsets(self, request, obj=None):
		""" Get the fields public, required and always on the first line without defining fieldsets in every subclass. This saves a lot of space. """

		form = self.get_formset(request, obj, fields=None).form
		fields = form.base_fields.keys() + list(self.get_readonly_fields(request, obj))
		fields.remove('public')
		fields.remove('required')
		fields.remove('always')
		fields.remove('critical')
	        return [(self.model.description(), {'fields':(('public', 'required', 'always', 'critical'),)}),
						(None, {'fields': fields })]

class CheckerResultAdmin(admin.ModelAdmin):
	model = CheckerResult
	list_display = ["edit", "view_solution", "solution_final", "checker", "passed", "creation_date", "runtime"]
	readonly_fields = ["solution", "checker", "passed", "creation_date", "runtime"]
	list_filter = ["solution__final", "passed", "solution__task", "creation_date"]

	def get_queryset(self,request):
		qs = super(CheckerResultAdmin,self).get_queryset(request)
		qs = qs.select_related("solution", "solution__task", "solution__author")
		qs = qs.prefetch_related("checker")
		return qs

	def edit(self,checkerResult):
		return 'Edit'
	edit.short_description = 'Edit (Admin Site)'

	def view_solution(self,checkerResult):
		return '<a href="%s">%s</a>' % (reverse('solution_detail_full', args=[checkerResult.solution.id]),checkerResult.solution)
	view_solution.allow_tags = True
	view_solution.short_description = 'View Solution (User Site)'

	def solution_final(self,checkerResult):
		return checkerResult.solution.final
	solution_final.boolean = True

	def has_add_permission(self, request):
		return False

admin.site.register(CheckerResult, CheckerResultAdmin)
