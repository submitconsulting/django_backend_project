from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.mod_ventas.views',
	url(r'^mod_ventas_dashboard/$', 'mod_ventas_dashboard', name="mod_ventas_dashboard"),

) 