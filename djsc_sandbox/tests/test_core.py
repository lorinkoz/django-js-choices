from datetime import date

from django.test import override_settings
from django.test.testcases import SimpleTestCase
from django.utils.translation import gettext_lazy as _

from django_js_choices.core import generate_choices, generate_js, prepare_choices


class PrepareChoicesTestCase(SimpleTestCase):
    """
    Test prepare_choices function.
    """

    def test_prepare(self):
        choices = prepare_choices(
            [
                ("x"),
                ("a", "a"),
                ("b", _("b")),
                (1, 1),
                (2, 2, 2),
                (date(2000, 1, 1), True),
            ]
        )
        self.assertEqual(
            choices,
            [
                ("a", "a"),
                ("b", "b"),
                (1, "1"),
                ("2000-01-01", "True"),
            ],
        )


class GenerateChoicesTestCase(SimpleTestCase):
    """
    Test generate_choices function.
    """

    def test_present_long_names_and_choice_count(self):
        raw_choices, named_choices = generate_choices()
        self.assertEqual(len(raw_choices[named_choices["myapp_modela_year_in_school"]]), 5)
        self.assertEqual(len(raw_choices[named_choices["myapp_modelb_year_in_school"]]), 4)
        self.assertEqual(len(raw_choices[named_choices["myapp_modelb_media"]]), 5)
        self.assertEqual(len(raw_choices[named_choices["myapp_modelc_medals"]]), 3)
        self.assertEqual(len(raw_choices[named_choices["myapp_modelc_media"]]), 5)

    def test_present_medium_names(self):
        raw_choices, named_choices = generate_choices()
        self.assertIn("modela_year_in_school", named_choices)
        self.assertIn("modelb_year_in_school", named_choices)
        self.assertIn("modelb_media", named_choices)
        self.assertIn("modelc_medals", named_choices)
        self.assertIn("modelc_media", named_choices)

    def test_present_short_names(self):
        raw_choices, named_choices = generate_choices()
        self.assertIn("media", named_choices)
        self.assertIn("medals", named_choices)
        self.assertIn("media", named_choices)  # Not excluded because it's the same on all models
        self.assertNotIn("year_in_school", named_choices)  # Excluded due to conflict between models

    def test_locale_translation(self):
        raw_choices, named_choices = generate_choices("es")
        self.assertEqual(
            [x[1] for x in raw_choices[named_choices["myapp_modela_year_in_school"]]],
            [
                "Estudiante de primer año",
                "Estudiante de segundo año",
                "Estudiante de tercer año",
                "Estudiante de último año",
                "Graduado",
            ],
        )
        self.assertEqual(
            [x[1] for x in raw_choices[named_choices["myapp_modelb_year_in_school"]]],
            [
                "Estudiante de primer año",
                "Estudiante de segundo año",
                "Estudiante de tercer año",
                "Estudiante de último año",
            ],
        )
        self.assertEqual(
            [x[1] for x in raw_choices[named_choices["myapp_modelb_media"]]],
            ["Vinil", "CD", "Cinta VHS", "DVD", "Desconocido"],
        )
        self.assertEqual(
            [x[1] for x in raw_choices[named_choices["myapp_modelc_medals"]]],
            ["Oro", "Plata", "Bronce"],
        )


class GenerateJSTestCase(SimpleTestCase):
    """
    Test generate_js function.
    """

    @override_settings(JS_CHOICES_JS_MINIFY=True)
    def test_generation_with_jsmin(self):
        json_content = generate_js()
        self.assertIn("Freshman", json_content)
        self.assertIn("Sophomore", json_content)
        self.assertIn("Junior", json_content)
        self.assertIn("Senior", json_content)
        self.assertIn("Graduate", json_content)
        self.assertIn("Vinyl", json_content)
        self.assertIn("CD", json_content)
        self.assertIn("VHS Tape", json_content)
        self.assertIn("DVD", json_content)
        self.assertIn("Unknown", json_content)
        self.assertIn("Gold", json_content)
        self.assertIn("Silver", json_content)
        self.assertIn("Bronze", json_content)

    @override_settings(JS_CHOICES_JS_MINIFY=False)
    def test_generation_without_jsmin(self):
        json_content = generate_js()
        self.assertIn("Freshman", json_content)
        self.assertIn("Sophomore", json_content)
        self.assertIn("Junior", json_content)
        self.assertIn("Senior", json_content)
        self.assertIn("Graduate", json_content)
        self.assertIn("Vinyl", json_content)
        self.assertIn("CD", json_content)
        self.assertIn("VHS Tape", json_content)
        self.assertIn("DVD", json_content)
        self.assertIn("Unknown", json_content)
        self.assertIn("Gold", json_content)
        self.assertIn("Silver", json_content)
        self.assertIn("Bronze", json_content)

    def test_generation_with_locale(self):
        json_content = generate_js("es")
        self.assertIn("Estudiante de primer a\\u00f1o", json_content)
        self.assertIn("Estudiante de segundo a\\u00f1o", json_content)
        self.assertIn("Estudiante de tercer a\\u00f1o", json_content)
        self.assertIn("Estudiante de \\u00faltimo a\\u00f1o", json_content)
        self.assertIn("Graduado", json_content)
        self.assertIn("Vinil", json_content)
        self.assertIn("CD", json_content)
        self.assertIn("Cinta VHS", json_content)
        self.assertIn("DVD", json_content)
        self.assertIn("Desconocido", json_content)
        self.assertIn("Oro", json_content)
        self.assertIn("Plata", json_content)
        self.assertIn("Bronce", json_content)
