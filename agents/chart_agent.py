# agents/chart_agent.py
from crewai import Agent
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

def create_chart_agent():
    """Agent to create comparative charts for insider trading data"""
    llm = ChatGroq(
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant"
    )
    
    return Agent(
        role="Data Visualization Specialist",
        goal="Create comparative charts showing 24hr vs prior week insider trading activity",
        backstory="""You are a data visualization expert who creates compelling charts
        and graphs to help identify trends, spikes, and notable trades in insider activity.
        You specialize in comparative analysis visualizations that highlight patterns
        between recent activity and historical baselines.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )