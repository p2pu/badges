from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^test$', 'open_badges.views.test', name='ob_test'),
    url(r'^assertion/(?P<uid>[\d]+)$', 'open_badges.views.get_assertion', name='ob_get_assertion'),
    url(r'^badge/(?P<badge_id>[\d]+)$', 'open_badges.views.get_badge', name='ob_get_badge'),
    url(r'^organisation$', 'open_badges.views.get_organisation', name='ob_get_organisation'),
)
