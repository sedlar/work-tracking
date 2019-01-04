build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

test:
	docker-compose run --rm work-tracking pytest tests -v

test-coverage:
	docker-compose run --rm work-tracking pytest tests -v --cov=wt --cov-report term-missing

pylint:
	docker-compose run --rm work-tracking pylint /app/wt
