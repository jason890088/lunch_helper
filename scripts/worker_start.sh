#!/bin/bash

set -o errexit
set -o nounset

celery -A lunch_helper worker -l INFO