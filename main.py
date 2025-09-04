import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
import matplotlib.pyplot as plt
from datetime import datetime

# Import the real SEC data scraper
from tools.sec_scraper import get_live_sec_data

# Load environment variables
load_dotenv()

# Disable CrewAI telemetry to avoid timeout issues
os.environ['OTEL_SDK_DISABLED'] = 'true'

def setup_environment():
    """Setup Groq environment with proper authentication"""
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key:
        print("❌ GROQ_API_KEY not found in .env file!")
        print("📝 Please check your .env file contains:")
        print("   GROQ_API_KEY=gsk_your_actual_api_key_here")
        return False
    
    if not groq_key.startswith('gsk_'):
        print("❌ Invalid GROQ_API_KEY format!")
        print("📝 Groq API keys should start with 'gsk_'")
        return False
    
    # Set environment variables for CrewAI/LiteLLM
    os.environ['GROQ_API_KEY'] = groq_key
    os.environ['OPENAI_API_KEY'] = groq_key  # Fallback for compatibility
    
    print(f"✅ Groq API Key loaded (starts with: {groq_key[:10]}...)")
    return True

def create_chart(sec_data):
    """Create a chart based on real SEC data"""
    try:
        os.makedirs('reports', exist_ok=True)
        
        # Extract companies and transaction volumes from real data
        filings = sec_data.get('recent_filings', [])
        
        if not filings:
            print("⚠️ No recent filings to chart")
            return "No recent SEC filings to chart"
        
        # Aggregate data by company
        company_volumes = {}
        for filing in filings:
            company = filing.get('company', 'UNKNOWN')
            shares = filing.get('shares', 0)
            
            if company in company_volumes:
                company_volumes[company] += shares
            else:
                company_volumes[company] = shares
        
        if not company_volumes:
            print("⚠️ No volume data to chart")
            return "No volume data available for charting"
        
        # Create chart
        companies = list(company_volumes.keys())
        volumes = list(company_volumes.values())
        
        _, ax = plt.subplots(figsize=(12, 8))
        bars = ax.bar(companies, volumes, color='darkblue', alpha=0.7)
        
        # Add value labels on bars
        for bar, volume in zip(bars, volumes):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{volume:,}', ha='center', va='bottom')
        
        ax.set_xlabel('Companies')
        ax.set_ylabel('Trading Volume (shares)')
        ax.set_title(f'Insider Trading Activity - Last 24 Hours\n({len(filings)} total filings)')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)
        
        chart_path = 'reports/insider_trading_chart.png'
        plt.tight_layout()
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📈 Chart created: {chart_path}")
        return f"Chart created with {len(companies)} companies and {sum(volumes):,} total shares traded"
        
    except Exception as e:
        print(f"⚠️ Chart creation error: {e}")
        return f"Chart creation error: {e}"

def main():
    """Main function with real SEC data retrieval"""
    print("🚀 Starting CrowdWisdomTrading AI Agent...")
    
    if not setup_environment():
        return
    
    try:
        # Updated LLM configurations with proper Groq setup
        llm_configs_to_try = [
            "groq/llama-3.1-8b-instant",
            "groq/llama-3.1-70b-versatile", 
            "groq/llama-3.3-70b-versatile"
        ]
        
        # FETCH REAL SEC DATA
        print("🔍 Fetching live SEC insider trading data from last 24 hours...")
        sec_data = get_live_sec_data(24)  # Get data from last 24 hours
        
        print(f"📊 Found {len(sec_data.get('recent_filings', []))} recent insider trading filings")
        
        # Try each LLM configuration
        for i, llm_config in enumerate(llm_configs_to_try, 1):
            try:
                print(f"🔄 Trying LLM configuration {i}/3...")
                
                # Create agents with current config
                data_agent = Agent(
                    role="SEC Data Analyst",
                    goal="Analyze real SEC insider trading data and identify key patterns from the last 24 hours",
                    backstory="You are an expert financial analyst specializing in insider trading patterns and SEC filings analysis. You analyze real-time SEC Form 4 filings.",
                    verbose=True,
                    llm=llm_config
                )
                
                chart_agent = Agent(
                    role="Data Visualization Expert", 
                    goal="Interpret real insider trading data visualizations",
                    backstory="You are a data visualization specialist who excels at interpreting charts of real market data and explaining their significance.",
                    verbose=True,
                    llm=llm_config
                )
                
                report_agent = Agent(
                    role="Financial Report Writer",
                    goal="Create comprehensive reports based on real SEC insider trading data",
                    backstory="You are a professional financial writer who creates detailed reports based on real SEC filings and market data.",
                    verbose=True,
                    llm=llm_config
                )
                
                # Create chart from real data
                chart_result = create_chart(sec_data)
                
                # Create tasks with real data
                analysis_task = Task(
                    description=f"""Analyze this REAL SEC insider trading data from the last 24 hours: {sec_data}
                    
                    This is live data from SEC EDGAR database. Please provide:
                    1. Summary of the most active insider trading in the last 24 hours
                    2. Key patterns and trends identified in the real data
                    3. Notable transactions by volume and value
                    4. Analysis of buying vs selling activity
                    5. Any unusual or significant insider activity
                    
                    Data source: {sec_data.get('data_source', 'SEC EDGAR API')}
                    Search period: {sec_data.get('hours_searched', 24)} hours
                    Total filings found: {len(sec_data.get('recent_filings', []))}""",
                    expected_output="Comprehensive analysis of real insider trading patterns with key insights and statistics",
                    agent=data_agent
                )
                
                chart_task = Task(
                    description=f"""Interpret this chart of real insider trading data: {chart_result}
                    
                    This chart shows actual insider trading volume from SEC filings in the last 24 hours.
                    Explain what trends and patterns this real market data reveals.""",
                    expected_output="Clear interpretation of the real market data visualization and its significance",
                    agent=chart_agent
                )
                
                report_task = Task(
                    description="""Create a comprehensive insider trading activity report based on REAL SEC data.
                    
                    Combine the real data analysis and chart interpretation into a professional report that includes:
                    1. Executive Summary
                    2. Key Findings from Real SEC Filings
                    3. Most Active Insider Trading in Last 24 Hours
                    4. Chart Analysis of Real Market Data  
                    5. Market Implications and Trends
                    6. Recommendations Based on Current Activity
                    
                    Emphasize that this analysis is based on actual SEC EDGAR database filings.""",
                    expected_output="Complete professional insider trading analysis report based on real SEC data",
                    agent=report_agent,
                    context=[analysis_task, chart_task]
                )
                
                # Create and run crew
                crew = Crew(
                    agents=[data_agent, chart_agent, report_agent],
                    tasks=[analysis_task, chart_task, report_task],
                    verbose=True
                )
                
                print("🔄 Running CrewAI analysis with real SEC data...")
                result = crew.kickoff()
                
                print(f"✅ Success with configuration {i}!")
                break
                
            except Exception as config_error:
                print(f"❌ Configuration {i} failed: {str(config_error)}")
                if i == len(llm_configs_to_try):
                    raise RuntimeError("All LLM configurations failed")
                continue
        
        # Save results
        os.makedirs('reports', exist_ok=True)
        with open('reports/final_report.txt', 'w', encoding='utf-8') as f:
            f.write("CrowdWisdomTrading AI Analysis Report - REAL SEC DATA\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Data Source: {sec_data.get('data_source', 'SEC EDGAR API')}\n")
            f.write(f"Search Period: {sec_data.get('hours_searched', 24)} hours\n")
            f.write(f"Filings Analyzed: {len(sec_data.get('recent_filings', []))}\n")
            f.write("Model: Groq Llama3.1-8B-Instant\n")
            f.write("="*60 + "\n\n")
            f.write(str(result))
        
        # Also save raw SEC data
        with open('reports/raw_sec_data.json', 'w', encoding='utf-8') as f:
            import json
            json.dump(sec_data, f, indent=2, default=str)
        
        print("\n" + "="*60)
        print("✅ ANALYSIS COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("📊 Report saved to: reports/final_report.txt")
        print("📈 Chart saved to: reports/insider_trading_chart.png") 
        print("📄 Raw data saved to: reports/raw_sec_data.json")
        print(f"🔍 Analyzed {len(sec_data.get('recent_filings', []))} real SEC filings")
        
        # Print summary
        print("\n📋 SUMMARY:")
        print("-" * 40)
        result_str = str(result)
        summary = result_str[:800] + "..." if len(result_str) > 800 else result_str
        print(summary)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your .env file has: GROQ_API_KEY=gsk_your_actual_key")
        print("2. Get free API key from: https://console.groq.com/")
        print("3. Make sure you have internet connection")
        print("4. Verify API key starts with 'gsk_'")
        print("5. SEC EDGAR API may be temporarily unavailable")

if __name__ == "__main__":
    main()