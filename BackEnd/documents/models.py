from django.db import models


class Document(models.Model):
    url = models.TextField(blank=False, default='')
    raw_HTML = models.TextField(blank=True, default='')
    text_body = models.TextField(blank=True, default='')
    cleaned_tokens = models.TextField(blank=True, default='')
