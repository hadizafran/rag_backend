#!/bin/bash
# Start FastAPI server for Render deployment
uvicorn app:app --host 0.0.0.0 --port $PORT
