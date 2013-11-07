from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.mod_backend.views',
	url(r'^dashboard/$', 'mod_backend_dashboard', name='mod_backend_dashboard'),

) 