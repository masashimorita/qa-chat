.PHONY: build install sh run down

up:
	docker compose -f docker-compose.yml up

down:
	docker compose -f docker-compose.yml down

build:
	docker compose -f docker-compose.yml build

bash:
	docker compose -f docker-compose.yml run --rm app bash

shell:
	docker compose -f docker-compose.yml run --rm app bash poetry shell
