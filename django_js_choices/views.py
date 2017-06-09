# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django_js_choices.core import generate_js
from django.http import HttpResponse


def choices_js(request):
    locale = request.GET.get('lang', None) or request.GET.get('locale', None)
    response_body = generate_js(locale)
    return HttpResponse(response_body, **{'content_type': 'application/javascript'})
