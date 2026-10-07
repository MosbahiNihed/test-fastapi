"""A small stateless FastAPI service: no database, every replica is identical."""
import os
import socket
from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel, Field

APP_NAME = os.getenv("APP_NAME", "hello-fastapi")
APP_VERSION = os.getenv("APP_VERSION", "dev")
GREETING = os.getenv("GREETING", "Hello")
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

app = FastAPI(title=APP_NAME, version=APP_VERSION)


class EchoRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)


@app.get("/")
def root():
    return {"message": f"{GREETING} from {APP_NAME}!", "version": APP_VERSION}


@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"{GREETING}, {name}!"}


@app.get("/info")
def info():
    """Shows which pod answered: refresh a few times to watch the Service load-balance."""
    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "hostname": socket.gethostname(),
        "time": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/echo")
def echo(payload: EchoRequest):
    return {"echo": payload.message, "length": len(payload.message)}


@app.get("/healthz", tags=["health"])
def healthz():
    return {"status": "ok"}


@app.get("/readyz", tags=["health"])
def readyz():
    return {"status": "ready"}
