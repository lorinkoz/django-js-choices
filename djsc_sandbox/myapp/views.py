from django.shortcuts import render


def inline_choices(request):
    return render(request, "inline_choices.html")
