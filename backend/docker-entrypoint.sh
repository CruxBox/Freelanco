#!/bin/bash

set -exo pipefail

run_migrations(){
    echo 'Running Migrations'
    python3 manage.py makemigrations
    python3 manage.py migrate
}

start_app(){
    echo 'Starting Django Server'
    python3 manage.py runserver 0.0.0.0:8000
}

run_dev () {
  echo "Running in Development environment"
  cd freelanco/
  run_migrations
  start_app
}

run_dev