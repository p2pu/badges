from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.views.generic import simple


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = i18n_patterns('',
    url(r'^scrapy/doc/', include('django.contrib.admindocs.urls')),
    url(r'^scrapy/', include(admin.site.urls)),
    url(r'^$', include('landing.urls')),
    url(r'^badge/', include('badge.urls')),
    url(r'^project/', include('project.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^about$', 'django.views.generic.simple.direct_to_template', {'template': 'about/home.html'}, name='about'),
)

urlpatterns += patterns('',
    url(r'^oauth/', include('oauthclient.urls')),
    url(r'^openbadges/', include('open_badges.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
