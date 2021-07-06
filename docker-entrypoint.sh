#!/bin/bash
set -e

PORT=${2:-8000}

case "$1" in
    api)
        exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
        ;;
    start)
        uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload
        ;;
    tests)
        isort -c --diff --settings-file .isort.cfg .
        black --config pyproject.toml --check .
        pylint --rcfile=.pylintrc --errors-only app
        mypy .
        MONGO_DB_NAME='test' pytest -s -vv tests/
        ;;
    pytest)
        MONGO_DB_NAME='test' pytest -s -vv -x tests/
        ;;
    *)
        exec "$@"
        ;;
esac
