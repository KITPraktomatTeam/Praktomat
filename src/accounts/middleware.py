from accounts.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class LazyUser(object):
	def __get__(self, request, obj_type=None):
		if not hasattr(request, '_cached_user'):
			from django.contrib.auth import get_user
			user = get_user(request)
			try: # Anonymous user has no custom user
				request._cached_user = user.user
			except:	
				request._cached_user = user
		return request._cached_user

class AuthenticationMiddleware(object):
	""" Get user subclass insted of baseclass in request.user"""
	def process_request(self, request):
		request.__class__.user = LazyUser() 
		return None

class LogoutInactiveUserMiddleware(object):
	""" Logout users who have been set to inactive so they cant use their sessions to operate on the site. """
	def process_request(self, request):
		if not request.user.is_authenticated():
			return
		if not request.user.is_active:
			userid = request.user.id
			logout(request)
			return HttpResponseRedirect(reverse('registration_deactivated', kwargs={ 'user_id' : userid }))
