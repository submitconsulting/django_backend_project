from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.rrhh.views',
	url(r'^employee/index/(?P<field>[\w\d\-]+)/(?P<value>.*)/(?P<order>[\w\d\-]+)/$', 'employee_index', name='employee_index'),
	url(r'^employee/index/(?P<field>[\w\d\-]+)/(?P<value>.*)/$', 'employee_index', name='employee_index'),
	url(r'^employee/index/$', 'employee_index', name='employee_index'),
	url(r'^employee/add/$', 'employee_add', name='employee_add'),
	url(r'^employee/choice/(?P<key>.*)/$', 'employee_choice', name='employee_choice'),
	url(r'^employee/edit/$', 'employee_edit', name='employee_edit'),
	url(r'^employee/delete/(?P<key>.*)/$', 'employee_delete', name='employee_delete'),
	url(r'^employee_json_by_filter/$','employee_json_by_filter', name="employee_json_by_filter"),

	url(r'^employee/add_all/$', 'employee_add_all', name='employee_add_all'),
	
) 