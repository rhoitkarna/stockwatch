COMPOSE = docker-compose
EXEC_WEB = $(COMPOSE) exec web

# Command to build and start containers in background
up:
	$(COMPOSE) up -d --build

# Command to stop containers
stop:
	$(COMPOSE) stop

# Command to stop and remove containers/networks
down:
	$(COMPOSE) down

# Database Migrations
migrate:
	$(EXEC_WEB) python manage.py makemigrations
	$(EXEC_WEB) python manage.py migrate

# Create Superuser
superuser:
	$(EXEC_WEB) python manage.py createsuperuser


# View Logs (Follow)
logs:
	$(COMPOSE) logs -f

# Enter the container's shell (for debugging)
shell:
	$(EXEC_WEB) /bin/bash

# Clean up docker system (use with caution)
clean:
	docker system prune -f