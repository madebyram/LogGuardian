from fastapi import FastAPI
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

app = FastAPI()

error_counter = Counter('error_logs_total', 'Total error logs detected')

@app.get("/")
def read_root():
    return {"message": "Welcome to LogGuardian"}

@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

@app.post("/log")
def ingest_log(log: dict):
    # Imagine log parsing here, increase error counter on condition
    if log.get("level") == "error":
        error_counter.inc()
    return {"status": "log received"}
