from django.db import models


class Document(models.Model):
    url = models.TextField(blank=False, default='')
    raw_HTML = models.TextField(blank=True, default='')
    text_body = models.TextField(blank=True, default='')
    cleaned_tokens = models.TextField(blank=True, default='')


class Tweet(models.Model):
    created_at = models.TextField(blank=False, default='')
    text = models.TextField(blank=True, default='')
    favorite_count = models.TextField(blank=False, default='')
    user_location = models.TextField(blank=True, default='')
