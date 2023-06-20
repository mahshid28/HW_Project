from django.db import models
from django.utils.translation import gettext as _

class BaseModel(models.Model):
    class Meta:
        abstract = True

class TimeStampMixin:
    created_at = models.DateTimeField(_("Created time"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated time"), auto_now=True)
