#!/bin/bash
set -e

echo "Checking if Playwright Chromium is already installed..."
if python -c "from playwright.sync_api import sync_playwright; import os, sys; p = sync_playwright().start(); browser = p.chromium; sys.exit(0 if os.path.exists(browser.executable_path) else 1)" 2>/dev/null; then
    echo "Playwright Chromium is already installed, skipping download."
else
    echo "Playwright Chromium not found. Installing..."
    playwright install chromium
fi

echo "Starting FastAPI server..."
exec uvicorn gmaps_scraper_server.main_api:app --host 0.0.0.0 --port 8001
