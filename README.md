# 🧠 Chackra Web

**Chackra Web** es una aplicación backend modular construida con **Clean Architecture**, diseñada para integrar inteligencia artificial local (Ollama), tareas programadas (Celery), notificaciones (Telegram) y gestión de datos (PostgreSQL). Ideal como base para sistemas autónomos, agentes de IA o plataformas de automatización.

> 🚀 **Características clave**:  
> - Arquitectura limpia (dominio, aplicación, infraestructura)  
> - Soporte para LLMs locales (Ollama) con tipado Pydantic  
> - Tareas asíncronas y programadas (Celery + Redis)  
> - Notificaciones en tiempo real (Telegram)  
> - Listo para Docker y producción  

---

## 📦 Requisitos

- Python 3.8+
- Docker y Docker Compose (para despliegue)
- Make
- Hatch

---

## 🛠️ Instalación rápida (con Docker)

1. Clona el repositorio:
   ```bash
   git clone https://github.com/vmgabriel/chackra-web.git
   cd chackra-web
   ```

2. Configura tus variables de entorno:
   ```bash
   cp .env.example .env
   # Edita .env con tus credenciales
   ```

3. Levanta los servicios:
   ```bash
   make docker-up
   ```

✅ **Servicios disponibles**:
- **API Web**: `http://localhost:8000`
- **Base de datos**: PostgreSQL en `localhost:5432`
- **Cola de tareas**: Redis en `localhost:6379`

---

## 💻 Desarrollo local (sin Docker)

1. Crea un entorno virtual y dependencias:
   ```bash
   make install
   ```

2. Inicia los servicios manualmente:

   - **Base de datos**: asegúrate de tener PostgreSQL corriendo.
   - **Redis**: `redis-server`
   - **Ollama** (opcional): `ollama serve`

3. Ejecuta los componentes:
   ```bash
   # Servidor web
   make web

   # Worker de tareas
   make worker

   # Scheduler (Celery Beat)
   make scheduler
   ```

---

## 🧪 Pruebas y calidad

```bash
# Ejecutar tests
make test

# Verificar tipado estático
make type-check
```

---

## 📁 Estructura del proyecto

```
src/
├── chackra_web/
│   ├── shared/               # Dominio compartido (entidades, puertos)
│   ├── application/          # Casos de uso y lógica de aplicación
│   ├── infrastructure/       # Adaptadores (DB, Celery, Ollama, Telegram)
│   └── entrypoints/          # Puntos de entrada (web, workers)
├── scripts/                  # Scripts auxiliares (migraciones, etc.)
└── tests/                    # Pruebas unitarias e integración
```

> 🔑 **Principios**:
> - El dominio no depende de frameworks externos.
> - Los adaptadores implementan puertos definidos en la capa de aplicación.
> - Los casos de uso orquestan flujos sin conocer detalles técnicos.

---

## ⚙️ Integraciones clave

### 🤖 Ollama (IA local)
- Usa cualquier modelo compatible (ej. `deepseek-coder`, `ministral`).
- Abstracción genérica con entrada/salida tipada (`Pydantic`).
- Configurable vía `OLLAMA_BASE_URL` en `.env`.

### 📬 Telegram
- Envío de alertas y notificaciones.
- Configura `TELEGRAM_TOKEN` y `TELEGRAM_CHANNEL_ID` en `.env`.

### 🔄 Celery
- **Worker**: procesa tareas asíncronas.
- **Scheduler**: ejecuta tareas programadas (medianoche, etc.).
- Backend: Redis.

---

## 🐳 Comandos útiles

| Comando | Descripción |
|--------|-------------|
| `make docker-up` | Inicia todos los servicios |
| `make docker-down` | Detiene los servicios |
| `make docker-logs` | Muestra logs en tiempo real |
| `make web` | Inicia solo el servidor Flask |
| `make worker` | Inicia el worker de Celery |
| `make scheduler` | Inicia Celery Beat |

---

## 🧩 Personalización

- **Agregar nuevos modelos de IA**: implementa `GenericLLMPort`.
- **Nuevos canales de notificación**: crea un adaptador para `NotificationPort`.
- **Tareas programadas**: define nuevas tareas en `infrastructure/tasks/`.

---

## 📜 Licencia

MIT License — ver [LICENSE](LICENSE).

---

## 🙌 Contribuciones

¡Las contribuciones son bienvenidas! Por favor, abre un issue o PR con mejoras.

> 💡 **¿Encontraste un bug?** Incluye pasos para reproducirlo y tu entorno (OS, Python, Docker versiones).
