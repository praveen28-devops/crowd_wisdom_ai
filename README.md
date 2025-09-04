SEC Insider Trading Analyzer

🏢 A Production-Ready CrewAI-Based System for SEC Insider Trading Analysis

[![Python](https://img.shields.io/badge/PythonAIAI's modern multi-agent flow to deliver actionable insights and comprehensive executive reporting on SEC insider trading activity.

    Live SEC EDGAR data retrieval (24hr + weekly for true comparison)

    Agent-driven data processing: Each agent specializes in a single task

    Visualization: Comparative and interactive charts

    Sentiment analysis: Financial news, social media, and creator content

    Error-tolerant workflow: Robust logging, retry logic, and safe fallback

    Report automation: Executive summaries, ranking, and recommendations

    All pure Python — no Docker required

🚀 Quick Start
Prerequisites

    Python 3.8+

    Groq API key (free)

    Internet connection for live SEC data

Installation

    Clone and set up environment:

bash
git clone <repository-url>
cd crewai-sec-analyzer
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

bash
pip install -r requirements.txt

Configure environment variables:

bash
cp .env.example .env
# Then edit .env with your Groq API and contact email for SEC API compliance

Run demo or production analysis:

    bash
    # To run a full validation demo (all features)
    python demo_comprehensive.py
    # For full production analysis
    python crowdwisdom_complete.py
    # For a quick simplified test
    python simplified_main.py

🔧 Configuration

Required environment variables in your .env file:

text
GROQ_API_KEY="gsk_your_groq_api_key_here"
CONTACT_EMAIL="your-email@company.com"  # Required for SEC API compliance

Optional variables for sentiment (Twitter, YouTube):

text
TWITTER_API_KEY="your_twitter_key"
TWITTER_API_SECRET="your_twitter_secret"
TWITTER_ACCESS_TOKEN="your_access_token"
TWITTER_ACCESS_TOKEN_SECRET="your_access_token_secret"
YOUTUBE_API_KEY="your_youtube_api_key"
LOG_LEVEL="INFO"

🏗️ Architecture

text
┌─────────────────────────────────────────────┐
│          CrewAI Flow Orchestration          │
├─────────────────────────────────────────────┤
│    📊 Data Agents        📈 Chart Agent      │
│   • 24hr SEC Data       • Comparative       │
│   • Weekly SEC Data     • Interactive       │
│   • Data Processing     • Visualizations    │
│   🎭 Sentiment Agents                       │
│   • Financial News      • Social Media      │
│   • YouTube Content                          │
│    📄 Report Agent                          │
└─────────────────────────────────────────────┘

Key directories:

    agents/ - Single-responsibility agents for each analysis step

    tools/ - Data scraping, charting, sentiment analysis utilities

    flows/ - Full CrewAI pipeline orchestration

    reports/ - All outputs (charts, logs, reports)

🔥 Features
1. SEC Data Retrieval

    Live insider trading from SEC EDGAR (Form 4, 24hr and 1-week scraping)

    Rate-limited, resilient interface with sample fallback

2. Modular Agents & CrewAI Flow

    Specialized agents for:

        Real-time data scraping

        Weekly baseline comparison

        Data normalization and aggregation

        Visual chart generation (matplotlib/plotly)

        Sentiment analysis (news, Twitter/X, YouTube transcripts)

        Comprehensive report writing

3. Professional Charting

    24hr vs weekly bar charts

    Transaction type and company ranking

    Interactive dashboards (Plotly, HTML)

4. Sentiment Analysis

    Financial news and press coverage

    Twitter/X public discussions

    YouTube transcripts (10X creators)

    Sentiment correlation with trading activity

5. Robust Reporting

    Multi-section text & markdown reports

    Executive summary, risk flags, actionable signals

    Files saved in reports/ with logs for every run

6. Production-Ready Logging

    Multi-level file and console logging

    Error capture and fallback for API failures and rate limits

📊 Sample Usage

Quick SEC Data Analysis

python
from tools.sec_scraper import get_live_sec_data
data_24hr = get_live_sec_data(24)
print(f"Filings in last 24h: {len(data_24hr['recent_filings'])}")

Basic Sentiment Analysis

python
from tools.sentiment_analyzer import analyze_market_sentiment
sentiment = analyze_market_sentiment(json.dumps(['AAPL', 'MSFT']))
print(sentiment)

Generate Charts

python
from tools.chart_generator import create_comparison_chart
# Compare two datasets for volume by company
chart_result = create_comparison_chart(data_24hr, data_weekly)
print(chart_result)

📂 Output Files

Generated in /reports/:

    crowdwisdom_final_

    report.txt - Main analysis and executive summary

    volume_comparison_chart.png - Comparative bar chart

    transaction_type_comparison.png - Transaction summary chart

    interactive_comparison.html - Interactive Plotly dashboard

    crowdwisdom_detailed.log - Complete execution log

    raw_sec_data.json - All SEC data for reproducibility

🛡️ Error Handling

    Data validation for API and format consistency

    Graceful fallback to sample data if live API unavailable

    Comprehensive logs for all pipeline steps

    Retry logic for API errors or rate limits

🧪 Testing

bash
python demo_comprehensive.py    # Validates all modules and agents
python simplified_main.py       # Minimal end-to-end pipeline

🎬 Demo & Contributions

For a full run-through, see demo_comprehensive.py.
To contribute: fork, create a branch, make your changes, add tests, and submit a pull request.
📄 License

MIT License — see the LICENSE file for details.

Built with ❤️ using CrewAI, Groq LLM, and the SEC EDGAR API
