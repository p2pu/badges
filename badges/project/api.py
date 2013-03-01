from project.models import Project
from datetime import datetime


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
        raise Exception('A user can only submit 1 project for a badge')

    project_db = Project(
        title=title,
        image_uri=image_uri,
        work_url=work_url,
        steps=steps,
        reflection=reflection,
        tags=','.join(tags),
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


def revise_project(project_uri, improvements, work_url=None):
    pass


def submit_feedback(project_uri, expert_uri, red, green, blue):
    pass



