from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^login/$', 'oauthclient.views.login', name='oauth_login'),
    url(r'^logout/$', 'oauthclient.views.logout', name='oauth_logout'),
    url(r'^redirect/$', 'oauthclient.views.redirect', name='oauth_redirect'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^become/(?P<username>[\w\-\.]+)/$', 'oauthclient.views.become'),
    )
