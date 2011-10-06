from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext

def phpbb(request):
	return render_to_response('sessionprofile/phpbb.html',{'phpbburl': 'https://praktomat.info.uni-karlsruhe.de/praktomat_2011_WS/forum/',},context_instance=RequestContext(request))
#	return HttpResponse(t.render(c))
#	return HttpResponse("Hello, world. You're at the poll index.")
