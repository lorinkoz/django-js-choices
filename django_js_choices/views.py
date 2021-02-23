from django.http import JsonResponse

from .core import generate_js


def choices_js(request):
    locale = request.GET.get("lang", None) or request.GET.get("locale", None)
    js_content = generate_js(locale)
    return JsonResponse(js_content)
