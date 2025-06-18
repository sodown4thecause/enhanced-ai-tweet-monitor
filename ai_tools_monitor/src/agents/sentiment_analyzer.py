import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models import API, APIChange
import openai
from textblob import TextBlob
import numpy as np
from collections import defaultdict

class SentimentAnalyzer:
    def __init__(self, db: Session, config: Dict[str, Any]):
        self.db = db
        self.config = config
        self.setup_logging()
        self.setup_openai()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename='sentiment_analyzer.log'
        )
        self.logger = logging.getLogger('SentimentAnalyzer')

    def setup_openai(self):
        """Initialize OpenAI client."""
        openai.api_key = self.config['openai_api_key']

    def analyze_text_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of text using TextBlob."""
        try:
            blob = TextBlob(text)
            return {
                'polarity': blob.sentiment.polarity,  # -1 to 1
                'subjectivity': blob.sentiment.subjectivity  # 0 to 1
            }
        except Exception as e:
            self.logger.error(f"Error analyzing text sentiment: {str(e)}")
            return {'polarity': 0, 'subjectivity': 0}

    def analyze_social_metrics(self, tool: Dict[str, Any]) -> Dict[str, float]:
        """Analyze social media metrics for a tool."""
        try:
            metrics = {
                'engagement_score': 0.0,
                'hype_score': 0.0
            }
            
            if 'raw_data' in tool:
                raw_data = tool['raw_data']
                
                # Twitter metrics
                if 'metrics' in raw_data:
                    twitter_metrics = raw_data['metrics']
                    metrics['engagement_score'] += (
                        twitter_metrics.get('retweet_count', 0) * 0.3 +
                        twitter_metrics.get('reply_count', 0) * 0.2 +
                        twitter_metrics.get('like_count', 0) * 0.5
                    ) / 1000  # Normalize
                
                # Reddit metrics
                if 'score' in raw_data and 'num_comments' in raw_data:
                    metrics['engagement_score'] += (
                        raw_data['score'] * 0.6 +
                        raw_data['num_comments'] * 0.4
                    ) / 1000  # Normalize
                
                # Product Hunt metrics
                if 'votes_count' in raw_data:
                    metrics['engagement_score'] += raw_data['votes_count'] / 1000
            
            return metrics
        except Exception as e:
            self.logger.error(f"Error analyzing social metrics: {str(e)}")
            return {'engagement_score': 0.0, 'hype_score': 0.0}

    def calculate_hype_score(self, tool: Dict[str, Any]) -> float:
        """Calculate overall hype score for a tool."""
        try:
            # Get sentiment scores
            sentiment = self.analyze_text_sentiment(tool['description'])
            
            # Get social metrics
            social_metrics = self.analyze_social_metrics(tool)
            
            # Calculate hype score (weighted combination)
            hype_score = (
                sentiment['polarity'] * 0.3 +
                sentiment['subjectivity'] * 0.2 +
                social_metrics['engagement_score'] * 0.5
            )
            
            # Normalize to 0-1 range
            hype_score = (hype_score + 1) / 2
            
            return hype_score
        except Exception as e:
            self.logger.error(f"Error calculating hype score: {str(e)}")
            return 0.0

    def analyze_competitor_sentiment(self, tool: Dict[str, Any], competitors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze sentiment and positioning relative to competitors."""
        try:
            # Get tool's sentiment
            tool_sentiment = self.analyze_text_sentiment(tool['description'])
            
            # Get competitor sentiments
            competitor_sentiments = []
            for competitor in competitors:
                sentiment = self.analyze_text_sentiment(competitor['description'])
                competitor_sentiments.append(sentiment)
            
            # Calculate average competitor sentiment
            avg_competitor_polarity = np.mean([s['polarity'] for s in competitor_sentiments])
            avg_competitor_subjectivity = np.mean([s['subjectivity'] for s in competitor_sentiments])
            
            return {
                'tool_sentiment': tool_sentiment,
                'competitor_sentiment': {
                    'avg_polarity': avg_competitor_polarity,
                    'avg_subjectivity': avg_competitor_subjectivity
                },
                'sentiment_difference': {
                    'polarity': tool_sentiment['polarity'] - avg_competitor_polarity,
                    'subjectivity': tool_sentiment['subjectivity'] - avg_competitor_subjectivity
                }
            }
        except Exception as e:
            self.logger.error(f"Error analyzing competitor sentiment: {str(e)}")
            return {}

    def generate_sentiment_report(self, tool: Dict[str, Any], competitors: List[Dict[str, Any]]) -> str:
        """Generate a human-readable sentiment report using OpenAI."""
        try:
            # Get sentiment analysis
            sentiment = self.analyze_text_sentiment(tool['description'])
            social_metrics = self.analyze_social_metrics(tool)
            hype_score = self.calculate_hype_score(tool)
            competitor_analysis = self.analyze_competitor_sentiment(tool, competitors)
            
            # Format data for GPT
            prompt = f"""
            Analyze this AI tool's sentiment and hype:
            
            Tool: {tool['name']}
            Description: {tool['description']}
            
            Sentiment Analysis:
            - Polarity: {sentiment['polarity']}
            - Subjectivity: {sentiment['subjectivity']}
            
            Social Metrics:
            - Engagement Score: {social_metrics['engagement_score']}
            - Hype Score: {hype_score}
            
            Competitor Analysis:
            {competitor_analysis}
            
            Generate a concise report about the tool's market positioning and hype level.
            """
            
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI market analyst. Generate concise, insightful reports about AI tool sentiment and hype."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            self.logger.error(f"Error generating sentiment report: {str(e)}")
            return "Error generating sentiment report"

    def analyze_tool_sentiment(self, tool: Dict[str, Any], competitors: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Main method to analyze sentiment and hype for a tool."""
        try:
            if competitors is None:
                competitors = []
            
            sentiment = self.analyze_text_sentiment(tool['description'])
            social_metrics = self.analyze_social_metrics(tool)
            hype_score = self.calculate_hype_score(tool)
            competitor_analysis = self.analyze_competitor_sentiment(tool, competitors)
            sentiment_report = self.generate_sentiment_report(tool, competitors)
            
            return {
                'sentiment': sentiment,
                'social_metrics': social_metrics,
                'hype_score': hype_score,
                'competitor_analysis': competitor_analysis,
                'sentiment_report': sentiment_report,
                'analysis_date': datetime.utcnow()
            }
        except Exception as e:
            self.logger.error(f"Error in sentiment analysis: {str(e)}")
            return {} 