## Async template on FastAPI and MongoDB with Motor

### Description
Production-ready dockerized async REST API on FastAPI with Motor and MongoDB

## Key Features
- tests on `pytest` with automatic cleanup after each test case
- separate requirements files for dev and production using `pip-tools`
- configs for `mypy`, `pylint`, `isort` and `black`

### After `git clone` run
```bash
make help
```

### Prepare virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install pip-tools
```
