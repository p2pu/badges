from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = i18n_patterns('',
    # Examples:
    # url(r'^$', 'badges.views.home', name='home'),
    # url(r'^badges/', include('badges.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', include('landing.urls')),
    url(r'^badge/', include('badge.urls')),
    url(r'^project/', include('project.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
)

urlpatterns += patterns('',
    url(r'^oauth/', include('oauthclient.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
