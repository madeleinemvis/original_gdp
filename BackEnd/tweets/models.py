from django.db import models

class Tweet(models.Model):
    created_at = models.TextField(blank=False, default='')
    text = models.TextField(blank=True, default='')
    favorite_count = models.TextField(blank=False, default='')
    user_location = models.TextField(blank=True, default='')
