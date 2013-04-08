from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^test$', 'open_badges.views.test', name='ob_test'),
)
