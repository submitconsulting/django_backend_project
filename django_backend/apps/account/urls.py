from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.account.views',
	url(r'^add_enterprise/$', 'add_enterprise', name="add_enterprise"),
	url(r'^signup/$', 'signup_sys', name="signup_sys"),
	url(r'^login/$', 'login_sys', name="login_sys"),
	url(r'^load_access/(?P<headquart_id>.*)/(?P<module_id>.*)/$', 'load_access', name="load_access"),
	url(r'^logout/$', 'logout_sys', name="logout_sys"),
	url(r'^profile/$', 'profile', name="profile"),
	
)