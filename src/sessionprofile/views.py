from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.conf import settings


def phpbb(request):
	return render_to_response('sessionprofile/phpbb.html',{'phpbburl': settings.BASE_URL+'forum/',},context_instance=RequestContext(request))
