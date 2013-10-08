from datetime import datetime

from .models import Project
from .models import Revision
from .models import Feedback
from .notification_helpers import send_project_creation_notification, send_badge_needs_partner_feedback_notification
from .notification_helpers import send_project_creation_expert_notification
from .notification_helpers import send_feedback_notification
from .notification_helpers import send_revision_notification

from badge.models import get_badge
from badge.models import get_badge_experts
from p2pu_user import models as p2pu_user_api


class MultipleProjectError(Exception):
    pass


def uri2id(uri):
    return uri.strip('/').split('/')[-1]


def id2uri(id):
    return '/uri/project/{0}'.format(id)


def _project2dict(project_db):
    project = {
        'id': project_db.id,
        'uri': id2uri(project_db.id),
        'title': project_db.title,
        'image_uri': project_db.image_uri,
        'work_url': project_db.work_url,
        'description': project_db.description,
        'reflection': project_db.reflection,
        'tags': project_db.tags.split(','),
        'badge_uri': project_db.badge_uri,
        'author_uri': project_db.author_uri,
        'date_created': project_db.date_created,
    }
    return project


def create_project(badge_uri, author_uri, title, image_uri, work_url, description, reflection, tags):

    if Project.objects.filter(author_uri=author_uri, badge_uri=badge_uri, date_deleted__isnull=True).exists():
        raise MultipleProjectError('A user can only submit 1 project for a badge')

    badge = get_badge(badge_uri)

    if author_uri in get_badge_experts(badge_uri):
        raise Exception(u'Badge {0} already awarded to user'.format(badge_uri))

    if isinstance(tags, list):
        tags = ','.join(tags)

    project_db = Project(
        title=title,
        image_uri=image_uri,
        work_url=work_url,
        description=description,
        reflection=reflection,
        tags=tags,
        badge_uri=badge_uri,
        author_uri=author_uri,
        date_created=datetime.utcnow(),
        date_updated=datetime.utcnow()
    )
    project_db.save()

    project = get_project(id2uri(project_db.id))

    send_project_creation_notification(project)
    experts = get_badge_experts(project['badge_uri'])
    send_project_creation_expert_notification(project, badge, experts)
    return project


def get_project(uri):
    project_db = Project.objects.get(id=uri2id(uri))
    if not project_db.date_deleted is None:
        raise Exception('Project deleted')

    return _project2dict(project_db)


def last_n_projects(n):
    projects = Project.objects.filter(date_deleted__isnull=True).order_by('-pk')[:n]
    return [_project2dict(project) for project in projects]


def get_projects():
    projects = Project.objects.filter(date_deleted__isnull=True)
    return [_project2dict(project) for project in projects]


def get_projects_submitted_by_user(user_uri):
    projects = Project.objects.filter(author_uri=user_uri)
    if projects:
        for project in projects:
            feedback = get_project_feedback(id2uri(project.pk))
    return [_project2dict(project) for project in projects]


def get_project_awarded_to_expert(badge_uri, expert_uri):

    projects = Project.objects.filter(badge_uri=badge_uri, author_uri=expert_uri)

    return [_project2dict(project) for project in projects]


def search_projects_awarded_badges(badge_uri=None, author_uri=None):
    projects = []

    if badge_uri:
        projects = Project.objects.filter(badge_uri=badge_uri, feedback__badge_awarded=True,
                                          date_deleted__isnull=True)
    if author_uri:
        projects = Project.objects.filter(author_uri=author_uri, feedback__badge_awarded=True,
                                          date_deleted__isnull=True)

    return [_project2dict(project) for project in projects]


def search_projects(badge_uri=None, author_uri=None):
    projects = Project.objects.filter(date_deleted__isnull=True)
    if badge_uri:
        projects = projects.filter(badge_uri=badge_uri)
    if author_uri:
        projects = projects.filter(author_uri=author_uri)
    return [_project2dict(project) for project in projects]


def get_projects_ready_for_feedback(badge_uri):
    """
    Getting projects for a Badge that are ready for feedback
    """
    projects_list = []

    projects = Project.objects.filter(date_deleted__isnull=True, badge_uri=badge_uri)

    for project in projects:
        feedback = Feedback.objects.filter(project=project, badge_awarded=True).exists()

        if project and not feedback and ready_for_feedback(id2uri(project.id), project):
            projects_list.append(_project2dict(project))
    return projects_list


def can_revise_project(project_uri):
    project=Project.objects.get(id=uri2id(project_uri))

    last_revision = None
    if project.revision_set.count() > 0:
        last_revision = project.revision_set.latest('date_created')
    last_feedback = None
    if project.feedback_set.count() > 0:
        last_feedback = project.feedback_set.latest('date_created')

    if not last_feedback:  #or last_revision and last_revision.date_created > last_feedback.date_created:
        return False
    if last_feedback and last_feedback.badge_awarded:
        return False
    return True


def revise_project(project_uri, improvement, work_url=None):
    project = Project.objects.get(id=uri2id(project_uri))

    if not can_revise_project(project_uri):
        raise Exception('Revision can only be given before badge is awarded')
    
    last_feedback = None
    if project.feedback_set.count() > 0:
        last_feedback = project.feedback_set.latest('date_created')

    revision = Revision(
        project=project,
        improvement=improvement,
        date_created=datetime.utcnow()
    )
    if work_url:
        revision.work_url = work_url
    revision.save()

    send_revision_notification(
        get_project(project_uri),
        [last_feedback.expert_uri]
    )
    return _revision2dict(revision)


def ready_for_feedback(project_uri, project=None):
    """
    Check if this is the right time in the cycle for an expert to give feedback
    """
    if not project:
        project = Project.objects.get(id=uri2id(project_uri))

    last_feedback = None
    if project.feedback_set.count() > 0:
        last_feedback = project.feedback_set.latest('date_created')

    if last_feedback:
        if last_feedback.badge_awarded:
            return False

    return True


def can_badge_be_awarded(badge, expert_uri):
    if not badge['partner_name']:
        return True
    elif badge['partner_name'] and expert_uri == badge['author_uri']:
        return True
    return False


class submit_feedback_result:
    AWARDED = 1
    NOT_AWARDED = 2
    REQUIRES_APPROVAL = 3


def submit_feedback(project_uri, expert_uri, good, bad, ugly, award_badge=False):
    """
    Checks if badge can be awarded and creates feedback
    """

    project = Project.objects.get(id=uri2id(project_uri))
    badge = get_badge(project.badge_uri)
    result = submit_feedback_result.NOT_AWARDED

    if not expert_uri in get_badge_experts(project.badge_uri):
        raise Exception('Only experts can submit feedback on projects.')

    if not ready_for_feedback(project_uri):
        raise Exception('Badge has already been awarded to project.')

    feedback = Feedback(
        project=project,
        expert_uri=expert_uri,
        good=good,
        bad=bad,
        ugly=ugly,
        date_created=datetime.utcnow(),
        badge_awarded=False
    )

    if award_badge and can_badge_be_awarded(badge, expert_uri):
        result = submit_feedback_result.AWARDED
        feedback.badge_awarded = True
    elif award_badge: #and badge requires approval by partner
        result = submit_feedback_result.REQUIRES_APPROVAL
        send_badge_needs_partner_feedback_notification(badge, _project2dict(project), expert_uri)

    last_revision = None
    if project.revision_set.count() > 0:
        last_revision = project.revision_set.latest('date_created')

    if last_revision:
        feedback.revision = last_revision

    feedback.save()

    send_feedback_notification(get_project(project_uri))
    #return _feedback2dict(feedback)
    return result


def _revision2dict(revision):
    json = {
        'improvement': revision.improvement,
        'date_created': revision.date_created
    }
    if revision.work_url:
        json['work_url'] = revision.work_url
    return json


def _feedback2dict(feedback):

    json = {
        'expert_uri': feedback.expert_uri,
        'expert': p2pu_user_api.get_user(feedback.expert_uri),
        'good': feedback.good,
        'bad': feedback.bad,
        'ugly': feedback.ugly,
        'date_created': feedback.date_created,
        'badge_awarded': feedback.badge_awarded,
        'project': _project2dict(feedback.project)
    }
    return json


def get_project_feedback(project_uri):
    feedback_revision = []

    project=Project.objects.get(id=uri2id(project_uri))

    for feedback in Feedback.objects.filter(project=project).order_by('date_created'):
        feedback_revision += [_feedback2dict(feedback)]

    for revision in Revision.objects.filter(project=project).order_by('date_created'):
        feedback_revision += [_revision2dict(revision)]

    keyfunc = lambda obj: obj['date_created']
    feedback_revision.sort(key=keyfunc)

    return feedback_revision


def get_badge_uri_from_project_under_revision(project_uri):
    project=Project.objects.get(id=uri2id(project_uri))

    if project.feedback_set.count() > 0:
        last_feedback = project.feedback_set.latest('date_created')
        if last_feedback and last_feedback.badge_awarded:
            return None
    return project.badge_uri


def get_projects_user_gave_feedback(user_uri):

    project_list = Project.objects.filter(feedback__expert_uri=user_uri).distinct()

    return [_project2dict(project) for project in project_list]


