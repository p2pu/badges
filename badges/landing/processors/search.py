from django.db.models import Q

from badge import models as badge_api
from badge.view_helpers import fetch_badge_resources

from project import processors as project_api
from project.view_helpers import fetch_resources as fetch_project_resources

from p2pu_user import models as p2pu_user_api


def search_badges(text):
    query = Q(title__icontains=text) | \
            Q(description__icontains=text) | \
            Q(requirements__icontains=text) | \
            Q(author_uri__icontains=text)
    badges = badge_api.Badge.objects.filter(query, deleted=False, date_published__isnull=False) \
        .order_by('title').distinct().all()
    badges_val = []
    for badge in badges:
        badges_val.append(fetch_badge_resources(badge_api._badge2dict(badge)))
    return badges_val


def search_projects(text):
    query = Q(title__icontains=text) | \
            Q(image_uri__icontains=text) | \
            Q(work_url__icontains=text) | \
            Q(description__icontains=text) | \
            Q(reflection__icontains=text) | \
            Q(tags__icontains=text) | \
            Q(badge_uri__icontains=text) | \
            Q(author_uri__icontains=text)
    projects = project_api.Project.objects.filter(query, date_deleted__isnull=True) \
        .order_by('title').distinct().all()
    projects_val = []
    for project in projects:
        projects_val.append(fetch_project_resources(project_api._project2dict(project)))
    return projects_val


def search_users(text):
    query = Q(username__icontains=text) | \
            Q(image_url__icontains=text)
    users = p2pu_user_api.User.objects.filter(query) \
        .order_by('username').distinct().all()
    users_val = []
    for user in users:
        users_val.append(p2pu_user_api._user2dict(user))
    print users_val
    return users_val


def search_results(text):
    return{
        'badges': search_badges(text),
        'projects': search_projects(text),
        'learners': search_users(text)
    }
