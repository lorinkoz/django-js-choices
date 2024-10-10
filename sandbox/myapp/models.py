from django.db import models
from multiselectfield.db.fields import MultiSelectField

from . import choices


class ModelA(models.Model):
    year_in_school = models.CharField(max_length=2, blank=True, choices=choices.YEAR_IN_SCHOOL_CHOICES)
    year_in_school_2 = models.CharField(max_length=2, blank=True, choices=choices.YEAR_IN_SCHOOL_CHOICES_2)


class ModelB(models.Model):
    year_in_school = models.CharField(max_length=2, blank=True, choices=choices.YEAR_IN_SCHOOL_CHOICES[:-1])
    media = models.CharField(max_length=10, blank=True, choices=choices.MEDIA_CHOICES)
    media_2 = models.CharField(max_length=10, blank=True, choices=choices.MEDIA_CHOICES_2)


class ModelC(models.Model):
    medals = MultiSelectField(blank=True, choices=choices.MEDAL_TYPES)
    medals_2 = MultiSelectField(blank=True, choices=choices.MedalTypes2)
    media = models.CharField(max_length=10, blank=True, choices=choices.MEDIA_CHOICES)


class ModelD(models.Model):
    medals = models.CharField(max_length=6, choices=choices.MEDAL_TYPES)
    medals_2 = models.CharField(max_length=6, choices=choices.MedalTypes2)

    yes_no = models.CharField(max_length=3, blank=True, choices=choices.YES_NO_ANSWER)
    yes_no_2 = models.CharField(max_length=3, blank=True, choices=choices.YesNoAnswer2)
