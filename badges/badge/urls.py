from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^create/$', 'badge.views.create', name='badge_create'),
    url(r'^preview/(?P<badge_id>[\d]+)/$', 'badge.views.preview', name='badge_preview'),
    url(r'^edit/(?P<badge_id>[\d]+)/$', 'badge.views.edit', name='badge_edit'),
    url(r'^publish/(?P<badge_id>[\d]+)/$', 'badge.views.publish', name='badge_publish'),
    url(r'^view/(?P<badge_id>[\d]+)/$', 'badge.views.view', name='badge_view'),
    url(r'^pushed/(?P<award_id>[\d]+)/$', 'badge.views.pushed_to_backpack', name='badge_pushed_to_backpack'),
    url(r'^delete/(?P<badge_id>[\d]+)/$', 'badge.views.delete', name='badge_delete'),
    url(r'^view/(?P<badge_id>[\d]+)/embedded/$', 'badge.views.view_embedded', name='badge_view_embedded'),
    url(r'^featured_feed/$', 'badge.views.featured_feed', name='badge_featured_feed'),
    url(r'^name_search/$', 'badge.views.name_search', name='name_search'),
)
