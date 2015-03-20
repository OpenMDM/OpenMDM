from django.conf.urls import patterns, url
from public_gate import views

urlpatterns = patterns('',
    # Base
    url(r'^home',                                           'public_gate.views.home',                       name="home"),
    url(r'^about/$',                                        'public_gate.views.about',                      name="about"),
    url(r'^contact/$',                                      'public_gate.views.contact',                    name="contact"),
    url(r'^test/$',                                         'public_gate.views.test',                       name="test"),

    # Authentication
    url(r'^login/$',                                        'public_gate.views.site_login',                 name="site_login"),
    url(r'^logout/$',                                       'public_gate.views.site_logout',                name="site_logout"),

    # Property lists
    url(r'^property_list/$',                                'public_gate.views.property_lists',             name="property_lists"),
    url(r'^property_list/(?P<plist_id>\d+)/$',              views.property_list_detail,                     name='property_list_detail'),
    url(r'^property_list/(?P<plist_id>\d+)/download/$',     views.property_list_download,                   name='property_list_download'),
    url(r'^user/property_lists/$',                          'public_gate.views.property_lists_for_user',    name='property_lists_for_user'),
    url(r'^property_list/add/$',                            'public_gate.views.add_property_list',          name="property_list_add"),

    # Users
    url(r'^client/$',                                       'public_gate.views.users',                      name="users"),
    url(r'^client/(?P<user_id>\d+)/$',                      views.user_detail,                              name="user_detail"),
    url(r'^client/add/$',                                   'public_gate.views.add_user',                   name="user_add"),
)