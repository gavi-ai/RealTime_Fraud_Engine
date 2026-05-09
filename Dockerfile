# Use a lightweight Python base image
FROM python:3.11-slim

# Set the VIP room inside the container
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy our god-tier source code
COPY src/ /app/src/