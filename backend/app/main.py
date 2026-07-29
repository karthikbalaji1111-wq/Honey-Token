from fastapi import FastAPI

app = FastAPI(title="HoneyShield", version="0.1.0")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"service": "HoneyShield API", "status": "running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}
