from django.db import models

def UriField(**kwargs):
    return models.CharField(max_length=255, **kwargs)

class Badge(models.Model):
    title = models.CharField(max_length=128)
    image_uri = UriField()
    description = models.CharField(max_length=128)
    requirements = models.CharField(max_length=1024)
    author_uri = UriField()
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    date_published = models.DateTimeField(blank=True, null=True)
