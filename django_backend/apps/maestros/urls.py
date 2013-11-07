from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.maestros.views',
	url(r'^producto/index/(?P<field>[\w\d\-]+)/(?P<value>.*)/(?P<order>[\w\d\-]+)/$', 'producto_index', name='producto_index'),
	url(r'^producto/index/(?P<field>[\w\d\-]+)/(?P<value>.*)/$', 'producto_index', name='producto_index'),
	url(r'^producto/index/$', 'producto_index', name='producto_index'),
	url(r'^producto/add/$', 'producto_add', name='producto_add'),
	url(r'^producto/edit/(?P<key>.*)/$', 'producto_edit', name='producto_edit'),
	url(r'^producto/delete/(?P<key>.*)/$', 'producto_delete', name='producto_delete'),
	
) 