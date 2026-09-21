from fastapi import FastAPI

app = FastAPI(title="Demo Docker API")


@app.get("/")
def root():
    return {
        "message": "Bonjour depuis Docker !"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/hello/{name}")
def hello(name: str):
    return {
        "message": f"Bonjour {name} !"
    }


@app.get("/info")
def info():
    return {
        "application": "Demo FastAPI",
        "version": "1.0.0",
        "environment": "docker"
    }