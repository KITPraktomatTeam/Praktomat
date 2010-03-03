from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.cache import never_cache
from django.utils import simplejson

@login_required
@never_cache
def checker_progress(request):
    """ Return JSON object with information about the progress of the checker run."""
    try:
        checker_progress = request.session['checker_progress']
    except:
        checker_progress = 0    
        # return HttpResponseBadRequest('Server Error')    
    json = simplejson.dumps({'progress': checker_progress})
    return HttpResponse(json)
