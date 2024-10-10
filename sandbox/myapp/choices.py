from django.db import models
from django.utils.translation import gettext_lazy as _

from django_js_choices.core import register_choice

YEAR_IN_SCHOOL_CHOICES = [
    ("FR", _("Freshman")),
    ("SO", _("Sophomore")),
    ("JR", _("Junior")),
    ("SR", _("Senior")),
    ("GR", _("Graduate")),
]

MEDIA_CHOICES = [
    (
        "Audio",
        (
            ("vinyl", _("Vinyl")),
            ("cd", _("CD")),
        ),
    ),
    (
        "Video",
        (
            ("vhs", _("VHS Tape")),
            ("dvd", _("DVD")),
        ),
    ),
    ("unknown", _("Unknown")),
]

MEDAL_TYPES = [
    ("Gold", _("Gold")),
    ("Silver", _("Silver")),
    ("Bronze", _("Bronze")),
]

YES_NO_ANSWER = [
    (None, _("(Unknown)")),
    (0, _("No")),
    (1, _("Yes")),
]

FRUITS_CUSTOM_CHOICES = [
    ("banana", _("Banana")),
    ("apple", _("Apple")),
    ("orange", _("Orange")),
]

register_choice("fruits", FRUITS_CUSTOM_CHOICES)

YEAR_IN_SCHOOL_CHOICES_2 = {
    "FR": _("Freshman"),
    "SO": _("Sophomore"),
    "JR": _("Junior"),
    "SR": _("Senior"),
    "GR": _("Graduate"),
}

MEDIA_CHOICES_2 = {
    "Audio": {
        "vinyl": _("Vinyl"),
        "cd": _("CD"),
    },
    "Video": {
        "vhs": _("VHS Tape"),
        "dvd": _("DVD"),
    },
    "unknown": _("Unknown"),
}


class MedalTypes2(models.TextChoices):
    GOLD = "Gold"
    SILVER = "Silver"
    BRONZE = "Bronze"


class YesNoAnswer2(models.IntegerChoices):
    NO = 0, _("No")
    YES = 1, _("Yes")
    __empty__ = _("(Unknown)")
