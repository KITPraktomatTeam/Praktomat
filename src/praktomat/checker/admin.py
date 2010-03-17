from django.contrib import admin

class CheckerInline(admin.StackedInline):
	""" Base class for checker inlines """
	extra = 0
