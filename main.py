from fastapi import FastAPI

app = FastAPI(title="Job-Queue-API")

@app.get("/")
def home():
    return {
        "status": "successful",
        "service": "job-queue-api"
    }