from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^logout/$', 'oauthclient.views.logout', name='oauth_logout'),
    url(r'^redirect/$', 'oauthclient.views.redirect', name='oauth_redirect'),
)
