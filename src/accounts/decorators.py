from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.http import Http404

def shibboleth_support_required(the_func):
	"""
	Decorator for views that are only meaningful if SHIB_ENABLED is True
	"""
	def _decorated(*args, **kwargs):
		if settings.SHIB_ENABLED:
			return the_func(*args, **kwargs)
		else:
			raise Http404("Shibboleth support is disabled in this praktomat instance")
	return _decorated


def shibboleth_user_required(login_url=None):
    """
    Decorator for views that checks that the user is logged in and a
    shibboleth user.
    """
    return user_passes_test(lambda u: u.is_shibboleth_user(), login_url=login_url)

def local_user_required(func):
    """
    Decorator for views that checks that the user is logged in and not a
    shibboleth user.
    """
    decorator= user_passes_test(lambda u: not u.is_shibboleth_user())
    return decorator(func)
