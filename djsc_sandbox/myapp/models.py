from django.db import models
from multiselectfield.db import fields as multiselect

from .choices import MEDAL_TYPES, MEDIA_CHOICES, YEAR_IN_SCHOOL_CHOICES


class ModelA(models.Model):

    year_in_school = models.CharField(max_length=2, blank=True, choices=YEAR_IN_SCHOOL_CHOICES)


class ModelB(models.Model):

    year_in_school = models.CharField(max_length=2, blank=True, choices=YEAR_IN_SCHOOL_CHOICES[:-1])
    media = models.CharField(max_length=10, blank=True, choices=MEDIA_CHOICES)


class ModelC(models.Model):

    medals = multiselect.MultiSelectField(blank=True, choices=MEDAL_TYPES)
    media = models.CharField(max_length=10, blank=True, choices=MEDIA_CHOICES)
