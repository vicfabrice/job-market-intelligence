# Job Market Intelligence Platform

A backend application built with **FastAPI** to collect, normalize, store, and analyze job postings from external sources.

This project demonstrates backend engineering practices through REST API development, third-party API integration, relational data modeling, automated testing, and deterministic skill-based job matching.

## Features

- **Company Management:** Create, retrieve, and list companies.
- **Job Offer Management:** Create, retrieve, update, delete, and filter job postings.
- **Application Tracking:** Manage job applications associated with job offers.
- **Greenhouse Integration:** Import job postings from configured Greenhouse job boards.
- **Idempotent Ingestion:** Identify previously imported offers and avoid duplicate records.
- **Skill Extraction:** Extract and normalize technical skills from job descriptions.
- **Skill-Based Matching:** Compare candidate skills with job requirements and return matched skills, missing skills, and a compatibility score.
- **Automated Testing:** Unit and API tests using pytest.

## Tech Stack

| Category | Technologies |
|---|---|
| Language | Python 3.12 |
| API | FastAPI, Pydantic |
| Database | PostgreSQL 17 |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| HTTP Client | HTTPX |
| Testing | pytest |
| Development Environment | Docker Compose |

## Architecture

The application follows a layered architecture with a separation of responsibilities:

| Directory | Responsibility |
|---|---|
| `app/api/v1/` | REST endpoints and request handling |
| `app/services/` | Business logic, ingestion, skill extraction, and matching |
| `app/repositories/` | Database access and persistence |
| `app/models/` | SQLAlchemy entities and relationships |
| `app/schemas/` | Pydantic validation and data transfer models |
| `app/integrations/greenhouse/` | External API integration and data mapping |
| `app/core/` | Application configuration and database connectivity |
| `scripts/` | Executable ingestion and development scripts |

The ingestion pipeline separates external data retrieval from normalization and persistence. Skill extraction and matching are implemented as application services, keeping business logic independent of HTTP request handling.

## Getting Started

### Prerequisites

- Python 3.12
- Docker and Docker Compose
- Git

### Installation

Clone the repository and navigate to its root directory.

Create and activate a virtual environment (Windows PowerShell):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements-dev.txt
```

Create your local environment configuration:

```powershell
Copy-Item .env.example .env
```

The default `.env.example` values are intended for local development and should match the credentials configured in `docker-compose.yml`.

Start PostgreSQL:

```powershell
docker compose up -d
```

Apply database migrations:

```powershell
alembic upgrade head
```

Start the application:

```powershell
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

Interactive API documentation (Swagger UI):

`http://localhost:8000/docs`

## Greenhouse Job Ingestion

The application retrieves job postings from the Greenhouse Job Board API.

The ingestion process:

1. Fetches job postings from configured Greenhouse boards.
2. Converts external data into a normalized representation.
3. Creates or reuses company records.
4. Identifies existing job postings to prevent duplicates.
5. Extracts and normalizes technical skills from job descriptions.
6. Persists job offers and their associated skills in PostgreSQL.

### Configuring Companies

Companies are configured in `app/integrations/greenhouse/config.py`.

The current configuration includes Anthropic:

```python
GREENHOUSE_COMPANIES = [
    GreenhouseCompanyConfig(
        name="Anthropic",
        board_token="anthropic",
        sector="Technology",
    ),
]
```

Additional companies can be included by adding new `GreenhouseCompanyConfig` entries with valid Greenhouse board tokens.

### Running the Ingestion

From the project root, execute:

```powershell
python -m scripts.import_greenhouse_jobs
```

The script displays the number of received, created, and skipped job postings, along with the number of companies created.

Repeated imports are designed to avoid duplicate job offers.

## Skill-Based Job Matching

The application provides a REST endpoint to compare a candidate's technical skills against those associated with a stored job offer.

**Endpoint**

`POST /api/v1/job-offers/{job_offer_id}/match`

**Example Request**

```json
{
  "candidate_skills": ["python", "aws", "docker"]
}
```

**Example Response**

```json
{
  "matched_skills": ["aws", "python"],
  "missing_skills": ["kubernetes", "postgresql"],
  "score": 50.0
}
```

The compatibility score represents the percentage of job skills matched by the candidate:

`score = (matched job skills / total job skills) × 100`

The response depends on the skills stored for the selected job offer.

Matching is deterministic and based on normalized technical skills. It does not use an LLM or semantic similarity model.

## Running Tests

Execute the automated test suite from the project root:

```powershell
python -m pytest -q
```

The project includes unit tests for business logic and API tests for endpoint behavior.

## Project Scope

This repository represents a completed backend MVP focused on job posting ingestion, structured persistence, skill extraction, and candidate-job matching.

The application is intended as a backend engineering portfolio project rather than a production-ready job recommendation platform.

Potential future improvements include scheduled ingestion, candidate profiles, more advanced matching strategies, and deployment automation.