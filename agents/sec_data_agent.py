# agents/sec_data_agent.py
from crewai import Agent
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

def create_24hr_sec_data_agent():
    """Agent to fetch SEC insider trading data from last 24 hours"""
    llm = ChatGroq(
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant"
    )
    
    return Agent(
        role="24-Hour SEC Data Retriever",
        goal="Retrieve and analyze SEC insider trading filings from the past 24 hours",
        backstory="""You are an expert at navigating SEC EDGAR databases and extracting
        recent insider trading information. You specialize in Forms 3, 4, and 5 which
        contain insider trading disclosures. You focus on the most recent 24-hour period
        to identify immediate trading activity by corporate insiders.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

def create_weekly_sec_data_agent():
    """Agent to fetch SEC insider trading data from prior week for comparison"""
    llm = ChatGroq(
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant"
    )
    
    return Agent(
        role="Weekly SEC Data Retriever",
        goal="Retrieve and analyze SEC insider trading filings from the prior week for comparison analysis",
        backstory="""You are an expert at navigating SEC EDGAR databases and extracting
        historical insider trading information for comparative analysis. You specialize in
        gathering data from the prior week to establish baseline trading patterns and
        identify trends when compared to recent 24-hour activity.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

def create_data_processing_agent():
    """Agent to process and aggregate retrieved insider trading data"""
    llm = ChatGroq(
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant"
    )
    
    return Agent(
        role="Data Processing Specialist",
        goal="Process, normalize and aggregate insider trading data for analysis",
        backstory="""You are a data processing expert who specializes in cleaning,
        normalizing and aggregating financial data. You excel at identifying the most
        active insiders by volume and value, standardizing data formats, and preparing
        datasets for comparative analysis between different time periods.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
