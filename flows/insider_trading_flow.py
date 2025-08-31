from crewai import Agent, Task, Crew
from crewai.flow import Flow, listen, start
import os

class InsiderTradingFlow(Flow):
    
    def __init__(self):
        super().__init__()
        # Configure Groq for all agents
        self.llm_config = {
            "model": "groq/llama3-8b-8192",
            "api_key": os.getenv('GROQ_API_KEY'),
            "base_url": "https://api.groq.com/openai/v1"
        }
    
    @start()
    def fetch_recent_data(self):
        """Step 1: Get recent SEC data"""
        agent = Agent(
            role="SEC Data Retriever",
            goal="Retrieve and analyze SEC insider trading data",
            backstory="You are an expert at analyzing SEC insider trading filings.",
            verbose=True,
            llm_config=self.llm_config
        )
        
        task = Task(
            description="Analyze recent insider trading activity and identify key patterns",
            expected_output="Summary of recent insider trading activity with key insights",
            agent=agent
        )
        
        crew = Crew(agents=[agent], tasks=[task])
        result = crew.kickoff()
        return result.raw
    
    @listen(fetch_recent_data)
    def analyze_trading_patterns(self, recent_data):
        """Step 2: Analyze the retrieved data"""
        agent = Agent(
            role="Trading Pattern Analyzer",
            goal="Identify and analyze insider trading patterns",
            backstory="You are a financial analyst specializing in insider trading patterns.",
            verbose=True,
            llm_config=self.llm_config
        )
        
        task = Task(
            description=f"Analyze this data and identify the most active insider trading: {recent_data}",
            expected_output="Detailed analysis of insider trading patterns and trends",
            agent=agent
        )
        
        crew = Crew(agents=[agent], tasks=[task])
        result = crew.kickoff()
        return result.raw
    
    @listen(analyze_trading_patterns)
    def create_visualizations(self, analysis):
        """Step 3: Create comparison charts"""
        agent = Agent(
            role="Data Visualization Specialist",
            goal="Create informative charts and visualizations",
            backstory="You are a data visualization expert.",
            verbose=True,
            llm_config=self.llm_config
        )
        
        task = Task(
            description=f"Describe how to visualize this analysis: {analysis}",
            expected_output="Recommendations for charts and visualizations",
            agent=agent
        )
        
        crew = Crew(agents=[agent], tasks=[task])
        result = crew.kickoff()
        return result.raw
    
    @listen(create_visualizations)
    def generate_report(self, charts_info):
        """Step 4: Generate final report"""
        agent = Agent(
            role="Financial Report Writer",
            goal="Write comprehensive financial reports",
            backstory="You are a professional financial writer.",
            verbose=True,
            llm_config=self.llm_config
        )
        
        task = Task(
            description=f"Create a comprehensive insider trading report including: {charts_info}",
            expected_output="Complete insider trading activity report with analysis",
            agent=agent
        )
        
        crew = Crew(agents=[agent], tasks=[task])
        result = crew.kickoff()
        return result.raw