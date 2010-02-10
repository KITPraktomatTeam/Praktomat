from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.cache import never_cache
from django.utils import simplejson
import random

@login_required
@never_cache
def checker_progress(request):
    """ Return JSON object with information about the progress of the checker run."""
    checker_progress = request.session['checker_progress']    
    #checker_progress = random.randint(0, 100)
#    if checker_progress:
#        print checker_progress
#        json = simplejson.dumps({'progress': checker_progress})
#        return HttpResponse(json)
#    else:
#        return HttpResponseBadRequest('Server Error')
    if not checker_progress:
        checker_progress = 0
    print checker_progress
    json = simplejson.dumps({'progress': checker_progress})
    return HttpResponse(json)
