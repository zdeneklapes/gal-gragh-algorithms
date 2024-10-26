# Makefile for Docker Nginx PHP Composer MySQL

help: ## Show this help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {sub("\\\\n",sprintf("\n%22c"," "), $$2);printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build the project.
	docker compose build

run: ## Go into the app shell.
	docker compose -f docker-compose.yml -f docker-compose.yml run --remove-orphans app fish

restart: down up ## Restart the project (Remove all containers and start again).
