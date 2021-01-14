from django.db import models


# Definition of a Tweet object
class Tweet(models.Model):
    uid = models.TextField(blank=False)
    screen_name = models.TextField(blank=False, default='')
    created_at = models.DateTimeField()
    text = models.TextField(blank=True, default='')
    favorite_count = models.IntegerField(default=0)
    retweet_count = models.IntegerField(default=0)
    user_location = models.TextField(blank=True, default='')
    sentiment = models.TextField(blank=True, default='')


# Definition of a Query object
class Query(models.Model):
    uid = models.TextField(blank=False, default='')
    query = models.TextField(blank=False, default='')
