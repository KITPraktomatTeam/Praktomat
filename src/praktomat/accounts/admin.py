from random import randint
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.auth.models import User as UserBase
from django.contrib.auth.admin import UserAdmin as UserBaseAdmin
from django.db.models import Count
from praktomat.accounts.models import User, Tutorial
from praktomat.accounts.templatetags.in_group import in_group
from praktomat.accounts.forms import AdminUserCreationForm, AdminUserChangeForm

 
class UserAdmin(UserBaseAdmin):
	model = User
	
	# add active status
	list_display = ('username', 'first_name', 'last_name', 'mat_number', 'tutorial', 'is_active', 'is_trainer', 'is_tutor', 'email', 'date_joined' )
	list_filter = ('groups', 'tutorial', 'is_staff', 'is_superuser', 'is_active')
	date_hierarchy = 'date_joined'
	actions = ['set_active', 'set_inactive', 'distribute_to_tutorials', 'export_users']
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
	
	def set_active(self, request, queryset):
		""" Export Task action """
		queryset.update(is_active=True)
		self.message_user(request, "Users were successfully activated.")
	
	def set_inactive(self, request, queryset):
		""" Export Task action """
		queryset.update(is_active=False)
		self.message_user(request, "Users were successfully inactivated.")

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
		my_urls = patterns('', url(r'^import/$', 'praktomat.accounts.views.import_user', name='user_import')) 
		return my_urls + urls

admin.site.unregister(UserBase) 
admin.site.register(User, UserAdmin)

class TutorialAdmin(admin.ModelAdmin):
	model = Tutorial
	list_display = ('name', 'tutors_flat',)
		
admin.site.register(Tutorial, TutorialAdmin)
