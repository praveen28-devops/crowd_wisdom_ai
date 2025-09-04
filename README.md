🏢 SEC Insider Trading Analyzer

An advanced, production-ready system that uses a multi-agent AI crew to analyze SEC insider trading filings, providing comprehensive reports and actionable insights.

This project retrieves live data from SEC EDGAR, processes it through specialized AI agents for sentiment analysis and data comparison, generates professional charts, and compiles a detailed executive report.

✅ Key Features

    Live SEC Data: Fetches Form 4 insider trading filings from the last 24 hours and the past week for true comparative analysis.

    Agent-Driven Workflow: A modular crew of AI agents, each specializing in a single task like data scraping, sentiment analysis, chart generation, or report writing.

    Advanced Sentiment Analysis: Gathers insights from financial news, social media (Twitter/X), and financial YouTube creator content to gauge market sentiment.

    Professional Visualizations: Automatically generates comparative bar charts and interactive Plotly dashboards to visualize trading volume and transaction types.

    Robust & Resilient: Features comprehensive logging, error handling with safe fallbacks, and retry logic for API rate limits.

    Automated Reporting: Produces detailed executive summaries, highlights risk flags, and delivers actionable signals in a clean, readable format.

🚀 Getting Started

Follow these steps to get the SEC Insider Trading Analyzer up and running on your local machine.

Prerequisites

    Python 3.8 or higher

    A Groq API Key (available for free from GroqCloud)

    An active internet connection to fetch live SEC data

1. Installation

First, clone the repository and navigate into the project directory.
Bash

git clone https://github.com/your-username/crewai-sec-analyzer.git
cd crewai-sec-analyzer

Next, create and activate a Python virtual environment.
Bash

# Create the virtual environment
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate

Finally, install all the required dependencies.
Bash

pip install -r requirements.txt

2. Configuration

You need to configure your API keys and a contact email for SEC compliance.

    Create a .env file by copying the example file.
    Bash

cp .env.example .env

Open the new .env file and add your credentials.
Plaintext

    # Required for the AI agents to function
    GROQ_API_KEY="gsk_your_groq_api_key_here"

    # Required by the SEC EDGAR API for identification
    CONTACT_EMAIL="your-email@example.com"

    # Optional: For enhanced sentiment analysis
    TWITTER_API_KEY="your_twitter_key"
    TWITTER_API_SECRET="your_twitter_secret"
    YOUTUBE_API_KEY="your_youtube_api_key"

    # Optional: Set logging level (e.g., INFO, DEBUG)
    LOG_LEVEL="INFO"

⚙️ Usage

The analyzer can be run in several modes depending on your needs. All generated outputs, including charts, logs, and reports, will be saved in the /reports directory.

Comprehensive Demo

This is the recommended first step. It runs the entire pipeline using sample data to validate all features and agents without making live API calls.
Bash

python demo_comprehensive.py

Quick Test

Runs a simplified, minimal version of the pipeline with live data. Ideal for a quick end-to-end test.
Bash

python simplified_main.py

Full Production Analysis

Executes the complete, production-grade analysis. It fetches live 24-hour and 7-day data from the SEC, performs full sentiment analysis, and generates a comprehensive report.
Bash

python main.py

🏗️ Project Structure

The project is organized into modular directories, each with a specific responsibility.

    📄 main.py / demo_*.py: The main entry points for running different analysis flows.

    agents/: Contains the definitions for each specialized AI agent (e.g., sec_data_agent, sentiment_agent, report_agent).

    tools/: Includes utility functions and classes for data scraping, API interaction, chart generation, and sentiment analysis.

    flows/: Orchestrates the entire workflow, defining the sequence of tasks and the crew of agents that will execute them.

    reports/: The output directory where all generated files (logs, charts, JSON data, and the final text report) are saved.

    data/: Stores sample data used for demos and fallback scenarios when live APIs are unavailable.

📄 License

This project is licensed under the MIT License. See the LICENSE file for more details.
