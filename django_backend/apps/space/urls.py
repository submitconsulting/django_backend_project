from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.space.views',
	

	#enterprise controllers
	#url(r'^solution_add/$', 'solution_add', name="solution_add"),
	url(r'^enterprise/edit/$', 'enterprise_edit', name="enterprise_edit"),

	#solution controllers
	url(r'^solution/index/$', 'solution_index', name="solution_index"),
	url(r'^solution/add/$', 'solution_add', name="solution_add"),
	url(r'^solution/edit/(?P<key>.*)/$', 'solution_edit', name="solution_edit"),
	url(r'^solution/delete/(?P<key>.*)/$', 'solution_delete', name="solution_delete"),


) 