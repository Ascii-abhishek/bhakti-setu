#!/bin/bash

# Bhakti Setu - Run script with Doppler environment variables
# This script uses Doppler to inject environment variables and starts the application

# Set Doppler token for production environment

# Activate virtual environment
source .venv/bin/activate
doppler run -- uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
