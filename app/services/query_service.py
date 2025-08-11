import re
import logging
import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models.document import Document
from openai import OpenAI

from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain import hub
from langgraph.prebuilt import create_react_agent
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.database import get_db, get_langchain_db

load_dotenv()

logger = logging.getLogger(__name__)

class QueryService:
    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is not set")
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

    def process_query(self, question: str, db: Session) -> List[Dict[str, Any]]:
        """Process natural language query and return structured results"""
        try:
            prompt = (
                "Analyze the user's question to identify which category they are asking about and its value. "
                "Categories are: agreement_type (e.g., NDA, MSA), governing_law (e.g., UAE, UK), "
                "geography (e.g., Middle East, Europe), industry (e.g., Technology, Oil & Gas).\n\n"
                "Output a JSON with two fields:\n"
                "- filter: the category being asked about (must be exactly one of: agreement_type, governing_law, geography, industry)\n"
                "- value: the specific value mentioned for that category\n\n"
                "Example 1: 'Show me all documents from the Technology industry'\n"
                "Response: {\"filter\": \"industry\", \"value\": \"Technology\"}\n\n"
                "Example 2: 'What agreements are governed by UAE law?'\n"
                "Response: {\"filter\": \"governing_law\", \"value\": \"UAE\"}\n\n"
                "User question: " + question
            )
            response = self.client.chat.completions.create(
                model="anthropic/claude-3.7-sonnet:beta",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a legal document classifier that helps identify search criteria from user questions. "
                        "You analyze questions and determine which category (agreement_type, governing_law, geography, or industry) "
                        "is being asked about and what specific value is being searched for."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0
            )

            content = response.choices[0].message.content
            content = content.replace('```json', '').replace('```', '').strip()
            metadata = json.loads(content)
            return self._query_general(metadata['filter'], metadata['value'], db)
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return []
    
    def _query_general(self, filter: str, value: str, db: Session) -> List[Dict[str, Any]]:
        documents = db.query(Document).filter(getattr(Document, filter) == value).all()
        return self._format_results(documents)
    
    def _format_results(self, documents: List[Document]) -> List[Dict[str, Any]]:
        """Format document results for API response"""
        results = []

        for doc in documents:
            result = {
                'document': doc.filename,
                'governing_law': doc.governing_law,
                'agreement_type': doc.agreement_type,
                'industry': doc.industry,
                'geography': doc.geography
            }
            results.append(result)

        return results
