#!/bin/bash
set -e

run() {
  exec ./run.sh
}

case $1 in
  run)
    shift
    run
    ;;
  *)
    exec "$@"
    ;;
esac
