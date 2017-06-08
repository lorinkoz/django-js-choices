# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.apps import apps
from django.conf import settings
from django.template import loader
from django.utils.encoding import force_text
from django.utils.translation import activate, deactivate

from . import js_choices_settings as default_settings
from . import rjsmin


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


def generate_js(locale=None):
    raw_choices = []
    named_choices = {}
    used_names = []
    if locale:
        activate(locale)
    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            for field in model._meta.get_fields():
                choices = getattr(field, 'flatchoices', None)
                if choices:
                    full_name = '{}_{}'.format(
                        model._meta.label_lower.replace('.', '_'),
                        field.name
                    )
                    simple_name = '{}_{}'.format(model._meta.model_name.lower(), field.name)
                    name = field.name
                    value = json.dumps(prepare_choices(choices))
                    try:
                        index = raw_choices.index(value)
                    except ValueError:
                        index = len(raw_choices)
                        raw_choices.append(value)
                    finally:
                        named_choices[full_name] = index
                        if simple_name not in used_names:
                            named_choices[simple_name] = index
                            used_names.append(simple_name)
                        if name not in used_names:
                            named_choices[name] = index
                            used_names.append(name)
    if locale:
        deactivate()
    js_var_name = getattr(settings, 'JS_CHOICES_JS_VAR_NAME', default_settings.JS_VAR_NAME)
    js_global_object_name = getattr(settings, 'JS_CHOICES_JS_GLOBAL_OBJECT_NAME', default_settings.JS_GLOBAL_OBJECT_NAME)
    minfiy = getattr(settings, 'JS_CHOICES_JS_MINIFY', default_settings.JS_MINIFY)
    js_content = loader.render_to_string('django_js_choices/choices_js.tpl', {
        'raw_choices_list': raw_choices,
        'named_choices': json.dumps(named_choices),
        'js_var_name': js_var_name,
        'js_global_object_name': js_global_object_name,
    })
    if minfiy:
        js_content = rjsmin.jsmin(js_content)
    return js_content