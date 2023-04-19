from django.db import models
from multiselectfield.db.fields import MultiSelectField
from multiselectfield.utils import get_max_length

from .choices import MEDAL_TYPES, MEDIA_CHOICES, YEAR_IN_SCHOOL_CHOICES


class ModelA(models.Model):
    year_in_school = models.CharField(max_length=2, blank=True, choices=YEAR_IN_SCHOOL_CHOICES)


class ModelB(models.Model):
    year_in_school = models.CharField(max_length=2, blank=True, choices=YEAR_IN_SCHOOL_CHOICES[:-1])
    media = models.CharField(max_length=10, blank=True, choices=MEDIA_CHOICES)


class ModelC(models.Model):
    medals = MultiSelectField(blank=True, choices=MEDAL_TYPES, max_length=get_max_length(MEDAL_TYPES, None))
    media = models.CharField(max_length=10, blank=True, choices=MEDIA_CHOICES)
