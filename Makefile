.PHONY: help build start stop restart logs shell test clean setup

help:
	@echo "GEANT4 Simulation with MCP Server"
	@echo ""
	@echo "Available commands:"
	@echo "  make setup    - Run complete setup (build and start)"
	@echo "  make build    - Build Docker image"
	@echo "  make start    - Start containers"
	@echo "  make stop     - Stop containers"
	@echo "  make restart  - Restart containers"
	@echo "  make logs     - View container logs"
	@echo "  make shell    - Open shell in container"
	@echo "  make test     - Run tests"
	@echo "  make run      - Run simulation with default config"
	@echo "  make clean    - Stop and remove containers"
	@echo ""

setup:
	@./setup.sh

build:
	@echo "Building Docker image..."
	@docker-compose build

start:
	@echo "Starting containers..."
	@docker-compose up -d
	@echo "✓ Containers started"

stop:
	@echo "Stopping containers..."
	@docker-compose down
	@echo "✓ Containers stopped"

restart: stop start

logs:
	@docker-compose logs -f

shell:
	@docker exec -it geant4-simulation /bin/bash

test:
	@./test.sh

run:
	@echo "Running simulation with default configuration..."
	@docker exec geant4-simulation python3 simulation.py

clean:
	@echo "Cleaning up..."
	@docker-compose down -v
	@rm -rf output/*.json
	@echo "✓ Cleanup complete"

status:
	@echo "Container status:"
	@docker ps | grep geant4-simulation || echo "Container not running"
	@echo ""
	@echo "Output files:"
	@ls -lh output/ 2>/dev/null || echo "No output files"
