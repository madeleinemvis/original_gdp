from djongo import models
from django import forms
from django.contrib.postgres.fields import ArrayField
from jsonfield import JSONField


class Document(models.Model):
    uid = models.TextField(blank=False, default='')
    content_type = models.TextField(blank=False, default='')
    url = models.TextField(blank=False, default='')
    raw_html = models.TextField(blank=True, default='')
    title = models.TextField(blank=True, default='')
    text_body = models.TextField(blank=True, default='')
    cleaned_tokens = JSONField()
    html_links = JSONField()