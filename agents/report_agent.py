# agents/report_agent.py
from crewai import Agent
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

def create_report_agent():
    """Agent to generate comprehensive insider trading reports"""
    llm = ChatGroq(
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant"
    )
    
    return Agent(
        role="Financial Report Writer",
        goal="Generate comprehensive reports aggregating insider trading data, sentiment analysis, and charts",
        backstory="""You are a professional financial report writer who specializes in
        creating detailed insider trading analysis reports. You excel at consolidating
        data from multiple sources including SEC filings, sentiment analysis, and
        visualizations to highlight the most active insiders and market insights.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
