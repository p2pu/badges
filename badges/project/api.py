
def _project2json(project_db):
    project = {
        'id': '1',
        'uri': '/uri/project/1',
        'title': 'Title',
        'image_uri': '/uri/image/1/',
        'work_url': 'http://example.com',
        'steps': 'Step 1 and then 2',
        'reflection': 'Ill do it different next time',
        'tags': ['tag1', 'tag2', 'tag3' ],
        'badge_uri': '/uri/badge/1/',
        'user_uri': '/uri/user/username/'
    }
    return project


def create_project(badge_uri, user_uri, title, image_uri, work_url, steps, reflection, tags):
    # TODO create project
    return get_project(None)


def get_project(uri):
    # TODO get project
    return _project2json(None)


def revise_project(project_uri, improvements, work_url=None):
    pass


def submit_feedback(project_uri, expert_uri, red, green, blue):
    pass



