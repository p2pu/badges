from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^create/(?P<badge_id>[\d]+)/$', 'project.views.create', name='project_create'),
    url(r'^view/(?P<project_id>[\d]+)/$', 'project.views.view', name='project_view'),
)
