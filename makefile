# Variables
-include .env
PYTHONPATH = $(shell pwd)

run:
	@uvicorn "backend.app:app" --port 5000 --reload

deploy: upgrade
	@poetry run gunicorn "backend.app:app" -c "./backend/gunicorn.py"

test:
	@ENVIRONMENT=test pytest tests

docker:
	@docker rm -f backend || true
	@docker build -t backend .
	@docker run --expose 80 --env-file .env.docker --name=backend --network=global-default -p 8000:80 -d backend make deploy

format:
	@poetry run black backend tests migration
	@poetry run isort backend tests migration
	@poetry run autoflake8 --remove-unused-variables --recursive --exclude=__init__.py --in-place backend tests migration
	@poetry run flake8 backend tests migration

revision:
	@PYTHONPATH="${PYTHONPATH}" poetry run alembic revision --autogenerate

upgrade:
	@PYTHONPATH="${PYTHONPATH}" poetry run alembic upgrade head

downgrade:
	@PYTHONPATH="${PYTHONPATH}" poetry run alembic downgrade head

clean-pyc:
	@find . -name "__pycache__" -exec rm -rf {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
