from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^oembed$', 'oembed.views.oembed', name='oembed'),
)
