# Redis-Based Job Queue System (Celery-like)

A minimal distributed job queue system built using **FastAPI + Redis**, inspired by tools like Celery.

This project demonstrates how to decouple request handling from background processing using a producer-consumer architecture.

---

## Overview

Instead of processing heavy tasks inside an API request, this system:

1. Accepts a job via API
2. Pushes it to a Redis queue
3. A worker process consumes and executes the job
4. Results and status are stored in Redis
5. Client can query job status anytime

---

## Architecture

```
Client → FastAPI → Redis (Queue)
                     ↓
                  Worker
                     ↓
              Redis (Result Store)
                     ↑
                FastAPI → Client
```

---

## Tech Stack

* FastAPI (API layer)
* Redis (queue + storage)
* Python (worker execution)
* Uvicorn (ASGI server)
* Docker (for Redis)

---

## Project Structure

```
job-queue/
│
├── app/
│   └── main.py          # FastAPI app (producer)
│
├── worker/
│   └── worker.py        # Background worker (consumer)
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd job-queue
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Start Redis (Docker)

```bash
docker run -d -p 6379:6379 redis
```

---

### 4. Run FastAPI server

```bash
uvicorn app.main:app --reload
```

---

### 5. Start Worker

```bash
python worker/worker.py
```

---

## API Usage

### Create Job

```bash
POST /jobs
```

Request body:

```json
{
  "type": "sum",
  "payload": {
    "a": 5,
    "b": 10
  }
}
```

Response:

```json
{
  "job_id": "uuid",
  "status": "PENDING"
}
```

---

### Get Job Status

```bash
GET /jobs/{job_id}
```

Response:

```json
{
  "job": {
    "status": "SUCCESS"
  },
  "result": {
    "result": 15
  }
}
```

---

## Job Lifecycle

```
PENDING → STARTED → SUCCESS / FAILED
```

---

## How It Works

* FastAPI pushes jobs into Redis using `LPUSH`
* Worker consumes jobs using `BRPOP`
* Job status and results are stored as Redis keys:

  * `job:{id}` → status
  * `result:{id}` → output

---

## Limitations (Current Version)

* No retry mechanism
* No job scheduling
* No priority queues
* No persistence beyond Redis
* No multi-worker coordination handling

---

## Future Improvements

* Retry + backoff strategy
* Delayed jobs (Redis ZSET)
* Multiple workers (horizontal scaling)
* PostgreSQL for persistent storage
* WebSocket for real-time updates
* Idempotency handling

---

## Learning Goals

This project helps understand:

* Asynchronous processing
* Producer-consumer pattern
* Distributed system basics
* Queue-based architectures
