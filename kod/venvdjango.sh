#!/bin/bash
virtualenv --python=python3.5  py_django

source py_django/bin/activate
pip install --upgrade pip

pip install -r requirements.txt
deactivate
