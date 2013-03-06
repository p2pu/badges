from media import models as media_api

def fetch_resources( project ):
    project['image'] = media_api.get_image(project['image_uri'])
    # TODO fetch user details
    project['author'] = {
        'username': project['author_uri'].strip('/').split('/')[-1],
        'uri': project['author_uri']
    }
    return project
