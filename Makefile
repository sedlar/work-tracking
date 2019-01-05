MESSAGE=""
REMOTE_DEBUGGER=""

build:
	docker-compose build

up:
	REMOTE_DEBUGGER=$(REMOTE_DEBUGGER) docker-compose up

down:
	docker-compose down

test:
	docker-compose run --rm work-tracking pytest tests -v

test-coverage:
	docker-compose run --rm work-tracking pytest tests -v --cov=wt --cov-report term-missing

pylint:
	docker-compose run --rm work-tracking pylint /app/wt

migration:
	docker-compose run --rm -w '/app' work-tracking alembic revision --autogenerate -m $(MESSAGE)

migrate:
	docker-compose run --rm -w '/app' work-tracking alembic upgrade head
