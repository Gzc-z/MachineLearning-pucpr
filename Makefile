COMPOSE ?= docker compose
SCRIPT = ./script.sh

all: clean up logs

build: 
	@$(COMPOSE) build

up:
	@$(COMPOSE) up puc-ml -d

down:
	@$(COMPOSE) down puc-ml

restart:
	@$(COMPOSE) restart puc-ml

logs:
	@$(COMPOSE) logs -f --no-log-prefix

shell:
	@$(COMPOSE) up puc-ml -d
	@$(COMPOSE) exec puc-ml bash
	
clean:
	@$(COMPOSE) down -v --remove-orphans puc-ml


# workspace

r:
	@$(SCRIPT)
