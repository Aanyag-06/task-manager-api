# Engineering Decisions — Task Manager API

This document details the architectural choices, framework selections, database design strategies, and real-world bugs resolved during development.

---

## 1. Framework Selection: FastAPI
I chose FastAPI over traditional frameworks like Django or Flask for  benefits such as:
* **High Performance:** Built on top of Starlette and Uvicorn, making it one of the fastest Python frameworks available.
* **Asynchronous Support:** Native support for `async/await` syntax allows efficient handling of concurrent network requests.
* **Automatic Documentation:** Out-of-the-box generation of interactive OpenAPI (Swagger) documentation simplifies API testing.
* **Data Validation:** Seamless integration with **Pydantic v2** ensures strict data parsing and automatic error responses.

## 2. Database & ORM Strategy
* **PostgreSQL:** It was selected as the primary relational database (RDBMS) for its robust support for ACID compliance and structural data integrity.
* **SQLAlchemy:** Utilized as the Object-Relational Mapper (ORM) to interact with the database using clean, Pythonic object-oriented principles.
* **Alembic:** Integrated as the database migration tool to track changes dynamically without manual database manipulation.

## 3. Real-World Challenges & Resolved Bugs

During the containerization and deployment process, we hit and successfully resolved several structural hurdles:

* **Bug 1: Docker Compose & Configuration Filename Typos**
  * *Issue:* The initial run failed with `no configuration file provided: not found`. 
  * *Resolution:* Identified naming convention mismatches (`docker_compose.yml` used an underscore instead of a hyphen, and `DockerFile` used an uppercase 'F'). Corrected them to `docker-compose.yml` and `Dockerfile` to match Docker's strict Linux-based case sensitivity.

* **Bug 2: ASGI App Import Module Pathing Error**
  * *Issue:* Docker container threw `Error loading ASGI app. Could not import module "main"`.
  * *Resolution:* The application entrypoint file `main.py` was nested inside an `app/` directory (`app/main.py`). The Dockerfile `CMD` instruction was updated from `"main:app"` to `"app.main:app"` so Uvicorn could accurately traverse the directory structure inside the container.

* **Bug 3: Missing Pydantic Email Validation Dependency**
  * *Issue:* The application crashed on startup with `ImportError: email-validator is not installed`.
  * *Resolution:* Discovered that Pydantic v2 requires explicit email validation extensions when processing email fields. Appended `email-validator` and `pydantic[email]` directly into `requirements.txt` and triggered a forced rebuild (`docker-compose up --build`) to re-cache the installation layers.