from django.db import models

class User(models.Model):
    # id implicit
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True, null=True)
    image_url = models.CharField(max_length=255)
    date_joined = models.DateTimeField()
    date_updated = models.DateTimeField()

    def __unicode__(self):
        return '%s, %s' % (self.username, self.email)


class Partner(models.Model):
    # id implicit
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships
    users = models.ManyToManyField(User, blank=True, null=True)

    def __unicode__(self):
        return self.name
