from django.conf import settings

def from_settings(request):
	''' A context processor to add the "current site" to the current Context '''
	return {
		'SITE_NAME': settings.SITE_NAME,
	    'LOGIN_URL': settings.LOGIN_URL,
	    'REGISTRATION_POSSIBLE': settings.REGISTRATION_POSSIBLE,
	}

