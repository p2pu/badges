from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'landing.views.home', name='landing'),
    url(r'^search$', 'landing.views.search', name='search'),
    url(r'^browse', 'landing.views.browse_all_badges', name='browse_all_badges'),
)
