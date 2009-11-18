from django.conf.urls.defaults import *

urlpatterns = patterns('praktomat.attestation.views',
	url(r'^statistics$', 'statistics', name='statistics'),
	url(r'^$', 'attestation_list', name='attestation_list'),
	url(r'^$', 'attestation', name='attestation'),
)
