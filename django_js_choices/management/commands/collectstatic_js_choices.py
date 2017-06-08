# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.management.base import BaseCommand

from ... import js_choices_settings as default_settings
from ...core import generate_js


class Command(BaseCommand):
    help = 'Creates a static choices.js file for django-js-choices'

    def add_arguments(self, parser):
        parser.add_argument('-l', '--locale',
            action='store',
            dest='locale',
            default=settings.LANGUAGE_CODE,
            help='Pass custom locale to generate choices file',
        )

    def get_location(self):
        output_path = getattr(settings, 'JS_CHOICES_OUTPUT_PATH', default_settings.JS_OUTPUT_PATH)
        if output_path:
            return output_path
        if not hasattr(settings, 'STATIC_ROOT') or not settings.STATIC_ROOT:
            raise ImproperlyConfigured('The collectstatic_js_choices command needs settings.JS_CHOICES_OUTPUT_PATH '
                                       'or settings.STATIC_ROOT to be set.')
        return os.path.join(settings.STATIC_ROOT, 'django_js_choices', 'js')

    def handle(self, *args, **options):
        locale = options['locale']
        location = self.get_location()
        file = 'choices-{}.js'.format(locale)
        fs = FileSystemStorage(location=location)
        if fs.exists(file):
            fs.delete(file)
        content = generate_js(locale)
        fs.save(file, ContentFile(content))
        if len(sys.argv) > 1 and sys.argv[1] in ['collectstatic_js_choices']:
            self.stdout.write('{0} file written to {1}'.format(file, location))
