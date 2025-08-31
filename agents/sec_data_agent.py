# agents/sec_data_agent.py
from crewai import Agent
from tools.sec_scraper import get_sec_data

def create_sec_data_agent():
    return Agent(
        role="SEC Data Retriever",
        goal="Retrieve the latest SEC insider trading filings from the past 24 hours",
        backstory="""You are an expert at navigating SEC databases and extracting 
        relevant insider trading information. You focus on Forms 3, 4, and 5 which 
        contain insider trading disclosures.""",
        tools=[get_sec_data],
        verbose=True,
        allow_delegation=False
    )