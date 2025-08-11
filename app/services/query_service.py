import re
import logging
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from ..models.document import Document

logger = logging.getLogger(__name__)

class QueryService:
    """Service for handling natural language queries across documents"""
    
    def __init__(self):
        # Query patterns for different types of questions
        self.query_patterns = {
            'jurisdiction': r'\b(?:which|what).*?(?:governed by|jurisdiction|law).*?(UAE|UK|US|Singapore|Hong Kong|Qatar|Saudi Arabia|Kuwait|Bahrain|Oman)\b',
            'agreement_type': r'\b(?:which|what).*?(?:NDA|MSA|Franchise|Employment|License|Service|Purchase|Lease)\b',
            'industry': r'\b(?:which|what).*?(?:technology|oil|gas|healthcare|finance|real estate|manufacturing|retail|transportation)\b',
            'geography': r'\b(?:which|what).*?(?:Middle East|Europe|Asia|North America|Africa|Australia)\b'
        }
    
    def process_query(self, question: str, db: Session) -> List[Dict[str, Any]]:
        """Process natural language query and return structured results"""
        try:
            # Determine query type
            query_type = self._determine_query_type(question)
            
            # Execute query based on type
            if query_type == 'jurisdiction':
                return self._query_by_jurisdiction(question, db)
            elif query_type == 'agreement_type':
                return self._query_by_agreement_type(question, db)
            elif query_type == 'industry':
                return self._query_by_industry(question, db)
            elif query_type == 'geography':
                return self._query_by_geography(question, db)
            else:
                # Default: search across all documents
                return self._query_general(question, db)
                
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return []
    
    def _determine_query_type(self, question: str) -> str:
        """Determine the type of query being asked"""
        question_lower = question.lower()
        
        for query_type, pattern in self.query_patterns.items():
            if re.search(pattern, question_lower, re.IGNORECASE):
                return query_type
        
        return 'general'
    
    def _query_by_jurisdiction(self, question: str, db: Session) -> List[Dict[str, Any]]:
        """Query documents by jurisdiction"""
        # Extract jurisdiction from question
        jurisdiction = self._extract_jurisdiction_from_question(question)
        
        if not jurisdiction:
            return []
        
        # Query database
        documents = db.query(Document).filter(
            or_(
                Document.governing_law == jurisdiction,
                Document.jurisdiction == jurisdiction
            )
        ).all()
        
        return self._format_results(documents)
    
    def _query_by_agreement_type(self, question: str, db: Session) -> List[Dict[str, Any]]:
        """Query documents by agreement type"""
        # Extract agreement type from question
        agreement_type = self._extract_agreement_type_from_question(question)
        
        if not agreement_type:
            return []
        
        # Query database
        documents = db.query(Document).filter(
            Document.agreement_type == agreement_type
        ).all()
        
        return self._format_results(documents)
    
    def _query_by_industry(self, question: str, db: Session) -> List[Dict[str, Any]]:
        """Query documents by industry"""
        # Extract industry from question
        industry = self._extract_industry_from_question(question)
        
        if not industry:
            return []
        
        # Query database
        documents = db.query(Document).filter(
            Document.industry == industry
        ).all()
        
        return self._format_results(documents)
    
    def _query_by_geography(self, question: str, db: Session) -> List[Dict[str, Any]]:
        """Query documents by geography"""
        # Extract geography from question
        geography = self._extract_geography_from_question(question)
        
        if not geography:
            return []
        
        # Query database
        documents = db.query(Document).filter(
            Document.geography == geography
        ).all()
        
        return self._format_results(documents)
    
    def _query_general(self, question: str, db: Session) -> List[Dict[str, Any]]:
        """General query across all documents"""
        # For now, return all documents
        # In production, this would use vector search or LLM
        documents = db.query(Document).all()
        return self._format_results(documents)
    
    def _extract_jurisdiction_from_question(self, question: str) -> str:
        """Extract jurisdiction from question"""
        jurisdictions = ['UAE', 'UK', 'US', 'Singapore', 'Hong Kong', 'Qatar', 'Saudi Arabia', 'Kuwait', 'Bahrain', 'Oman']
        question_lower = question.lower()
        
        for jurisdiction in jurisdictions:
            if jurisdiction.lower() in question_lower:
                return jurisdiction
        
        return None
    
    def _extract_agreement_type_from_question(self, question: str) -> str:
        """Extract agreement type from question"""
        agreement_types = ['NDA', 'MSA', 'Franchise Agreement', 'Employment Agreement', 'License Agreement', 'Service Agreement', 'Purchase Agreement', 'Lease Agreement']
        question_lower = question.lower()
        
        for agreement_type in agreement_types:
            if agreement_type.lower() in question_lower:
                return agreement_type
        
        return None
    
    def _extract_industry_from_question(self, question: str) -> str:
        """Extract industry from question"""
        industries = ['Technology', 'Oil & Gas', 'Healthcare', 'Finance', 'Real Estate', 'Manufacturing', 'Retail', 'Transportation']
        question_lower = question.lower()
        
        for industry in industries:
            if industry.lower() in question_lower:
                return industry
        
        return None
    
    def _extract_geography_from_question(self, question: str) -> str:
        """Extract geography from question"""
        geographies = ['Middle East', 'Europe', 'Asia', 'North America', 'Africa', 'Australia']
        question_lower = question.lower()
        
        for geography in geographies:
            if geography.lower() in question_lower:
                return geography
        
        return None
    
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
