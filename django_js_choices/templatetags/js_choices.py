# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.utils.safestring import mark_safe

from ..core import generate_js


register = template.Library()

@register.simple_tag(takes_context=True)
def js_choices_inline(context):
    """
    Outputs a string of javascript that can access model field choices.
    """
    locale = None
    if 'request' in context:
        request = context['request']
        locale = locale = request.GET.get('lang', None) or request.GET.get('locale', None)
    return mark_safe(generate_js(locale))
