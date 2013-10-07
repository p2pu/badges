"""
Processors for dashboard
"""
from badge.models import get_badge
from badge.view_helpers import fetch_badge_resources

from project.processors import get_projects_ready_for_feedback
from project.processors import get_project_feedback
from project.processors import get_projects_user_gave_feedback
from project.processors import search_projects
from project.view_helpers import fetch_resources


def check_if_owner(request_user, request_username, user):
    """
    Cheking if user is owner of this dashboard
    """

    if request_user and request_user['username'] == request_username:
        user['is_owner'] = True

    return user


def list_projects_ready_for_feedback(badges):
    """
    Listing all projects for badges
    """

    projects_list = []

    for badge in badges:
        projects = get_projects_ready_for_feedback(badge['uri'])
        if projects:
            projects = get_feedback_for_project_list(projects)
            projects_list.append(projects)

    return [project for items in projects_list for project in items]


def get_feedback_for_project_list(project_list):
    """
    Fetching all feedback that is attached to project
    """

    for project in project_list:
        feedback_list = get_project_feedback(project['uri'])
        fetch_resources(project, feedback_list=feedback_list)

    return project_list


def list_projects_by_user(user_uri):
    """
    Listing all the projects that user has
    """
    projects = search_projects(author_uri=user_uri)

    for project in projects:
        badge = get_badge(project['badge_uri'])
        fetch_badge_resources(badge)
        feedback_list = get_project_feedback(project['uri'])
        fetch_resources(project, feedback_list=feedback_list)

    return projects


def list_projects_that_user_gave_feedback(user_uri):
    """
    Listing all project that user gave feedback to
    """

    projects_list = get_projects_user_gave_feedback(user_uri)

    for project in projects_list:
        badge = get_badge(project['badge_uri'])
        fetch_badge_resources(badge)

        feedback_list = get_project_feedback(project['uri'])
        fetch_resources(project, feedback_list=feedback_list)

    return projects_list

