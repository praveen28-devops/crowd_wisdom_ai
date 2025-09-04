# agents/sentiment_agent.py
from crewai import Agent
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

def create_sentiment_analysis_agent():
    """Agent to perform sentiment analysis on 10-X creators content"""
    llm = ChatGroq(
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant"
    )
    
    return Agent(
        role="Sentiment Analysis Specialist",
        goal="Analyze sentiment from 10-X creators content including news, social media, and filings",
        backstory="""You are a sentiment analysis expert who specializes in analyzing
        textual data related to financial markets and insider trading. You can process
        news articles, social media posts, YouTube transcripts, and SEC filings to
        extract sentiment insights that correlate with insider trading activity.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

def create_social_media_agent():
    """Agent to gather and analyze social media content"""
    llm = ChatGroq(
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant"
    )
    
    return Agent(
        role="Social Media Content Analyst",
        goal="Gather and analyze social media content from X (Twitter) and YouTube related to insider trading",
        backstory="""You are a social media analyst who specializes in gathering
        relevant content from platforms like X (Twitter) and YouTube. You can extract
        transcripts, posts, and discussions related to insider trading and financial
        markets to provide context for sentiment analysis.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

def create_news_sentiment_agent():
    """Agent for analyzing financial news sentiment"""
    llm = ChatGroq(
        temperature=0.1,
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant"
    )
    
    return Agent(
        role="Financial News Analyst",
        goal="Analyze sentiment from financial news sources and correlate with insider trading activity",
        backstory="""You are a financial journalism expert who specializes in analyzing
        news sentiment and its impact on stock performance. You monitor major financial
        news outlets, press releases, and analyst reports to gauge market sentiment
        around companies with significant insider trading activity. You understand how
        news cycles affect investor behavior and can identify sentiment trends that
        may predict or explain insider trading patterns.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
