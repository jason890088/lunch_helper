#!/bin/bash

set -o errexit
set -o nounset

rm -f './celerybeat.pid'
celery -A lunch_helper beat -l INFO