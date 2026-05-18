# Real-Time Fraud Detection Engine

Stream processing pipeline that detects fraudulent transactions in 
milliseconds using Redis In-Memory Streams. Fully containerised — 
clone and run in under 60 seconds with Docker.

---

## What this solves

Batch fraud detection catches fraud after the fact. This pipeline 
evaluates every transaction on arrival — no disk I/O, no queue 
backlog — and freezes accounts the moment they exceed velocity 
thresholds.

---

## How it works
[Producer]                    [Redis Stream]           [Consumer — "Sniper"]
Faker generates           →   XADD pushes events   →   XREAD polls continuously
synthetic transactions        to in-memory stream        evaluates swipe velocity
                                                     if user exceeds N swipes
                                                     within 60s TTL window:
                                                       → account flagged
                                                       → event pushed to dashboard

                                                [Streamlit Dashboard]
                                                Live radar: flagged accounts,
                                                transaction volume, freeze log

Producer and consumer are fully decoupled — if the consumer restarts, 
the Redis stream retains unconsumed events. No data loss.

---

## Tech stack

| Component | Tool |
|---|---|
| Stream transport | Redis Streams (XADD / XREAD) |
| Fraud logic | Python, in-memory state |
| Observability UI | Streamlit |
| Containerisation | Docker, Docker Compose |
| Data generation | Faker |

---

## Quick start

```bash
git clone https://github.com/gavi-ai/RealTime_Fraud_Engine.git
cd RealTime_Fraud_Engine

docker compose up --build
```

Then open `http://localhost:8501` for the live dashboard.

That's it. Docker handles Redis, the producer, the consumer, and the 
dashboard — all in isolated containers.

---

## Repository structure
RealTime_Fraud_Engine/
├── src/
│   ├── producer.py       # Generates synthetic transaction stream
│   ├── consumer.py       # Fraud detection logic (velocity rules + TTL)
│   └── dashboard.py      # Streamlit live radar UI
├── Dockerfile
├── docker-compose.yml    # Wires Redis + producer + consumer + dashboard
├── requirements.txt
├── architecture.png
└── dashboard-preview.png

---

## Fraud detection logic

Each transaction is evaluated against a per-user rolling window:

- Window size: 60 seconds (Redis TTL)
- Threshold: configurable swipe velocity limit
- On breach: user ID is flagged, added to frozen accounts set, 
  broadcast to dashboard in real time

No database writes. No disk I/O. Pure in-memory evaluation.
