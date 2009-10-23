from django.contrib import admin
from django.contrib.contenttypes import generic

class CheckerInline(admin.StackedInline):
	""" Base class for checker inlines """
	extra = 1
	#template = "admin/stacked.html"
	
from django import forms
class addChangedFieldForm(forms.ModelForm):
	changed = forms.CharField(max_length=100,required=False,widget=forms.HiddenInput)
	
class AllDefaultCheckerInline(CheckerInline):
	""" Base class for checker inlines, which required fields have all default values """
	# Add a hidden field which is populated by java script when adding an new item so that django recognizes the item as saveworthy
	form = addChangedFieldForm







	

# weg!
from praktomat.checker.models import CheckerProxy
class CheckerProxyInline(generic.GenericTabularInline):
	model = CheckerProxy
	extra = 1
	max_num = 1









