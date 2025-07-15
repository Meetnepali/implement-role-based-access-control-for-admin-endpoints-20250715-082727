#!/bin/bash
set -e
apt-get update && apt-get install -y --no-install-recommends gcc
pip install --no-cache-dir fastapi==0.100.0 uvicorn==0.22.0
