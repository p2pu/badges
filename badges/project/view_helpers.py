"""
Project helpers
"""
from badge.models import get_badge
from badge.view_helpers import fetch_badge_resources

from media.processors import get_image
from p2pu_user.models import get_user


def fetch_resources(project, feedback_list=None):
    project['image'] = get_image(project['image_uri'])
    project['author'] = get_user(project['author_uri'])

    project['badge'] = get_badge(project['badge_uri'])
    fetch_badge_resources(project['badge'])

    if feedback_list:
        add_feedback_to_project(feedback_list, project)

    return project


def add_feedback_to_project(feedback_list, project):
    """
    Setting attributes to projects if Badge was awarded
    """

    if not feedback_list:
        return project

    ret_val = {}
    for feedback in feedback_list:
        if 'badge_awarded' in feedback and feedback['badge_awarded']:
            ret_val['badge_awarded'] = True
            ret_val['badge_awarded_date'] = feedback['date_created']
        else:
            ret_val['badge_awarded'] = False

    if ret_val:
        project['feedback'] = ret_val

    return project
