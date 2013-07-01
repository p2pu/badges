from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^oembed$', 'services.views.oembed', name='oembed'),
)
