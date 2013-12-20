from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.params.views',
	url(r'^$', 'params_index', name='index'),

	#locality controllers
	url(r'^locality/index/(?P<field>[\w\d\-]+)/(?P<value>.*)/(?P<order>[\w\d\-]+)/$', 'locality_index', name='locality_index'),
	url(r'^locality/index/(?P<field>[\w\d\-]+)/(?P<value>.*)/$', 'locality_index', name='locality_index'),
	url(r'^locality/index/$', 'locality_index', name='locality_index'),
	url(r'^locality/$', 'locality_index', name='locality_index'),
	url(r'^locality/add/$', 'locality_add', name='locality_add'),
	url(r'^locality/edit/(?P<key>.*)/$', 'locality_edit', name='locality_edit'),
	url(r'^locality/delete/(?P<key>.*)/$', 'locality_delete', name='locality_delete'),
	url(r'^locality/state/(?P<state>[\w\d\-]+)/(?P<key>.*)/$', 'locality_state', name='locality_state'),
	url(r'^locality/report/(?P<field>[\w\d\-]+)/(?P<value>.*)/(?P<order>[\w\d\-]+)/$', 'locality_report', name='locality_report'),
	url(r'^locality/report/$', 'locality_report', name='locality_report'),
	#Fin locality controllers


) 