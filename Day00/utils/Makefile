# Define variables
COMPOSE_FILE := docker-compose.yml
CMD := docker compose -f $(COMPOSE_FILE)
POSTGRES_SERVICE := db


.PHONY: help up down stop clean prune all logs logdb logad re execd

all: up

help: ## Display available commands in this Makefile
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

logs: ## Show logs for all containers
	$(CMD) logs -f

logdb: ## Show logs for PostgreSQL container
	$(CMD) logs -f $(POSTGRES_SERVICE)

ps: ## Show running containers
	docker ps

execd: ## Exec bash in the PostgreSQL container
	$(CMD) exec -it $(POSTGRES_SERVICE) bash

up: ## Start containers defined in docker-compose.yml
	$(CMD) up -d --build

down: ## Stop and remove containers defined in docker-compose.yml
	$(CMD) down

stop: ## Stop containers defined in docker-compose.yml
	$(CMD) stop

re: stop up ## Restart the containers


clean: stop ## Stop and remove containers, networks, and volumes
	$(CMD) down -v --remove-orphans
	$(CMD) rm -f

prune: clean ## Remove all unused containers, networks, images, and volumes
	docker system prune -af
