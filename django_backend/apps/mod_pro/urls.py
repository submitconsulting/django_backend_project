from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.mod_pro.views',
	url(r'^dashboard/$', 'mod_pro_dashboard', name='mod_pro_dashboard'),

) 