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
    ("GOLD", _("Gold")),
    ("SILVER", _("Silver")),
    ("BRONZE", _("Bronze")),
]

FRUITS_CUSTOM_CHOICES = [
    ("banana", _("Banana")),
    ("apple", _("Apple")),
    ("orange", _("Orange")),
]

register_choice("fruits", FRUITS_CUSTOM_CHOICES)
