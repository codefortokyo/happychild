#!/bin/bash
set -e

run() {
  exec ./run.sh
}

run_develop() {
  exec /run_develop.sh
}

update_shinagawa() {
  exec python manage.py update_shinagawa_nursery_free_num

}

case $1 in
  run)
    shift
    run
    ;;
  run_develop)
    shift
    run_develop
    ;;
  update_shinagawa)
    shift
    update_shinagawa
    ;;
  *)
    exec "$@"
    ;;
esac
