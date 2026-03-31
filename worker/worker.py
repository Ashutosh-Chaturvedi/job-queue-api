import redis 
import json 
import time

r = redis.Redis(decode_responses=True)

try:
    while True: 
        job_data = r.brpop("job_queue", timeout=5)
        
        if job_data is None:
            continue  
        
        _, job_data = job_data
        
        job = json.loads(job_data)
        job_id = job["id"]
        
        r.set(f"job:{job_id}", json.dumps({
            "status": "STARTED"
        }))
        
        time.sleep(15)
        
        try:
            result = sum(job["payload"].values())
            
            r.set(f"job:{job_id}", json.dumps({"result": result}))
            
            r.set(f"job:{job_id}", json.dumps({"status": "SUCCESS"}))
            
        except Exception as e: 
            r.set(f"job: {job_id}", json.dumps({
                "status": "FAILED",
                "error": str(e)
            }))
        
except KeyboardInterrupt:
    print("Worker Shutting down")
    