#!/bin/bash
python3.5 -m venv py_django
source py_django/bin/activate
pip install --upgrade pip

pip install -r requirements.txt

#pip install django==2.0.4 xlrd ipython pylint mypy bs4
#pip install scrapy scrapy-splash scrapyd scrapy-djangoitem
#pip install social-auth-app-django
#pip install django-utils
deactivate
