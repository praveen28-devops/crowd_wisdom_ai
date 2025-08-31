# tools/sec_scraper.py
from crewai.tools import tool
from sec_api import QueryApi
import os
import json

@tool("SEC Data Scraper")
def sec_data_scraper(days_back: int = 8) -> str:
    """
    Scrapes SEC EDGAR database for recent insider trading filings (Form 4).
    Returns a JSON string of the filings.
    """
    try:
        queryApi = QueryApi(api_key=os.getenv("SEC_API_KEY"))
        
        # Query for Form 4 filed in the last N days
        date_query = f"filedAt:[-{days_back}d TO *]"
        query = {
          "query": { "query_string": { "query": f"formType:\"4\" AND {date_query}" } },
          "from": "0",
          "size": "200",
          "sort": [{ "filedAt": { "order": "desc" } }]
        }

        filings = queryApi.get_filings(query)
        # Return the actual data as a JSON string
        return json.dumps(filings, indent=2)

    except Exception as e:
        return f"Error retrieving SEC data: {str(e)}"