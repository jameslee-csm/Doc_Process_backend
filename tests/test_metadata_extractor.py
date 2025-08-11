import pytest
from app.services.metadata_extractor import MetadataExtractor

class TestMetadataExtractor:
    def setup_method(self):
        self.extractor = MetadataExtractor()
    
    def test_extract_agreement_type_nda(self):
        content = "This is a Non-Disclosure Agreement between parties."
        filename = "nda_contract.pdf"
        
        metadata = self.extractor.extract_metadata(content, filename)
        
        assert metadata['agreement_type'] == 'NDA'
    
    def test_extract_agreement_type_msa(self):
        content = "Master Service Agreement terms and conditions."
        filename = "service_contract.docx"
        
        metadata = self.extractor.extract_metadata(content, filename)
        
        assert metadata['agreement_type'] == 'MSA'
    
    def test_extract_jurisdiction_uae(self):
        content = "This agreement is governed by UAE law and Dubai courts."
        filename = "contract.pdf"
        
        metadata = self.extractor.extract_metadata(content, filename)
        
        assert metadata['jurisdiction'] == 'UAE'
        assert metadata['governing_law'] == 'UAE'
    
    def test_extract_jurisdiction_uk(self):
        content = "This agreement is governed by UK law and English courts."
        filename = "contract.pdf"
        
        metadata = self.extractor.extract_metadata(content, filename)
        
        assert metadata['jurisdiction'] == 'UK'
        assert metadata['governing_law'] == 'UK'
    
    def test_extract_industry_technology(self):
        content = "Software development and technology services agreement."
        filename = "tech_contract.pdf"
        
        metadata = self.extractor.extract_metadata(content, filename)
        
        assert metadata['industry'] == 'Technology'
    
    def test_extract_industry_oil_gas(self):
        content = "Oil and gas exploration agreement."
        filename = "energy_contract.pdf"
        
        metadata = self.extractor.extract_metadata(content, filename)
        
        assert metadata['industry'] == 'Oil & Gas'
    
    def test_extract_geography_middle_east(self):
        content = "This agreement covers operations in the Middle East region."
        filename = "contract.pdf"
        
        metadata = self.extractor.extract_metadata(content, filename)
        
        assert metadata['geography'] == 'Middle East'
    
    def test_no_metadata_found(self):
        content = "This is a generic contract with no specific metadata."
        filename = "generic.pdf"
        
        metadata = self.extractor.extract_metadata(content, filename)
        
        assert metadata['agreement_type'] is None
        assert metadata['jurisdiction'] is None
        assert metadata['industry'] is None
        assert metadata['geography'] is None
