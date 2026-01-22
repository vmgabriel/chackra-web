FROM python:3.12-slim AS builder

# Crear usuario no-root
ARG USER=app
ARG GROUP=app
ARG UID=1000
ARG GID=1000

RUN addgroup --gid $GID $GROUP \
    && adduser --uid $UID --gid $GID --disabled-password --gecos "" $USER

# Cambiar a root para preparar el entorno
USER root
WORKDIR /home/$USER/app

# Asegurar que el usuario app sea dueño del directorio
RUN chown -R $UID:$GID /home/$USER/app

# Ahora cambiar a usuario app
USER $USER

# Instalar Hatch
RUN pip install --user hatch
ENV PATH="/home/$USER/.local/bin:$PATH"

# Copiar código (ahora como app)
COPY . .

# Ejecutar Hatch — ahora tiene permisos
RUN hatch env create && hatch build

# --- Runtime ---
FROM python:3.12-slim AS runtime

ARG USER=app
ARG GROUP=app
ARG UID=1000
ARG GID=1000

RUN addgroup --gid $GID $GROUP \
    && adduser --uid $UID --gid $GID --disabled-password --gecos "" $USER

USER $USER
WORKDIR /home/$USER/app

# Copiar el wheel generado
COPY --from=builder /home/$USER/app/dist/*.whl ./
RUN pip install --no-cache-dir *.whl

# Copiar código fuente (opcional, si usas recursos dinámicos)
COPY . .

EXPOSE 8000

HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "chackra_web.entrypoints.web"]