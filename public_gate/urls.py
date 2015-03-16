from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^home', 'public_gate.views.home', name="home"),
    url(r'^about/$', 'public_gate.views.about', name="about"),
    url(r'^contact/$', 'public_gate.views.contact', name="contact"),
    url(r'^login/$', 'public_gate.views.site_login', name="site_login"),
    url(r'^logout/$', 'public_gate.views.site_logout', name="site_logout"),
)