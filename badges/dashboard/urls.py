from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^(?P<username>[\w\.\- ]+)/$', 'dashboard.views.profile_dashboard', name='dashboard'),
    url(r'^(?P<username>[\w\.\- ]+)/badges$', 'dashboard.views.profile_badges', name='profile_badges'),
    url(r'^(?P<username>[\w\.\- ]+)/feedback$', 'dashboard.views.profile_feedback', name='profile_feedback'),
)
