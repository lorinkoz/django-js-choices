from django.utils.translation import gettext_lazy as _

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
