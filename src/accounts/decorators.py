from django.contrib.auth.decorators import user_passes_test

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
