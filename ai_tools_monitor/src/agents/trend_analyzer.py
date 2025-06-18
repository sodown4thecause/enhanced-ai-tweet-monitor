import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import API, APIChange
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import openai

class TrendAnalyzer:
    def __init__(self, db: Session, config: Dict[str, Any]):
        self.db = db
        self.config = config
        self.setup_logging()
        self.setup_openai()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename='trend_analyzer.log'
        )
        self.logger = logging.getLogger('TrendAnalyzer')

    def setup_openai(self):
        """Initialize OpenAI client."""
        openai.api_key = self.config['openai_api_key']

    def get_recent_tools(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get tools discovered in the last N days."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        tools = self.db.query(API).filter(API.discovered_at >= cutoff_date).all()
        return [tool.to_dict() for tool in tools]

    def analyze_category_trends(self, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze trends in tool categories."""
        try:
            # Count categories
            all_categories = []
            for tool in tools:
                if 'categories' in tool and tool['categories']:
                    all_categories.extend(tool['categories'])
            
            category_counts = Counter(all_categories)
            
            # Calculate growth rate
            previous_tools = self.get_recent_tools(days=14)  # Get tools from previous week
            previous_categories = []
            for tool in previous_tools:
                if 'categories' in tool and tool['categories']:
                    previous_categories.extend(tool['categories'])
            
            previous_counts = Counter(previous_categories)
            
            # Calculate growth rates
            growth_rates = {}
            for category in category_counts:
                prev_count = previous_counts.get(category, 0)
                current_count = category_counts[category]
                if prev_count > 0:
                    growth_rate = (current_count - prev_count) / prev_count * 100
                else:
                    growth_rate = float('inf')
                growth_rates[category] = growth_rate
            
            return {
                'category_counts': dict(category_counts),
                'growth_rates': growth_rates,
                'top_categories': category_counts.most_common(5)
            }
        except Exception as e:
            self.logger.error(f"Error analyzing category trends: {str(e)}")
            return {}

    def cluster_similar_tools(self, tools: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """Cluster similar tools using text similarity."""
        try:
            # Prepare text data
            texts = [f"{tool['name']} {tool['description']}" for tool in tools]
            
            # Create TF-IDF vectors
            vectorizer = TfidfVectorizer(stop_words='english')
            X = vectorizer.fit_transform(texts)
            
            # Perform clustering
            clustering = DBSCAN(eps=0.3, min_samples=2, metric='cosine')
            clusters = clustering.fit_predict(X.toarray())
            
            # Group tools by cluster
            clustered_tools = {}
            for i, cluster_id in enumerate(clusters):
                if cluster_id not in clustered_tools:
                    clustered_tools[cluster_id] = []
                clustered_tools[cluster_id].append(tools[i])
            
            return list(clustered_tools.values())
        except Exception as e:
            self.logger.error(f"Error clustering tools: {str(e)}")
            return []

    def detect_spikes(self, tools: List[Dict[str, Any]], window_days: int = 3) -> List[Dict[str, Any]]:
        """Detect sudden spikes in tool launches."""
        try:
            # Convert to DataFrame for easier analysis
            df = pd.DataFrame(tools)
            df['discovered_at'] = pd.to_datetime(df['discovered_at'])
            
            # Group by date and count
            daily_counts = df.groupby(df['discovered_at'].dt.date).size()
            
            # Calculate rolling mean and std
            rolling_mean = daily_counts.rolling(window=window_days, center=True).mean()
            rolling_std = daily_counts.rolling(window=window_days, center=True).std()
            
            # Detect spikes (values more than 2 standard deviations above mean)
            spikes = daily_counts[daily_counts > (rolling_mean + 2 * rolling_std)]
            
            # Get tools from spike days
            spike_tools = []
            for date in spikes.index:
                day_tools = df[df['discovered_at'].dt.date == date]
                spike_tools.append({
                    'date': date,
                    'count': len(day_tools),
                    'tools': day_tools.to_dict('records')
                })
            
            return spike_tools
        except Exception as e:
            self.logger.error(f"Error detecting spikes: {str(e)}")
            return []

    def generate_trend_report(self, tools: List[Dict[str, Any]]) -> str:
        """Generate a human-readable trend report using OpenAI."""
        try:
            # Prepare trend data
            category_trends = self.analyze_category_trends(tools)
            clusters = self.cluster_similar_tools(tools)
            spikes = self.detect_spikes(tools)
            
            # Format data for GPT
            prompt = f"""
            Analyze these AI tool trends and generate a concise report:
            
            Category Trends:
            {category_trends}
            
            Similar Tool Clusters:
            {clusters}
            
            Launch Spikes:
            {spikes}
            
            Generate a report highlighting the most interesting trends and patterns.
            """
            
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI trend analyst. Generate concise, insightful reports about AI tool trends."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            self.logger.error(f"Error generating trend report: {str(e)}")
            return "Error generating trend report"

    def analyze_trends(self) -> Dict[str, Any]:
        """Main method to analyze all trends."""
        try:
            # Get recent tools
            tools = self.get_recent_tools()
            
            # Perform analyses
            category_trends = self.analyze_category_trends(tools)
            clusters = self.cluster_similar_tools(tools)
            spikes = self.detect_spikes(tools)
            trend_report = self.generate_trend_report(tools)
            
            return {
                'category_trends': category_trends,
                'similar_tool_clusters': clusters,
                'launch_spikes': spikes,
                'trend_report': trend_report,
                'analysis_date': datetime.utcnow()
            }
        except Exception as e:
            self.logger.error(f"Error in trend analysis: {str(e)}")
            return {} 