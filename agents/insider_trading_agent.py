# agents/insider_trading_agent.py
from crewai import Agent

def create_insider_trading_agent():
    return Agent(
        role="Insider Trading Analyzer",
        goal="Analyze insider trading patterns and identify the most active insider activity",
        backstory="""You are a financial analyst specializing in insider trading patterns. 
        You can identify trends, unusual activity, and provide insights on trading behavior.""",
        verbose=True,
        allow_delegation=False
    )