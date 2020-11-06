from django.db import models

class Tweet(models.Model):
    created_at = models.TextField(blank=False, default='')
    text = models.TextField(blank=True, default='')
    favorite_count = models.TextField(blank=False, default=0)
    retweet_count = models.IntegerField(blank=False, default=0)
    user_location = models.TextField(blank=True, default='')
    sentiment = models.TextField(blank=True, default='')
