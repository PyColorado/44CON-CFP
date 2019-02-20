#!/bin/bash

set -eu
set -o pipefail

readonly PROJECT_ROOT="$(pwd)"
readonly BUILD_SRC="$PROJECT_ROOT/build"
readonly LESS_SRC="$PROJECT_ROOT/bower_components/flat-ui/less/flat-ui.less"
readonly CSS_DEST="$PROJECT_ROOT/bower_components/flat-ui/dist/css/flat-ui.min.css"

prepare_db() {
  python manage.py makemigrations gambit
  python manage.py migrate
}

prepare_assets() {
  bower install --save --production
  # Build minified CSS with inline source map
  lessc --source-map-less-inline --source-map-map-inline --clean-css "$LESS_SRC" "$CSS_DEST"
  python manage.py collectstatic --noinput --clear --verbosity 0
  python manage.py compress --force --verbosity 0
}

run_tests() {
  coverage run --source="$PROJECT_ROOT" manage.py test gambit
}

main() {
  cd "$PROJECT_ROOT"
  prepare_db
  prepare_assets
  run_tests
}

main
