from project.db import Project
from project.db import Revision
from project.db import Feedback
from datetime import datetime


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
        'steps': project_db.steps,
        'reflection': project_db.reflection,
        'tags': project_db.tags.split(','),
        'badge_uri': project_db.badge_uri,
        'user_uri': project_db.user_uri
    }
    return project


def create_project(badge_uri, user_uri, title, image_uri, work_url, steps, reflection, tags):
    
    if Project.objects.filter(user_uri=user_uri, badge_uri=badge_uri, date_deleted__isnull=True).exists():
        raise MultipleProjectError('A user can only submit 1 project for a badge')

    if isinstance(tags, list):
        tags = ','.join(tags)

    project_db = Project(
        title=title,
        image_uri=image_uri,
        work_url=work_url,
        steps=steps,
        reflection=reflection,
        tags=tags,
        badge_uri=badge_uri,
        user_uri=user_uri,
        date_created=datetime.utcnow(),
        date_updated=datetime.utcnow()
    )
    project_db.save()

    return get_project(id2uri(project_db.id))


def get_project(uri):
    project_db = Project.objects.get(id=uri2id(uri))
    if not project_db.date_deleted == None:
        raise Exception('Project deleted')

    return _project2dict(project_db)


def get_projects_for_badge(badge_uri):
    projects = Project.objects.filter(badge_uri=badge_uri, date_deleted__isnull=True)
    return [_project2dict(project) for project in projects]


def revise_project(project_uri, improvement, work_url=None):
    project=Project.objects.get(id=uri2id(project_uri))

    last_revision = None
    if project.revision_set.count() > 0:
        last_revision = project.revision_set.latest('date_created')
    last_feedback = None
    if project.feedback_set.count() > 0:
        last_feedback = project.feedback_set.latest('date_created')

    if not last_feedback or last_revision and last_revision.date_created > last_feedback.date_created:
        raise Exception('Cannot submit a revison before receiving a review')

    revision = Revision(
        project=project,
        improvement=improvement,
        date_created=datetime.utcnow()
    )
    if work_url:
        revision.work_url = work_url
    revision.save()


def submit_feedback(project_uri, expert_uri, good, bad, ugly):
    project=Project.objects.get(id=uri2id(project_uri))

    last_revision = None
    if project.revision_set.count() > 0:
        last_revision = project.revision_set.latest('date_created')
    last_feedback = None
    if project.feedback_set.count() > 0:
        last_feedback = project.feedback_set.latest('date_created')

    if last_feedback:
        if not last_revision or last_feedback.date_created > last_revision.date_created:
            raise Exception('No revision submitted on last feedback')

    feedback = Feedback(
        project=project,
        expert_uri=expert_uri,
        good=good,
        bad=bad,
        ugly=ugly,
        date_created=datetime.utcnow()
    )
    
    if last_revision:
        feedback.revision = last_revision

    feedback.save()
        


def _revision2json(revision):
    json = {
        'improvement': revision.improvement,
        'date_created': revision.date_created
    }
    if revision.work_url:
        json['work_url'] = revision.work_url
    return json


def _feedback2json(feedback):
    json = {
        'expert_uri': feedback.expert_uri,
        'good': feedback.good,
        'bad': feedback.bad,
        'ugly': feedback.ugly,
        'date_created': feedback.date_created
    }
    return json


def get_project_feedback(project_uri):
    feedback_revision = []

    project=Project.objects.get(id=uri2id(project_uri))

    for feedback in Feedback.objects.filter(project=project).order_by('date_created'):
        feedback_revision += [_feedback2json(feedback)]

    for revision in Revision.objects.filter(project=project).order_by('date_created'):
        feedback_revision += [_revision2json(revision)]

    keyfunc = lambda obj: obj['date_created']
    feedback_revision.sort(key=keyfunc)

    return feedback_revision
