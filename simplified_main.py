import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
import matplotlib.pyplot as plt
from datetime import datetime

# Load environment variables
load_dotenv()

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
    # Some versions of CrewAI also check for OPENAI_API_KEY when using custom models
    os.environ['OPENAI_API_KEY'] = groq_key  # Fallback for compatibility
    
    print(f"✅ Groq API Key loaded (starts with: {groq_key[:10]}...)")
    return True

def create_chart():
    """Create a simple comparison chart"""
    try:
        os.makedirs('reports', exist_ok=True)
        
        companies = ['AAPL', 'MSFT', 'TSLA', 'GOOGL', 'AMZN']
        current_week = [50000, 25000, 100000, 30000, 45000]
        previous_week = [40000, 30000, 80000, 25000, 50000]
        
        x = range(len(companies))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar([i - width/2 for i in x], previous_week, width, label='Previous Week', alpha=0.8, color='lightblue')
        ax.bar([i + width/2 for i in x], current_week, width, label='Current Week', alpha=0.8, color='darkblue')
        
        ax.set_xlabel('Companies')
        ax.set_ylabel('Trading Volume (shares)')
        ax.set_title('Insider Trading Activity Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(companies)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        chart_path = 'reports/insider_trading_chart.png'
        plt.tight_layout()
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📈 Chart created: {chart_path}")
        return f"Chart saved to {chart_path}"
    except Exception as e:
        print(f"⚠️ Chart creation warning: {e}")
        return f"Chart creation attempted: {e}"

def main():
    """Main function with improved Groq configuration"""
    print("🚀 Starting CrowdWisdomTrading AI Agent...")
    
    if not setup_environment():
        return
    
    try:
        # Get API key
        groq_key = os.getenv('GROQ_API_KEY')
        
        # Try different LLM configurations for CrewAI + Groq compatibility
        llm_configs_to_try = [
            # Method 1: Direct Groq configuration
            {
                "model": "groq/llama3-8b-8192",
                "api_key": groq_key,
                "base_url": "https://api.groq.com/openai/v1"
            },
            # Method 2: LiteLLM format
            {
                "provider": "groq",
                "model": "llama3-8b-8192",
                "api_key": groq_key
            },
            # Method 3: Simple model name (let CrewAI handle)
            "groq/llama3-8b-8192"
        ]
        
        # Try each configuration
        for i, llm_config in enumerate(llm_configs_to_try, 1):
            try:
                print(f"🔄 Trying LLM configuration {i}/3...")
                
                # Create agents with current config
                data_agent = Agent(
                    role="SEC Data Analyst",
                    goal="Analyze SEC insider trading data and identify key patterns",
                    backstory="You are an expert financial analyst specializing in insider trading patterns and SEC filings analysis.",
                    verbose=True,
                    llm=llm_config if isinstance(llm_config, str) else None,
                    **({} if isinstance(llm_config, str) else {"llm_config": llm_config})
                )
                
                chart_agent = Agent(
                    role="Data Visualization Expert", 
                    goal="Interpret and explain data visualizations and charts",
                    backstory="You are a data visualization specialist who excels at interpreting charts and explaining their significance.",
                    verbose=True,
                    llm=llm_config if isinstance(llm_config, str) else None,
                    **({} if isinstance(llm_config, str) else {"llm_config": llm_config})
                )
                
                report_agent = Agent(
                    role="Financial Report Writer",
                    goal="Create comprehensive financial analysis reports",
                    backstory="You are a professional financial writer who creates detailed, well-structured reports for institutional investors.",
                    verbose=True,
                    llm=llm_config if isinstance(llm_config, str) else None,
                    **({} if isinstance(llm_config, str) else {"llm_config": llm_config})
                )
                
                # Mock SEC data for demonstration
                sec_data = {
                    'recent_filings': [
                        {'company': 'AAPL', 'insider': 'Tim Cook', 'transaction': 'Sale', 'shares': 50000, 'date': '2024-08-30', 'price': 225.50},
                        {'company': 'MSFT', 'insider': 'Satya Nadella', 'transaction': 'Purchase', 'shares': 25000, 'date': '2024-08-30', 'price': 420.75},
                        {'company': 'TSLA', 'insider': 'Elon Musk', 'transaction': 'Sale', 'shares': 100000, 'date': '2024-08-29', 'price': 250.00},
                        {'company': 'GOOGL', 'insider': 'Sundar Pichai', 'transaction': 'Sale', 'shares': 30000, 'date': '2024-08-29', 'price': 165.25},
                        {'company': 'AMZN', 'insider': 'Andy Jassy', 'transaction': 'Purchase', 'shares': 15000, 'date': '2024-08-28', 'price': 180.50}
                    ]
                }
                
                # Create chart first
                chart_result = create_chart()
                
                # Create tasks
                analysis_task = Task(
                    description=f"""Analyze this SEC insider trading data: {sec_data}
                    
                    Please provide:
                    1. Summary of most active insider trading in the last 24 hours
                    2. Key patterns and trends identified
                    3. Notable transactions by volume and value
                    4. Analysis of buying vs selling activity""",
                    expected_output="Comprehensive analysis of insider trading patterns with key insights and statistics",
                    agent=data_agent
                )
                
                chart_task = Task(
                    description=f"""Interpret this chart information: {chart_result}
                    
                    The chart shows insider trading volume comparison between current week and previous week.
                    Explain what trends and patterns this visualization reveals.""",
                    expected_output="Clear interpretation of the chart data and its significance",
                    agent=chart_agent
                )
                
                report_task = Task(
                    description="""Create a comprehensive insider trading activity report.
                    
                    Combine the data analysis and chart interpretation into a professional report that includes:
                    1. Executive Summary
                    2. Key Findings
                    3. Most Active Insider Trading Today
                    4. Chart Analysis
                    5. Market Implications
                    6. Recommendations""",
                    expected_output="Complete professional insider trading analysis report suitable for institutional investors",
                    agent=report_agent,
                    context=[analysis_task, chart_task]
                )
                
                # Create and run crew
                crew = Crew(
                    agents=[data_agent, chart_agent, report_agent],
                    tasks=[analysis_task, chart_task, report_task],
                    verbose=True
                )
                
                print(f"🔄 Running CrewAI analysis with configuration {i}...")
                result = crew.kickoff()
                
                # If we get here, it worked!
                print(f"✅ Success with configuration {i}!")
                break
                
            except Exception as config_error:
                print(f"❌ Configuration {i} failed: {str(config_error)}")
                if i == len(llm_configs_to_try):
                    raise Exception("All LLM configurations failed")
                continue
        
        # Save results
        os.makedirs('reports', exist_ok=True)
        with open('reports/final_report.txt', 'w', encoding='utf-8') as f:
            f.write(f"CrowdWisdomTrading AI Analysis Report\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Model: Groq Llama3-8B\n")
            f.write("="*60 + "\n\n")
            f.write(str(result))
        
        print("\n" + "="*60)
        print("✅ ANALYSIS COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"📊 Report saved to: reports/final_report.txt")
        print(f"📈 Chart saved to: reports/insider_trading_chart.png")
        
        # Print summary
        print(f"\n📋 SUMMARY:")
        print("-" * 40)
        result_str = str(result)
        summary = result_str[:800] + "..." if len(result_str) > 800 else result_str
        print(summary)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print(f"\n🔧 Troubleshooting:")
        print(f"1. Check your .env file has: GROQ_API_KEY=gsk_your_actual_key")
        print(f"2. Get free API key from: https://console.groq.com/")
        print(f"3. Make sure you have internet connection")
        print(f"4. Verify API key starts with 'gsk_'")

if __name__ == "__main__":
    main()