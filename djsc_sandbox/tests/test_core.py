from datetime import date

from django.test import override_settings
from django.test.testcases import SimpleTestCase
from django.utils.translation import gettext_lazy as _, override
from dukpy import evaljs

from django_js_choices.core import generate_choices, generate_js, prepare_choices, register_choice
from djsc_sandbox.myapp.choices import MEDAL_TYPES, MEDIA_CHOICES, YEAR_IN_SCHOOL_CHOICES


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

    def test_external_choices(self):
        new_medals_choices = [(1, "1"), (2, "2")]
        register_choice("medals", new_medals_choices)
        raw_choices, named_choices = generate_choices()
        self.assertIn("fruits", named_choices)
        # "medals" has a name clash, but it should be present because manually registered names should not change
        self.assertIn("medals", named_choices)
        medals_index = named_choices["medals"]
        self.assertEqual(raw_choices[medals_index], new_medals_choices)

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

    def get_display(self, json_content, field, key):
        return evaljs(f"{json_content} Choices.display('{field}', '{key}')")

    def get_pairs(self, json_content, field):
        return evaljs(f"{json_content} Choices.pairs('{field}')")

    @override_settings(JS_CHOICES_JS_MINIFY=True)
    def test_display_with_jsmin(self):
        json_content = generate_js()
        self.assertTrue(evaljs(f"{json_content} Choices.display !== undefined"))
        self.assertEqual(self.get_display(json_content, "modela_year_in_school", "FR"), "Freshman")
        self.assertEqual(self.get_display(json_content, "modela_year_in_school", "SO"), "Sophomore")
        self.assertEqual(self.get_display(json_content, "modela_year_in_school", "JR"), "Junior")
        self.assertEqual(self.get_display(json_content, "modela_year_in_school", "SR"), "Senior")
        self.assertEqual(self.get_display(json_content, "modela_year_in_school", "GR"), "Graduate")
        self.assertEqual(self.get_display(json_content, "modelb_year_in_school", "GR"), None)
        self.assertEqual(self.get_display(json_content, "modelb_media", "vinyl"), "Vinyl")
        self.assertEqual(self.get_display(json_content, "modelb_media", "cd"), "CD")
        self.assertEqual(self.get_display(json_content, "modelb_media", "vhs"), "VHS Tape")
        self.assertEqual(self.get_display(json_content, "modelb_media", "dvd"), "DVD")
        self.assertEqual(self.get_display(json_content, "modelb_media", "unknown"), "Unknown")
        self.assertEqual(self.get_display(json_content, "modelc_medals", "GOLD"), "Gold")
        self.assertEqual(self.get_display(json_content, "modelc_medals", "SILVER"), "Silver")
        self.assertEqual(self.get_display(json_content, "modelc_medals", "BRONZE"), "Bronze")

    @override_settings(JS_CHOICES_JS_MINIFY=False)
    def test_display_without_jsmin(self):
        json_content = generate_js()
        self.assertTrue(evaljs(f"{json_content} Choices.display !== undefined"))
        self.assertEqual(self.get_display(json_content, "modela_year_in_school", "FR"), "Freshman")
        self.assertEqual(self.get_display(json_content, "modela_year_in_school", "SO"), "Sophomore")
        self.assertEqual(self.get_display(json_content, "modela_year_in_school", "JR"), "Junior")
        self.assertEqual(self.get_display(json_content, "modela_year_in_school", "SR"), "Senior")
        self.assertEqual(self.get_display(json_content, "modela_year_in_school", "GR"), "Graduate")
        self.assertEqual(self.get_display(json_content, "modelb_year_in_school", "GR"), None)
        self.assertEqual(self.get_display(json_content, "modelb_media", "vinyl"), "Vinyl")
        self.assertEqual(self.get_display(json_content, "modelb_media", "cd"), "CD")
        self.assertEqual(self.get_display(json_content, "modelb_media", "vhs"), "VHS Tape")
        self.assertEqual(self.get_display(json_content, "modelb_media", "dvd"), "DVD")
        self.assertEqual(self.get_display(json_content, "modelb_media", "unknown"), "Unknown")
        self.assertEqual(self.get_display(json_content, "modelc_medals", "GOLD"), "Gold")
        self.assertEqual(self.get_display(json_content, "modelc_medals", "SILVER"), "Silver")
        self.assertEqual(self.get_display(json_content, "modelc_medals", "BRONZE"), "Bronze")

    def test_display_with_locale(self):
        json_content = generate_js("es")
        self.assertTrue(evaljs(f"{json_content} Choices.display !== undefined"))
        self.assertEqual(self.get_display(json_content, "modela_year_in_school", "FR"), "Estudiante de primer año")
        self.assertEqual(self.get_display(json_content, "modela_year_in_school", "SO"), "Estudiante de segundo año")
        self.assertEqual(self.get_display(json_content, "modela_year_in_school", "JR"), "Estudiante de tercer año")
        self.assertEqual(self.get_display(json_content, "modela_year_in_school", "SR"), "Estudiante de último año")
        self.assertEqual(self.get_display(json_content, "modela_year_in_school", "GR"), "Graduado")
        self.assertEqual(self.get_display(json_content, "modelb_year_in_school", "GR"), None)
        self.assertEqual(self.get_display(json_content, "modelb_media", "vinyl"), "Vinil")
        self.assertEqual(self.get_display(json_content, "modelb_media", "cd"), "CD")
        self.assertEqual(self.get_display(json_content, "modelb_media", "vhs"), "Cinta VHS")
        self.assertEqual(self.get_display(json_content, "modelb_media", "dvd"), "DVD")
        self.assertEqual(self.get_display(json_content, "modelb_media", "unknown"), "Desconocido")
        self.assertEqual(self.get_display(json_content, "modelc_medals", "GOLD"), "Oro")
        self.assertEqual(self.get_display(json_content, "modelc_medals", "SILVER"), "Plata")
        self.assertEqual(self.get_display(json_content, "modelc_medals", "BRONZE"), "Bronce")

    @override_settings(JS_CHOICES_JS_MINIFY=True)
    def test_pairs_with_jsmin(self):
        json_content = generate_js()
        self.assertTrue(evaljs(f"{json_content} Choices.pairs !== undefined"))
        years_in_school = [{"value": value, "label": str(label)} for value, label in YEAR_IN_SCHOOL_CHOICES]
        media_choices = [
            {"value": value, "label": str(label)}
            for value, label in MEDIA_CHOICES[0][1] + MEDIA_CHOICES[1][1] + (MEDIA_CHOICES[2],)
        ]
        medal_types = [{"value": value, "label": str(label)} for value, label in MEDAL_TYPES]
        self.assertEqual(self.get_pairs(json_content, "modela_year_in_school"), years_in_school)
        self.assertEqual(self.get_pairs(json_content, "modelb_year_in_school"), years_in_school[:-1])
        self.assertEqual(self.get_pairs(json_content, "modelb_media"), media_choices)
        self.assertEqual(self.get_pairs(json_content, "modelc_medals"), medal_types)

    @override_settings(JS_CHOICES_JS_MINIFY=False)
    def test_pairs_without_jsmin(self):
        json_content = generate_js()
        self.assertTrue(evaljs(f"{json_content} Choices.pairs !== undefined"))
        years_in_school = [{"value": value, "label": str(label)} for value, label in YEAR_IN_SCHOOL_CHOICES]
        media_choices = [
            {"value": value, "label": str(label)}
            for value, label in MEDIA_CHOICES[0][1] + MEDIA_CHOICES[1][1] + (MEDIA_CHOICES[2],)
        ]
        medal_types = [{"value": value, "label": str(label)} for value, label in MEDAL_TYPES]
        self.assertEqual(self.get_pairs(json_content, "modela_year_in_school"), years_in_school)
        self.assertEqual(self.get_pairs(json_content, "modelb_year_in_school"), years_in_school[:-1])
        self.assertEqual(self.get_pairs(json_content, "modelb_media"), media_choices)
        self.assertEqual(self.get_pairs(json_content, "modelc_medals"), medal_types)

    def test_pairs_with_locale(self):
        json_content = generate_js("es")
        with override("es"):
            self.assertTrue(evaljs(f"{json_content} Choices.pairs !== undefined"))
            years_in_school = [{"value": value, "label": str(label)} for value, label in YEAR_IN_SCHOOL_CHOICES]
            media_choices = [
                {"value": value, "label": str(label)}
                for value, label in MEDIA_CHOICES[0][1] + MEDIA_CHOICES[1][1] + (MEDIA_CHOICES[2],)
            ]
            medal_types = [{"value": value, "label": str(label)} for value, label in MEDAL_TYPES]
        self.assertEqual(self.get_pairs(json_content, "modela_year_in_school"), years_in_school)
        self.assertEqual(self.get_pairs(json_content, "modelb_year_in_school"), years_in_school[:-1])
        self.assertEqual(self.get_pairs(json_content, "modelb_media"), media_choices)
        self.assertEqual(self.get_pairs(json_content, "modelc_medals"), medal_types)
