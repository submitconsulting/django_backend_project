from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.home.views',
	url(r'^$', 'index', name="index"),
	#url(r'^dashboard$', 'dashboard', name="dashboard"),
	url(r'^choice_headquart/$', 'choice_headquart', name="choice_headquart"),

) 