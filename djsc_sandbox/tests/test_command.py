from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import override_settings
from django.test.testcases import SimpleTestCase
from inmemorystorage import InMemoryStorage

from django_js_choices.core import generate_js


class MockedMemoryStorage(InMemoryStorage):
    def path(self, name):
        return name


storage = MockedMemoryStorage()


class CollectstaticJSTestCase(SimpleTestCase):
    """
    Tests collectstatic_js_choices management command.
    """

    @override_settings(STATICFILES_STORAGE="inmemorystorage.InMemoryStorage", INMEMORYSTORAGE_PERSIST=True)
    @patch("django_js_choices.management.commands.collectstatic_js_choices.staticfiles_storage", storage)
    def test_command_without_locale(self):
        with StringIO() as stdout:
            call_command("collectstatic_js_choices", stdout=stdout)
            self.assertEqual(stdout.getvalue().strip(), "choices-en-us.js saved to static root!")
        self.assertTrue(storage.exists("choices-en-us.js"))
        with storage.open("choices-en-us.js") as f:
            js_content = generate_js()
            self.assertEqual(f.read(), js_content)

    @override_settings(STATICFILES_STORAGE="inmemorystorage.InMemoryStorage", INMEMORYSTORAGE_PERSIST=True)
    @patch("django_js_choices.management.commands.collectstatic_js_choices.staticfiles_storage", storage)
    def test_command_with_locale(self):
        with StringIO() as stdout:
            call_command("collectstatic_js_choices", locale="es", stdout=stdout)
            self.assertEqual(stdout.getvalue().strip(), "choices-es.js saved to static root!")
        self.assertTrue(storage.exists("choices-es.js"))
        with storage.open("choices-es.js") as f:
            js_content = generate_js("es")
            self.assertEqual(f.read(), js_content)
