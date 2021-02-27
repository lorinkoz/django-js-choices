from django.urls import path
from myapp.views import inline_choices

from django_js_choices.views import choices_js

urlpatterns = [
    path("choices.js", choices_js, name="js-choices"),
    path("inline/", inline_choices, name="inline-choices"),
]
