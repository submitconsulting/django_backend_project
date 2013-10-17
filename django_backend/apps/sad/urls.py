from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.sad.views',
 	# micontroller/mi_action

	url(r'^menu/index/(?P<field>[\w\d\-]+)/(?P<value>.*)/(?P<order>[\w\d\-]+)/$', 'menu_index', name="menu_index"),
	url(r'^menu/index/(?P<field>[\w\d\-]+)/(?P<value>.*)/$', 'menu_index', name="menu_index"),
	url(r'^menu/index/$', 'menu_index', name="menu_index"),
	url(r'^menu/add/$', 'menu_add', name="menu_add"),
	url(r'^menu/edit/(?P<key>.*)/$', 'menu_edit', name="menu_edit"),
	url(r'^menu/delete/(?P<key>.*)/$', 'menu_delete', name="menu_delete"),




	url(r'^module/index/$', 'module_index', name="module_index"),
	url(r'^module/add/$', 'module_add', name="module_add"),
	url(r'^module/edit/(?P<key>.*)/$', 'module_edit', name="module_edit"),
	url(r'^module/delete/(?P<key>.*)/$', 'module_delete', name="module_delete"),
	url(r'^module/plans_edit/$', 'module_plans_edit', name="module_plans_edit"),

	url(r'^group/index/$', 'group_index', name="group_index"),
	url(r'^group/add/$', 'group_add', name="group_add"),
	url(r'^group/edit/(?P<key>.*)/$', 'group_edit', name="group_edit"),
	url(r'^group/delete/(?P<key>.*)/$', 'group_delete', name="group_delete"),
	url(r'^group/permissions_edit/$', 'group_permissions_edit', name="group_permissions_edit"),#agregar este recurso manualmente


	url(r'^resource/index/$', 'resource_index', name="resource_index"),
	url(r'^resource/add/$', 'resource_add', name="resource_add"),
	url(r'^resource/edit/(?P<key>.*)/$', 'resource_edit', name="resource_edit"),
	url(r'^resource/delete/(?P<key>.*)/$', 'resource_delete', name="resource_delete"),

) 