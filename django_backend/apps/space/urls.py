from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.space.views',
	
	#headquart controllers
	url(r'^headquart/index/$', 'headquart_index', name="headquart_index"),
	url(r'^headquart/add/$', 'headquart_add', name="headquart_add"),
	url(r'^headquart/edit/(?P<key>.*)/$', 'headquart_edit', name="headquart_edit"),
	url(r'^headquart/delete/(?P<key>.*)/$', 'headquart_delete', name="headquart_delete"),

	#enterprise controllers
	url(r'^enterprise/index/$', 'enterprise_index', name="enterprise_index"),
	url(r'^enterprise/add/$', 'enterprise_add', name="enterprise_add"),
	url(r'^enterprise/edit/(?P<key>.*)/$', 'enterprise_edit', name="enterprise_edit"),
	url(r'^enterprise/delete/(?P<key>.*)/$', 'enterprise_delete', name="enterprise_delete"),
	url(r'^enterprise/edit_current/$', 'enterprise_edit_current', name="enterprise_edit_current"),
	url(r'^enterprise/upload/$', 'enterprise_upload', name="enterprise_upload"),
	
	#association controllers
	url(r'^association/edit_current/$', 'association_edit_current', name="association_edit_current"),
	url(r'^association/upload/$', 'association_upload', name="association_upload"),
	
	#solution controllers
	url(r'^solution/index/$', 'solution_index', name="solution_index"),
	url(r'^solution/add/$', 'solution_add', name="solution_add"),
	url(r'^solution/edit/(?P<key>.*)/$', 'solution_edit', name="solution_edit"),
	url(r'^solution/delete/(?P<key>.*)/$', 'solution_delete', name="solution_delete"),


) 