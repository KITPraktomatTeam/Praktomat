from django.conf import settings
from django.urls import reverse

def from_settings(request):
    ''' A context processor to add the "current site" to the current Context '''
    return {
            'SITE_NAME': settings.SITE_NAME,
        'LOGIN_URL': reverse(settings.LOGIN_URL),
        'REGISTRATION_POSSIBLE': settings.REGISTRATION_POSSIBLE,
	    'ACCOUNT_CHANGE_POSSIBLE': settings.ACCOUNT_CHANGE_POSSIBLE,
        'MIRROR': settings.MIRROR,
        'HAS_JPLAG': hasattr(settings, 'JPLAGJAR'),
    }
