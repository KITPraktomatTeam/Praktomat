from django.contrib import admin
from django.forms.models import BaseInlineFormSet, ModelForm

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
		if self.declared_fieldsets:
				return self.declared_fieldsets
		form = self.get_formset(request).form
		fields = form.base_fields.keys() + list(self.get_readonly_fields(request, obj))
		fields.remove('public')
		fields.remove('required')
		fields.remove('always')
		return [(self.model.description(), {'fields':(('public', 'required', 'always'),)}),
						(None, {'fields': fields })]
	
	
