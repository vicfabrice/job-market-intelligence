from fastapi import FastAPI

app = FastAPI(
    title="Job Market Intelligence API",
    description="API para buscar ofertas laborales y gestionar postulaciones",
    version="0.1.0",
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Job Market Intelligence API is running!"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}
