from django.contrib import admin
from django.forms.models import BaseInlineFormSet, ModelForm

class AlwaysChangedModelForm(ModelForm):
	def has_changed(self):
		""" Should returns True if data differs from initial. 
		By always returning true even unchanged inlines will get validated and saved."""
		return True

class CheckerInline(admin.StackedInline):
	""" Base class for checker inlines """
	extra = 0
	form = AlwaysChangedModelForm
