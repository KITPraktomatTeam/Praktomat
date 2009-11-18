from django.conf.urls.defaults import *

urlpatterns = patterns('praktomat.solutions.views',
	url(r'^(?P<solution_id>\d+)/$', 'solution_detail', name='solution_detail'),
)



