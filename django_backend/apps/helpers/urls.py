from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.helpers.views',
	url(r'^error/$', 'error', name="error"),
	
)