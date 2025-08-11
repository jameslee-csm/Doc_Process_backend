import pytest
from unittest.mock import Mock
from app.services.query_service import QueryService

class TestQueryService:
    def setup_method(self):
        self.query_service = QueryService()
        self.mock_db = Mock()
    
    def test_query_by_jurisdiction_uae(self):
        # Mock document with UAE jurisdiction
        mock_document = Mock()
        mock_document.filename = "uae_contract.pdf"
        mock_document.governing_law = "UAE"
        mock_document.jurisdiction = "UAE"
        mock_document.agreement_type = "NDA"
        mock_document.industry = "Technology"
        mock_document.geography = "Middle East"
        
        self.mock_db.query.return_value.filter.return_value.all.return_value = [mock_document]
        
        question = "Which agreements are governed by UAE law?"
        results = self.query_service.process_query(question, self.mock_db)
        
        assert len(results) == 1
        assert results[0]['document'] == "uae_contract.pdf"
        assert results[0]['governing_law'] == "UAE"
    
    def test_query_by_agreement_type_nda(self):
        # Mock document with NDA agreement type
        mock_document = Mock()
        mock_document.filename = "nda_contract.pdf"
        mock_document.agreement_type = "NDA"
        mock_document.governing_law = "UK"
        mock_document.industry = "Technology"
        mock_document.jurisdiction = "UK"
        mock_document.geography = "Europe"
        
        self.mock_db.query.return_value.filter.return_value.all.return_value = [mock_document]
        
        question = "Show me all NDA contracts"
        results = self.query_service.process_query(question, self.mock_db)
        
        assert len(results) == 1
        assert results[0]['document'] == "nda_contract.pdf"
        assert results[0]['agreement_type'] == "NDA"
    
    def test_query_by_industry_technology(self):
        # Mock document with technology industry
        mock_document = Mock()
        mock_document.filename = "tech_contract.pdf"
        mock_document.industry = "Technology"
        mock_document.agreement_type = "MSA"
        mock_document.governing_law = "US"
        mock_document.jurisdiction = "US"
        mock_document.geography = "North America"
        
        self.mock_db.query.return_value.filter.return_value.all.return_value = [mock_document]
        
        question = "Find technology industry agreements"
        results = self.query_service.process_query(question, self.mock_db)
        
        assert len(results) == 1
        assert results[0]['document'] == "tech_contract.pdf"
        assert results[0]['industry'] == "Technology"
    
    def test_query_general_no_specific_pattern(self):
        # Mock multiple documents for general query
        mock_doc1 = Mock()
        mock_doc1.filename = "contract1.pdf"
        mock_doc1.agreement_type = "NDA"
        mock_doc1.governing_law = "UK"
        mock_doc1.industry = "Technology"
        mock_doc1.jurisdiction = "UK"
        mock_doc1.geography = "Europe"
        
        mock_doc2 = Mock()
        mock_doc2.filename = "contract2.pdf"
        mock_doc2.agreement_type = "MSA"
        mock_doc2.governing_law = "UAE"
        mock_doc2.industry = "Oil & Gas"
        mock_doc2.jurisdiction = "UAE"
        mock_doc2.geography = "Middle East"
        
        self.mock_db.query.return_value.all.return_value = [mock_doc1, mock_doc2]
        
        question = "What contracts do we have?"
        results = self.query_service.process_query(question, self.mock_db)
        
        assert len(results) == 2
        assert results[0]['document'] == "contract1.pdf"
        assert results[1]['document'] == "contract2.pdf"
    
    def test_query_no_results(self):
        self.mock_db.query.return_value.filter.return_value.all.return_value = []
        
        question = "Which agreements are governed by Singapore law?"
        results = self.query_service.process_query(question, self.mock_db)
        
        assert len(results) == 0
