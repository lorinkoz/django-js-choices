import json

from django.apps import apps
from django.conf import settings
from django.template import loader
from django.utils.encoding import force_text
from django.utils.translation import activate, deactivate

from . import js_choices_settings as default_settings


def prepare_choices(choices):
    new_choices = []
    for choice in choices:
        if len(choice) != 2:
            continue
        try:
            json.dumps(choice[0])
            new_choices.append((choice[0], force_text(choice[1])))
        except TypeError:
            new_choices.append((force_text(choice[0]), force_text(choice[1])))
    return new_choices


class ExternalChoices:
    def __init__(self):
        self.choices = []

    def __iter__(self):
        return iter(self.choices)


external_choices = ExternalChoices()


def register_choice(name, choices):
    external_choices.choices.append((name, choices))


def generate_choices(locale=None):
    raw_choices = []
    named_choices = {}
    conflicting_names = set()

    if locale:
        activate(locale)

    def handle_save_choice(choices_names, choices):
        value = prepare_choices(choices)
        try:
            index = raw_choices.index(value)
        except ValueError:
            index = len(raw_choices)
            raw_choices.append(value)
        for name in choices_names:
            if name not in named_choices:
                named_choices[name] = index
            elif raw_choices[named_choices[name]] != value:
                conflicting_names.add(name)

    for choice_name, choices in external_choices:
        handle_save_choice([choice_name], choices)

    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            for field in model._meta.get_fields():
                try:
                    choices = list(getattr(field, "flatchoices", []))
                    assert len(choices)
                except Exception:
                    continue
                short_name = field.name
                medium_name = "{}_{}".format(model._meta.model_name.lower(), field.name)
                full_name = "{}_{}".format(model._meta.label_lower.replace(".", "_"), field.name)
                handle_save_choice([short_name, medium_name, full_name], choices)
    for name in conflicting_names:
        del named_choices[name]
    if locale:
        deactivate()
    return raw_choices, named_choices


def generate_js(locale=None):
    raw_choices, named_choices = generate_choices(locale)

    js_var_name = getattr(settings, "JS_CHOICES_JS_VAR_NAME", default_settings.JS_VAR_NAME)
    js_global_object_name = getattr(
        settings, "JS_CHOICES_JS_GLOBAL_OBJECT_NAME", default_settings.JS_GLOBAL_OBJECT_NAME
    )
    minify = getattr(settings, "JS_CHOICES_JS_MINIFY", default_settings.JS_MINIFY)

    js_content = loader.render_to_string(
        "django_js_choices/choices_js.tpl",
        {
            "raw_choices_list": [json.dumps(x) for x in raw_choices],
            "named_choices": json.dumps(named_choices),
            "js_var_name": js_var_name,
            "js_global_object_name": js_global_object_name,
        },
    )

    if minify:
        try:
            from rjsmin import jsmin

            js_content = jsmin(js_content)
        except ImportError:
            pass

    return js_content
