#!/bin/bash
set -e

show_help() {
  echo """
  Commands
  -----------------------------------------
  start_dev      : start the django dev server
  test           : run unit tests
  fix            : fix linting errors
  test_coverage  : report test coverage
  manage         : run django commands
  """
}

export PYTHONPATH="/code/:$PYTHONPATH"

case "$1" in
  "start_dev" )
    # run migrations first if theres any && start the dev server
    python ./mss_mall/manage.py migrate --noinput
    python ./mss_mall/manage.py runserver 0.0.0.0:8000
  ;;
  "test" )
    # linting first
    flake8 ./
    # run python tests and pass on any args e.g individual tests
    python ./mss_mall/manage.py test "${@:2}"
  ;;
  "fix" )
    # fix all linting errors automagically
    autopep8 --in-place -a -a -r ./
  ;;
  "test_coverage" )
    # generate test coverage
    coverage run --source='.' python ./mss_mall/manage.py test
    coverage report
  ;;
  "manage" )
    # run django commands
    python ./mss_mall/manage.py "${@:2}"
  ;;
  * )
    show_help
  ;;
esac
