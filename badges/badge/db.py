from django.db import models


def UriField(**kwargs):
    return models.CharField(max_length=255, **kwargs)


class Badge(models.Model):
    title = models.CharField(max_length=128, unique=True)
    image_uri = UriField()
    description = models.CharField(max_length=128)
    requirements = models.CharField(max_length=1024)
    featured = models.BooleanField(default=False)
    author_uri = UriField()
    partner_name = models.CharField(max_length=255, null=True, blank=True)
    deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    date_published = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.title


class Award(models.Model):
    OPEN_BADGES_STATE_CHOICES = (
        ('NOT_PUBLISHED', 'NOT_PUBLISHED'),
        ('PUBLISHED', 'PUBLISHED'),
        ('REVOKED', 'REVOKED'),
    )

    user_uri = UriField()
    expert_uri = UriField()
    evidence_url = models.CharField(max_length=255)
    date_awarded = models.DateTimeField()
    ob_state = models.CharField(max_length=20, choices=OPEN_BADGES_STATE_CHOICES, default='NOT_PUBLISHED')
    ob_date_published = models.DateTimeField(null=True, blank=True)
    ob_date_revoked = models.DateTimeField(null=True, blank=True)

    # relationships
    badge = models.ForeignKey(Badge)

    def __unicode__(self):
        return self.badge.title
