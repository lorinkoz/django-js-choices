from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from ...core import generate_js


class Command(BaseCommand):
    help = "Creates a static choices.js file for django-js-choices"

    def add_arguments(self, parser):
        parser.add_argument(
            "-l",
            "--locale",
            action="store",
            dest="locale",
            default=settings.LANGUAGE_CODE,
            help="Locale to generate choices file",
        )

    def handle(self, *args, **options):
        locale = options["locale"]
        content = generate_js(locale)
        file_name = staticfiles_storage.path(f"choices-{locale}.js")
        if staticfiles_storage.exists(file_name):
            staticfiles_storage.delete(file_name)
        staticfiles_storage.save(file_name, ContentFile(content))
        self.stdout.write(f"{file_name} saved to static root!")
