# Makefile for django-js-choices

.PHONY: test
test:
	poetry run djsc_sandbox/manage.py test tests

.PHONY: coverage
coverage:
	poetry run coverage run djsc_sandbox/manage.py test tests

.PHONY: coverage-html
coverage-html:
	poetry run coverage run djsc_sandbox/manage.py test tests && poetry run coverage html

.PHONY: reqs
reqs:
	poetry export --without-hashes --dev --format requirements.txt > requirements.txt
