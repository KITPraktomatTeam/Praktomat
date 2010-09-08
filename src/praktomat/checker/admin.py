from django.contrib import admin
from django.forms.models import BaseInlineFormSet

class RequiredInlineFormSet(BaseInlineFormSet):
	"""
	Generates an inline formset that is required
	"""



class CheckerInline(admin.StackedInline):
	""" Base class for checker inlines """
	extra = 0
	formset = RequiredInlineFormSet
