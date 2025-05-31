from fastapi import FastAPI, Request, HTTPException
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import re

app = FastAPI()

# Metric for suspicious logs count
SUSPICIOUS_LOGS = Counter(
    "suspicious_log_entries_total",
    "Total number of suspicious log entries detected"
)

# Define suspicious keywords or patterns
SUSPICIOUS_PATTERNS = [
    re.compile(r"error", re.IGNORECASE),
    re.compile(r"failed", re.IGNORECASE),
    re.compile(r"unauthorized", re.IGNORECASE),
    re.compile(r"exception", re.IGNORECASE),
    # Add more patterns as needed
]

def is_suspicious(log_entry: str) -> bool:
    return any(pattern.search(log_entry) for pattern in SUSPICIOUS_PATTERNS)

@app.post("/log")
async def receive_log(log: dict):
    """
    Receive a log entry as JSON with a 'message' field.
    Example:
    {
      "message": "User login failed due to invalid password"
    }
    """
    message = log.get("message")
    if not message:
        raise HTTPException(status_code=400, detail="Missing 'message' field in log")

    if is_suspicious(message):
        SUSPICIOUS_LOGS.inc()
        # Here, you could also trigger alerts, save to DB, etc.

    return {"status": "received", "suspicious": is_suspicious(message)}

@app.get("/metrics")
async def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
