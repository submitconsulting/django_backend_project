from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.mod_ventas.views',
	url(r'^dashboard/$', 'mod_ventas_dashboard', name="mod_ventas_dashboard"),

) 