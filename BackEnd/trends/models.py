from django.db import models


class Trend(models.Model):
    uid = models.TextField(blank=False)
    econ_count = models.IntegerField(default=0)
    econ_estimate = models.FloatField(default=0.0)
    econ_random = models.FloatField(default=0.0)
    econ_unobserved = models.FloatField(default=0.0)
    econ_placebo = models.FloatField(default=0.0)
    econ_subset = models.FloatField(default=0.0)
    health_count = models.IntegerField(default=0)
    health_estimate = models.FloatField(default=0.0)
    health_random = models.FloatField(default=0.0)
    health_unobserved = models.FloatField(default=0.0)
    health_placebo = models.FloatField(default=0.0)
    health_subset = models.FloatField(default=0.0)
    politics_count = models.IntegerField(default=0)
    politics_estimate = models.FloatField(default=0.0)
    politics_random = models.FloatField(default=0.0)
    politics_unobserved = models.FloatField(default=0.0)
    politics_placebo = models.FloatField(default=0.0)
    politics_subset = models.FloatField(default=0.0)
