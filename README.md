# ⚡ Real-Time Fraud Detection Engine (Stream Processing)

## 📌 Executive Summary
This project is an enterprise-grade, real-time data streaming pipeline designed to detect and block fraudulent credit card transactions in milliseconds. Moving beyond traditional batch processing, this system utilizes in-memory databases and stream-processing architectures to evaluate high-velocity transactional data on the fly.

## 🏗️ Architecture Design (Producer-Consumer Model)
The system mimics Tier-1 FinTech infrastructures (like Uber/Stripe) to process data with zero-latency:

* 📡 **The Producer (Data Ingestion):** A Python-based generator utilizing `Faker` to continuously stream mock transactions (UUIDs, user IDs, amounts, merchants) into an active message queue.
* ⚡ **The Highway (In-Memory Message Broker):** Utilizes **Redis Streams (`XADD`)** as the ultra-fast data highway, avoiding the disk-I/O bottlenecks of traditional SQL databases.
* 🎯 **The Consumer (Fraud Evaluation Logic):** An asynchronous "Sniper" script that reads the live stream (`XREAD`) and applies dynamic business logic:
    * **Velocity Checks:** Uses Redis `INCR` and `EXPIRE` (TTL) features to track swipe frequency. 
    * **Fraud Blocking:** Automatically freezes transactions if a user exceeds 3 swipes within a rolling 60-second window.
    * **VIP Whitelisting:** Seamlessly overrides fraud triggers for hardcoded elite accounts.

## ⚙️ Tech Stack & Tooling
* **Stream Processing:** Python, Redis (Streams, Pub/Sub logic)
* **Data Mocking:** Python Faker, NumPy
* **Environment:** Fully isolated via `venv` (PEP 668 compliance).

## 🚀 Business Impact (ROI)
* **Loss Prevention:** Instantly blocks fraudulent spikes, saving the business from catastrophic chargebacks.
* **Zero Latency:** Evaluates business logic entirely in RAM (Redis), allowing for uncompromised user experience during checkout.