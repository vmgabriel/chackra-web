.PHONY: install run test clean build dev help docker-build docker-up docker-down

# Variables
PYTHON = python3
HATCH = hatch

help:
	@echo "Comandos disponibles:"
	@echo "  make install  - Instala las dependencias del proyecto"
	@echo "  make run      - Ejecuta la aplicación Flask"
	@echo "  make dev      - Ejecuta la aplicación en modo desarrollo"
	@echo "  make test     - Ejecuta las pruebas"
	@echo "  make clean    - Limpia archivos temporales"
	@echo "  make build    - Construye el proyecto"

install:
	$(HATCH) env create

run:
	$(HATCH) run run-server

dev:
	$(HATCH) run python -m flask run --debug

test:
	$(HATCH) run pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +

build:
	$(HATCH) build

# Nuevos comandos Docker
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-ps:
	docker-compose ps

# ... resto del Makefile existente