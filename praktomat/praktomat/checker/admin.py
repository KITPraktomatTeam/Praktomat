from django.contrib import admin
from django.contrib.contenttypes import generic
	
from django import forms
class addChangedFieldForm(forms.ModelForm):
	# Add a hidden field which is populated by java script when adding an new item so that django recognizes the item as saveworthy
	changed = forms.CharField(max_length=100,required=False,widget=forms.HiddenInput)

class CheckerInline(admin.StackedInline):
	""" Base class for checker inlines """
	extra = 1
	form = addChangedFieldForm
	#template = "admin/stacked.html"	