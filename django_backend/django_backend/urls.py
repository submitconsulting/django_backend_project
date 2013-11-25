from django.conf.urls import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_backend.views.home', name='home'),
    # url(r'^django_backend/', include('django_backend.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #Atajos
    url(r'^$', 'apps.home.views.index', name='index'),
    #url(r'^choice_headquart/$', 'apps.home.views.choice_headquart', name='choice_headquart'),
    #url(r'^mod_backend_dashboard/$', 'apps.mod_backend.views.mod_backend_dashboard', name='mod_backend_dashboard'),
    #url(r'^mod_ventas_dashboard/$', 'apps.mod_ventas.views.mod_ventas_dashboard', name='mod_ventas_dashboard'),

    #Modules
    url(r'^home/', include('apps.home.urls')),
    url(r'^account/', include('apps.account.urls')),
    url(r'^params/', include('apps.params.urls')),

    url(r'^mod_backend/', include('apps.mod_backend.urls')),
    url(r'^mod_ventas/', include('apps.mod_ventas.urls')),
    url(r'^mod_pro/', include('apps.mod_pro.urls')),

    url(r'^sad/', include('apps.sad.urls')),
    url(r'^space/', include('apps.space.urls')),

    url(r'^maestros/', include('apps.maestros.urls')),

    url(r'^rrhh/', include('apps.rrhh.urls')),
    

    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),
)
