from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any
import logging
import asyncio

# Import the new scraper function
try:
    from gmaps_scraper_server.scraper import scrape_single_url, scrape_google_maps
except ImportError:
    logging.error("Could not import scraper functions from scraper.py")
    def scrape_single_url(*args, **kwargs):
        raise ImportError("Scraper function not available.")

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI(
    title="Google Maps URL Scraper API",
    description="API to extract data from a single Google Maps URL.",
    version="0.1.0",
)

class ExtractRequest(BaseModel):
    url: str
    headless: bool = True
    lang: str = "en"

@app.post("/extract", response_model=Dict[str, Any])
async def run_extract(request: ExtractRequest):
    """
    Extracts Google Maps data for a given URL.
    """
    logging.info(f"Received extract request for URL: '{request.url}', lang: {request.lang}, headless: {request.headless}")
    
    # Basic validation to ensure it looks like a Google Maps URL
    if "google.com/maps" not in request.url and "goo.gl/maps" not in request.url and "maps.app.goo.gl" not in request.url:
         raise HTTPException(status_code=400, detail="Invalid Google Maps URL provided.")

    try:
        # Run the scraping task with timeout
        result = await asyncio.wait_for(
            scrape_single_url(
                url=request.url,
                headless=request.headless,
                lang=request.lang
            ),
            timeout=120  # 2 minutes timeout for a single URL
        )
        
        if result is None:
            raise HTTPException(status_code=404, detail="Could not extract data from the provided URL.")
            
        logging.info(f"Data extraction finished for URL: '{request.url}'.")
        return result
        
    except asyncio.TimeoutError:
        logging.error(f"Scraping timeout for URL '{request.url}' after 120 seconds")
        raise HTTPException(status_code=504, detail="Scraping request timed out after 2 minutes")
    except ImportError as e:
         logging.error(f"ImportError during scraping for URL '{request.url}': {e}")
         raise HTTPException(status_code=500, detail="Server configuration error: Scraper not available.")
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"An error occurred during scraping for URL '{request.url}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An internal error occurred during scraping: {str(e)}")

# Basic root endpoint for health check or info
@app.get("/")
async def read_root():
    return {"message": "Google Maps URL Scraper API is running."}