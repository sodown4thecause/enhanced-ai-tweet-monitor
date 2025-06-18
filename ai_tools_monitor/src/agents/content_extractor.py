import logging
from typing import List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import API, APIChange
import openai
from bs4 import BeautifulSoup
import re

class ContentExtractor:
    def __init__(self, db: Session, config: Dict[str, Any]):
        self.db = db
        self.config = config
        self.setup_logging()
        self.setup_openai()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename='content_extractor.log'
        )
        self.logger = logging.getLogger('ContentExtractor')

    def setup_openai(self):
        """Initialize OpenAI client."""
        openai.api_key = self.config['openai_api_key']

    def clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove HTML tags
        text = BeautifulSoup(text, 'html.parser').get_text()
        
        # Remove special characters
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        
        return text.strip()

    def extract_categories(self, text: str) -> List[str]:
        """Extract categories from text using OpenAI."""
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts AI tool categories from text. Return only a comma-separated list of categories."},
                    {"role": "user", "content": f"Extract AI tool categories from this text: {text}"}
                ],
                temperature=0.3,
                max_tokens=100
            )
            
            categories = response.choices[0].message.content.strip().split(',')
            return [cat.strip() for cat in categories if cat.strip()]
        except Exception as e:
            self.logger.error(f"Error extracting categories: {str(e)}")
            return []

    def extract_pricing(self, text: str) -> Dict[str, Any]:
        """Extract pricing information from text using OpenAI."""
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts pricing information from text. Return a JSON object with 'model', 'price', and 'currency' fields."},
                    {"role": "user", "content": f"Extract pricing information from this text: {text}"}
                ],
                temperature=0.3,
                max_tokens=150
            )
            
            pricing_info = response.choices[0].message.content.strip()
            # Parse the JSON response
            import json
            return json.loads(pricing_info)
        except Exception as e:
            self.logger.error(f"Error extracting pricing: {str(e)}")
            return {}

    def summarize_description(self, text: str) -> str:
        """Summarize tool description using OpenAI."""
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes AI tool descriptions. Keep it concise and informative."},
                    {"role": "user", "content": f"Summarize this AI tool description: {text}"}
                ],
                temperature=0.3,
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            self.logger.error(f"Error summarizing description: {str(e)}")
            return text[:200] + "..."  # Fallback to truncation

    def process_tool(self, tool: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single tool's data."""
        try:
            # Clean basic fields
            tool['name'] = self.clean_text(tool['name'])
            tool['description'] = self.clean_text(tool['description'])
            
            # Extract additional information
            tool['categories'] = self.extract_categories(tool['description'])
            tool['pricing'] = self.extract_pricing(tool['description'])
            tool['summary'] = self.summarize_description(tool['description'])
            
            # Extract launch date if available
            if 'raw_data' in tool:
                raw_data = tool['raw_data']
                if isinstance(raw_data, dict):
                    if 'created_at' in raw_data:
                        tool['launch_date'] = raw_data['created_at']
                    elif 'created_utc' in raw_data:
                        tool['launch_date'] = datetime.fromtimestamp(raw_data['created_utc'])
            
            return tool
        except Exception as e:
            self.logger.error(f"Error processing tool {tool.get('name', 'unknown')}: {str(e)}")
            return tool

    def process_all_tools(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process all tools and update database."""
        processed_tools = []
        
        for tool in tools:
            try:
                processed_tool = self.process_tool(tool)
                
                # Update database
                existing_tool = self.db.query(API).filter_by(url=tool['url']).first()
                if existing_tool:
                    # Check for significant changes
                    changes = []
                    for key, value in processed_tool.items():
                        if hasattr(existing_tool, key) and getattr(existing_tool, key) != value:
                            changes.append({
                                'field': key,
                                'old_value': getattr(existing_tool, key),
                                'new_value': value
                            })
                            setattr(existing_tool, key, value)
                    
                    # Record changes if any
                    if changes:
                        change_record = APIChange(
                            api_id=existing_tool.id,
                            changes=changes,
                            changed_at=datetime.utcnow()
                        )
                        self.db.add(change_record)
                else:
                    # Create new tool
                    new_tool = API(**processed_tool)
                    self.db.add(new_tool)
                
                self.db.commit()
                processed_tools.append(processed_tool)
                
            except Exception as e:
                self.logger.error(f"Error processing tool {tool.get('name', 'unknown')}: {str(e)}")
                self.db.rollback()
        
        return processed_tools 