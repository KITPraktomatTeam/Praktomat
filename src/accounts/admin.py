from random import randint
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.auth.models import User as UserBase, Group
from django.contrib.auth.admin import UserAdmin as UserBaseAdmin
from django.db.models import Count
from accounts.models import User, Tutorial, ShowAllUser
from accounts.templatetags.in_group import in_group
from accounts.forms import AdminUserCreationForm, AdminUserChangeForm


class UserAdmin(UserBaseAdmin):
	model = User
	
	# add active status
	list_display = ('username', 'first_name', 'last_name', 'mat_number', 'tutorial', 'is_active', 'is_trainer', 'is_tutor', 'email', 'date_joined','is_failed_attempt' )
	list_filter = ('groups', 'tutorial', 'is_staff', 'is_superuser', 'is_active')
	search_fields = ['username', 'first_name', 'last_name', 'mat_number', 'email']
	date_hierarchy = 'date_joined'
	actions = ['set_active', 'set_inactive', 'set_tutor', 'distribute_to_tutorials', 'export_users']
	readonly_fields = ('last_login','date_joined')
	# exclude user_permissions
	fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'mat_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        (_('Groups'), {'fields': ('groups','tutorial')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
	
	form = AdminUserChangeForm
	add_form = AdminUserCreationForm
	
	def is_trainer(self, user):
		return in_group(user,"Trainer")
	is_trainer.boolean = True
		
	def is_tutor(self, user):
		return in_group(user,"Tutor")
	is_tutor.boolean = True

	def is_failed_attempt(self,user):
		successfull = [ u for u in User.objects.all().filter(mat_number=user.mat_number) if u.is_active]
		return (not successfull) 	
	is_failed_attempt.boolean = True
	
	def set_active(self, request, queryset):
		""" Export Task action """
		queryset.update(is_active=True)
		self.message_user(request, "Users were successfully activated.")
	
	def set_inactive(self, request, queryset):
		""" Export Task action """
		queryset.update(is_active=False)
		self.message_user(request, "Users were successfully inactivated.")

	def set_tutor(self, request, queryset):
		""" Change students to tutors """
		tutor_group = Group.objects.get(name='Tutor')
		user_group = Group.objects.get(name='User')
		for user in queryset:
			user.groups.add(tutor_group)
			user.groups.remove(user_group)
			user.save()
		self.message_user(request, "Users were successfully made to tutors.")

	def distribute_to_tutorials(self, request, queryset):
		""" Distribute selectet users evenly to all tutorials """
		users = list(queryset)
		for user in users:
			# remove tutorial from users so we can find the tutorial with the least amount of users
			user.tutorial = None
			user.save()
		while(users):
			# get random user an put him in the least populated tutorial
			user = users.pop(randint(0,len(users)-1))
			tutorial = Tutorial.objects.annotate(Count('user')).order_by('user__count')[0]
			user.tutorial = tutorial
			user.save()
		self.message_user(request, "All users were successfully distributed.")

	def export_users(self, request, queryset):
		from django.http import HttpResponse
		data = User.export_user(queryset)		
		response = HttpResponse(data, mimetype="application/xml")
		response['Content-Disposition'] = 'attachment; filename=user_export.xml'
		return response

	def get_urls(self):
		""" Add URL to user import """
		urls = super(UserAdmin, self).get_urls()
		from django.conf.urls.defaults import url, patterns
		my_urls = patterns('', url(r'^import/$', 'accounts.views.import_user', name='user_import')) 
		my_urls += patterns('', url(r'^import_tutorial_assignment/$', 'accounts.views.import_tutorial_assignment', name='import_tutorial_assignment')) 
		return my_urls + urls

# This should work in Django 1.4 :O
# from django.contrib.admin import SimpleListFilter
# class FailedRegistrationAttempts(admin.SimpleListFilter):
#	title = _('Registration')
#	
#	def lookups(self,request,model_admin):
#		return ( (('failed'), _('failed')), (('successfull'), _('sucessfull')) )
#
#	def queryset(self,request,users):
#		failed = User.objects.all().values('mat_number').annotate(failed=Count('mat_number')).filter(failed__gt=1)
#		if self.value() == 'failed':
#			return users.filter(mat_number__in=[u['mat_number'] for u in  failed])
#		
#		if self.value() == 'successfull':
#			return user.exclude(mat_number__in=[u['mat_number'] for u in  failed])


admin.site.unregister(UserBase) 
admin.site.register(User, UserAdmin)


class ShowAllUserAdmin(UserAdmin):
	model = User
	
	def __init__(self, model, admin_site):
		UserAdmin.__init__(self,User,admin_site)	

	def get_paginator(self, request, queryset, per_page, orphans=0, allow_empty_first_page=True):
		return self.paginator(queryset, 10000, orphans, allow_empty_first_page)

class TutorialAdmin(admin.ModelAdmin):
	model = Tutorial
	list_display = ('name', 'tutors_flat',)
		
	class Media:
		css = {
			"all": ("styles/admin_style.css",)
		}
admin.site.register(ShowAllUser,ShowAllUserAdmin)
		
admin.site.register(Tutorial, TutorialAdmin)
