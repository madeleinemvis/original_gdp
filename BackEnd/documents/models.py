from djongo import models
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
    sentiment = models.TextField(blank=True, default='')
    stance = models.TextField(blank=True, default='')

class Claim(models.Model):
    uid = models.TextField(blank=False, default='')
    claim = models.TextField(blank=False, default='')
