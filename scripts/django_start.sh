#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py migrate
gunicorn --bind 0.0.0.0:8000 lunch_helper.wsgi