from django.db import models


class Trend(models.Model):
    uid = models.TextField(blank=False)
    econ_count = models.IntegerField(default=0)
    health_count = models.IntegerField(default=0)
    politics_count = models.IntegerField(default=0)
