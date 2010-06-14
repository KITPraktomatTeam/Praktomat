from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from praktomat.accounts.models import UserProfile, Tutorial
from praktomat.accounts.templatetags.in_group import in_group


class UserProfileInline(admin.StackedInline):
    model = UserProfile
 
class UserProfileAdmin(UserAdmin):
	inlines = [UserProfileInline]
	
	# add activationstatus to list_display
	list_display = ('username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'is_trainer', 'is_tutor', 'email' )
    
	list_filter = ('groups', 'is_staff', 'is_superuser', 'is_active')
    
	def is_trainer(self, user):
		return in_group(user,"Trainer")
	is_trainer.boolean = True
		
	def is_tutor(self, user):
		return in_group(user,"Tutor")
	is_tutor.boolean = True

admin.site.unregister(User) 
admin.site.register(User, UserProfileAdmin)

class TutorialAdmin(admin.ModelAdmin):
	model = Tutorial
	list_display = ('name', 'tutors_flat',)
		
admin.site.register(Tutorial, TutorialAdmin)