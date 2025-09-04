from crewai import Agent, Task, Crew
from crewai.flow import Flow, listen, start
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv

# Import our custom agents and tools
from agents.sec_data_agent import create_24hr_sec_data_agent, create_weekly_sec_data_agent, create_data_processing_agent
from agents.chart_agent import create_chart_agent
from agents.sentiment_agent import create_sentiment_analysis_agent, create_social_media_agent
from agents.report_agent import create_report_agent
from tools.sec_scraper import get_live_sec_data
from tools.chart_generator import create_comparison_chart, create_interactive_chart
from tools.sentiment_analyzer import analyze_market_sentiment, gather_social_content

load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reports/insider_trading_flow.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class InsiderTradingFlow(Flow):
    """Comprehensive CrewAI Flow for SEC Insider Trading Analysis"""
    
    def __init__(self):
        super().__init__()
        self.flow_id = f"insider_trading_flow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"Initializing InsiderTradingFlow: {self.flow_id}")
        
        # Ensure reports directory exists
        os.makedirs('reports', exist_ok=True)
        
        # Store flow state
        self.flow_state = {
            'start_time': datetime.now().isoformat(),
            'data_24hr': None,
            'data_weekly': None,
            'processed_data': None,
            'sentiment_data': None,
            'charts_created': [],
            'errors': []
        }
    
    @start()
    def fetch_24hr_data(self) -> Dict[str, Any]:
        """Step 1: Fetch SEC insider trading data from last 24 hours"""
        try:
            logger.info("Starting 24-hour SEC data retrieval")
            
            # Get live SEC data
            data_24hr = get_live_sec_data(24)
            self.flow_state['data_24hr'] = data_24hr
            
            # Create agent for analysis
            agent = create_24hr_sec_data_agent()
            
            task = Task(
                description=f"""Analyze the following SEC insider trading data from the last 24 hours:
                
                {json.dumps(data_24hr, indent=2)}
                
                Provide a comprehensive analysis including:
                1. Total number of filings processed
                2. Most active companies by trading volume
                3. Most active insiders by transaction value
                4. Notable transactions (large volumes or unusual activity)
                5. Buying vs selling activity breakdown
                6. Key patterns and trends identified
                
                Focus on actionable insights for investors and market analysts.""",
                expected_output="Detailed analysis of 24-hour insider trading activity with key metrics and insights",
                agent=agent
            )
            
            crew = Crew(agents=[agent], tasks=[task], verbose=True)
            result = crew.kickoff()
            
            logger.info("24-hour data analysis completed successfully")
            return {
                'raw_data': data_24hr,
                'analysis': result.raw,
                'status': 'success',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            error_msg = f"Error in 24hr data fetch: {str(e)}"
            logger.error(error_msg)
            self.flow_state['errors'].append(error_msg)
            return {
                'raw_data': None,
                'analysis': f"Error: {error_msg}",
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }
    
    @listen(fetch_24hr_data)
    def fetch_weekly_comparison_data(self, data_24hr_result: Dict[str, Any]) -> Dict[str, Any]:
        """Step 2: Fetch prior week data for comparison"""
        try:
            logger.info("Starting weekly SEC data retrieval for comparison")
            
            # Get weekly SEC data (7 days)
            data_weekly = get_live_sec_data(168)  # 7 days * 24 hours
            self.flow_state['data_weekly'] = data_weekly
            
            # Create agent for weekly analysis
            agent = create_weekly_sec_data_agent()
            
            task = Task(
                description=f"""Analyze the following SEC insider trading data from the prior week:
                
                {json.dumps(data_weekly, indent=2)}
                
                Compare this with the 24-hour data analysis: {data_24hr_result['analysis']}
                
                Provide:
                1. Weekly trading volume and activity summary
                2. Daily average vs 24-hour activity comparison
                3. Identification of unusual spikes or patterns
                4. Baseline establishment for comparison analysis
                5. Most consistently active companies and insiders
                """,
                expected_output="Comprehensive weekly baseline analysis with comparison insights",
                agent=agent
            )
            
            crew = Crew(agents=[agent], tasks=[task], verbose=True)
            result = crew.kickoff()
            
            logger.info("Weekly comparison data analysis completed")
            return {
                'raw_data_24hr': data_24hr_result['raw_data'],
                'raw_data_weekly': data_weekly,
                'analysis_24hr': data_24hr_result['analysis'],
                'analysis_weekly': result.raw,
                'status': 'success',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            error_msg = f"Error in weekly data fetch: {str(e)}"
            logger.error(error_msg)
            self.flow_state['errors'].append(error_msg)
            return {
                'raw_data_24hr': data_24hr_result.get('raw_data'),
                'raw_data_weekly': None,
                'analysis_24hr': data_24hr_result.get('analysis'),
                'analysis_weekly': f"Error: {error_msg}",
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }
    
    @listen(fetch_weekly_comparison_data)
    def process_and_normalize_data(self, comparison_data: Dict[str, Any]) -> Dict[str, Any]:
        """Step 3: Process and normalize the retrieved data"""
        try:
            logger.info("Starting data processing and normalization")
            
            # Create data processing agent
            agent = create_data_processing_agent()
            
            task = Task(
                description=f"""Process and normalize the following insider trading data:
                
                24-Hour Data: {json.dumps(comparison_data.get('raw_data_24hr', {}), indent=2)}
                Weekly Data: {json.dumps(comparison_data.get('raw_data_weekly', {}), indent=2)}
                
                24-Hour Analysis: {comparison_data.get('analysis_24hr', '')}
                Weekly Analysis: {comparison_data.get('analysis_weekly', '')}
                
                Tasks:
                1. Normalize data formats and align time periods
                2. Identify most active insiders by volume and value
                3. Calculate percentage changes and trends
                4. Aggregate data by company, insider, and transaction type
                5. Prepare data for visualization and reporting
                6. Flag any anomalies or exceptional activity
                """,
                expected_output="Processed and normalized dataset with key metrics and aggregations ready for analysis",
                agent=agent
            )
            
            crew = Crew(agents=[agent], tasks=[task], verbose=True)
            result = crew.kickoff()
            
            processed_result = {
                'processed_analysis': result.raw,
                'raw_data_24hr': comparison_data.get('raw_data_24hr'),
                'raw_data_weekly': comparison_data.get('raw_data_weekly'),
                'analysis_24hr': comparison_data.get('analysis_24hr'),
                'analysis_weekly': comparison_data.get('analysis_weekly'),
                'status': 'success',
                'timestamp': datetime.now().isoformat()
            }
            
            self.flow_state['processed_data'] = processed_result
            logger.info("Data processing completed successfully")
            return processed_result
            
        except Exception as e:
            error_msg = f"Error in data processing: {str(e)}"
            logger.error(error_msg)
            self.flow_state['errors'].append(error_msg)
            return {
                'processed_analysis': f"Error: {error_msg}",
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }
    
    @listen(process_and_normalize_data)
    def create_comparative_charts(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Step 4: Create comparative charts and visualizations"""
        try:
            logger.info("Starting chart creation")
            
            # Create chart agent
            agent = create_chart_agent()
            
            # Generate charts using tools
            chart_results = []
            
            # Create comparison charts
            if processed_data.get('raw_data_24hr') and processed_data.get('raw_data_weekly'):
                chart_result = create_comparison_chart(
                    json.dumps(processed_data['raw_data_24hr']),
                    json.dumps(processed_data['raw_data_weekly'])
                )
                chart_results.append(chart_result)
                
                # Create interactive chart
                interactive_result = create_interactive_chart(
                    json.dumps(processed_data['raw_data_24hr'])
                )
                chart_results.append(interactive_result)
            
            # Agent task for chart interpretation
            task = Task(
                description=f"""Interpret and analyze the following chart creation results:
                
                Chart Results: {chart_results}
                
                Processed Data Analysis: {processed_data.get('processed_analysis', '')}
                
                Provide:
                1. Interpretation of visual trends and patterns
                2. Key insights from comparative analysis
                3. Notable spikes, anomalies, or trends
                4. Investment implications of the visualized data
                5. Recommendations for further investigation
                """,
                expected_output="Comprehensive interpretation of charts and visual analysis with actionable insights",
                agent=agent
            )
            
            crew = Crew(agents=[agent], tasks=[task], verbose=True)
            result = crew.kickoff()
            
            chart_data = {
                'chart_results': chart_results,
                'chart_interpretation': result.raw,
                'processed_data': processed_data,
                'status': 'success',
                'timestamp': datetime.now().isoformat()
            }
            
            self.flow_state['charts_created'] = chart_results
            logger.info("Chart creation completed successfully")
            return chart_data
            
        except Exception as e:
            error_msg = f"Error in chart creation: {str(e)}"
            logger.error(error_msg)
            self.flow_state['errors'].append(error_msg)
            return {
                'chart_results': [],
                'chart_interpretation': f"Error: {error_msg}",
                'processed_data': processed_data,
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }
    
    @listen(create_comparative_charts)
    def analyze_market_sentiment(self, chart_data: Dict[str, Any]) -> Dict[str, Any]:
        """Step 5: Perform sentiment analysis on related content"""
        try:
            logger.info("Starting sentiment analysis")
            
            # Extract companies from processed data
            companies = []
            raw_data = chart_data.get('processed_data', {}).get('raw_data_24hr', {})
            filings = raw_data.get('recent_filings', [])
            
            for filing in filings:
                company = filing.get('company', '')
                if company and company not in companies:
                    companies.append(company)
            
            # Limit to top 10 companies to avoid rate limits
            companies = companies[:10]
            
            # Create sentiment analysis agent
            sentiment_agent = create_sentiment_analysis_agent()
            social_agent = create_social_media_agent()
            
            # Gather sentiment data
            sentiment_result = analyze_market_sentiment(json.dumps(companies))
            social_content = gather_social_content(json.dumps(companies))
            
            # Agent analysis of sentiment
            sentiment_task = Task(
                description=f"""Analyze the following sentiment data for companies with recent insider trading:
                
                Companies Analyzed: {companies}
                
                Sentiment Analysis Results: {sentiment_result}
                
                Social Media Content: {social_content}
                
                Chart Analysis: {chart_data.get('chart_interpretation', '')}
                
                Provide:
                1. Correlation between insider trading and market sentiment
                2. Sentiment trends that may influence or reflect insider activity
                3. Social media buzz analysis related to insider trading
                4. Risk assessment based on sentiment patterns
                5. Investment implications of sentiment vs insider activity
                """,
                expected_output="Comprehensive sentiment analysis with correlation to insider trading activity",
                agent=sentiment_agent
            )
            
            crew = Crew(agents=[sentiment_agent], tasks=[sentiment_task], verbose=True)
            result = crew.kickoff()
            
            sentiment_data = {
                'companies_analyzed': companies,
                'sentiment_results': sentiment_result,
                'social_content': social_content,
                'sentiment_analysis': result.raw,
                'chart_data': chart_data,
                'status': 'success',
                'timestamp': datetime.now().isoformat()
            }
            
            self.flow_state['sentiment_data'] = sentiment_data
            logger.info("Sentiment analysis completed successfully")
            return sentiment_data
            
        except Exception as e:
            error_msg = f"Error in sentiment analysis: {str(e)}"
            logger.error(error_msg)
            self.flow_state['errors'].append(error_msg)
            return {
                'companies_analyzed': [],
                'sentiment_results': f"Error: {error_msg}",
                'sentiment_analysis': f"Error: {error_msg}",
                'chart_data': chart_data,
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }
    
    @listen(analyze_market_sentiment)
    def generate_comprehensive_report(self, sentiment_data: Dict[str, Any]) -> str:
        """Step 6: Generate final comprehensive report"""
        try:
            logger.info("Starting comprehensive report generation")
            
            # Create report agent
            agent = create_report_agent()
            
            # Compile all data for the report
            all_data = {
                'flow_id': self.flow_id,
                'flow_state': self.flow_state,
                'sentiment_data': sentiment_data,
                'execution_summary': {
                    'start_time': self.flow_state['start_time'],
                    'end_time': datetime.now().isoformat(),
                    'errors_count': len(self.flow_state['errors']),
                    'charts_created': len(self.flow_state['charts_created']),
                    'status': 'success' if not self.flow_state['errors'] else 'completed_with_errors'
                }
            }
            
            task = Task(
                description=f"""Generate a comprehensive insider trading analysis report using all collected data:
                
                EXECUTIVE SUMMARY REQUIREMENTS:
                - Key findings from 24-hour vs weekly comparison
                - Most active insiders and companies
                - Notable transactions and patterns
                - Market sentiment correlation
                - Investment implications and recommendations
                
                DETAILED ANALYSIS SECTIONS:
                1. Data Collection Summary
                2. 24-Hour Activity Analysis
                3. Weekly Baseline Comparison
                4. Most Active Insiders by Volume/Value
                5. Chart Analysis and Visual Insights
                6. Sentiment Analysis and Market Context
                7. Risk Assessment and Anomalies
                8. Investment Recommendations
                9. Methodology and Data Sources
                
                ALL COLLECTED DATA:
                {json.dumps(all_data, indent=2, default=str)}
                
                Create a professional, actionable report that highlights the most significant insider trading activity and its implications.
                """,
                expected_output="Complete professional insider trading analysis report with executive summary, detailed analysis, and actionable recommendations",
                agent=agent
            )
            
            crew = Crew(agents=[agent], tasks=[task], verbose=True)
            result = crew.kickoff()
            
            # Save the final report
            report_filename = f'reports/comprehensive_insider_trading_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write(f"SEC Insider Trading Analysis Report\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Flow ID: {self.flow_id}\n")
                f.write("=" * 80 + "\n\n")
                f.write(str(result.raw))
                f.write("\n\n" + "=" * 80 + "\n")
                f.write(f"Execution Summary:\n")
                f.write(f"- Start Time: {self.flow_state['start_time']}\n")
                f.write(f"- End Time: {datetime.now().isoformat()}\n")
                f.write(f"- Charts Created: {len(self.flow_state['charts_created'])}\n")
                f.write(f"- Errors: {len(self.flow_state['errors'])}\n")
                if self.flow_state['errors']:
                    f.write(f"- Error Details: {self.flow_state['errors']}\n")
            
            logger.info(f"Comprehensive report saved to: {report_filename}")
            
            final_result = {
                'report': result.raw,
                'report_file': report_filename,
                'flow_summary': all_data['execution_summary'],
                'status': 'completed'
            }
            
            return json.dumps(final_result, indent=2)
            
        except Exception as e:
            error_msg = f"Error in report generation: {str(e)}"
            logger.error(error_msg)
            self.flow_state['errors'].append(error_msg)
            return json.dumps({
                'report': f"Error generating report: {error_msg}",
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            })


# Guardrails and Error Handling
class FlowGuardrails:
    """Guardrails for the insider trading flow"""
    
    @staticmethod
    def validate_sec_data(data: Dict) -> bool:
        """Validate SEC data structure"""
        required_fields = ['recent_filings', 'data_source', 'timestamp']
        return all(field in data for field in required_fields)
    
    @staticmethod
    def validate_filing(filing: Dict) -> bool:
        """Validate individual filing data"""
        required_fields = ['company', 'insider', 'transaction', 'shares']
        return all(field in filing for field in required_fields)
    
    @staticmethod
    def sanitize_company_name(company: str) -> str:
        """Sanitize company name for analysis"""
        if not company or not isinstance(company, str):
            return 'UNKNOWN'
        return company.strip().upper()[:10]  # Limit length and standardize
    
    @staticmethod
    def validate_flow_state(flow_state: Dict) -> List[str]:
        """Validate flow state and return any issues"""
        issues = []
        
        if not flow_state.get('start_time'):
            issues.append('Missing start_time in flow state')
            
        if flow_state.get('errors') and len(flow_state['errors']) > 5:
            issues.append('Too many errors in flow execution')
            
        return issues

# Utility function to run the flow
def run_insider_trading_analysis():
    """Run the complete insider trading analysis flow"""
    try:
        logger.info("Starting Insider Trading Analysis Flow")
        flow = InsiderTradingFlow()
        result = flow.kickoff()
        logger.info("Flow completed successfully")
        return result
    except Exception as e:
        logger.error(f"Flow execution failed: {str(e)}")
        raise