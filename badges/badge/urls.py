from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^create/$', 'badge.views.create', name='badge_create'),
    url(r'^preview/(?P<badge_id>[\d]+)/$', 'badge.views.preview', name='badge_preview'),
    url(r'^publish/(?P<badge_id>[\d]+)/$', 'badge.views.publish', name='badge_publish'),
    url(r'^view/(?P<badge_id>[\d]+)/$', 'badge.views.view', name='badge_view'),
)
