from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.home.views',
	url(r'^$', 'index', name='index'),
	url(r'^choice_headquart/(?P<field>[\w\d\-]+)/(?P<value>.*)/$', 'choice_headquart', name='choice_headquart'),
	url(r'^choice_headquart/$', 'choice_headquart', name='choice_headquart'),


) 