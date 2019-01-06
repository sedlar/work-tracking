MESSAGE=""
REMOTE_DEBUGGER=""

build:
	docker-compose build

up:
	REMOTE_DEBUGGER=$(REMOTE_DEBUGGER) docker-compose up

down:
	docker-compose down

down-test:
	docker-compose -f docker-compose.test.yml down

test: build
	REMOTE_DEBUGGER=$(REMOTE_DEBUGGER) docker-compose -f docker-compose.test.yml run --rm work-tracking-test pytest tests -v

test-coverage: build
	REMOTE_DEBUGGER=$(REMOTE_DEBUGGER) docker-compose -f docker-compose.test.yml run --rm work-tracking-test pytest tests -v --cov=wt --cov-report term-missing

pylint: build
	docker-compose -f docker-compose.test.yml run --rm work-tracking-test pylint /app/wt

migration:
	docker-compose run --rm work-tracking alembic revision --autogenerate -m $(MESSAGE)

migrate:
	docker-compose run --rm work-tracking alembic upgrade head

default-user:
	docker-compose run --rm work-tracking python /app/wt/app.py add-user --username=username --password=password
