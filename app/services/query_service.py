import re
import logging
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models.document import Document

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
from app.models.database import get_db

load_dotenv()

logger = logging.getLogger(__name__)



class QueryService:
    """Service for handling natural language queries across documents"""
    def __init__(self, db: Session):
        self.db = db
        self.prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
        self.system_message = self.prompt_template.format(dialect="PostgreSQL", top_k=5) 
        self.model = "mistralai/codestral-2508"
        self.llm = ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENROUTER_API_KEY"),
                model=self.model,
            )
        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)


    def process_query(self, question: str) -> List[Dict[str, Any]]:
        """Process natural language query and return structured results"""
        try:
            self.tools = self.toolkit.get_tools()
            self.agent_executor = create_react_agent(
                llm=self.llm,
                toolkit=self.toolkit,
                system_message=self.system_message,
            )
            result = self.agent_executor.invoke({"input": question})
            return self._format_results(result['message'][-1])
                
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return []
    
    def _format_results(self, documents: List[Document]) -> List[Dict[str, Any]]:
        """Format document results for API response"""
        results = []
        
        for doc in documents:
            result = {
                'document': doc.filename,
                'governing_law': doc.governing_law,
                'agreement_type': doc.agreement_type,
                'industry': doc.industry,
                'jurisdiction': doc.jurisdiction,
                'geography': doc.geography
            }
            results.append(result)
        
        return results
