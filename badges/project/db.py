from django.db import models


def UriField(**kwargs):
    return models.CharField(max_length=255, **kwargs)


class Project(models.Model):
    title = models.CharField(max_length=255)
    image_uri = UriField()
    work_url = models.URLField()
    description = models.CharField(max_length=1024)
    reflection = models.CharField(max_length=1024)
    tags = models.CharField(max_length=255)
    badge_uri = UriField()
    author_uri = UriField()
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    date_deleted = models.DateTimeField(null=True, blank=True)


class Revision(models.Model):
    project = models.ForeignKey(Project)
    improvement = models.CharField(max_length=1024)
    work_url = models.URLField(null=True, blank=True)
    date_created = models.DateTimeField()


class Feedback(models.Model):
    project = models.ForeignKey(Project)
    revision = models.ForeignKey(Revision, null=True, blank=True)
    expert_uri = UriField()
    good = models.CharField(max_length=1024)
    bad = models.CharField(max_length=1024)
    ugly = models.CharField(max_length=1024)
    date_created = models.DateTimeField()
    badge_awarded = models.BooleanField(default=False)
