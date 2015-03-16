from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.contrib import admin
import public_gate.urls

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^public_gate/', include(public_gate.urls, namespace='public_gate')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'.*', RedirectView.as_view(url='/public_gate/home')),
)

