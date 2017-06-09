=================
Django JS Choices
=================


**javascript model field's choices handling for Django.**


Overview
--------

Django JS Choices is a small Django app that makes handling of
`model field choices <https://docs.djangoproject.com/en/dev/ref/models/fields.html#django.db.models.Field.choices>`_
in javascript easy.

For example, given the model...

models.py:
::
    class Student(models.Model):
        FRESHMAN = 'FR'
        SOPHOMORE = 'SO'
        JUNIOR = 'JR'
        SENIOR = 'SR'
        YEAR_IN_SCHOOL_CHOICES = (
            (FRESHMAN, 'Freshman'),
            (SOPHOMORE, 'Sophomore'),
            (JUNIOR, 'Junior'),
            (SENIOR, 'Senior'),
        )
        year_in_school = models.CharField(
            max_length=2,
            choices=YEAR_IN_SCHOOL_CHOICES,
            default=FRESHMAN,
        )

...the choices are accesible in javascript.
::
    Choices.pairs("year_in_school");

Result:
::
    [
        {value: "FR", label: "Freshman"},
        {value: "SO", label: "Sophomore"},
        {value: "JR", label: "Junior"},
        {value: "SR", label: "Senior"}
    ]

Display values are also accesible.
::
    Choices.display("year_in_school", "FR")
    Choices.display("year_in_school", {"year_in_school": "FR"})

In both cases the result is
::
    "Freshman"


Requirements
------------

-  Python (2.6, 2.7, 3.1, 3.3, 3.4, 3.5)
-  Django (1.5 and above)


Installation
------------

Install using ``pip``...
::
    pip install django-js-choices

...or clone the project from GitHub.
::
    git clone https://github.com/lorinkoz/django-js-choices.git

Add ``'django_js_choices'`` to your ``INSTALLED_APPS`` setting.
::
    INSTALLED_APPS = (
        ...
        'django_js_choices',
    )


Usage as static file
--------------------

First generate static file by
::
    ./manage.py collectstatic_js_choices

If you add apps, models, or change some existing choices,
you may update the choices.js file by running the command again.

The choices files is always created with a locale prefix: ``choices-en-us.js``
but you can pass any locale to the command...
::
    ./manage.py collectstatic_js_choices --locale es

...and the generated file will be ``choices-es.js``

After this add the file to your template.
::
    <script src="{% static 'django_js_choices/js/choices-es.js' %}"></script>


Usage with views
----------------

Include non-cached view...
::
    from django_js_choices.views import choices_js
    urlpatterns = [
        url(r'^jschoices/$', choices_js, name='js_choices'),
    ]

...or use cache to save some bandwith.
::
    from django_js_choices.views import choices_js
    urlpatterns = [
        url(r'^jschoices/$', cache_page(3600)(choices_js), name='js_choices'),
    ]

Include javascript in your template.
::
    <script src="{% url 'js_choices' %}" type="text/javascript"></script>


Usage as template tag
---------------------

If you want to generate the javascript code inline, use the template tag.
::
    {% load js_choices %}
    <script type="text/javascript" charset="utf-8">
        {% js_choices_inline %}
    </script>


Use the choices in javascript
-----------------------------

For every model field with choices, they will be available by the following names.
::
    Choices.pairs("<app_label>_<model_name>_<field_name>")
    Choices.pairs("<model_name>_<field_name>")
    Choices.pairs("<field_name>")

If any of these names conflict with other model fields,
the conflicting names won't be accessible to prevent ambiguity.


Options
-------

Optionally, you can overwrite the default javascript variable 'Choices' used
to access the choices by Django setting.
::
    JS_CHOICES_JS_VAR_NAME = 'Choices'

Optionally, you can change the name of the global object the javascript variable
used to access the choices is attached to. Default is :code:`this`.
::
    JS_CHOICES_JS_GLOBAL_OBJECT_NAME = 'window'

Optionally, you can disable the minfication of the generated javascript file
by Django setting.
::
    JS_CHOICES_JS_MINIFY = False

By default collectstatic_js_choices writes its output (`choices-en-us.js`)
to your project's `STATIC_ROOT`, but you can change the output path.
::
    JS_CHOICES_OUTPUT_PATH = 'some/other/path'


Running the test suite
----------------------

NOT YET AVAILABLE


Credits
-------

Inspired by (and conceptually forked from)
`django-js-reverse <https://github.com/ierror/django-js-reverse>`


License
-------

`MIT <https://raw.github.com/lorinkoz/django-js-choices/develop/LICENSE>`_


Contact
-------

lorinkoz@gmail.com

`@lorinkoz <https://twitter.com/lorinkoz>`_
