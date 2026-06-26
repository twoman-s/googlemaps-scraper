#!/bin/bash
set -e

echo "Ensuring Playwright Chromium is installed..."
playwright install chromium

echo "Starting FastAPI server..."
exec uvicorn gmaps_scraper_server.main_api:app --host 0.0.0.0 --port 8001
