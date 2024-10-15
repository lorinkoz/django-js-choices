django-js-choices
=================

.. image:: https://img.shields.io/badge/packaging-poetry-purple.svg
    :alt: Packaging: poetry
    :target: https://github.com/sdispater/poetry

.. image:: https://img.shields.io/badge/code%20style-black-black.svg
    :alt: Code style: black
    :target: https://github.com/ambv/black

.. image:: https://github.com/lorinkoz/django-js-choices/workflows/code/badge.svg
    :alt: Build status
    :target: https://github.com/lorinkoz/django-js-choices/actions

.. image:: https://coveralls.io/repos/github/lorinkoz/django-js-choices/badge.svg?branch=master
    :alt: Code coverage
    :target: https://coveralls.io/github/lorinkoz/django-js-choices?branch=master

.. image:: https://badge.fury.io/py/django-js-choices.svg
    :alt: PyPi version
    :target: http://badge.fury.io/py/django-js-choices

.. image:: https://pepy.tech/badge/django-js-choices/month
    :alt: Downloads
    :target: https://pepy.tech/project/django-js-choices

|

Overview
--------

Django JS Choices makes handling of `model field choices`_ in javascript easy.

.. _model field choices: https://docs.djangoproject.com/en/dev/ref/models/fields.html#django.db.models.Field.choices

For example, given the model...

.. code-block:: python

    # models.py:

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

.. code-block:: javascript

    Choices.pairs("year_in_school");

Result:

.. code-block:: javascript

    [
        {value: "FR", label: "Freshman"},
        {value: "SO", label: "Sophomore"},
        {value: "JR", label: "Junior"},
        {value: "SR", label: "Senior"}
    ]

Display values are also accesible.

.. code-block:: javascript

    Choices.display("year_in_school", "FR")
    Choices.display("year_in_school", {"year_in_school": "FR"})

In both cases the result is

.. code-block:: javascript

    "Freshman"


Installation
------------

Install using ``pip``...

.. code-block:: bash

    pip install django-js-choices

...or clone the project from GitHub.

.. code-block:: bash

    git clone https://github.com/lorinkoz/django-js-choices.git

Add ``'django_js_choices'`` to your ``INSTALLED_APPS`` setting.

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_js_choices',
    )


Usage as static file
--------------------

First generate static file by

.. code-block:: bash

    python manage.py collectstatic_js_choices

If you add apps, models, or change some existing choices,
you may update the choices.js file by running the command again.

The choices files is created with the locale prefix defined in your settings,
but you can pass any locale to the command...

.. code-block:: bash

    python manage.py collectstatic_js_choices --locale es

In this case, the generated file will be ``choices-es.js``.

After this add the file to your template.

.. code-block:: html

    <script src="{% static 'choices-es.js' %}"></script>


Usage with views
----------------

Include non-cached view...

.. code-block:: python

    from django_js_choices.views import choices_js

    urlpatterns = [
        path("jschoices/", choices_js, name="js_choices"),
    ]

...or use cache to save some bandwith.

.. code-block:: python

    from django_js_choices.views import choices_js

    urlpatterns = [
        path("jschoices/", cache_page(3600)(choices_js), name="js_choices"),
    ]

Include javascript in your template.

.. code-block:: html

    <script src="{% url 'js_choices' %}" type="text/javascript"></script>


Usage as template tag
---------------------

If you want to generate the javascript code inline, use the template tag.

.. code-block:: html

    {% load js_choices %}
    <script type="text/javascript" charset="utf-8">
        {% js_choices_inline %}
    </script>


Use the choices in javascript
-----------------------------

For every model field with choices, they will be available by the following
names.

.. code-block:: javascript

    Choices.pairs("<app_label>_<model_name>_<field_name>")
    Choices.pairs("<model_name>_<field_name>")
    Choices.pairs("<field_name>")

If any of these names conflict with other model fields,
the conflicting names won't be accessible to prevent ambiguity.


Register other choices not in models
------------------------------------

If you have some choices you want to expose to javascript, and they don't fit into any
model, lets say for example, a list of actions, you can add those too:

.. code-block:: python

    from django_js_choices.core import register_choice

    POSSIBLE_ACTIONS = (
        ("go_down", "Go down"),
        ("go_top", "Go top"),
        ("nothing", "Stay")
    )
    ...
    # register_choice(name: string, choices: list)
    register_choice("possible_actions", POSSIBLE_ACTIONS)

- If any of the names of a manually registered choice conflicts with some model fields, the one you manually
  registered will be the one you'll access.
- The 2nd argument is the same type that you'd pass to a CharField `choices` argument.

You can only access the ``POSSIBLE_ACTIONS`` choices through the name ``possible_actions``

PLEASE NOTE: You must ensure the file where you are registering your choice is been processed by django

.. code-block:: javascript

    Choices.pairs("possible_actions")


Options
-------

Optionally, you can overwrite the default javascript variable 'Choices' used
to access the choices by Django setting.

.. code-block:: python

    JS_CHOICES_JS_VAR_NAME = 'Choices'

Optionally, you can change the name of the global object the javascript
variable used to access the choices is attached to. Default is ``this``.

.. code-block:: python

    JS_CHOICES_JS_GLOBAL_OBJECT_NAME = 'window'

Optionally, you can disable the minfication of the generated javascript file
by Django setting.

.. code-block:: python

    JS_CHOICES_JS_MINIFY = False


Contributing
------------

- PRs are welcome!
- To run the test suite run ``make`` or ``make coverage``. The tests for this
  project live inside a small django project called ``sandbox``.


Credits
-------

Inspired by (and conceptually forked from)
`django-js-reverse <https://github.com/ierror/django-js-reverse>`_