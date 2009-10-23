from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from praktomat.accounts.models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
 
class UserProfileAdmin(UserAdmin):
	inlines = [UserProfileInline]
	
	# add activationstatus to list_display
	list_display = ('username', 'first_name', 'last_name', 'is_active', 'is_staff', 'email' )
    
    #exclude = ('last_login_0',) #That wont work!


admin.site.unregister(User) 
admin.site.register(User, UserProfileAdmin)
