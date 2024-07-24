#!/bin/bash

set -e

echo "Starting application"

uvicorn app:app --reload --host=0.0.0.0 --port=8008 --log-config configs/log_conf.yml --proxy-headers --forwarded-allow-ips=*

