from praktomat.accounts.models import User

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