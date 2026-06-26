# Google Maps URL Scraper API

A FastAPI-based web service that extracts data (including photos, reviews count, rating, categories, contact info, etc.) from a single Google Maps URL using Playwright.

## Features

- **Single Endpoint API:** Pass a Google Maps URL, get structured data back.
- **Robust Extraction:** Gathers core place details and photos.
- **Built-in Swagger UI:** Easily test the API via the `/docs` endpoint.
- **Docker-ready:** Comes with `Dockerfile` and `docker-compose.yml` for easy deployment.

## API Documentation (Swagger UI)

FastAPI automatically generates interactive API documentation.
Once the server is running, open your browser and navigate to:

- **Swagger UI:** [http://localhost:8001/docs](http://localhost:8001/docs)

You can use the Swagger UI to test the API directly from your browser.

## Running the Application

### Option 1: Running with Docker (Recommended)

The easiest way to run the application is using Docker Compose.

1. Ensure you have Docker and Docker Compose installed.
2. Run the following command in the project root:

   ```bash
   docker compose up --build
   ```

3. The API will be available at `http://localhost:8001`.

### Option 2: Running Locally (Without Docker)

To run the application locally without Docker, you need Python 3.10+ installed.

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Playwright browsers (required for scraping):
   ```bash
   playwright install chromium
   ```

4. Start the server using Uvicorn:
   ```bash
   uvicorn gmaps_scraper_server.main_api:app --host 0.0.0.0 --port 8001 --reload
   ```

5. The API will be available at `http://localhost:8001`.

## Usage

### Endpoint: `/extract` (POST)

**Request Body (JSON):**

```json
{
  "url": "https://www.google.com/maps/place/...",
  "headless": true,
  "lang": "en"
}
```

**cURL Example:**

```bash
curl -X 'POST' \
  'http://localhost:8001/extract' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "url": "https://www.google.com/maps/place/Googleplex/@37.4220656,-122.0840897,17z/data=!3m1!4b1!4m6!3m5!1s0x808fba02425dad8f:0x6c296c66619367e0!8m2!3d37.4220656!4d-122.0840897!16zL20vMGc1cXc?entry=ttu",
  "headless": true,
  "lang": "en"
}'
```

**Response (JSON):**

```json
{
  "name": "Googleplex",
  "place_id": "ChIJj63aQkL6j4AR4GeTYWZsKWw",
  "address": "1600 Amphitheatre Pkwy, Mountain View, CA 94043, United States",
  "rating": 4.5,
  "reviews_count": 14500,
  "photos": [
    "https://lh5.googleusercontent.com/p/AF1QipP..."
  ],
  "website": "https://careers.google.com/",
  "phone": "650-253-0000"
}
```
