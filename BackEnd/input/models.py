from django.db import models
import JSONField
# Create your models here.

class Input(models.Model):
    uid = models.UUIDField()
    links = JSONField()
    