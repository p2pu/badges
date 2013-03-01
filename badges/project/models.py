from django.db import models


def UriField(**kwargs):
    return models.CharField(max_length=255, **kwargs)


class Project(models.Model):
    title = models.CharField(max_length=255)
    image_uri = UriField()
    work_url = models.URLField()
    steps = models.CharField(max_length=255)
    reflection = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)
    badge_uri = UriField()
    user_uri = UriField()
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    date_deleted = models.DateTimeField(null=True, blank=True)
