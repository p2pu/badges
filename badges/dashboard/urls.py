from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^(?P<username>[\w\.\- ]+)/$', 'dashboard.views.profile', name='dashboard'),
)
