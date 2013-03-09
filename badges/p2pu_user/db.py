from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    date_joined = models.DateTimeField()
    date_updated = models.DateTimeField()
    #auth_token
    #refresh_token
