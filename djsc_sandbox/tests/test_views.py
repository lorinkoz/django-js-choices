from django.test.testcases import TestCase


class ChoicesJSTestCase(TestCase):
    """
    Test choices_js view.
    """

    def test_view(self):
        response = self.client.get("/choices.js")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Freshman")
        self.assertContains(response, "Vinyl")
        self.assertContains(response, "Unknown")
        self.assertContains(response, "Gold")

    def test_view_with_parameter_lang(self):
        response = self.client.get("/choices.js?lang=es")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Estudiante de primer a\\u00f1o")
        self.assertContains(response, "Vinil")
        self.assertContains(response, "Desconocido")
        self.assertContains(response, "Oro")

    def test_view_with_parameter_locale(self):
        response = self.client.get("/choices.js?locale=es")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Estudiante de primer a\\u00f1o")
        self.assertContains(response, "Vinil")
        self.assertContains(response, "Desconocido")
        self.assertContains(response, "Oro")
