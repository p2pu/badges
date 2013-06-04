from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'landing.views.home', name='landing'),
    url(r'^search$', 'landing.views.search', name='search')
)
