from fastapi import FastAPI
import redis
import uuid
import json

app = FastAPI(title="Job-Queue-API")
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

@app.post("/jobs")
def create_job(payload: dict):
    job_id = str(uuid.uuid4())
    
    job = {
        "id": job_id, 
        "payload": payload
    }
    
    r.set(f"job:{job_id}", json.dumps({
        "status": "PENDING"
    }))
    
    r.lpush("job_queue", json.dumps(job))
    
    return {
        "job_id": job_id, 
        "status": "PENDING"
    }
    
@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    job = r.get(f"job:{job_id}")
    result = r.get(f"result:{job_id}")

    if not job:
        return {"error": "Job not found"}

    return {
        "job": json.loads(job),
        "result": json.loads(result) if result else None
    }

