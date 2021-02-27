from django.http import HttpResponse

from .core import generate_js


def choices_js(request):
    locale = request.GET.get("lang", None) or request.GET.get("locale", None)
    js_content = generate_js(locale)
    return HttpResponse(js_content, content_type="application/javascript")
