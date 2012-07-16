from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# for some reason include('django.contrib.auth.urls') wouldn't work with {% url ... %} aka reverse() 
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
	url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='auth_login'),
	url(r'^logout/$', auth_views.logout_then_login, name='auth_logout'),
	url(r'^change/$', 'accounts.views.change', name='registration_change'),				   
	url(r'^password/change/$', auth_views.password_change, name='auth_password_change'),
	url(r'^password/change/done/$', auth_views.password_change_done, name='auth_password_change_done'),
	url(r'^password/reset/$', auth_views.password_reset, name='auth_password_reset'),
	url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name='auth_password_reset_confirm'),
	url(r'^password/reset/complete/$', auth_views.password_reset_complete, name='auth_password_reset_complete'),
	url(r'^password/reset/done/$', auth_views.password_reset_done, name='auth_password_reset_done'),
	url(r'^register/$', 'accounts.views.register', name='registration_register'),
	url(r'^register/complete/$', direct_to_template, {'template': 'registration/registration_complete.html'}, name='registration_complete'),
	url(r'^register/allow/(?P<user_id>\d+)/$', 'accounts.views.activation_allow', name='activation_allow'),
	url(r'^activate/(?P<activation_key>.+)/$', 'accounts.views.activate', name='registration_activate'),
)

