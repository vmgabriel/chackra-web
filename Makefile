.PHONY: help install run dev test clean build \
        web worker scheduler \
        docker-build docker-up docker-down docker-restart \
        docker-logs docker-shell docker-ps docker-prune \
        db-init db-migrate

# ==============================
# Variables
# ==============================
PYTHON = python3
HATCH = hatch
COMPOSE = docker-compose
APP_NAME = chackra-web

# ==============================
# Help
# ==============================
help:
	@echo "🚀 Comandos disponibles:"
	@echo ""
	@echo "🔧 Desarrollo local (con Hatch):"
	@echo "  make install         - Crea el entorno virtual y dependencias"
	@echo "  make web             - Ejecuta solo el servidor Flask"
	@echo "  make worker          - Ejecuta el worker de Celery"
	@echo "  make scheduler       - Ejecuta Celery Beat"
	@echo "  make dev             - Ejecuta Flask en modo debug"
	@echo "  make test            - Ejecuta pruebas"
	@echo "  make type-check      - Verifica tipado con mypy"
	@echo ""
	@echo "🐳 Docker / Producción:"
	@echo "  make docker-build    - Construye las imágenes"
	@echo "  make docker-up       - Levanta servicios en background"
	@echo "  make docker-down     - Detiene y elimina contenedores"
	@echo "  make docker-restart  - Reinicia servicios"
	@echo "  make docker-logs     - Muestra logs en tiempo real"
	@echo "  make docker-shell    - Accede al shell del contenedor web"
	@echo "  make docker-ps       - Lista servicios"
	@echo ""
	@echo "🧹 Mantenimiento:"
	@echo "  make clean           - Limpia cachés y artefactos"
	@echo "  make docker-prune    - Limpia volúmenes y redes huérfanas"

# ==============================
# Local Environment
# ==============================
install:
	$(HATCH) env create

web:
	$(HATCH) run run-server

worker:
	$(HATCH) run run-worker

scheduler:
	$(HATCH) run run-schedule-worker

dev:
	FLASK_DEBUG=1 $(HATCH) run python -m flask run --host=0.0.0.0 --port=8000

test:
	$(HATCH) run pytest

type-check:
	$(HATCH) env run types check

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f \( -name "*.pyc" -o -name "*.pyo" -o -name ".coverage" \) -delete 2>/dev/null || true
	rm -rf .pytest_cache .mypy_cache build dist *.egg-info .hatch

build:
	$(HATCH) build

docker-build:
	$(COMPOSE) build --no-cache

docker-up:
	$(COMPOSE) up -d

docker-down:
	$(COMPOSE) down

docker-restart: docker-down docker-up

docker-logs:
	$(COMPOSE) logs -f --tail=100

docker-shell:
	$(COMPOSE) exec web sh

docker-ps:
	$(COMPOSE) ps

docker-prune:
	$(COMPOSE) down -v --remove-orphans
	docker volume prune -f
	docker network prune -f

# ==============================
# DB
# ==============================
db-init:
	$(COMPOSE) exec web $(PYTHON) scripts/db_init.py


# Comandos de producción
run-prod:
	$(HATCH) -e prod run web

build-prod:
	$(HATCH) -e prod build
