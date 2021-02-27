from django.urls import path

from django_js_choices.views import choices_js

urlpatterns = [
    path("choices.js", choices_js, name="js-choices"),
]
