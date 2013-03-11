from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^create/(?P<badge_id>[\d]+)/$', 'project.views.create', name='project_create'),
    url(r'^(?P<project_id>[\d]+)/$', 'project.views.view', name='project_view'),
    url(r'^(?P<project_id>[\d]+)/feedback/$', 'project.views.feedback', name='project_feedback'),
    url(r'^(?P<project_id>[\d]+)/revise/$', 'project.views.revise', name='project_revise'),
    url(r'^review/$', 'project.views.review', name='project_review'),
)
