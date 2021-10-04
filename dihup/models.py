from django.db import models


class BaseModel(models.Model):
    updated = models.DateField(blank=True, null=True)
    # version = models.PositiveIntegerField()
    created = models.CharField(max_length=64)
    modified = models.CharField(max_length=64)

    class Meta:
        abstract = True
