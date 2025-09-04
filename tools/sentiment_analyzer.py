# tools/sentiment_analyzer.py
import os
import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import feedparser
from crewai.tools import tool
import tweepy
from youtube_transcript_api import YouTubeTranscriptApi
import re
from dotenv import load_dotenv

load_dotenv()

class SentimentAnalyzer:
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.twitter_api = self._setup_twitter_api()
        
    def _setup_twitter_api(self):
        """Setup Twitter API if credentials are available"""
        try:
            api_key = os.getenv('TWITTER_API_KEY')
            api_secret = os.getenv('TWITTER_API_SECRET')
            access_token = os.getenv('TWITTER_ACCESS_TOKEN')
            access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            
            if all([api_key, api_secret, access_token, access_token_secret]):
                auth = tweepy.OAuthHandler(api_key, api_secret)
                auth.set_access_token(access_token, access_token_secret)
                return tweepy.API(auth, wait_on_rate_limit=True)
        except Exception as e:
            print(f"Twitter API setup failed: {e}")
        return None
    
    def analyze_text_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of text using multiple methods"""
        # TextBlob analysis
        blob = TextBlob(text)
        textblob_sentiment = {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }
        
        # VADER analysis
        vader_scores = self.vader_analyzer.polarity_scores(text)
        
        # Combined analysis
        combined_score = (textblob_sentiment['polarity'] + vader_scores['compound']) / 2
        
        if combined_score >= 0.1:
            sentiment_label = 'positive'
        elif combined_score <= -0.1:
            sentiment_label = 'negative'
        else:
            sentiment_label = 'neutral'
            
        return {
            'text': text[:200] + "..." if len(text) > 200 else text,
            'textblob': textblob_sentiment,
            'vader': vader_scores,
            'combined_score': combined_score,
            'sentiment': sentiment_label,
            'confidence': abs(combined_score)
        }
    
    def get_financial_news_sentiment(self, companies: List[str]) -> List[Dict]:
        """Get sentiment from financial news for given companies"""
        news_sentiment = []
        
        try:
            # Use RSS feeds from financial news sources
            rss_feeds = [
                'https://feeds.finance.yahoo.com/rss/2.0/headline',
                'https://www.reuters.com/business/finance/rss',
                'https://www.marketwatch.com/rss/topstories'
            ]
            
            for feed_url in rss_feeds:
                try:
                    feed = feedparser.parse(feed_url)
                    
                    for entry in feed.entries[:10]:  # Limit to recent entries
                        title = entry.get('title', '')
                        description = entry.get('description', '')
                        content = f"{title} {description}"
                        
                        # Check if any company is mentioned
                        mentioned_companies = [comp for comp in companies 
                                             if comp.upper() in content.upper()]
                        
                        if mentioned_companies:
                            sentiment = self.analyze_text_sentiment(content)
                            sentiment['source'] = 'financial_news'
                            sentiment['companies'] = mentioned_companies
                            sentiment['url'] = entry.get('link', '')
                            sentiment['published'] = entry.get('published', '')
                            news_sentiment.append(sentiment)
                            
                except Exception as e:
                    print(f"Error processing feed {feed_url}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error fetching financial news: {e}")
            
        return news_sentiment
    
    def get_twitter_sentiment(self, companies: List[str]) -> List[Dict]:
        """Get sentiment from Twitter/X posts about companies"""
        twitter_sentiment = []
        
        if not self.twitter_api:
            print("Twitter API not configured, skipping Twitter sentiment analysis")
            return []
            
        try:
            for company in companies[:5]:  # Limit companies to avoid rate limits
                query = f"${company} OR {company} insider trading -RT"
                
                try:
                    tweets = tweepy.Cursor(self.twitter_api.search_tweets,
                                         q=query,
                                         lang="en",
                                         result_type="recent",
                                         tweet_mode="extended").items(20)
                    
                    for tweet in tweets:
                        sentiment = self.analyze_text_sentiment(tweet.full_text)
                        sentiment['source'] = 'twitter'
                        sentiment['company'] = company
                        sentiment['tweet_id'] = tweet.id
                        sentiment['created_at'] = tweet.created_at.isoformat()
                        sentiment['user'] = tweet.user.screen_name
                        twitter_sentiment.append(sentiment)
                        
                except Exception as e:
                    print(f"Error fetching tweets for {company}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error in Twitter sentiment analysis: {e}")
            
        return twitter_sentiment
    
    def get_youtube_sentiment(self, search_terms: List[str]) -> List[Dict]:
        """Get sentiment from YouTube video transcripts"""
        youtube_sentiment = []
        
        try:
            # This is a simplified implementation
            # In practice, you'd need YouTube Data API to search for videos
            # and then get transcripts
            
            # Sample implementation for demonstration
            sample_video_ids = ['dQw4w9WgXcQ']  # Replace with actual video IDs
            
            for video_id in sample_video_ids:
                try:
                    transcript = YouTubeTranscriptApi.get_transcript(video_id)
                    
                    # Combine transcript text
                    full_text = ' '.join([entry['text'] for entry in transcript])
                    
                    # Check if search terms are mentioned
                    mentioned_terms = [term for term in search_terms 
                                     if term.upper() in full_text.upper()]
                    
                    if mentioned_terms:
                        sentiment = self.analyze_text_sentiment(full_text)
                        sentiment['source'] = 'youtube'
                        sentiment['video_id'] = video_id
                        sentiment['mentioned_terms'] = mentioned_terms
                        youtube_sentiment.append(sentiment)
                        
                except Exception as e:
                    print(f"Error processing YouTube video {video_id}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error in YouTube sentiment analysis: {e}")
            
        return youtube_sentiment
    
    def get_social_media_sentiment(self, companies: List[str]) -> List[Dict]:
        """Aggregate sentiment from all social media sources"""
        all_sentiment = []
        
        # Get Twitter sentiment
        twitter_data = self.get_twitter_sentiment(companies)
        all_sentiment.extend(twitter_data)
        
        # Get YouTube sentiment
        youtube_data = self.get_youtube_sentiment(companies)
        all_sentiment.extend(youtube_data)
        
        return all_sentiment

@tool("Sentiment Analysis Tool")
def analyze_market_sentiment(companies_json: str) -> str:
    """
    Analyze sentiment from multiple sources for given companies.
    Input should be JSON string with list of company tickers.
    """
    try:
        companies = json.loads(companies_json) if isinstance(companies_json, str) else companies_json
        
        if isinstance(companies, dict):
            companies = companies.get('companies', [])
        elif not isinstance(companies, list):
            companies = [str(companies)]
            
        analyzer = SentimentAnalyzer()
        
        # Collect sentiment from multiple sources
        all_sentiment = []
        
        # Financial news sentiment
        news_sentiment = analyzer.get_financial_news_sentiment(companies)
        all_sentiment.extend(news_sentiment)
        
        # Twitter sentiment
        twitter_sentiment = analyzer.get_twitter_sentiment(companies)
        all_sentiment.extend(twitter_sentiment)
        
        # YouTube sentiment
        youtube_sentiment = analyzer.get_youtube_sentiment(companies)
        all_sentiment.extend(youtube_sentiment)
        
        # Aggregate results
        if not all_sentiment:
            return json.dumps({
                'companies': companies,
                'total_mentions': 0,
                'overall_sentiment': 'neutral',
                'sentiment_breakdown': {},
                'message': 'No sentiment data found for the given companies'
            })
        
        # Calculate overall sentiment
        positive_count = sum(1 for s in all_sentiment if s['sentiment'] == 'positive')
        negative_count = sum(1 for s in all_sentiment if s['sentiment'] == 'negative')
        neutral_count = sum(1 for s in all_sentiment if s['sentiment'] == 'neutral')
        
        total_mentions = len(all_sentiment)
        
        if positive_count > negative_count:
            overall_sentiment = 'positive'
        elif negative_count > positive_count:
            overall_sentiment = 'negative'
        else:
            overall_sentiment = 'neutral'
        
        # Source breakdown
        source_breakdown = {}
        for sentiment in all_sentiment:
            source = sentiment['source']
            if source not in source_breakdown:
                source_breakdown[source] = {'positive': 0, 'negative': 0, 'neutral': 0}
            source_breakdown[source][sentiment['sentiment']] += 1
        
        result = {
            'companies': companies,
            'total_mentions': total_mentions,
            'overall_sentiment': overall_sentiment,
            'sentiment_breakdown': {
                'positive': positive_count,
                'negative': negative_count,
                'neutral': neutral_count
            },
            'source_breakdown': source_breakdown,
            'detailed_sentiment': all_sentiment[:10],  # Top 10 for brevity
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({
            'error': f"Sentiment analysis failed: {str(e)}",
            'companies': companies if 'companies' in locals() else [],
            'timestamp': datetime.now().isoformat()
        })

@tool("Social Media Content Gatherer")
def gather_social_content(search_terms_json: str) -> str:
    """
    Gather content from social media platforms for sentiment analysis.
    """
    try:
        search_terms = json.loads(search_terms_json) if isinstance(search_terms_json, str) else search_terms_json
        
        analyzer = SentimentAnalyzer()
        
        # Gather content from multiple sources
        content = {
            'twitter_content': analyzer.get_twitter_sentiment(search_terms),
            'youtube_content': analyzer.get_youtube_sentiment(search_terms),
            'news_content': analyzer.get_financial_news_sentiment(search_terms),
            'collection_timestamp': datetime.now().isoformat(),
            'search_terms': search_terms
        }
        
        return json.dumps(content, indent=2)
        
    except Exception as e:
        return json.dumps({
            'error': f"Content gathering failed: {str(e)}",
            'timestamp': datetime.now().isoformat()
        })
