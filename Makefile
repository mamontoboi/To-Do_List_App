# Phony targets
.PHONY: build stop status purge


# Build and start the Docker container
build:
	docker-compose up -d  --build


# Stop the Docker containers
stop:
	docker-compose down


# View status of all running Docker containers
status:
	docker-compose ps


# Remove all unused Docker containers and images
purge:
	docker system prune -a